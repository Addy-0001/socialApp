<template>
    <div class="my-campaigns-page">
        <div class="container">
            <!-- Page Header -->
            <div class="page-header">
                <div class="page-title">
                    <h1>My Campaigns</h1>
                    <p class="page-subtitle" style="color: white;">Manage and track all your created campaigns</p>
                </div>
                <div class="page-actions">
                    <router-link to="/campaigns/create" class="btn btn-primary">
                        <i class="fas fa-plus"></i>
                        Create Campaign
                    </router-link>
                </div>
            </div>

            <!-- Filters and Controls -->
            <div class="campaigns-controls">
                <div class="filters-wrapper">
                    <div class="search-filter">
                        <div class="search-input-wrapper">
                            <i class="fas fa-search search-icon"></i>
                            <input type="text" v-model="searchQuery" placeholder="Search campaigns..."
                                class="search-input" />
                            <button v-if="searchQuery" @click="clearSearch" class="clear-search-btn">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>

                    <div class="filter-group">
                        <div class="filter-select">
                            <label for="status-filter">Status</label>
                            <select id="status-filter" v-model="statusFilter" class="select-input">
                                <option value="all">All Status</option>
                                <option value="active">Active</option>
                                <option value="draft">Draft</option>
                                <option value="completed">Completed</option>
                                <option value="featured">Featured</option>
                            </select>
                        </div>

                        <div class="filter-select">
                            <label for="category-filter">Category</label>
                            <select id="category-filter" v-model="categoryFilter" class="select-input">
                                <option value="all">All Categories</option>
                                <option v-for="category in categories" :key="category.id" :value="category.id">
                                    {{ category.name }}
                                </option>
                            </select>
                        </div>

                        <div class="filter-select">
                            <label for="sort-by">Sort By</label>
                            <select id="sort-by" v-model="sortBy" class="select-input">
                                <option value="newest">Newest First</option>
                                <option value="oldest">Oldest First</option>
                                <option value="name-asc">Name (A-Z)</option>
                                <option value="name-desc">Name (Z-A)</option>
                                <option value="progress-asc">Progress (Low to High)</option>
                                <option value="progress-desc">Progress (High to Low)</option>
                                <option value="deadline-asc">Deadline (Soonest)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="view-toggle">
                    <button @click="viewMode = 'grid'" class="view-toggle-btn" :class="{ active: viewMode === 'grid' }"
                        aria-label="Grid view">
                        <i class="fas fa-th-large"></i>
                    </button>
                    <button @click="viewMode = 'list'" class="view-toggle-btn" :class="{ active: viewMode === 'list' }"
                        aria-label="List view">
                        <i class="fas fa-list"></i>
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>Loading your campaigns...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="error-container">
                <div class="error-icon">!</div>
                <h3>Oops! Something went wrong</h3>
                <p>{{ error }}</p>
                <button @click="fetchCampaigns" class="btn btn-primary">Try Again</button>
            </div>

            <!-- Empty State -->
            <div v-else-if="filteredCampaigns.length === 0 && !loading" class="empty-state">
                <div v-if="hasFiltersApplied">
                    <div class="empty-icon">
                        <i class="fas fa-filter"></i>
                    </div>
                    <h3>No campaigns match your filters</h3>
                    <p>Try adjusting your search criteria or clear filters to see all your campaigns.</p>
                    <button @click="clearFilters" class="btn btn-primary">Clear Filters</button>
                </div>
                <div v-else>
                    <div class="empty-icon">
                        <i class="fas fa-bullhorn"></i>
                    </div>
                    <h3>No Campaigns Yet</h3>
                    <p>You haven't created any campaigns yet. Start making a difference today!</p>
                    <router-link to="/campaigns/create" class="btn btn-primary">Create Your First Campaign</router-link>
                </div>
            </div>

            <!-- Campaigns Grid View -->
            <div v-else-if="viewMode === 'grid'" class="campaigns-grid">
                <div v-for="campaign in paginatedCampaigns" :key="campaign.id" class="campaign-card">
                    <div class="campaign-image">
                        <img :src="campaign.cover_image || '/placeholder.jpg'" :alt="campaign.title"
                            @error="handleImageError" />
                        <div v-if="campaign.is_featured" class="featured-badge">Featured</div>
                        <div class="campaign-status-badge" :class="getCampaignStatusClass(campaign)">
                            {{ getCampaignStatus(campaign) }}
                        </div>
                    </div>
                    <div class="campaign-content">
                        <div class="campaign-category">{{ getCategoryName(campaign.category?.id) }}</div>
                        <h3 class="campaign-title">{{ campaign.title }}</h3>

                        <div class="campaign-progress">
                            <div class="progress-bar">
                                <div class="progress-fill" :style="{ width: calculateProgress(campaign) + '%' }"></div>
                            </div>
                            <div class="progress-stats">
                                <span class="funding-goal">${{ formatNumber(campaign.funding_goal) }} Goal</span>
                                <span class="funding-progress">{{ calculateProgress(campaign) }}%</span>
                            </div>
                        </div>

                        <div class="campaign-meta">
                            <div class="campaign-deadline">
                                <i class="fas fa-clock"></i>
                                {{ formatDeadline(campaign.deadline) }}
                            </div>
                            <div class="campaign-supporters">
                                <i class="fas fa-users"></i>
                                {{ campaign.supporters || 0 }} Supporters
                            </div>
                        </div>

                        <div class="campaign-actions">
                            <router-link :to="`/campaigns/${campaign.id}`" class="btn btn-sm btn-outline">
                                <i class="fas fa-eye"></i>
                                View
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Campaigns List View -->
            <div v-else class="campaigns-list">
                <div v-for="campaign in paginatedCampaigns" :key="campaign.id" class="campaign-list-item">
                    <div class="campaign-list-image">
                        <img :src="campaign.cover_image || '/placeholder.jpg'" :alt="campaign.title"
                            @error="handleImageError" />
                    </div>
                    <div class="campaign-list-content">
                        <div class="campaign-list-header">
                            <h3 class="campaign-list-title">{{ campaign.title }}</h3>
                            <div class="campaign-list-status" :class="getCampaignStatusClass(campaign)">
                                {{ getCampaignStatus(campaign) }}
                            </div>
                        </div>
                        <div class="campaign-list-category">{{ getCategoryName(campaign.category?.id) }}</div>
                        <p class="campaign-list-description">{{ truncateText(campaign.description, 120) }}</p>

                        <div class="campaign-list-stats">
                            <div class="campaign-list-stat">
                                <i class="fas fa-chart-line"></i>
                                <span>{{ calculateProgress(campaign) }}% Funded</span>
                            </div>
                            <div class="campaign-list-stat">
                                <i class="fas fa-dollar-sign"></i>
                                <span>${{ formatNumber(campaign.current_amount || 0) }} of ${{
                                    formatNumber(campaign.funding_goal) }}</span>
                            </div>
                            <div class="campaign-list-stat">
                                <i class="fas fa-clock"></i>
                                <span>{{ formatDeadline(campaign.deadline) }}</span>
                            </div>
                            <div class="campaign-list-stat">
                                <i class="fas fa-users"></i>
                                <span>{{ campaign.supporters || 0 }} Supporters</span>
                            </div>
                        </div>
                    </div>
                    <div class="campaign-list-actions">
                        <router-link :to="`/campaigns/${campaign.id}`" class="btn btn-sm btn-outline">
                            <i class="fas fa-eye"></i>
                            View
                        </router-link>
                        <router-link :to="`/campaigns/${campaign.id}/edit`" class="btn btn-sm btn-outline">
                            <i class="fas fa-edit"></i>
                            Edit
                        </router-link>
                        <button class="btn btn-sm btn-outline" @click="duplicateCampaign(campaign)">
                            <i class="fas fa-copy"></i>
                            Duplicate
                        </button>
                        <button class="btn btn-sm btn-outline btn-danger" @click="confirmDelete(campaign)">
                            <i class="fas fa-trash-alt"></i>
                            Delete
                        </button>
                    </div>
                </div>
            </div>

            <!-- Pagination -->
            <div v-if="filteredCampaigns.length > 0" class="pagination">
                <button class="pagination-btn" :disabled="currentPage === 1" @click="currentPage--">
                    <i class="fas fa-chevron-left"></i>
                    Previous
                </button>
                <div class="pagination-info">
                    Page {{ currentPage }} of {{ totalPages }}
                </div>
                <button class="pagination-btn" :disabled="currentPage === totalPages" @click="currentPage++">
                    Next
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-container">
                <div class="modal-header">
                    <h3>Confirm Delete</h3>
                    <button @click="showDeleteModal = false" class="modal-close-btn">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <p>Are you sure you want to delete the campaign <strong>"{{ campaignToDelete?.title }}"</strong>?
                    </p>
                    <p class="modal-warning">This action cannot be undone.</p>
                </div>
                <div class="modal-footer">
                    <button @click="showDeleteModal = false" class="btn btn-outline">
                        Cancel
                    </button>
                    <button @click="deleteCampaign" class="btn btn-danger">
                        <i class="fas fa-trash-alt"></i>
                        Delete Campaign
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import apiClient from '@/axios';
import { useAuthStore } from '@/stores/auth';

