<template>
    <div class="profile-page">
        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading profile...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-container">
            <div class="error-icon">!</div>
            <h3>Oops! Something went wrong</h3>
            <p>{{ error }}</p>
            <button @click="fetchUserData" class="btn btn-primary">Try Again</button>
        </div>

        <!-- Profile Content -->
        <div v-else-if="user" class="profile-content">
            <!-- Profile Header -->
            <section class="profile-header">
                <div class="container">
                    <div class="profile-header-content">
                        <div class="profile-avatar-container">
                            <div v-if="user.profile_image" class="profile-avatar">
                                <img :src="user.profile_image" :alt="user.full_name" />
                            </div>
                            <div v-else class="profile-avatar-placeholder">
                                {{ userInitials }}
                            </div>
                            <button class="change-avatar-btn" @click="openFileUpload">
                                <i class="fas fa-camera"></i>
                                <input type="file" ref="fileInput" accept="image/*" class="file-input"
                                    @change="handleAvatarChange" />
                            </button>
                        </div>

                        <div class="profile-info">
                            <h1 class="profile-name">{{ user.full_name }}</h1>
                            <div class="profile-meta">
                                <div class="profile-role">
                                    <span class="role-badge" :class="roleClass">{{ user.role }}</span>
                                </div>
                                <div class="profile-joined">
                                    <i class="fas fa-calendar-alt"></i>
                                    <span>Joined {{ formatDate(user.date_joined) }}</span>
                                </div>
                                <div class="profile-email">
                                    <i class="fas fa-envelope"></i>
                                    <span>{{ user.email }}</span>
                                </div>
                            </div>
                            <div class="profile-stats">
                                <div class="stat-item">
                                    <div class="stat-value">{{ userCampaigns.length }}</div>
                                    <div class="stat-label">Campaigns</div>
                                </div>

                            </div>
                        </div>

                        <div class="profile-actions">
                            <router-link to="/profile/edit" class="btn btn-outline">
                                <i class="fas fa-edit"></i>
                                Edit Profile
                            </router-link>
                            <router-link to="/settings" class="btn btn-outline">
                                <i class="fas fa-cog"></i>
                                Settings
                            </router-link>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Profile Tabs -->
            <section class="profile-tabs-section">
                <div class="container">
                    <div class="profile-tabs">
                        <button class="tab-button" :class="{ active: activeTab === 'campaigns' }"
                            @click="activeTab = 'campaigns'">
                            My Campaigns
                        </button>

                    </div>

                    <!-- Tab Content -->
                    <div class="tab-content">
                        <!-- My Campaigns Tab -->
                        <div v-if="activeTab === 'campaigns'" class="tab-panel">
                            <div class="tab-header">
                                <h2>My Campaigns</h2>
                                <router-link to="/campaigns/create" class="btn btn-primary">
                                    <i class="fas fa-plus"></i>
                                    Create Campaign
                                </router-link>
                            </div>

                            <!-- Loading State for Campaigns -->
                            <div v-if="loadingCampaigns" class="loading-container">
                                <div class="loading-spinner"></div>
                                <p>Loading campaigns...</p>
                            </div>

                            <!-- Empty State -->
                            <div v-else-if="userCampaigns.length === 0" class="empty-state">
                                <div class="empty-icon">
                                    <i class="fas fa-bullhorn"></i>
                                </div>
                                <h3>No Campaigns Yet</h3>
                                <p>You haven't created any campaigns yet. Start making a difference today!</p>
                                <router-link to="/campaigns/create" class="btn btn-primary">Create Your First
                                    Campaign</router-link>
                            </div>

                            <!-- Campaigns List -->
                            <div v-else class="campaigns-grid">
                                <div v-for="campaign in userCampaigns" :key="campaign.id" class="campaign-card">
                                    <div class="campaign-image">
                                        <img :src="campaign.cover_image" :alt="campaign.title"
                                            @error="handleImageError" />
                                        <div v-if="campaign.is_featured" class="featured-badge">Featured</div>
                                        <div class="campaign-status-badge" :class="getCampaignStatusClass(campaign)">
                                            {{ getCampaignStatus(campaign) }}
                                        </div>
                                    </div>
                                    <div class="campaign-content">
                                        <div class="campaign-category">{{ campaign.category.name }}</div>
                                        <h3 class="campaign-title">{{ campaign.title }}</h3>

                                        <div class="campaign-progress">
                                            <div class="progress-bar">
                                                <div class="progress-fill"
                                                    :style="{ width: calculateProgress(campaign) + '%' }"></div>
                                            </div>
                                            <div class="progress-stats">
                                                <span class="funding-goal">${{ formatNumber(campaign.funding_goals) }}
                                                    Goal</span>
                                                <span class="funding-progress">{{ calculateProgress(campaign) }}%</span>
                                            </div>
                                        </div>

                                        <div class="campaign-meta">
                                            <div class="campaign-deadline">
                                                <i class="fas fa-clock"></i>
                                                {{ formatDeadline(campaign.deadline) }}
                                            </div>
                                        </div>

                                        <div class="campaign-actions">
                                            <router-link :to="`/campaigns/${campaign.id}`"
                                                class="btn btn-sm btn-outline">
                                                View
                                            </router-link>
                                            <router-link :to="`/campaigns/${campaign.id}/edit`"
                                                class="btn btn-sm btn-outline">
                                                Edit
                                            </router-link>
                                            <button class="btn btn-sm btn-outline" @click="shareCampaign(campaign)">
                                                Share
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import apiClient from '@/axios';
import { useAuthStore } from '@/stores/auth';

