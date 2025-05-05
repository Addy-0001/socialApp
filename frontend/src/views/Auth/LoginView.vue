<template>
    <div class="login-page">
        <div class="auth-container">
            <div class="auth-card">
                <!-- Logo and Header -->
                <div class="auth-header">
                    <router-link to="/" class="auth-logo">EcoImpact</router-link>
                    <h1 class="auth-title">Welcome Back</h1>
                    <p class="auth-subtitle">
                        Sign in to your account to continue your journey
                    </p>
                </div>

                <!-- Registration Success Message -->
                <div v-if="registrationSuccess" class="alert alert-success">
                    <i class="fas fa-check-circle"></i>
                    Registration successful! Please sign in with your new account.
                </div>

                <!-- Form -->
                <form @submit.prevent="handleSubmit" class="auth-form" novalidate>
                    <!-- Email -->
                    <div class="form-group">
                        <label for="email" class="form-label">Email Address</label>
                        <input id="email" v-model="form.email" type="email" class="form-control"
                            :class="{ 'is-invalid': errors.email }" placeholder="Enter your email"
                            @blur="validateField('email')" required />
                        <div v-if="errors.email" class="invalid-feedback">
                            {{ errors.email }}
                        </div>
                    </div>

                    <!-- Password -->
                    <div class="form-group">
                        <div class="password-header">
                            <label for="password" class="form-label">Password</label>
                            <router-link to="/forgot-password" class="forgot-password">
                                Forgot Password?
                            </router-link>
                        </div>
                        <div class="password-input-wrapper">
                            <input id="password" v-model="form.password" :type="showPassword ? 'text' : 'password'"
                                class="form-control" :class="{ 'is-invalid': errors.password }"
                                placeholder="Enter your password" @blur="validateField('password')" required />
                            <button type="button" class="password-toggle-btn" @click="showPassword = !showPassword"
                                tabindex="-1" aria-label="Toggle password visibility">
                                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                        </div>
                        <div v-if="errors.password" class="invalid-feedback">
                            {{ errors.password }}
                        </div>
                    </div>

                    <!-- Remember Me -->
                    <div class="form-group">
                        <div class="checkbox-wrapper">
                            <input id="remember-me" v-model="form.rememberMe" type="checkbox" class="form-checkbox" />
                            <label for="remember-me" class="checkbox-label">
                                Remember me
                            </label>
                        </div>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" class="btn btn-primary btn-block" :disabled="isSubmitting">
                        <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status"
                            aria-hidden="true"></span>
                        {{ isSubmitting ? "Signing In..." : "Sign In" }}
                    </button>

                    <!-- API Error Message -->
                    <div v-if="apiError" class="alert alert-danger">
                        <i class="fas fa-exclamation-circle"></i>
                        {{ apiError }}
                    </div>
                </form>

                <!-- Social Login -->
                <div class="social-login">
                    <div class="divider">
                        <span>Or continue with</span>
                    </div>
                    <div class="social-buttons">
                        <button class="btn btn-outline social-btn">
                            <i class="fab fa-google"></i>
                            Google
                        </button>
                        <button class="btn btn-outline social-btn">
                            <i class="fab fa-facebook-f"></i>
                            Facebook
                        </button>
                    </div>
                </div>

                <!-- Don't have an account -->
                <div class="auth-footer">
                    Don't have an account?
                    <router-link to="/signup" class="text-link">Sign Up</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, reactive, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";

export default {
    name: "LoginPage",
    setup() {
        const router = useRouter();
        const route = useRoute();
        const authStore = useAuthStore();

        // Check if user was redirected from registration
        const registrationSuccess = ref(route.query.registered === "success");

        // Form data
        const form = reactive({
            email: "",
            password: "",
            rememberMe: false,
        });

        // Form state
        const errors = reactive({});
        const isSubmitting = ref(false);
        const apiError = ref("");
        const showPassword = ref(false);

        // Validation functions
        const validateEmail = (email) => {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        };

        const validateField = (field) => {
            errors[field] = "";

            switch (field) {
                case "email":
                    if (!form.email) {
                        errors.email = "Email is required";
                    } else if (!validateEmail(form.email)) {
                        errors.email = "Please enter a valid email address";
                    }
                    break;

                case "password":
                    if (!form.password) {
                        errors.password = "Password is required";
                    }
                    break;
            }
        };

        const validateForm = () => {
            // Validate all fields
            validateField("email");
            validateField("password");

            // Check if there are any errors
            return !Object.values(errors).some((error) => error);
        };

        // Form submission
        const handleSubmit = async () => {
            // Reset API error
            apiError.value = "";

            // Validate form
            if (!validateForm()) {
                return;
            }

            // Set submitting state
            isSubmitting.value = true;

            try {
                // Prepare data for API
                const credentials = {
                    email: form.email,
                    password: form.password,
                };

                // Send login request using Pinia store
                const result = await authStore.login(credentials);

                if (result.success) {
                    // Handle successful login
                    console.log("Login successful:", result.data);

                    // Clear registration success message if present
                    registrationSuccess.value = false;

                    // Redirect to dashboard or home page
                    router.push("/campaigns");
                } else {
                    // Handle login failure
                    apiError.value = result.error;

                    if (typeof result.error === "object") {
                        // Handle structured error response
                        if (result.error.email) {
                            errors.email = Array.isArray(result.error.email)
                                ? result.error.email[0]
                                : result.error.email;
                        }

                        if (result.error.password) {
                            errors.password = Array.isArray(result.error.password)
                                ? result.error.password[0]
                                : result.error.password;
                        }

                        if (result.error.non_field_errors) {
                            apiError.value = Array.isArray(result.error.non_field_errors)
                                ? result.error.non_field_errors[0]
                                : result.error.non_field_errors;
                        } else if (!errors.email && !errors.password) {
                            apiError.value = "Invalid email or password. Please try again.";
                        }
                    }
                }
            } catch (error) {
                console.error("Login submission error:", error);
                apiError.value = "An unexpected error occurred. Please try again.";
            } finally {
                isSubmitting.value = false;
            }
        };

        // Check if user is already logged in
        onMounted(() => {
            if (authStore.isAuthenticated) {
                router.push("/campaigns");
            }
        });

        return {
            form,
            errors,
            isSubmitting,
            apiError,
            showPassword,
            registrationSuccess,
            validateField,
            handleSubmit,
        };
    },
};
</script>