export default {
    name: 'MyCampaignsPage',
    setup() {
        const authStore = useAuthStore();

        // State variables
        const campaigns = ref([]);
        const loading = ref(true);
        const error = ref(null);
        const viewMode = ref('grid');
        const searchQuery = ref('');
        const statusFilter = ref('all');
        const categoryFilter = ref('all');
        const sortBy = ref('newest');
        const currentPage = ref(1);
        const itemsPerPage = ref(9);
        const showDeleteModal = ref(false);
        const campaignToDelete = ref(null);
        const categories = ref([]);

        // Fetch user campaigns
        const fetchCampaigns = async () => {
            loading.value = true;
            error.value = null;

            try {
                // Get all campaigns
                const response = await apiClient.get('/campaigns/campaigns');

                // Filter campaigns by the current user's ID
                if (authStore.user && authStore.user.id) {
                    // Filter campaigns created by the current user
                    campaigns.value = response.data.filter(
                        campaign => campaign.created_by?.id === authStore.user.id
                    );

                    // Extract unique categories from user's campaigns
                    const uniqueCategories = new Map();
                    campaigns.value.forEach(campaign => {
                        if (campaign.category && !uniqueCategories.has(campaign.category.id)) {
                            uniqueCategories.set(campaign.category.id, campaign.category);
                        }
                    });

                    categories.value = Array.from(uniqueCategories.values());
                } else {
                    campaigns.value = [];
                    console.error('User not authenticated or missing ID');
                    error.value = 'User authentication required. Please log in.';
                }
            } catch (err) {
                console.error('Error fetching campaigns:', err);
                error.value = 'Failed to load your campaigns. Please try again later.';
            } finally {
                loading.value = false;
            }
        };

        // Computed properties
        const filteredCampaigns = computed(() => {
            let result = [...campaigns.value];

            // Apply search filter
            if (searchQuery.value) {
                const query = searchQuery.value.toLowerCase();
                result = result.filter(campaign =>
                    campaign.title.toLowerCase().includes(query) ||
                    (campaign.description && campaign.description.toLowerCase().includes(query))
                );
            }

            // Apply status filter
            if (statusFilter.value !== 'all') {
                switch (statusFilter.value) {
                    case 'active':
                        result = result.filter(campaign => campaign.is_active && !campaign.is_completed && !campaign.is_featured);
                        break;
                    case 'draft':
                        result = result.filter(campaign => !campaign.is_active);
                        break;
                    case 'completed':
                        result = result.filter(campaign => campaign.is_completed);
                        break;
                    case 'featured':
                        result = result.filter(campaign => campaign.is_featured);
                        break;
                }
            }

            // Apply category filter
            if (categoryFilter.value !== 'all') {
                result = result.filter(campaign => campaign.category?.id === parseInt(categoryFilter.value));
            }

            // Apply sorting
            switch (sortBy.value) {
                case 'newest':
                    result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                    break;
                case 'oldest':
                    result.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
                    break;
                case 'name-asc':
                    result.sort((a, b) => a.title.localeCompare(b.title));
                    break;
                case 'name-desc':
                    result.sort((a, b) => b.title.localeCompare(a.title));
                    break;
                case 'progress-asc':
                    result.sort((a, b) => calculateProgress(a) - calculateProgress(b));
                    break;
                case 'progress-desc':
                    result.sort((a, b) => calculateProgress(b) - calculateProgress(a));
                    break;
                case 'deadline-asc':
                    result.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));
                    break;
            }

            return result;
        });

        // Pagination
        const paginatedCampaigns = computed(() => {
            const startIndex = (currentPage.value - 1) * itemsPerPage.value;
            const endIndex = startIndex + itemsPerPage.value;
            return filteredCampaigns.value.slice(startIndex, endIndex);
        });

        const totalPages = computed(() => {
            return Math.max(1, Math.ceil(filteredCampaigns.value.length / itemsPerPage.value));
        });

        // Check if filters are applied
        const hasFiltersApplied = computed(() => {
            return searchQuery.value !== '' || statusFilter.value !== 'all' || categoryFilter.value !== 'all';
        });

        // Reset page when filters change
        watch([searchQuery, statusFilter, categoryFilter], () => {
            currentPage.value = 1;
        });

        // Helper functions
        const clearSearch = () => {
            searchQuery.value = '';
        };

        const clearFilters = () => {
            searchQuery.value = '';
            statusFilter.value = 'all';
            categoryFilter.value = 'all';
            sortBy.value = 'newest';
        };

        const getCategoryName = (categoryId) => {
            if (!categoryId) return 'Uncategorized';
            const category = categories.value.find(cat => cat.id === categoryId);
            return category ? category.name : 'Uncategorized';
        };

        const calculateProgress = (campaign) => {
            if (!campaign.funding_goal || campaign.funding_goal === 0) return 0;
            const currentAmount = campaign.current_amount || 0;
            const progress = (currentAmount / campaign.funding_goal) * 100;
            return Math.min(Math.round(progress), 100);
        };

        const formatNumber = (num) => {
            if (!num) return '0';
            return parseFloat(num).toLocaleString('en-US');
        };

        const formatDeadline = (dateString) => {
            if (!dateString) return 'No deadline';

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

        const getCampaignStatus = (campaign) => {
            if (!campaign) return 'Unknown';

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

        const getCampaignStatusClass = (campaign) => {
            if (!campaign) return '';

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

        const truncateText = (text, maxLength) => {
            if (!text) return '';
            if (text.length <= maxLength) return text;
            return text.substring(0, maxLength) + '...';
        };

        const handleImageError = (event) => {
            event.target.src = '/placeholder.jpg';
        };

        // Campaign actions
        const confirmDelete = (campaign) => {
            campaignToDelete.value = campaign;
            showDeleteModal.value = true;
        };

        const deleteCampaign = async () => {
            if (!campaignToDelete.value) return;

            try {
                // In a real app, you would send a delete request to your API
                await apiClient.delete(`/campaigns/${campaignToDelete.value.id}`);

                // Remove from local array
                campaigns.value = campaigns.value.filter(c => c.id !== campaignToDelete.value.id);

                // Close modal and reset
                showDeleteModal.value = false;
                campaignToDelete.value = null;

                // Show success message (in a real app, you might use a toast notification)
                alert('Campaign deleted successfully');
            } catch (err) {
                console.error('Error deleting campaign:', err);
                alert('Failed to delete campaign. Please try again.');
            }
        };

        const duplicateCampaign = async (campaign) => {
            try {
                // Create a copy of the campaign without the ID
                const campaignCopy = {
                    ...campaign,
                    title: `Copy of ${campaign.title}`,
                    is_active: false,
                    is_featured: false,
                    is_completed: false
                };

                // Remove the ID so a new one will be generated
                delete campaignCopy.id;

                // Send the new campaign to the API
                const response = await apiClient.post('/campaigns', campaignCopy);

                // Add the new campaign to the list
                campaigns.value.unshift(response.data);

                // Show success message
                alert('Campaign duplicated successfully. The new campaign is saved as a draft.');
            } catch (err) {
                console.error('Error duplicating campaign:', err);
                alert('Failed to duplicate campaign. Please try again.');
            }
        };

        // Fetch data when component mounts
        onMounted(() => {
            fetchCampaigns();
        });

        return {
            campaigns,
            loading,
            error,
            viewMode,
            searchQuery,
            statusFilter,
            categoryFilter,
            sortBy,
            currentPage,
            categories,
            filteredCampaigns,
            paginatedCampaigns,
            totalPages,
            hasFiltersApplied,
            showDeleteModal,
            campaignToDelete,
            fetchCampaigns,
            clearSearch,
            clearFilters,
            getCategoryName,
            calculateProgress,
            formatNumber,
            formatDeadline,
            getCampaignStatus,
            getCampaignStatusClass,
            truncateText,
            handleImageError,
            confirmDelete,
            deleteCampaign,
            duplicateCampaign
        };
    }
};
</script>

<style>
/* My Campaigns Page Styles */
.my-campaigns-page {
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

/* Filters and Controls */
.campaigns-controls {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--spacing-xl);
    flex-wrap: wrap;
    gap: var(--spacing-md);
}

.filters-wrapper {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
    flex: 1;
}

.search-filter {
    width: 100%;
    max-width: 500px;
}

.search-input-wrapper {
    position: relative;
    width: 100%;
}

.search-icon {
    position: absolute;
    left: var(--spacing-md);
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
}

.search-input {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md) var(--spacing-sm) calc(var(--spacing-md) * 2 + 16px);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    font-size: var(--font-size-md);
}

