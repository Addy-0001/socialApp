<template>
    <div class="signup-page">
        <div class="auth-container">
            <div class="auth-card">
                <!-- Logo and Header -->
                <div class="auth-header">
                    <router-link to="/" class="auth-logo">EcoImpact</router-link>
                    <h1 class="auth-title">Create an Account</h1>
                    <p class="auth-subtitle">
                        Join our community and start making a difference today
                    </p>
                </div>

                <!-- Form -->
                <form @submit.prevent="handleSubmit" class="auth-form" novalidate>
                    <!-- Full Name -->
                    <div class="form-group">
                        <label for="full-name" class="form-label">Full Name</label>
                        <input id="full-name" v-model="form.full_name" type="text" class="form-control"
                            :class="{ 'is-invalid': errors.full_name }" placeholder="Enter your full name"
                            @blur="validateField('full_name')" required />
                        <div v-if="errors.full_name" class="invalid-feedback">
                            {{ errors.full_name }}
                        </div>
                    </div>

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
                        <label for="password" class="form-label">Password</label>
                        <div class="password-input-wrapper">
                            <input id="password" v-model="form.password1" :type="showPassword ? 'text' : 'password'"
                                class="form-control" :class="{ 'is-invalid': errors.password1 }"
                                placeholder="Create a password" @blur="validateField('password1')" required />
                            <button type="button" class="password-toggle-btn" @click="showPassword = !showPassword"
                                tabindex="-1" aria-label="Toggle password visibility">
                                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                            </button>
                        </div>
                        <div v-if="errors.password1" class="invalid-feedback">
                            {{ errors.password1 }}
                        </div>
                        <div class="password-strength" v-if="form.password1">
                            <div class="strength-meter">
                                <div class="strength-meter-fill" :style="{ width: passwordStrength.score + '%' }"
                                    :class="passwordStrength.class"></div>
                            </div>
                            <div class="strength-text" :class="passwordStrength.class">
                                {{ passwordStrength.text }}
                            </div>
                        </div>
                    </div>

                    <!-- Confirm Password -->
                    <div class="form-group">
                        <label for="confirm-password" class="form-label">Confirm Password</label>
                        <div class="password-input-wrapper">
                            <input id="confirm-password" v-model="form.password2"
                                :type="showConfirmPassword ? 'text' : 'password'" class="form-control"
                                :class="{ 'is-invalid': errors.password2 }" placeholder="Confirm your password"
                                @blur="validateField('password2')" required />
                            <button type="button" class="password-toggle-btn"
                                @click="showConfirmPassword = !showConfirmPassword" tabindex="-1"
                                aria-label="Toggle password visibility">
                                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'
                                    "></i>
                            </button>
                        </div>
                        <div v-if="errors.password2" class="invalid-feedback">
                            {{ errors.password2 }}
                        </div>
                    </div>

                    <!-- Role Selection -->
                    <div class="form-group">
                        <label class="form-label">Account Type</label>
                        <div class="role-options">
                            <div class="role-option" :class="{ selected: form.role === 'USER' }"
                                @click="form.role = 'USER'">
                                <div class="role-radio">
                                    <div class="radio-inner" v-if="form.role === 'USER'"></div>
                                </div>
                                <div class="role-content">
                                    <div class="role-title">Individual</div>
                                    <div class="role-description">
                                        Support campaigns and make a difference as an individual
                                    </div>
                                </div>
                            </div>

                            <div class="role-option" :class="{ selected: form.role === 'BUSINESS' }"
                                @click="form.role = 'BUSINESS'">
                                <div class="role-radio">
                                    <div class="radio-inner" v-if="form.role === 'BUSINESS'"></div>
                                </div>
                                <div class="role-content">
                                    <div class="role-title">Business</div>
                                    <div class="role-description">
                                        Create campaigns and partner with others as a business
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div v-if="errors.role" class="invalid-feedback">
                            {{ errors.role }}
                        </div>
                    </div>

                    <!-- Terms and Conditions -->
                    <div class="form-group">
                        <div class="checkbox-wrapper">
                            <input id="terms" v-model="form.agreeToTerms" type="checkbox" class="form-checkbox"
                                @change="validateField('agreeToTerms')" />
                            <label for="terms" class="checkbox-label">
                                I agree to the
                                <router-link to="/terms" class="text-link">Terms of Service</router-link>
                                and
                                <router-link to="/privacy" class="text-link">Privacy Policy</router-link>
                            </label>
                        </div>
                        <div v-if="errors.agreeToTerms" class="invalid-feedback">
                            {{ errors.agreeToTerms }}
                        </div>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" class="btn btn-primary btn-block" :disabled="isSubmitting">
                        <span v-if="isSubmitting" class="spinner-border spinner-border-sm" role="status"
                            aria-hidden="true"></span>
                        {{ isSubmitting ? "Creating Account..." : "Sign Up" }}
                    </button>

                    <!-- API Error Message -->
                    <div v-if="apiError" class="alert alert-danger">
                        {{ apiError }}
                    </div>
                </form>

                <!-- Already have an account -->
                <div class="auth-footer">
                    Already have an account?
                    <router-link to="/login" class="text-link">Log In</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, reactive, computed } from "vue";