export default {
    name: 'ProfilePage',
    setup() {
        const authStore = useAuthStore();

        // State variables
        const user = ref(null);
        const loading = ref(true);
        const error = ref(null);
        const activeTab = ref('campaigns');
        const userCampaigns = ref([]);
        const loadingCampaigns = ref(false);
        const fileInput = ref(null);

        // Mock data for demo purposes
        const donationsCount = ref(8);

        // Computed properties
        const userInitials = computed(() => {
            if (!user.value || !user.value.full_name) return '';

            const names = user.value.full_name.split(' ');
            if (names.length >= 2) {
                return `${names[0][0]}${names[1][0]}`.toUpperCase();
            }
            return names[0][0].toUpperCase();
        });

        const roleClass = computed(() => {
            if (!user.value) return '';

            switch (user.value.role) {
                case 'ADMIN':
                    return 'role-admin';
                case 'BUSINESS':
                    return 'role-business';
                case 'USER':
                    return 'role-user';
                default:
                    return '';
            }
        });

        // Fetch user data
        const fetchUserData = async () => {
            loading.value = true;
            error.value = null;

            try {
                const response = await apiClient.get('auth/user/');
                user.value = response.data;

                // After getting user data, fetch their campaigns
                fetchUserCampaigns();
            } catch (err) {
                console.error('Error fetching user data:', err);
                error.value = 'Failed to load profile data. Please try again later.';
                loading.value = false;
            }
        };

        // Fetch user campaigns
        const fetchUserCampaigns = async () => {
            loadingCampaigns.value = true;

            try {
                // In a real app, you would fetch the user's campaigns
                // const response = await apiClient.get(`campaigns/user/${user.value.id}`);
                // userCampaigns.value = response.data;

                // For demo purposes, we'll simulate an API call with a timeout
                setTimeout(async () => {
                    try {
                        // Fetch all campaigns and filter by user ID
                        const response = await apiClient.get('campaigns/campaigns');
                        const allCampaigns = response.data;

                        // Filter campaigns created by the current user
                        userCampaigns.value = allCampaigns.filter(
                            campaign => campaign.created_by.id === user.value.id
                        );
                    } catch (err) {
                        console.error('Error fetching user campaigns:', err);
                    } finally {
                        loadingCampaigns.value = false;
                        loading.value = false;
                    }
                }, 800); // Simulate network delay

            } catch (err) {
                console.error('Error fetching user campaigns:', err);
                loadingCampaigns.value = false;
                loading.value = false;
            }
        };

        // Format date
        const formatDate = (dateString) => {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                month: 'long',
                day: 'numeric',
                year: 'numeric'
            });
        };

        // Format deadline date
        const formatDeadline = (dateString) => {
            const deadline = new Date(dateString);
            const now = new Date();
            const diffTime = deadline - now;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays < 0) {
                return 'Ended';
            } else if (diffDays === 0) {
                return 'Ends today';
            } else if (diffDays === 1) {
                return '1 day left';
            } else {
                return `${diffDays} days left`;
            }
        };

        // Calculate funding progress
        const calculateProgress = (campaign) => {
            // In a real app, you would calculate this based on actual donations
            // For now, we'll generate a random percentage between 10% and 90%
            const randomProgress = Math.floor(Math.random() * 80) + 10;
            return randomProgress;
        };

        // Format number with commas
        const formatNumber = (num) => {
            return parseFloat(num).toLocaleString('en-US');
        };

        // Get campaign status
        const getCampaignStatus = (campaign) => {
            if (campaign.is_completed) {
                return 'Completed';
            } else if (!campaign.is_active) {
                return 'Draft';
            } else if (campaign.is_featured) {
                return 'Featured';
            } else {
                return 'Active';
            }
        };

        // Get campaign status class
        const getCampaignStatusClass = (campaign) => {
            if (campaign.is_completed) {
                return 'status-completed';
            } else if (!campaign.is_active) {
                return 'status-draft';
            } else if (campaign.is_featured) {
                return 'status-featured';
            } else {
                return 'status-active';
            }
        };

        // Handle image loading errors
        const handleImageError = (event) => {
            event.target.src = '/placeholder.jpg'; // Fallback image
        };

        // Share campaign
        const shareCampaign = (campaign) => {
            if (navigator.share) {
                navigator.share({
                    title: campaign.title,
                    text: campaign.description,
                    url: `${window.location.origin}/campaigns/${campaign.id}`
                }).catch(err => console.error('Error sharing:', err));
            } else {
                // Fallback for browsers that don't support the Web Share API
                alert(`Share this link: ${window.location.origin}/campaigns/${campaign.id}`);
            }
        };

        // Open file upload dialog
        const openFileUpload = () => {
            fileInput.value.click();
        };

        // Handle avatar change
        const handleAvatarChange = async (event) => {
            const file = event.target.files[0];
            if (!file) return;

            // Create a FormData object to send the file
            const formData = new FormData();
            formData.append('profile_image', file);

            try {
                // In a real app, you would upload the image to your server
                // await apiClient.patch('auth/user/', formData, {
                //   headers: {
                //     'Content-Type': 'multipart/form-data'
                //   }
                // });

                // For demo purposes, create a local URL for the image
                const reader = new FileReader();
                reader.onload = (e) => {
                    user.value = {
                        ...user.value,
                        profile_image: e.target.result
                    };
                };
                reader.readAsDataURL(file);

                // Show success message
                alert('Profile image updated successfully!');
            } catch (err) {
                console.error('Error uploading profile image:', err);
                alert('Failed to update profile image. Please try again.');
            }
        };

        // Fetch data when component mounts
        onMounted(() => {
            fetchUserData();
        });

        return {
            user,
            loading,
            error,
            activeTab,
            userCampaigns,
            loadingCampaigns,
            donationsCount,
            userInitials,
            roleClass,
            fileInput,
            fetchUserData,
            formatDate,
            formatDeadline,
            calculateProgress,
            formatNumber,
            getCampaignStatus,
            getCampaignStatusClass,
            handleImageError,
            shareCampaign,
            openFileUpload,
            handleAvatarChange
        };
    }
};
</script>