.clear-search-btn {
    position: absolute;
    right: var(--spacing-md);
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0;
}

.filter-group {
    display: flex;
    gap: var(--spacing-md);
    flex-wrap: wrap;
}

.filter-select {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.filter-select label {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.select-input {
    padding: var(--spacing-xs) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    background-color: var(--background);
    min-width: 150px;
}

.view-toggle {
    display: flex;
    gap: var(--spacing-xs);
}

.view-toggle-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--background);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.view-toggle-btn.active {
    background-color: var(--primary);
    color: white;
    border-color: var(--primary);
}

/* Campaigns Grid */
.campaigns-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
}

.campaign-card {
    background-color: var(--background);
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid var(--border-color);
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

.campaign-deadline,
.campaign-supporters {
    display: flex;
    align-items: center;
    gap: 4px;
}

.campaign-actions {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
}

/* Campaigns List View */
.campaigns-list {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
}

.campaign-list-item {
    display: flex;
    background-color: var(--background);
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.campaign-list-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.campaign-list-image {
    width: 200px;
    height: 150px;
    flex-shrink: 0;
}

.campaign-list-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.campaign-list-content {
    flex: 1;
    padding: var(--spacing-md);
    display: flex;
    flex-direction: column;
}

.campaign-list-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--spacing-xs);
}

