<template>
    <div class="create-campaign-page">
        <div class="container">
            <!-- Page Header -->
            <div class="page-header">
                <div class="page-title" style="padding: 10px;">
                    <h1>Create Campaign</h1>
                    <p class="page-subtitle" style="color: white;">Start making a difference by creating your campaign
                    </p>
                </div>
                <div class="page-actions">
                    <router-link to="/campaigns/my-campaigns" class="btn btn-outline">
                        <i class="fas fa-arrow-left"></i>
                        Back to My Campaigns
                    </router-link>
                </div>
            </div>

            <!-- Form Container -->
            <div class="form-container">
                <!-- Loading State -->
                <div v-if="loading" class="loading-container">
                    <div class="loading-spinner"></div>
                    <p>Creating your campaign...</p>
                </div>

                <!-- Error State -->
                <div v-else-if="error" class="error-container">
                    <div class="error-icon">!</div>
                    <h3>Oops! Something went wrong</h3>
                    <p>{{ error }}</p>
                    <button @click="error = null" class="btn btn-primary">Try Again</button>
                </div>

                <!-- Success State -->
                <div v-else-if="submitted" class="success-container">
                    <div class="success-icon">
                        <i class="fas fa-check"></i>
                    </div>
                    <h3>Campaign Created Successfully!</h3>
                    <p>Your campaign has been sent to admin for approval and will be visible when approved.</p>
                    <div class="success-actions">
                        <router-link :to="`/campaigns/${createdCampaignId}`" class="btn btn-primary">
                            <i class="fas fa-eye"></i>
                            View Campaign
                        </router-link>
                        <router-link to="/my-campaigns" class="btn btn-outline">
                            <i class="fas fa-list"></i>
                            My Campaigns
                        </router-link>
                        <button @click="resetForm" class="btn btn-outline">
                            <i class="fas fa-plus"></i>
                            Create Another
                        </button>
                    </div>
                </div>

                <!-- Categories Loading State -->
                <div v-else-if="loadingCategories" class="loading-container">
                    <div class="loading-spinner"></div>
                    <p>Loading categories...</p>
                </div>

                <!-- Campaign Form -->
                <form v-else @submit.prevent="submitForm" class="campaign-form">
                    <div class="form-grid">
                        <div class="form-main">
                            <!-- Basic Information Section -->
                            <div class="form-section">
                                <h2 class="section-title">Basic Information</h2>

                                <div class="form-group">
                                    <label for="title" class="form-label">Campaign Title <span
                                            class="required">*</span></label>
                                    <input type="text" id="title" v-model="form.title" class="form-input"
                                        :class="{ 'input-error': errors.title }"
                                        placeholder="Enter a compelling title for your campaign" required />
                                    <p v-if="errors.title" class="error-message">{{ errors.title }}</p>
                                </div>

                                <div class="form-group">
                                    <label for="description" class="form-label">Campaign Description <span
                                            class="required">*</span></label>
                                    <textarea id="description" v-model="form.description" class="form-textarea"
                                        :class="{ 'input-error': errors.description }"
                                        placeholder="Describe your campaign, its goals, and impact" rows="6"
                                        required></textarea>
                                    <p v-if="errors.description" class="error-message">{{ errors.description }}</p>
                                </div>

                                <div class="form-group">
                                    <label for="location" class="form-label">Location</label>
                                    <input type="text" id="location" v-model="form.location" class="form-input"
                                        placeholder="Where will this campaign take place?" />
                                </div>

                                <div class="form-group">
                                    <label for="category" class="form-label">Category <span
                                            class="required">*</span></label>
                                    <select id="category" v-model="form.category_id" class="form-select"
                                        :class="{ 'input-error': errors.category_id }" required>
                                        <option value="" disabled selected>Select a category</option>
                                        <option v-for="category in categories" :key="category.id" :value="category.id">
                                            {{ category.name }}
                                        </option>
                                    </select>
                                    <p v-if="errors.category_id" class="error-message">{{ errors.category_id }}</p>
                                </div>
                            </div>

                            <!-- Funding Section -->
                            <div class="form-section">
                                <h2 class="section-title">Funding Details</h2>

                                <div class="form-group">
                                    <label for="funding_goals" class="form-label">Funding Goal ($) <span
                                            class="required">*</span></label>
                                    <input type="number" id="funding_goals" v-model="form.funding_goals"
                                        class="form-input" :class="{ 'input-error': errors.funding_goals }"
                                        placeholder="How much do you need to raise?" min="1" step="1" required />
                                    <p v-if="errors.funding_goals" class="error-message">{{ errors.funding_goals }}</p>
                                </div>

                                <div class="form-group">
                                    <label for="deadline" class="form-label">Campaign Deadline <span
                                            class="required">*</span></label>
                                    <input type="date" id="deadline" v-model="form.deadline" class="form-input"
                                        :class="{ 'input-error': errors.deadline }" :min="minDate" required />
                                    <p v-if="errors.deadline" class="error-message">{{ errors.deadline }}</p>
                                </div>
                            </div>
                        </div>

                        <div class="form-sidebar">
                            <!-- Cover Image Section -->
                            <div class="form-section">
                                <h2 class="section-title">Cover Image</h2>

                                <div class="image-upload-container">
                                    <div class="image-preview"
                                        :class="{ 'has-image': imagePreview, 'no-image': !imagePreview }">
                                        <img v-if="imagePreview" :src="imagePreview" alt="Cover image preview" />
                                        <div v-else class="upload-placeholder">
                                            <i class="fas fa-image"></i>
                                            <p>Upload a cover image</p>
                                        </div>
                                    </div>

                                    <div class="image-upload-actions">
                                        <label for="cover_image" class="btn btn-outline btn-upload">
                                            <i class="fas fa-upload"></i>
                                            {{ imagePreview ? 'Change Image' : 'Upload Image' }}
                                            <input type="file" id="cover_image" ref="fileInput"
                                                @change="handleImageUpload" accept="image/*" class="file-input" />
                                        </label>

                                        <button v-if="imagePreview" type="button" @click="removeImage"
                                            class="btn btn-outline btn-danger">
                                            <i class="fas fa-trash-alt"></i>
                                            Remove
                                        </button>
                                    </div>

                                    <p v-if="errors.cover_image" class="error-message">{{ errors.cover_image }}</p>
                                    <p class="image-help-text">Recommended size: 1200 x 630 pixels. Max size: 5MB.</p>
                                </div>
                            </div>

                            <!-- Campaign Preview -->
                            <div class="form-section">
                                <h2 class="section-title">Campaign Preview</h2>

                                <div class="campaign-preview-card">
                                    <div class="preview-image">
                                        <img :src="imagePreview || '/placeholder.jpg'" alt="Campaign preview" />
                                    </div>
                                    <div class="preview-content">
                                        <h3 class="preview-title">{{ form.title || 'Campaign Title' }}</h3>
                                        <p class="preview-description">{{ truncateText(form.description || 'Campaign description will appear here.', 100) }}</p>
                                        <div class="preview-meta">
                                            <div v-if="form.deadline" class="preview-deadline">
                                                <i class="fas fa-clock"></i>
                                                <span>Ends: {{ formatDate(form.deadline) }}</span>
                                            </div>
                                            <div v-if="form.funding_goals" class="preview-goal">
                                                <i class="fas fa-dollar-sign"></i>
                                                <span>Goal: ${{ formatNumber(form.funding_goals) }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Form Actions -->
                    <div class="form-actions">
                        <button type="button" @click="$router.go(-1)" class="btn btn-outline">
                            Cancel
                        </button>
                        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                            <i class="fas fa-save"></i>
                            {{ isSubmitting ? 'Creating...' : 'Create Campaign' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '@/axios';
import { useAuthStore } from '@/stores/auth';

export default {
    name: 'CreateCampaignPage',
    setup() {
        const router = useRouter();
        const authStore = useAuthStore();
        const fileInput = ref(null);

        // Form state
        const form = ref({
            title: '',
            description: '',
            location: '',
            category_id: '',
            cover_image: null,
            deadline: '',
            funding_goals: null,
            is_active: true,
            is_featured: false,
            is_completed: false,
            is_business: false
        });

        // UI state
        const errors = ref({});
        const loading = ref(false);
        const loadingCategories = ref(true);
        const submitted = ref(false);
        const error = ref(null);
        const isSubmitting = ref(false);
        const imagePreview = ref(null);
        const createdCampaignId = ref(null);

        // Categories from API
        const categories = ref([]);

        // Computed properties
        const minDate = computed(() => {
            const today = new Date();
            return today.toISOString().split('T')[0];
        });

        // Fetch categories from API
        const fetchCategories = async () => {
            loadingCategories.value = true;
            try {
                const response = await apiClient.get('campaigns/categories/');
                categories.value = response.data;
            } catch (err) {
                console.error('Error fetching categories:', err);
                error.value = 'Failed to load categories. Please refresh the page.';
            } finally {
                loadingCategories.value = false;
            }
        };

        // Set user-related fields
        const setUserFields = () => {
            if (authStore.user) {
                // Set is_business based on user role
                form.value.is_business = authStore.user.role === 'BUSINESS';
            }
        };

        // Handle image upload
        const handleImageUpload = (event) => {
            const file = event.target.files[0];
            if (!file) return;

            // Validate file type
            const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
            if (!validTypes.includes(file.type)) {
                errors.value.cover_image = 'Please upload a valid image file (JPEG, PNG, GIF, WEBP).';
                return;
            }

            // Validate file size (5MB max)
            if (file.size > 5 * 1024 * 1024) {
                errors.value.cover_image = 'Image size should not exceed 5MB.';
                return;
            }

            // Clear previous error
            errors.value.cover_image = null;

            // Create a preview URL
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.value = e.target.result;
            };
            reader.readAsDataURL(file);

            // Store the file for submission
            form.value.cover_image = file;
        };

        // Remove uploaded image
        const removeImage = () => {
            imagePreview.value = null;
            form.value.cover_image = null;
            if (fileInput.value) {
                fileInput.value.value = '';
            }
        };

        // Validate form
        const validateForm = () => {
            const newErrors = {};

            if (!form.value.title.trim()) {
                newErrors.title = 'Title is required';
            } else if (form.value.title.length < 5) {
                newErrors.title = 'Title must be at least 5 characters';
            }

            if (!form.value.description.trim()) {
                newErrors.description = 'Description is required';
            } else if (form.value.description.length < 20) {
                newErrors.description = 'Description must be at least 20 characters';
            }

            if (!form.value.category_id) {
                newErrors.category_id = 'Please select a category';
            }

            if (!form.value.funding_goals) {
                newErrors.funding_goals = 'Funding goal is required';
            } else if (form.value.funding_goals <= 0) {
                newErrors.funding_goals = 'Funding goal must be greater than zero';
            }

            if (!form.value.deadline) {
                newErrors.deadline = 'Deadline is required';
            } else {
                const deadlineDate = new Date(form.value.deadline);
                const today = new Date();
                today.setHours(0, 0, 0, 0);

                if (deadlineDate < today) {
                    newErrors.deadline = 'Deadline cannot be in the past';
                }
            }

            errors.value = newErrors;
            return Object.keys(newErrors).length === 0;
        };

        // Submit form
        const submitForm = async () => {
            if (!validateForm()) {
                // Scroll to the first error
                const firstError = document.querySelector('.error-message');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                return;
            }

            isSubmitting.value = true;
            loading.value = true;
            error.value = null;

            try {
                // Prepare form data
                const formData = new FormData();

                // Add the user ID from the auth store
                formData.append('created_by_id', authStore.user.id);

                // Add other form fields
                Object.keys(form.value).forEach(key => {
                    if (key !== 'cover_image') {
                        formData.append(key, form.value[key]);
                    }
                });

                // Add cover image if exists
                if (form.value.cover_image) {
                    formData.append('cover_image', form.value.cover_image);
                }

                // Send the request
                const response = await apiClient.post('campaigns/campaigns/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                // Store the created campaign ID
                createdCampaignId.value = response.data.id;

                // Show success state
                submitted.value = true;
            } catch (err) {
                console.error('Error creating campaign:', err);
                error.value = err.response?.data?.message || 'Failed to create campaign. Please try again.';

                // If there are validation errors from the server
                if (err.response?.data?.errors) {
                    errors.value = err.response.data.errors;
                }
            } finally {
                isSubmitting.value = false;
                loading.value = false;
            }
        };

        // Reset form for creating another campaign
        const resetForm = () => {
            form.value = {
                title: '',
                description: '',
                location: '',
                category_id: '',
                cover_image: null,
                deadline: '',
                funding_goals: null,
                is_active: true,
                is_featured: false,
                is_completed: false,
                is_business: false
            };

            imagePreview.value = null;
            errors.value = {};
            submitted.value = false;
            error.value = null;

            // Reset file input
            if (fileInput.value) {
                fileInput.value.value = '';
            }

            // Set user fields again
            setUserFields();

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        // Helper functions
        const truncateText = (text, maxLength) => {
            if (!text) return '';
            if (text.length <= maxLength) return text;
            return text.substring(0, maxLength) + '...';
        };

        const formatNumber = (num) => {
            if (!num) return '0';
            return parseFloat(num).toLocaleString('en-US');
        };

        const formatDate = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        };

        // Initialize component
        onMounted(() => {
            fetchCategories();
            setUserFields();
        });

        return {
            form,
            errors,
            loading,
            loadingCategories,
            submitted,
            error,
            isSubmitting,
            imagePreview,
            createdCampaignId,
            categories,
            minDate,
            fileInput,
            handleImageUpload,
            removeImage,
            submitForm,
            resetForm,
            truncateText,
            formatNumber,
            formatDate
        };
    }
};
</script>

<style>
/* Create Campaign Page Styles */
.create-campaign-page {
    padding: var(--spacing-xl) 0;
}

/* Page Header */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--spacing-xl);
}

.page-title h1 {
    margin: 0 0 var(--spacing-xs) 0;
    font-size: 2rem;
    font-weight: 700;
}

.page-subtitle {
    color: var(--text-secondary);
    margin: 0;
}

.page-actions {
    display: flex;
    gap: var(--spacing-md);
}

.page-actions .btn {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

/* Form Container */
.form-container {
    background-color: var(--background);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-md);
    overflow: hidden;
    border: 1px solid var(--border-color);
}

/* Form Grid Layout */
.form-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
}

