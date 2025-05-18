<template>
    <div class="create-donation-page">
        <div class="container">
            <!-- Page Header -->
            <div class="page-header" style="padding-inline: 20px;">
                <div class="page-title">
                    <h1>Make a Donation</h1>
                    <p class="page-subtitle" style="color: white;">Support this campaign and make a difference</p>
                </div>
                <div class="page-actions">
                    <button @click="goBack" class="btn btn-outline">
                        <i class="fas fa-arrow-left"></i>
                        Back to Campaign
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>Loading campaign details...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="error-container">
                <div class="error-icon">!</div>
                <h3>Oops! Something went wrong</h3>
                <p>{{ error }}</p>
                <button @click="fetchCampaign" class="btn btn-primary">Try Again</button>
                <button @click="goBack" class="btn btn-outline">Go Back</button>
            </div>

            <!-- Donation Form -->
            <div v-else-if="!submitted" class="donation-form-container">
                <div class="donation-grid">
                    <!-- Campaign Info -->
                    <div class="campaign-info-card">
                        <div class="campaign-image">
                            <img :src="campaign.cover_image || '/placeholder.jpg'" :alt="campaign.title"
                                @error="handleImageError" />
                        </div>
                        <div class="campaign-details">
                            <h2 class="campaign-title">{{ campaign.title }}</h2>
                            <div class="campaign-category" v-if="campaign.category">
                                {{ campaign.category.name }}
                            </div>
                            <p class="campaign-description">{{ truncateText(campaign.description, 150) }}</p>

                            <div class="campaign-progress">
                                <div class="progress-stats">
                                    <div class="progress-stat">
                                        <div class="stat-label">Raised</div>
                                        <div class="stat-value">${{ formatNumber(campaign.current_amount || 0) }}</div>
                                    </div>
                                    <div class="progress-stat">
                                        <div class="stat-label">Goal</div>
                                        <div class="stat-value">${{ formatNumber(campaign.funding_goals || 0) }}</div>
                                    </div>
                                </div>

                                <div class="progress-bar-container">
                                    <div class="progress-bar"
                                        :style="{ width: calculateProgress(campaign.current_amount, campaign.funding_goals) + '%' }">
                                    </div>
                                </div>

                                <div class="progress-percentage">
                                    {{ calculateProgress(campaign.current_amount, campaign.funding_goals) }}% of goal
                                    reached
                                </div>
                            </div>

                            <div class="campaign-deadline" v-if="campaign.deadline">
                                <i class="fas fa-clock"></i>
                                <span>{{ getRemainingTime(campaign.deadline) }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Donation Form -->
                    <div class="donation-form">
                        <h2 class="form-title">Your Donation</h2>

                        <form @submit.prevent="submitDonation">
                            <!-- Amount Input -->
                            <div class="form-group">
                                <label for="amount" class="form-label">Donation Amount <span
                                        class="required">*</span></label>
                                <div class="amount-input-wrapper">
                                    <span class="currency-symbol">$</span>
                                    <input type="number" id="amount" v-model="donationForm.amount"
                                        class="form-input amount-input" :class="{ 'input-error': errors.amount }"
                                        placeholder="Enter amount" min="1" step="0.01" required />
                                </div>
                                <p v-if="errors.amount" class="error-message">{{ errors.amount }}</p>
                            </div>

                            <!-- Suggested Amounts -->
                            <div class="suggested-amounts">
                                <button type="button" v-for="amount in suggestedAmounts" :key="amount"
                                    @click="selectAmount(amount)" class="suggested-amount-btn"
                                    :class="{ 'selected': donationForm.amount === amount }">
                                    ${{ amount }}
                                </button>
                            </div>

                            <!-- Receipt Upload -->
                            <div class="form-group">
                                <label for="receipt" class="form-label">Upload Receipt <span
                                        class="required">*</span></label>
                                <div class="receipt-upload-container"
                                    :class="{ 'has-file': receiptPreview, 'input-error': errors.receipt }">
                                    <div v-if="receiptPreview" class="receipt-preview">
                                        <div class="receipt-file-info">
                                            <i class="fas fa-file-alt receipt-icon"></i>
                                            <div class="receipt-file-name">{{ receiptFileName }}</div>
                                        </div>
                                        <button type="button" @click="removeReceipt" class="remove-receipt-btn">
                                            <i class="fas fa-times"></i>
                                        </button>
                                    </div>

                                    <div v-else class="receipt-upload-placeholder">
                                        <i class="fas fa-upload"></i>
                                        <p>Click to upload or drag and drop</p>
                                        <span class="upload-hint">Supported formats: PDF, JPG, PNG</span>
                                    </div>

                                    <input type="file" id="receipt" ref="receiptInput" @change="handleReceiptUpload"
                                        accept=".pdf,.jpg,.jpeg,.png" class="receipt-input" />
                                </div>
                                <p v-if="errors.receipt" class="error-message">{{ errors.receipt }}</p>
                            </div>

                            <!-- Message (Optional) -->
                            <div class="form-group">
                                <label for="message" class="form-label">Message (Optional)</label>
                                <textarea id="message" v-model="donationForm.message" class="form-textarea"
                                    placeholder="Add a message of support (will be visible to campaign organizers)"
                                    rows="3"></textarea>
                            </div>

                            <!-- Anonymous Donation -->
                            <div class="form-group checkbox-group">
                                <label class="checkbox-label">
                                    <input type="checkbox" v-model="donationForm.is_anonymous" />
                                    <span class="checkbox-text">Make this donation anonymous</span>
                                </label>
                                <p class="help-text">Your name will not be displayed publicly, but campaign organizers
                                    will still receive your information.</p>
                            </div>

                            <!-- Donation Summary -->
                            <div class="donation-summary-box">
                                <h3 class="summary-title">Donation Summary</h3>
                                <div class="summary-row">
                                    <div class="summary-label">Donation Amount</div>
                                    <div class="summary-value">${{ formatNumber(donationForm.amount || 0) }}</div>
                                </div>
                                <div class="summary-row total-row">
                                    <div class="summary-label">Total</div>
                                    <div class="summary-value">${{ formatNumber(donationForm.amount || 0) }}</div>
                                </div>
                            </div>

                            <!-- Form Actions -->
                            <div class="form-actions">
                                <button type="button" @click="goBack" class="btn btn-outline">
                                    Cancel
                                </button>
                                <button type="submit" class="btn btn-primary btn-donate" :disabled="isSubmitting">
                                    <i class="fas fa-heart"></i>
                                    {{ isSubmitting ? 'Processing...' : 'Complete Donation' }}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Success State -->
            <div v-else class="success-container">
                <div class="success-icon">
                    <i class="fas fa-check"></i>
                </div>
                <h2>Thank You for Your Donation!</h2>
                <p class="success-message">Your contribution of <strong>${{ formatNumber(donationForm.amount)
                }}</strong> to <strong>{{ campaign.title }}</strong> has been received.</p>

                <div class="donation-details-card">
                    <div class="donation-detail-row">
                        <div class="detail-label">Donation ID</div>
                        <div class="detail-value">{{ donationId }}</div>
                    </div>
                    <div class="donation-detail-row">
                        <div class="detail-label">Date</div>
                        <div class="detail-value">{{ formatDate(new Date()) }}</div>
                    </div>
                    <div class="donation-detail-row">
                        <div class="detail-label">Amount</div>
                        <div class="detail-value">${{ formatNumber(donationForm.amount) }}</div>
                    </div>
                    <div class="donation-detail-row">
                        <div class="detail-label">Campaign</div>
                        <div class="detail-value">{{ campaign.title }}</div>
                    </div>
                </div>

                <p class="receipt-note">A receipt has been sent to your email address.</p>

                <div class="success-actions">
                    <button @click="downloadReceipt" class="btn btn-outline">
                        <i class="fas fa-file-invoice"></i>
                        Download Receipt
                    </button>
                    <router-link :to="`/campaigns/${campaignId}`" class="btn btn-outline">
                        <i class="fas fa-eye"></i>
                        View Campaign
                    </router-link>
                    <router-link to="/donations/my-donations" class="btn btn-outline">
                        <i class="fas fa-list"></i>
                        My Donations
                    </router-link>
                    <router-link to="/campaigns" class="btn btn-primary">
                        <i class="fas fa-hand-holding-heart"></i>
                        Support More Campaigns
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import apiClient from '@/axios';
import { useAuthStore } from '@/stores/auth';

export default {
    name: 'CreateDonationPage',
    setup() {
        const router = useRouter();
        const route = useRoute();
        const authStore = useAuthStore();
        const receiptInput = ref(null);

        // Get campaign ID from route params
        const campaignId = computed(() => route.params.id);

        // State variables
        const campaign = ref({});
        const loading = ref(true);
        const error = ref(null);
        const submitted = ref(false);
        const isSubmitting = ref(false);
        const receiptPreview = ref(null);
        const receiptFileName = ref('');
        const donationId = ref('');
        const errors = ref({});

        // Donation form
        const donationForm = ref({
            amount: null,
            receipt: null,
            message: '',
            is_anonymous: false
        });

        // Suggested donation amounts
        const suggestedAmounts = ref([10, 25, 50, 100, 250]);

        // Fetch campaign details
        const fetchCampaign = async () => {
            loading.value = true;
            error.value = null;

            try {
                const response = await apiClient.get(`/campaigns/campaigns/${campaignId.value}`);
                campaign.value = response.data;

                // Adjust suggested amounts based on campaign goal
                if (campaign.value.funding_goals) {
                    const goal = parseFloat(campaign.value.funding_goals);
                    if (goal < 100) {
                        suggestedAmounts.value = [5, 10, 20, 50, 100];
                    } else if (goal > 10000) {
                        suggestedAmounts.value = [50, 100, 250, 500, 1000];
                    }
                }
            } catch (err) {
                console.error('Error fetching campaign:', err);
                error.value = 'Failed to load campaign details. Please try again later.';
            } finally {
                loading.value = false;
            }
        };

        // Handle receipt upload
        const handleReceiptUpload = (event) => {
            const file = event.target.files[0];
            if (!file) return;

            // Validate file type
            const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
            if (!validTypes.includes(file.type)) {
                errors.value.receipt = 'Please upload a valid file (PDF, JPG, PNG).';
                return;
            }

            // Validate file size (5MB max)
            if (file.size > 5 * 1024 * 1024) {
                errors.value.receipt = 'File size should not exceed 5MB.';
                return;
            }

            // Clear previous error
            errors.value.receipt = null;

            // Store the file for submission
            donationForm.value.receipt = file;
            receiptFileName.value = file.name;

            // Create a preview for the receipt (just showing the filename is enough)
            receiptPreview.value = true;
        };

        // Remove uploaded receipt
        const removeReceipt = () => {
            donationForm.value.receipt = null;
            receiptPreview.value = null;
            receiptFileName.value = '';

            // Reset file input
            if (receiptInput.value) {
                receiptInput.value.value = '';
            }
        };

        // Select a suggested amount
        const selectAmount = (amount) => {
            donationForm.value.amount = amount;
            errors.value.amount = null;
        };

        // Validate form
        const validateForm = () => {
            const newErrors = {};

            if (!donationForm.value.amount) {
                newErrors.amount = 'Please enter a donation amount';
            } else if (donationForm.value.amount <= 0) {
                newErrors.amount = 'Donation amount must be greater than zero';
            }

            if (!donationForm.value.receipt) {
                newErrors.receipt = 'Please upload a receipt';
            }

            errors.value = newErrors;
            return Object.keys(newErrors).length === 0;
        };

        // Submit donation
        const submitDonation = async () => {
            if (!validateForm()) {
                return;
            }

            if (!authStore.user || !authStore.user.id) {
                error.value = 'You must be logged in to make a donation';
                return;
            }

            isSubmitting.value = true;

            try {
                // Prepare form data
                const formData = new FormData();

                // Add user ID and campaign ID
                formData.append('user_id', authStore.user.id);
                formData.append('campaign_id', campaignId.value);

                // Add amount and receipt
                formData.append('amount', donationForm.value.amount);
                formData.append('receipt', donationForm.value.receipt);

                // Add optional fields
                if (donationForm.value.message) {
                    formData.append('message', donationForm.value.message);
                }

                if (donationForm.value.is_anonymous) {
                    formData.append('is_anonymous', donationForm.value.is_anonymous);
                }

                // Send the request
                const response = await apiClient.post('/campaigns/donations/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                // Store the donation ID for the receipt
                donationId.value = response.data.id || 'DON-' + Math.floor(Math.random() * 100000);

                // Show success state
                submitted.value = true;
            } catch (err) {
                console.error('Error submitting donation:', err);

                if (err.response?.data?.errors) {
                    errors.value = err.response.data.errors;
                } else {
                    error.value = err.response?.data?.message || 'Failed to process your donation. Please try again.';
                }
            } finally {
                isSubmitting.value = false;
            }
        };

        // Download receipt
        const downloadReceipt = () => {
            // In a real app, this would generate and download a receipt PDF
            alert('Your donation receipt is being generated and will download shortly.');
        };

        // Helper functions
        const formatNumber = (num) => {
            if (!num) return '0.00';
            return parseFloat(num).toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        };

        const formatDate = (dateObj) => {
            return dateObj.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        };

        const truncateText = (text, maxLength) => {
            if (!text) return '';
            if (text.length <= maxLength) return text;
            return text.substring(0, maxLength) + '...';
        };

        const calculateProgress = (current, goal) => {
            if (!current || !goal) return 0;
            const percentage = (parseFloat(current) / parseFloat(goal)) * 100;
            return Math.min(Math.round(percentage), 100);
        };

        const getRemainingTime = (deadlineStr) => {
            if (!deadlineStr) return 'No deadline set';

            const deadline = new Date(deadlineStr);
            const now = new Date();

            if (deadline < now) {
                return 'Campaign ended';
            }

            const diffTime = Math.abs(deadline - now);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays === 1) {
                return '1 day left';
            } else {
                return `${diffDays} days left`;
            }
        };

        const handleImageError = (event) => {
            event.target.src = '/placeholder.jpg';
        };

        const goBack = () => {
            router.push(`/campaigns/${campaignId.value}`);
        };

        // Fetch campaign data when component mounts
        onMounted(() => {
            fetchCampaign();
        });

        return {
            campaign,
            campaignId,
            loading,
            error,
            submitted,
            isSubmitting,
            donationForm,
            errors,
            receiptPreview,
            receiptFileName,
            receiptInput,
            donationId,
            suggestedAmounts,
            fetchCampaign,
            handleReceiptUpload,
            removeReceipt,
            selectAmount,
            submitDonation,
            downloadReceipt,
            formatNumber,
            formatDate,
            truncateText,
            calculateProgress,
            getRemainingTime,
            handleImageError,
            goBack
        };
    }
};
</script>

<style scoped>
/* Create Donation Page Styles */
.create-donation-page {
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

/* Donation Form Container */
.donation-form-container {
    background-color: var(--background);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-md);
    overflow: hidden;
    border: 1px solid var(--border-color);
}

/* Donation Grid Layout */
.donation-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
}