.campaign-list-title {
    margin: 0;
    font-size: var(--font-size-lg);
}

.campaign-list-status {
    padding: 4px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
}

.campaign-list-category {
    display: inline-block;
    background-color: var(--primary-light);
    color: var(--text-on-primary);
    padding: 2px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    margin-bottom: var(--spacing-sm);
    align-self: flex-start;
}

.campaign-list-description {
    margin: 0 0 var(--spacing-md) 0;
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    line-height: 1.5;
}

.campaign-list-stats {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-md);
    margin-top: auto;
}

.campaign-list-stat {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.campaign-list-actions {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    border-left: 1px solid var(--border-color);
    justify-content: center;
}

/* Pagination */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: var(--spacing-lg);
    margin-top: var(--spacing-xl);
}

.pagination-btn {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-xs) var(--spacing-md);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    background-color: var(--background);
    cursor: pointer;
    transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
    background-color: var(--surface);
}

.pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination-info {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

/* Modal */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1100;
}

.modal-container {
    background-color: var(--background);
    border-radius: var(--border-radius-md);
    width: 90%;
    max-width: 500px;
    box-shadow: var(--shadow-lg);
    overflow: hidden;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
    margin: 0;
}

.modal-close-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
}

.modal-body {
    padding: var(--spacing-lg);
}