.form-main {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xl);
}

.form-sidebar {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xl);
}

/* Form Sections */
.form-section {
    background-color: var(--surface);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-lg);
    border: 1px solid var(--border-color);
}

.section-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-xs);
    border-bottom: 1px solid var(--border-color);
}

/* Form Groups */
.form-group {
    margin-bottom: var(--spacing-md);
}

.form-label {
    display: block;
    margin-bottom: var(--spacing-xs);
    font-weight: 500;
}

.required {
    color: var(--error);
}

.form-input,
.form-textarea,
.form-select {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-md);
    background-color: var(--background);
    transition: border-color 0.2s ease;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
    border-color: var(--primary);
    outline: none;
}

.form-textarea {
    resize: vertical;
    min-height: 120px;
}

.input-error {
    border-color: var(--error);
}

.error-message {
    color: var(--error);
    font-size: var(--font-size-sm);
    margin-top: var(--spacing-xs);
    margin-bottom: 0;
}

.help-text {
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    margin-top: var(--spacing-xs);
    margin-bottom: 0;
}

/* Checkbox Styles */
.checkbox-group {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
}

.checkbox-label {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    cursor: pointer;
}

.checkbox-text {
    font-weight: 500;
}

/* Image Upload */
.image-upload-container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.image-preview {
    width: 100%;
    height: 200px;
    border-radius: var(--border-radius-md);
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.image-preview.has-image {
    border: none;
}

.image-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.upload-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: var(--background);
    color: var(--text-secondary);
}