/* Campaign Info Card */
.campaign-info-card {
    padding: var(--spacing-xl);
    background-color: var(--surface);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
}

.campaign-image {
    width: 100%;
    height: 200px;
    border-radius: var(--border-radius-md);
    overflow: hidden;
}

.campaign-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.campaign-details {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.campaign-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
}

.campaign-category {
    display: inline-block;
    background-color: var(--primary-light);
    color: var(--text-on-primary);
    padding: 4px 10px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    margin-bottom: var(--spacing-xs);
    align-self: flex-start;
}

.campaign-description {
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
}

.campaign-progress {
    margin-top: var(--spacing-md);
}

.progress-stats {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);
}

.progress-stat {
    display: flex;
    flex-direction: column;
}

.stat-label {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    margin-bottom: 4px;
}

.stat-value {
    font-size: var(--font-size-lg);
    font-weight: 700;
    color: var(--text-primary);
}

.progress-bar-container {
    width: 100%;
    height: 8px;
    background-color: var(--background);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: var(--spacing-xs);
}

.progress-bar {
    height: 100%;
    background-color: var(--primary);
    border-radius: 4px;
}

.progress-percentage {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    text-align: right;
}

.campaign-deadline {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    margin-top: var(--spacing-md);
}

/* Donation Form */
.donation-form {
    padding: var(--spacing-xl);
}