.modal-warning {
    color: var(--error);
    font-weight: 500;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    border-top: 1px solid var(--border-color);
}

.btn-danger {
    background-color: var(--error);
    border-color: var(--error);
    color: white;
}

.btn-danger:hover {
    background-color: var(--error-dark);
    border-color: var(--error-dark);
}

/* Loading, Error, Empty States */
.loading-container,
.error-container,
.empty-state {
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

.error-icon,
.empty-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin-bottom: var(--spacing-md);
}

.error-icon {
    background-color: var(--error);
    color: white;
    font-size: 2rem;
    font-weight: 700;
}

.empty-icon {
    background-color: var(--surface);
    color: var(--text-secondary);
    font-size: 1.5rem;
}

/* Responsive Styles */
@media (max-width: 992px) {
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

    .filter-group {
        width: 100%;
    }

    .filter-select {
        flex: 1;
    }
}

@media (max-width: 768px) {
    .campaigns-controls {
        flex-direction: column;
    }

    .view-toggle {
        align-self: flex-end;
    }

    .campaign-list-item {
        flex-direction: column;
    }

    .campaign-list-image {
        width: 100%;
        height: 200px;
    }

    .campaign-list-actions {
        flex-direction: row;
        border-left: none;
        border-top: 1px solid var(--border-color);
    }
}

@media (max-width: 576px) {
    .filter-group {
        flex-direction: column;
    }

    .campaign-actions {
        flex-direction: column;
    }

    .campaign-actions .btn {
        width: 100%;
    }

    .pagination {
        flex-direction: column;
        gap: var(--spacing-md);
    }
}
</style>