import { useRouter } from "vue-router";
import apiClient from "@/axios";

export default {
    name: "SignupPage",
    setup() {
        const router = useRouter();

        // Form data
        const form = reactive({
            email: "",
            password1: "",
            password2: "",
            full_name: "",
            role: "USER",
            agreeToTerms: false,
        });

        // Form state
        const errors = reactive({});
        const isSubmitting = ref(false);
        const apiError = ref("");
        const showPassword = ref(false);
        const showConfirmPassword = ref(false);

        // Password strength calculation
        const passwordStrength = computed(() => {
            if (!form.password1) {
                return { score: 0, text: "", class: "" };
            }

            let score = 0;
            let text = "";
            let className = "";

            // Length check
            if (form.password1.length >= 8) score += 25;

            // Complexity checks
            if (/[A-Z]/.test(form.password1)) score += 25;
            if (/[0-9]/.test(form.password1)) score += 25;
            if (/[^A-Za-z0-9]/.test(form.password1)) score += 25;

            // Determine strength text and class
            if (score <= 25) {
                text = "Weak";
                className = "weak";
            } else if (score <= 50) {
                text = "Fair";
                className = "fair";
            } else if (score <= 75) {
                text = "Good";
                className = "good";
            } else {
                text = "Strong";
                className = "strong";
            }

            return { score, text, class: className };
        });

        // Validation functions
        const validateEmail = (email) => {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        };

        const validateField = (field) => {
            errors[field] = "";

            switch (field) {
                case "full_name":
                    if (!form.full_name) {
                        errors.full_name = "Full name is required";
                    } else if (form.full_name.length < 2) {
                        errors.full_name = "Full name must be at least 2 characters";
                    }
                    break;

                case "email":
                    if (!form.email) {
                        errors.email = "Email is required";
                    } else if (!validateEmail(form.email)) {
                        errors.email = "Please enter a valid email address";
                    }
                    break;

                case "password1":
                    if (!form.password1) {
                        errors.password1 = "Password is required";
                    } else if (form.password1.length < 8) {
                        errors.password1 = "Password must be at least 8 characters";
                    } else if (!/[A-Z]/.test(form.password1)) {
                        errors.password1 =
                            "Password must contain at least one uppercase letter";
                    } else if (!/[0-9]/.test(form.password1)) {
                        errors.password1 = "Password must contain at least one number";
                    }

                    // If password2 is already filled, validate it again
                    if (form.password2) {
                        validateField("password2");
                    }
                    break;

                case "password2":
                    if (!form.password2) {
                        errors.password2 = "Please confirm your password";
                    } else if (form.password1 !== form.password2) {
                        errors.password2 = "Passwords do not match";
                    }
                    break;

                case "role":
                    if (!form.role) {
                        errors.role = "Please select an account type";
                    }
                    break;

                case "agreeToTerms":
                    if (!form.agreeToTerms) {
                        errors.agreeToTerms =
                            "You must agree to the Terms of Service and Privacy Policy";
                    }
                    break;
            }
        };

        const validateForm = () => {
            // Validate all fields
            validateField("full_name");
            validateField("email");
            validateField("password1");
            validateField("password2");
            validateField("role");
            validateField("agreeToTerms");

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
                const userData = {
                    email: form.email,
                    password1: form.password1,
                    password2: form.password2,
                    full_name: form.full_name,
                    role: form.role,
                };

                // Send registration request
                const response = await apiClient.post("auth/registration/", userData);

                // Handle successful registration
                console.log("Registration successful:", response.data);

                // Redirect to login page with success message
                router.push({
                    path: "/login",
                    query: { registered: "success" },
                });
            } catch (error) {
                console.error("Registration error:", error);

                // Handle API errors
                if (error.response && error.response.data) {
                    // Extract error messages from API response
                    const apiErrors = error.response.data;

                    if (typeof apiErrors === "string") {
                        apiError.value = apiErrors;
                    } else if (typeof apiErrors === "object") {
                        // Map API error fields to our form fields
                        Object.keys(apiErrors).forEach((key) => {
                            if (key in errors) {
                                errors[key] = Array.isArray(apiErrors[key])
                                    ? apiErrors[key][0]
                                    : apiErrors[key];
                            } else {
                                // General error
                                apiError.value = "Registration failed. Please try again.";
                            }
                        });
                    } else {
                        apiError.value = "An unexpected error occurred. Please try again.";
                    }
                } else {
                    apiError.value =
                        "Network error. Please check your connection and try again.";
                }
            } finally {
                isSubmitting.value = false;
            }
        };

        return {
            form,
            errors,
            isSubmitting,
            apiError,
            showPassword,
            showConfirmPassword,
            passwordStrength,
            validateField,
            handleSubmit,
        };
    },
};
</script>