.form-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 var(--spacing-lg) 0;
}

.form-group {
    margin-bottom: var(--spacing-lg);
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
.form-textarea {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-md);
    background-color: var(--background);
    transition: border-color 0.2s ease;
}

.form-input:focus,
.form-textarea:focus {
    border-color: var(--primary);
    outline: none;
}

.form-textarea {
    resize: vertical;
    min-height: 80px;
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

/* Amount Input */
.amount-input-wrapper {
    position: relative;
}

.currency-symbol {
    position: absolute;
    left: var(--spacing-md);
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    font-weight: 500;
}

.amount-input {
    padding-left: calc(var(--spacing-md) + 12px);
}

/* Suggested Amounts */
.suggested-amounts {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-lg);
}

.suggested-amount-btn {
    padding: var(--spacing-sm) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    background-color: var(--background);
    cursor: pointer;
    transition: all 0.2s ease;
    font-weight: 500;
}

.suggested-amount-btn:hover {
    border-color: var(--primary);
    color: var(--primary);
}

.suggested-amount-btn.selected {
    background-color: var(--primary);
    color: white;
    border-color: var(--primary);
}

/* Receipt Upload */
.receipt-upload-container {
    width: 100%;
    height: 120px;
    border: 2px dashed var(--border-color);
    border-radius: var(--border-radius-md);
    overflow: hidden;
    position: relative;
    cursor: pointer;
    transition: border-color 0.2s ease;
}