<style>
/* Login Page Styles */
.login-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xl) var(--spacing-md);
    background-color: var(--surface);
}

.auth-container {
    width: 100%;
    max-width: 450px;
}

.auth-card {
    background-color: var(--background);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-lg);
    padding: var(--spacing-xl);
}

.auth-header {
    text-align: center;
    margin-bottom: var(--spacing-xl);
}

.auth-logo {
    font-size: var(--font-size-xl);
    font-weight: 700;
    color: var(--primary);
    text-decoration: none;
    display: inline-block;
    margin-bottom: var(--spacing-md);
}

.auth-title {
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: var(--spacing-sm);
}

.auth-subtitle {
    color: var(--text-secondary);
}

.auth-form {
    margin-bottom: var(--spacing-lg);
}

.form-group {
    margin-bottom: var(--spacing-md);
}

.form-label {
    display: block;
    margin-bottom: var(--spacing-xs);
    font-weight: 500;
}

.password-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-xs);
}

.forgot-password {
    font-size: var(--font-size-sm);
    color: var(--primary);
    text-decoration: none;
}

.forgot-password:hover {
    text-decoration: underline;
}

.form-control {
    display: block;
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-md);
    line-height: 1.5;
    color: var(--text-primary);
    background-color: var(--background);
    background-clip: padding-box;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
    border-color: var(--primary);
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(46, 125, 50, 0.25);
}

.form-control.is-invalid {
    border-color: var(--error);
}

.invalid-feedback {
    display: block;
    width: 100%;
    margin-top: 0.25rem;
    font-size: var(--font-size-sm);
    color: var(--error);
}

.password-input-wrapper {
    position: relative;
}

.password-toggle-btn {
    position: absolute;
    right: var(--spacing-md);
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
}

.checkbox-wrapper {
    display: flex;
    align-items: center;
}

.form-checkbox {
    margin-right: var(--spacing-sm);
}

.checkbox-label {
    font-size: var(--font-size-sm);
}

.btn-block {
    display: block;
    width: 100%;
}

.alert {
    padding: var(--spacing-sm) var(--spacing-md);
    margin-bottom: var(--spacing-md);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-sm);
    display: flex;
    align-items: center;
}

.alert i {
    margin-right: var(--spacing-sm);
}

.alert-danger {
    background-color: rgba(244, 67, 54, 0.1);
    border: 1px solid rgba(244, 67, 54, 0.3);
    color: var(--error);
}

.alert-success {
    background-color: rgba(76, 175, 80, 0.1);
    border: 1px solid rgba(76, 175, 80, 0.3);
    color: var(--success);
}

.spinner-border {
    display: inline-block;
    width: 1rem;
    height: 1rem;
    border: 0.2em solid currentColor;
    border-right-color: transparent;
    border-radius: 50%;
    animation: spinner-border 0.75s linear infinite;
    margin-right: var(--spacing-sm);
}

@keyframes spinner-border {
    to {
        transform: rotate(360deg);
    }
}

.social-login {
    margin-top: var(--spacing-lg);
}

.divider {
    display: flex;
    align-items: center;
    text-align: center;
    margin-bottom: var(--spacing-md);
}

.divider::before,
.divider::after {
    content: "";
    flex: 1;
    border-bottom: 1px solid var(--border-color);
}

.divider span {
    padding: 0 var(--spacing-sm);
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
}

.social-buttons {
    display: flex;
    gap: var(--spacing-md);
}

.social-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
}

.auth-footer {
    text-align: center;
    margin-top: var(--spacing-lg);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.text-link {
    color: var(--primary);
    text-decoration: none;
}

.text-link:hover {
    text-decoration: underline;
}

/* Responsive Styles */
@media (max-width: 576px) {
    .auth-card {
        padding: var(--spacing-lg);
    }

    .social-buttons {
        flex-direction: column;
    }
}
</style>