.upload-placeholder i {
    font-size: 2rem;
    margin-bottom: var(--spacing-sm);
}

.image-upload-actions {
    display: flex;
    gap: var(--spacing-md);
}

.btn-upload {
    position: relative;
    overflow: hidden;
    flex: 1;
}

.file-input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.image-help-text {
    color: var(--text-secondary);
    font-size: var(--font-size-xs);
    margin: 0;
}

/* Campaign Preview */
.campaign-preview-card {
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
    background-color: var(--background);
}

.preview-image {
    height: 150px;
    overflow: hidden;
}

.preview-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.preview-content {
    padding: var(--spacing-md);
}

.preview-title {
    font-size: var(--font-size-lg);
    margin: 0 0 var(--spacing-sm) 0;
}

.preview-description {
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    margin: 0 0 var(--spacing-md) 0;
    line-height: 1.5;
}

.preview-meta {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.preview-deadline,
.preview-goal {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

/* Form Actions */
.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    border-top: 1px solid var(--border-color);
    background-color: var(--surface);
}

/* Loading, Error, Success States */
.loading-container,
.error-container,
.success-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xxl) 0;
    text-align: center;
    min-height: 400px;
}

.loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: var(--primary);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin-bottom: var(--spacing-md);
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.error-icon,
.success-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin-bottom: var(--spacing-md);
    font-size: 1.5rem;
}

.error-icon {
    background-color: var(--error);
    color: white;
    font-weight: 700;
}

.success-icon {
    background-color: var(--success);
    color: white;
}

.success-actions {
    display: flex;
    gap: var(--spacing-md);
    margin-top: var(--spacing-lg);
}

/* Responsive Styles */
@media (max-width: 992px) {
    .form-grid {
        grid-template-columns: 1fr;
    }

    .page-header {
        flex-direction: column;
        gap: var(--spacing-md);
    }

    .page-actions {
        width: 100%;
    }

    .page-actions .btn {
        flex: 1;
        justify-content: center;
    }

    .success-actions {
        flex-direction: column;
    }

    .success-actions .btn {
        width: 100%;
    }
}

@media (max-width: 768px) {
    .form-actions {
        flex-direction: column;
    }

    .form-actions .btn {
        width: 100%;
    }
}

@media (max-width: 576px) {
    .image-upload-actions {
        flex-direction: column;
    }
}
</style>