.receipt-upload-container:hover {
    border-color: var(--primary);
}

.receipt-upload-container.has-file {
    border-style: solid;
    border-color: var(--primary);
}

.receipt-upload-container.input-error {
    border-color: var(--error);
}

.receipt-upload-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
}

.receipt-upload-placeholder i {
    font-size: 1.5rem;
    margin-bottom: var(--spacing-xs);
}

.upload-hint {
    font-size: var(--font-size-xs);
    margin-top: var(--spacing-xs);
    opacity: 0.7;
}

.receipt-input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.receipt-preview {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--spacing-md);
    background-color: var(--surface);
}

.receipt-file-info {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.receipt-icon {
    font-size: 2rem;
    color: var(--primary);
}

.receipt-file-name {
    font-weight: 500;
    word-break: break-all;
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.remove-receipt-btn {
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: var(--spacing-xs);
    border-radius: 50%;
    transition: all 0.2s ease;
}

.remove-receipt-btn:hover {
    background-color: rgba(0, 0, 0, 0.1);
    color: var(--error);
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

.help-text {
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    margin-top: var(--spacing-xs);
    margin-bottom: 0;
    margin-left: calc(var(--spacing-sm) + 20px);
}

/* Donation Summary Box */
.donation-summary-box {
    background-color: var(--surface);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
    border: 1px solid var(--border-color);
}

.summary-title {
    font-size: var(--font-size-md);
    font-weight: 600;
    margin: 0 0 var(--spacing-md) 0;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);
}

.summary-row:last-child {
    margin-bottom: 0;
}

.summary-label {
    color: var(--text-secondary);
}

.summary-value {
    font-weight: 600;
}

.total-row {
    margin-top: var(--spacing-md);
    padding-top: var(--spacing-md);
    border-top: 1px solid var(--border-color);
}

.total-row .summary-label,
.total-row .summary-value {
    font-weight: 700;
    font-size: var(--font-size-lg);
    color: var(--text-primary);
}

/* Form Actions */
.form-actions {
    display: flex;
    justify-content: space-between;
    gap: var(--spacing-md);
}

.btn-donate {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-md);
    font-size: var(--font-size-md);
}

/* Success State */
.success-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: var(--spacing-xxl) var(--spacing-xl);
    background-color: var(--background);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-color);
}