<style>
/* Profile Page Styles */
.profile-page {
    min-height: 100vh;
}

/* Profile Header */
.profile-header {
    background-color: var(--surface);
    padding: var(--spacing-xl) 0;
    border-bottom: 1px solid var(--border-color);
}

.profile-header-content {
    display: flex;
    align-items: flex-start;
    gap: var(--spacing-xl);
}

.profile-avatar-container {
    position: relative;
    flex-shrink: 0;
}

.profile-avatar {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid var(--background);
    box-shadow: var(--shadow-md);
}

.profile-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.profile-avatar-placeholder {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background-color: var(--primary);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: 600;
    border: 4px solid var(--background);
    box-shadow: var(--shadow-md);
}

.change-avatar-btn {
    position: absolute;
    bottom: 5px;
    right: 5px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--background);
    border: 2px solid var(--primary);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
}

.change-avatar-btn:hover {
    background-color: var(--primary);
    color: white;
}

.file-input {
    display: none;
}

.profile-info {
    flex: 1;
}

.profile-name {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--spacing-sm);
}

.profile-meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    color: var(--text-secondary);
}

.profile-meta>div {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

.role-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
}

.role-admin {
    background-color: var(--primary);
    color: white;
}

.role-business {
    background-color: var(--secondary);
    color: white;
}

.role-user {
    background-color: var(--accent);
    color: white;
}