<style>
/* Signup Page Styles */
.signup-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xl) var(--spacing-md);
    background-color: var(--surface);
}

.auth-container {
    width: 100%;
    max-width: 500px;
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

.password-strength {
    margin-top: var(--spacing-xs);
}

.strength-meter {
    height: 4px;
    background-color: var(--border-color);
    border-radius: var(--border-radius-full);
    margin-bottom: 4px;
}

.strength-meter-fill {
    height: 100%;
    border-radius: var(--border-radius-full);
    transition: width 0.3s ease;
}

.strength-meter-fill.weak {
    background-color: var(--error);
}

.strength-meter-fill.fair {
    background-color: var(--warning);
}

.strength-meter-fill.good {
    background-color: var(--success);
}

.strength-meter-fill.strong {
    background-color: var(--primary);
}

.strength-text {
    font-size: var(--font-size-xs);
    text-align: right;
}

.strength-text.weak {
    color: var(--error);
}

.strength-text.fair {
    color: var(--warning);
}

.strength-text.good {
    color: var(--success);
}

.strength-text.strong {
    color: var(--primary);
}

.role-options {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    margin-top: var(--spacing-xs);
}

.role-option {
    display: flex;
    align-items: flex-start;
    padding: var(--spacing-sm);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
}

.role-option:hover {
    background-color: var(--surface);
}

.role-option.selected {
    border-color: var(--primary);
    background-color: rgba(46, 125, 50, 0.05);
}

.role-radio {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid var(--border-color);
    margin-right: var(--spacing-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
}

.role-option.selected .role-radio {
    border-color: var(--primary);
}

.radio-inner {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: var(--primary);
}

.role-content {
    flex: 1;
}

.role-title {
    font-weight: 600;
    margin-bottom: 2px;
}

.role-description {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.checkbox-wrapper {
    display: flex;
    align-items: flex-start;
}

.form-checkbox {
    margin-right: var(--spacing-sm);
    margin-top: 4px;
}

.checkbox-label {
    font-size: var(--font-size-sm);
    line-height: 1.4;
}

.text-link {
    color: var(--primary);
    text-decoration: none;
}

.text-link:hover {
    text-decoration: underline;
}

.btn-block {
    display: block;
    width: 100%;
}

.alert {
    padding: var(--spacing-sm) var(--spacing-md);
    margin-top: var(--spacing-md);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-sm);
}

.alert-danger {
    background-color: rgba(244, 67, 54, 0.1);
    border: 1px solid rgba(244, 67, 54, 0.3);
    color: var(--error);
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

.auth-footer {
    text-align: center;
    margin-top: var(--spacing-lg);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

/* Responsive Styles */
@media (max-width: 576px) {
    .auth-card {
        padding: var(--spacing-lg);
    }

    .role-options {
        flex-direction: column;
    }

    .role-option {
        width: 100%;
    }
}
</style>