.success-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: var(--success);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin-bottom: var(--spacing-lg);
}

.success-container h2 {
    font-size: 2rem;
    margin: 0 0 var(--spacing-md) 0;
}

.success-message {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-xl);
    max-width: 600px;
}

.donation-details-card {
    width: 100%;
    max-width: 500px;
    background-color: var(--surface);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
    border: 1px solid var(--border-color);
}

.donation-detail-row {
    display: flex;
    justify-content: space-between;
    padding: var(--spacing-sm) 0;
    border-bottom: 1px solid var(--border-color);
}

.donation-detail-row:last-child {
    border-bottom: none;
}

.detail-label {
    font-weight: 600;
    color: var(--text-secondary);
}

.detail-value {
    font-weight: 500;
}

.receipt-note {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-xl);
}

.success-actions {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-md);
    justify-content: center;
}

/* Loading, Error States */
.loading-container,
.error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xxl) 0;
    text-align: center;
    min-height: 400px;
    background-color: var(--background);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-color);
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

.error-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin-bottom: var(--spacing-md);
    font-size: 1.5rem;
    background-color: var(--error);
    color: white;
    font-weight: 700;
}

.error-container h3 {
    font-size: 1.5rem;
    margin: 0 0 var(--spacing-sm) 0;
}

.error-container p {
    color: var(--text-secondary);
    margin-bottom: var(--spacing-lg);
    max-width: 500px;
}

.error-container .btn {
    margin: 0 var(--spacing-xs);
}

/* Responsive Styles */
@media (max-width: 992px) {
    .donation-grid {
        grid-template-columns: 1fr;
    }

    .campaign-info-card {
        border-right: none;
        border-bottom: 1px solid var(--border-color);
    }

    .form-actions {
        flex-direction: column;
    }

    .form-actions .btn {
        width: 100%;
    }

    .success-actions {
        flex-direction: column;
        width: 100%;
    }

    .success-actions .btn {
        width: 100%;
    }
}

@media (max-width: 768px) {
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

    .suggested-amounts {
        justify-content: space-between;
    }

    .suggested-amount-btn {
        flex: 1;
        text-align: center;
        padding: var(--spacing-sm) var(--spacing-xs);
    }
}

@media (max-width: 576px) {
    .suggested-amounts {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
    }
}
</style>