.profile-stats {
    display: flex;
    gap: var(--spacing-xl);
    margin-top: var(--spacing-md);
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

.stat-label {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.profile-actions {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
}

.profile-actions .btn {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

/* Profile Tabs */
.profile-tabs-section {
    padding: var(--spacing-xl) 0;
}

.profile-tabs {
    display: flex;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: var(--spacing-lg);
}

.tab-button {
    padding: var(--spacing-md) var(--spacing-lg);
    background: none;
    border: none;
    cursor: pointer;
    font-weight: 500;
    color: var(--text-secondary);
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
}

.tab-button:hover {
    color: var(--primary);
}

.tab-button.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}

.tab-content {
    min-height: 400px;
}

.tab-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-lg);
}

.tab-header h2 {
    margin: 0;
}

.tab-header .btn {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

/* Campaigns Grid */
.campaigns-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--spacing-lg);
}

.campaign-card {
    background-color: var(--background);
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.campaign-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.campaign-image {
    position: relative;
    height: 180px;
    overflow: hidden;
}

.campaign-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.featured-badge {
    position: absolute;
    top: var(--spacing-sm);
    right: var(--spacing-sm);
    background-color: var(--accent);
    color: white;
    padding: 4px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
}

.campaign-status-badge {
    position: absolute;
    top: var(--spacing-sm);
    left: var(--spacing-sm);
    padding: 4px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
}

.status-active {
    background-color: var(--success);
    color: white;
}

.status-draft {
    background-color: var(--text-secondary);
    color: white;
}

.status-completed {
    background-color: var(--secondary);
    color: white;
}

.status-featured {
    background-color: var(--accent);
    color: white;
}

.campaign-content {
    padding: var(--spacing-md);
}

.campaign-category {
    display: inline-block;
    background-color: var(--primary-light);
    color: var(--text-on-primary);
    padding: 2px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    margin-bottom: var(--spacing-sm);
}

.campaign-title {
    font-size: var(--font-size-lg);
    margin-bottom: var(--spacing-md);
    line-height: 1.3;
}

.campaign-progress {
    margin-bottom: var(--spacing-md);
}

.progress-bar {
    height: 8px;
    background-color: var(--border-color);
    border-radius: var(--border-radius-full);
    overflow: hidden;
    margin-bottom: 4px;
}

.progress-fill {
    height: 100%;
    background-color: var(--primary);
    border-radius: var(--border-radius-full);
}

.progress-stats {
    display: flex;
    justify-content: space-between;
    font-size: var(--font-size-sm);
}

.funding-goal {
    color: var(--text-secondary);
}

.funding-progress {
    font-weight: 600;
    color: var(--primary);
}

.campaign-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.campaign-deadline {
    display: flex;
    align-items: center;
    gap: 4px;
}

.campaign-actions {
    display: flex;
    gap: var(--spacing-sm);
}

/* Empty State */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xxl) 0;
    text-align: center;
}

.empty-icon {
    font-size: 3rem;
    color: var(--text-secondary);
    margin-bottom: var(--spacing-md);
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: var(--surface);
    display: flex;
    align-items: center;
    justify-content: center;
}

.empty-state h3 {
    margin-bottom: var(--spacing-sm);
}

.empty-state p {
    color: var(--text-secondary);
    max-width: 400px;
    margin-bottom: var(--spacing-lg);
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
    min-height: 300px;
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
    background-color: var(--error);
    color: white;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: var(--spacing-md);
}

/* Responsive Styles */
@media (max-width: 992px) {
    .profile-header-content {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .profile-avatar-container {
        margin-bottom: var(--spacing-lg);
    }

    .profile-meta {
        justify-content: center;
    }

    .profile-stats {
        justify-content: center;
    }

    .profile-actions {
        flex-direction: row;
        margin-top: var(--spacing-lg);
    }
}

@media (max-width: 768px) {
    .profile-tabs {
        overflow-x: auto;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
    }

    .tab-button {
        padding: var(--spacing-sm) var(--spacing-md);
    }

    .tab-header {
        flex-direction: column;
        gap: var(--spacing-md);
        align-items: flex-start;
    }

    .campaigns-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 576px) {
    .profile-stats {
        flex-direction: column;
        gap: var(--spacing-md);
    }

    .profile-actions {
        flex-direction: column;
        width: 100%;
    }

    .campaign-actions {
        flex-direction: column;
    }

    .campaign-actions .btn {
        width: 100%;
    }
}
</style>