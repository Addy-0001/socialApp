<template>
    <div class="my-donations-page">
        <div class="container">
            <!-- Page Header -->
            <div class="page-header" style="padding-inline: 20px;">
                <div class="page-title">
                    <h1>My Donations</h1>
                    <p class="page-subtitle" style="color: white;">Track your contributions and the impact you've made
                    </p>
                </div>
                <div class="page-actions">

                    <router-link to="/campaigns" class="btn btn-primary">
                        <i class="fas fa-hand-holding-heart"></i>
                        Donate Again
                    </router-link>
                </div>
            </div>

            <!-- Donation Summary -->
            <div class="donation-summary">
                <div class="summary-card">
                    <div class="summary-icon">
                        <i class="fas fa-dollar-sign"></i>
                    </div>
                    <div class="summary-content">
                        <h3>Total Donated</h3>
                        <div class="summary-value">${{ formatNumber(totalDonated) }}</div>
                    </div>
                </div>

                <div class="summary-card">
                    <div class="summary-icon">
                        <i class="fas fa-gift"></i>
                    </div>
                    <div class="summary-content">
                        <h3>Donations Made</h3>
                        <div class="summary-value">{{ userDonations.length }}</div>
                    </div>
                </div>

                <div class="summary-card">
                    <div class="summary-icon">
                        <i class="fas fa-bullhorn"></i>
                    </div>
                    <div class="summary-content">
                        <h3>Campaigns Supported</h3>
                        <div class="summary-value">{{ uniqueCampaignsCount }}</div>
                    </div>
                </div>

                <div class="summary-card">
                    <div class="summary-icon">
                        <i class="fas fa-certificate"></i>
                    </div>
                    <div class="summary-content">
                        <h3>Impact Score</h3>
                        <div class="summary-value">{{ calculateImpactScore() }}</div>
                    </div>
                </div>
            </div>

            <!-- Filters and Controls -->
            <div class="donations-controls">
                <div class="filters-wrapper">
                    <div class="search-filter">
                        <div class="search-input-wrapper">
                            <i class="fas fa-search search-icon"></i>
                            <input type="text" v-model="searchQuery" placeholder="Search donations..."
                                class="search-input" />
                            <button v-if="searchQuery" @click="clearSearch" class="clear-search-btn">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>

                    <div class="filter-group">
                        <div class="filter-select">
                            <label for="date-filter">Time Period</label>
                            <select id="date-filter" v-model="dateFilter" class="select-input">
                                <option value="all">All Time</option>
                                <option value="this-month">This Month</option>
                                <option value="last-month">Last Month</option>
                                <option value="this-year">This Year</option>
                                <option value="last-year">Last Year</option>
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
                                <option value="date-desc">Date (Newest First)</option>
                                <option value="date-asc">Date (Oldest First)</option>
                                <option value="amount-desc">Amount (High to Low)</option>
                                <option value="amount-asc">Amount (Low to High)</option>
                                <option value="campaign">Campaign Name</option>
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
                <p>Loading your donations...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="error-container">
                <div class="error-icon">!</div>
                <h3>Oops! Something went wrong</h3>
                <p>{{ error }}</p>
                <button @click="fetchDonations" class="btn btn-primary">Try Again</button>
            </div>

            <!-- Empty State -->
            <div v-else-if="filteredDonations.length === 0 && !loading" class="empty-state">
                <div v-if="hasFiltersApplied">
                    <div class="empty-icon">
                        <i class="fas fa-filter"></i>
                    </div>
                    <h3>No donations match your filters</h3>
                    <p>Try adjusting your search criteria or clear filters to see all your donations.</p>
                    <button @click="clearFilters" class="btn btn-primary">Clear Filters</button>
                </div>
                <div v-else>
                    <div class="empty-icon">
                        <i class="fas fa-hand-holding-heart"></i>
                    </div>
                    <h3>No Donations Yet</h3>
                    <p>You haven't made any donations yet. Start supporting campaigns that matter to you!</p>
                    <router-link to="/campaigns" class="btn btn-primary">Browse Campaigns</router-link>
                </div>
            </div>

            <!-- Donations Grid View -->
            <div v-else-if="viewMode === 'grid'" class="donations-grid">
                <div v-for="donation in paginatedDonations" :key="donation.id" class="donation-card">
                    <div class="donation-header">
                        <div class="donation-amount">${{ formatNumber(donation.amount) }}</div>
                        <div class="donation-date">{{ formatDate(donation.created_at || donation.date) }}</div>
                    </div>

                    <div class="donation-campaign">
                        <img :src="donation.campaign?.cover_image || '/placeholder.jpg'" :alt="donation.campaign?.title"
                            class="campaign-image" @error="handleImageError" />
                        <div class="campaign-info">
                            <div class="campaign-category">{{ getCategoryName(donation.campaign?.category_id) }}</div>
                            <h3 class="campaign-title">{{ donation.campaign?.title }}</h3>
                        </div>
                    </div>

                    <div class="donation-details">
                        <div class="donation-status" :class="getDonationStatusClass(donation)">
                            {{ getDonationStatus(donation) }}
                        </div>
                        <div class="donation-reference">
                            Ref: {{ donation.reference_number || donation.id }}
                        </div>
                    </div>

                    <div class="donation-actions">
                        <router-link :to="`/campaigns/${donation.campaign.id}`" class="btn btn-sm btn-outline">
                            <i class="fas fa-eye"></i>
                            View Campaign
                        </router-link>

                        <button class="btn btn-sm btn-primary" @click="donateToCampaign(donation.campaign.id)">
                            <i class="fas fa-hand-holding-heart"></i>
                            Donate Again
                        </button>
                    </div>
                </div>
            </div>

            <!-- Donations List View -->
            <div v-else class="donations-list">
                <div v-for="donation in paginatedDonations" :key="donation.id" class="donation-list-item">
                    <div class="donation-list-image">
                        <img :src="donation.campaign?.cover_image || '/placeholder.jpg'" :alt="donation.campaign?.title"
                            @error="handleImageError" />
                    </div>

                    <div class="donation-list-content">
                        <div class="donation-list-header">
                            <h3 class="donation-list-title">{{ donation.campaign?.title }}</h3>
                            <div class="donation-list-amount">${{ formatNumber(donation.amount) }}</div>
                        </div>

                        <div class="donation-list-meta">
                            <div class="donation-list-category">{{ getCategoryName(donation.campaign?.category_id) }}
                            </div>
                            <div class="donation-list-date">{{ formatDate(donation.created_at || donation.date) }}</div>
                        </div>

                        <div class="donation-list-details">
                            <div class="donation-list-status" :class="getDonationStatusClass(donation)">
                                {{ getDonationStatus(donation) }}
                            </div>
                            <div class="donation-list-reference">
                                Reference: {{ donation.reference_number || donation.id }}
                            </div>
                        </div>

                        <div class="donation-list-message" v-if="donation.message">
                            <div class="message-label">Your Message:</div>
                            <div class="message-content">"{{ donation.message }}"</div>
                        </div>
                    </div>

                    <div class="donation-list-actions">
                        <router-link :to="`/campaigns/${donation.campaign.id}`" class="btn btn-sm btn-outline">
                            <i class="fas fa-eye"></i>
                            View Campaign
                        </router-link>

                        <button class="btn btn-sm btn-primary" @click="donateToCampaign(donation.campaign.id)">
                            <i class="fas fa-hand-holding-heart"></i>
                            Donate Again
                        </button>
                    </div>
                </div>
            </div>

            <!-- Pagination -->
            <div v-if="filteredDonations.length > 0" class="pagination">
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

            <!-- Tax Information -->
            <div class="tax-info-section">
                <div class="tax-info-icon">
                    <i class="fas fa-info-circle"></i>
                </div>
                <div class="tax-info-content">
                    <h3>Tax Deduction Information</h3>
                    <p>Donations to our registered nonprofit organization may be tax-deductible. Please consult with a
                        tax professional and keep your receipts for tax filing purposes.</p>
                    <p>Our Tax ID: 12-3456789</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import apiClient from '@/axios';
import { useAuthStore } from '@/stores/auth';

export default {
    name: 'MyDonationsPage',
    setup() {
        const router = useRouter();
        const route = useRoute();
        const authStore = useAuthStore();

        // State variables
        const allDonations = ref([]);
        const userDonations = ref([]);
        const loading = ref(true);
        const error = ref(null);
        const viewMode = ref('grid');
        const searchQuery = ref('');
        const dateFilter = ref('all');
        const categoryFilter = ref('all');
        const sortBy = ref('date-desc');
        const currentPage = ref(1);
        const itemsPerPage = ref(9);
        const categories = ref([]);
        const campaigns = ref({});

        // Get user ID from route params
        const userId = computed(() => {
            return route.params.id || (authStore.user ? authStore.user.id : null);
        });

        // Fetch all donations and filter by user ID
        const fetchDonations = async () => {
            if (!userId.value) {
                error.value = 'User ID not found. Please log in or check the URL.';
                loading.value = false;
                return;
            }

            loading.value = true;
            error.value = null;

            try {
                // Fetch all donations
                const response = await apiClient.get('/campaigns/donations/');
                allDonations.value = response.data;

                // Filter donations by user ID
                userDonations.value = allDonations.value.filter(donation =>
                    donation.user.id === parseInt(userId.value)
                );

                // Fetch campaign details for each donation
                await fetchCampaignDetails();

                // Extract categories from campaigns
                extractCategories();

            } catch (err) {
                console.error('Error fetching donations:', err);
                error.value = 'Failed to load donations. Please try again later.';

                // For demo purposes, load mock data if API fails
                loadMockData();
            } finally {
                loading.value = false;
            }
        };

        // Fetch campaign details for each donation
        const fetchCampaignDetails = async () => {
            const uniqueCampaignIds = [...new Set(userDonations.value.map(d => d.campaign.id))];

            try {
                // Fetch campaign details in parallel
                const campaignPromises = uniqueCampaignIds.map(async (campaignId) => {
                    try {
                        const response = await apiClient.get(`/campaigns/campaigns/${campaignId}`);
                        return { id: campaignId, data: response.data };
                    } catch (err) {
                        console.error(`Error fetching campaign ${campaignId}:`, err);
                        return { id: campaignId, data: null };
                    }
                });

                const campaignResults = await Promise.all(campaignPromises);

                // Create a map of campaign ID to campaign data
                campaignResults.forEach(result => {
                    if (result.data) {
                        campaigns.value[result.id] = result.data; // Store the full campaign data
                    }
                });

                // Attach campaign data to donations
                userDonations.value.forEach(donation => {
                    donation.campaign = campaigns.value[donation.campaign.id] || donation.campaign;
                });

            } catch (err) {
                console.error('Error fetching campaign details:', err);
            }
        };

        // Extract unique categories from campaigns
        const extractCategories = () => {
            const uniqueCategories = new Map();

            Object.values(campaigns.value).forEach(campaign => {
                if (campaign && campaign.category_id && !uniqueCategories.has(campaign.category_id)) {
                    uniqueCategories.set(campaign.category_id, {
                        id: campaign.category_id,
                        name: campaign.category?.name || `Category ${campaign.category_id}`
                    });
                }
            });

            categories.value = Array.from(uniqueCategories.values());
        };

        // Load mock data for demonstration
        const loadMockData = () => {
            const mockCategories = [
                { id: 1, name: 'Environment' },
                { id: 2, name: 'Education' },
                { id: 3, name: 'Healthcare' },
                { id: 4, name: 'Animal Welfare' },
                { id: 5, name: 'Human Rights' }
            ];

            categories.value = mockCategories;

            const mockCampaigns = {
                101: {
                    id: 101,
                    title: 'Clean Ocean Initiative',
                    cover_image: '/placeholder.jpg',
                    category_id: 1
                },
                102: {
                    id: 102,
                    title: 'School Supplies for Children',
                    cover_image: '/placeholder.jpg',
                    category_id: 2
                },
                103: {
                    id: 103,
                    title: 'Medical Aid for Refugees',
                    cover_image: '/placeholder.jpg',
                    category_id: 3
                },
                104: {
                    id: 104,
                    title: 'Wildlife Conservation Project',
                    cover_image: '/placeholder.jpg',
                    category_id: 4
                },
                105: {
                    id: 105,
                    title: 'Human Rights Advocacy',
                    cover_image: '/placeholder.jpg',
                    category_id: 5
                }
            };

            campaigns.value = mockCampaigns;

            const mockDonations = [
                {
                    id: 1,
                    amount: 50.00,
                    created_at: '2023-04-15T10:30:00Z',
                    status: 'completed',
                    reference_number: 'DON-12345',
                    message: 'Keep up the great work!',
                    campaign_id: 101,
                    donor_id: parseInt(userId.value)
                },
                {
                    id: 2,
                    amount: 100.00,
                    created_at: '2023-03-22T14:45:00Z',
                    status: 'completed',
                    reference_number: 'DON-12346',
                    message: 'This cause means a lot to me.',
                    campaign_id: 102,
                    donor_id: parseInt(userId.value)
                },
                {
                    id: 3,
                    amount: 25.00,
                    created_at: '2023-02-10T09:15:00Z',
                    status: 'completed',
                    reference_number: 'DON-12347',
                    message: null,
                    campaign_id: 103,
                    donor_id: parseInt(userId.value)
                },
                {
                    id: 4,
                    amount: 75.00,
                    created_at: '2023-01-05T16:20:00Z',
                    status: 'completed',
                    reference_number: 'DON-12348',
                    message: 'Happy to support this cause!',
                    campaign_id: 104,
                    donor_id: parseInt(userId.value)
                },
                {
                    id: 5,
                    amount: 150.00,
                    created_at: '2022-12-20T11:00:00Z',
                    status: 'completed',
                    reference_number: 'DON-12349',
                    message: 'Thank you for your important work.',
                    campaign_id: "Семен Маркович",
                    id: 105,
                    donor_id: parseInt(userId.value)
                }
            ];

            // Attach campaign data to donations
            mockDonations.forEach(donation => {
                donation.campaign = mockCampaigns[donation.campaign.id] || null;
            });

            userDonations.value = mockDonations;
            error.value = null;
        };

        // Computed properties
        const totalDonated = computed(() => {
            return userDonations.value.reduce((total, donation) => total + parseFloat(donation.amount || 0), 0);
        });

        const uniqueCampaignsCount = computed(() => {
            const uniqueCampaigns = new Set(userDonations.value.map(donation => donation.campaign.id));
            return uniqueCampaigns.size;
        });

        const filteredDonations = computed(() => {
            let result = [...userDonations.value];

            // Apply search filter
            if (searchQuery.value) {
                const query = searchQuery.value.toLowerCase();
                result = result.filter(donation =>
                    (donation.campaign?.title || '').toLowerCase().includes(query) ||
                    (donation.reference_number || '').toLowerCase().includes(query) ||
                    (donation.message && donation.message.toLowerCase().includes(query))
                );
            }

            // Apply date filter
            if (dateFilter.value !== 'all') {
                const now = new Date();
                const currentMonth = now.getMonth();
                const currentYear = now.getFullYear();

                switch (dateFilter.value) {
                    case 'this-month':
                        result = result.filter(donation => {
                            const donationDate = new Date(donation.created_at || donation.date);
                            return donationDate.getMonth() === currentMonth &&
                                donationDate.getFullYear() === currentYear;
                        });
                        break;
                    case 'last-month':
                        result = result.filter(donation => {
                            const donationDate = new Date(donation.created_at || donation.date);
                            const lastMonth = currentMonth === 0 ? 11 : currentMonth - 1;
                            const lastMonthYear = currentMonth === 0 ? currentYear - 1 : currentYear;
                            return donationDate.getMonth() === lastMonth &&
                                donationDate.getFullYear() === lastMonthYear;
                        });
                        break;
                    case 'this-year':
                        result = result.filter(donation => {
                            const donationDate = new Date(donation.created_at || donation.date);
                            return donationDate.getFullYear() === currentYear;
                        });
                        break;
                    case 'last-year':
                        result = result.filter(donation => {
                            const donationDate = new Date(donation.created_at || donation.date);
                            return donationDate.getFullYear() === currentYear - 1;
                        });
                        break;
                }
            }

            // Apply category filter
            if (categoryFilter.value !== 'all') {
                result = result.filter(donation =>
                    donation.campaign?.category_id === parseInt(categoryFilter.value)
                );
            }

            // Apply sorting
            switch (sortBy.value) {
                case 'date-desc':
                    result.sort((a, b) => new Date(b.created_at || b.date) - new Date(a.created_at || a.date));
                    break;
                case 'date-asc':
                    result.sort((a, b) => new Date(a.created_at || a.date) - new Date(b.created_at || b.date));
                    break;
                case 'amount-desc':
                    result.sort((a, b) => parseFloat(b.amount || 0) - parseFloat(a.amount || 0));
                    break;
                case 'amount-asc':
                    result.sort((a, b) => parseFloat(a.amount || 0) - parseFloat(b.amount || 0));
                    break;
                case 'campaign':
                    result.sort((a, b) => (a.campaign?.title || '').localeCompare(b.campaign?.title || ''));
                    break;
            }

            return result;
        });

        // Pagination
        const paginatedDonations = computed(() => {
            const startIndex = (currentPage.value - 1) * itemsPerPage.value;
            const endIndex = startIndex + itemsPerPage.value;
            return filteredDonations.value.slice(startIndex, endIndex);
        });

        const totalPages = computed(() => {
            return Math.max(1, Math.ceil(filteredDonations.value.length / itemsPerPage.value));
        });

        // Check if filters are applied
        const hasFiltersApplied = computed(() => {
            return searchQuery.value !== '' || dateFilter.value !== 'all' || categoryFilter.value !== 'all';
        });

        // Reset page when filters change
        watch([searchQuery, dateFilter, categoryFilter], () => {
            currentPage.value = 1;
        });

        // Helper functions
        const clearSearch = () => {
            searchQuery.value = '';
        };

        const clearFilters = () => {
            searchQuery.value = '';
            dateFilter.value = 'all';
            categoryFilter.value = 'all';
            sortBy.value = 'date-desc';
        };

        const getCategoryName = (categoryId) => {
            if (!categoryId) return 'Uncategorized';
            const category = categories.value.find(cat => cat.id === categoryId);
            return category ? category.name : 'Uncategorized';
        };

        const formatNumber = (num) => {
            if (!num) return '0.00';
            return parseFloat(num).toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
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

        const getDonationStatus = (donation) => {
            if (!donation) return 'Unknown';

            const status = donation.status || 'completed';

            switch (status.toLowerCase()) {
                case 'completed':
                    return 'Completed';
                case 'pending':
                    return 'Pending';
                case 'failed':
                    return 'Failed';
                case 'refunded':
                    return 'Refunded';
                default:
                    return status.charAt(0).toUpperCase() + status.slice(1);
            }
        };

        const getDonationStatusClass = (donation) => {
            if (!donation) return '';

            const status = donation.status || 'completed';

            switch (status.toLowerCase()) {
                case 'completed':
                    return 'status-completed';
                case 'pending':
                    return 'status-pending';
                case 'failed':
                    return 'status-failed';
                case 'refunded':
                    return 'status-refunded';
                default:
                    return '';
            }
        };

        const handleImageError = (event) => {
            event.target.src = '/placeholder.jpg';
        };

        const calculateImpactScore = () => {
            // In a real app, this would be a more complex calculation
            // based on donation amount, frequency, and other factors
            const baseScore = userDonations.value.length * 10;
            const amountBonus = Math.floor(totalDonated.value / 100) * 5;
            return baseScore + amountBonus;
        };

        const donateToCampaign = (campaignId) => {
            // In a real app, this would navigate to the donation page for the campaign
            router.push(`/campaigns/${campaignId}/donate`);
        };

        // Fetch data when component mounts
        onMounted(() => {
            fetchDonations();
        });

        return {
            userDonations,
            loading,
            error,
            viewMode,
            searchQuery,
            dateFilter,
            categoryFilter,
            sortBy,
            currentPage,
            categories,
            totalDonated,
            uniqueCampaignsCount,
            filteredDonations,
            paginatedDonations,
            totalPages,
            hasFiltersApplied,
            fetchDonations,
            clearSearch,
            clearFilters,
            getCategoryName,
            formatNumber,
            formatDate,
            getDonationStatus,
            getDonationStatusClass,
            handleImageError,
            calculateImpactScore,
            donateToCampaign
        };
    }
};
</script>

<style scoped>
/* My Donations Page Styles */
.my-donations-page {
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

/* Donation Summary */
.donation-summary {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
}

.summary-card {
    background-color: var(--surface);
    border-radius: var(--border-radius-md);
    padding: var(--spacing-lg);
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
}

.summary-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: var(--primary-light);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.summary-content {
    flex: 1;
}

.summary-content h3 {
    font-size: 1rem;
    margin: 0 0 var(--spacing-xs) 0;
    color: var(--text-secondary);
}

.summary-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text-primary);
}

/* Filters and Controls */
.donations-controls {
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

/* Donations Grid */
.donations-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
}

.donation-card {
    background-color: var(--background);
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-md);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
}

.donation-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.donation-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md);
    background-color: var(--surface);
    border-bottom: 1px solid var(--border-color);
}

.donation-amount {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

.donation-date {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.donation-campaign {
    padding: var(--spacing-md);
    display: flex;
    gap: var(--spacing-md);
    align-items: center;
    border-bottom: 1px solid var(--border-color);
}

.campaign-image {
    width: 60px;
    height: 60px;
    border-radius: var(--border-radius-md);
    object-fit: cover;
}

.campaign-info {
    flex: 1;
}

.campaign-category {
    display: inline-block;
    background-color: var(--primary-light);
    color: var(--text-on-primary);
    padding: 2px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    margin-bottom: var(--spacing-xs);
}

.campaign-title {
    font-size: var(--font-size-md);
    margin: 0;
    line-height: 1.3;
}

.donation-details {
    padding: var(--spacing-md);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
}

.donation-status {
    padding: 4px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
}

.status-completed {
    background-color: var(--success);
    color: white;
}

.status-pending {
    background-color: var(--warning);
    color: var(--text-on-warning);
}

.status-failed {
    background-color: var(--error);
    color: white;
}

.status-refunded {
    background-color: var(--secondary);
    color: white;
}

.donation-reference {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
}

.donation-actions {
    padding: var(--spacing-md);
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
    margin-top: auto;
}

/* Donations List View */
.donations-list {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
}

.donation-list-item {
    display: flex;
    background-color: var(--background);
    border-radius: var(--border-radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-color);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.donation-list-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.donation-list-image {
    width: 120px;
    height: 120px;
    flex-shrink: 0;
}

.donation-list-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.donation-list-content {
    flex: 1;
    padding: var(--spacing-md);
    display: flex;
    flex-direction: column;
}

.donation-list-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--spacing-xs);
}

.donation-list-title {
    margin: 0;
    font-size: var(--font-size-lg);
}

.donation-list-amount {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary);
}

.donation-list-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);
}

.donation-list-category {
    display: inline-block;
    background-color: var(--primary-light);
    color: var(--text-on-primary);
    padding: 2px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
}

.donation-list-date {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.donation-list-details {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);
}

.donation-list-status {
    padding: 4px 8px;
    border-radius: var(--border-radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
}

.donation-list-reference {
    font-size: var(--font-size-xs);
    color: var(--text-secondary);
}

.donation-list-message {
    margin-top: var(--spacing-sm);
    font-size: var(--font-size-sm);
}

.message-label {
    font-weight: 600;
    margin-bottom: 4px;
}

.message-content {
    font-style: italic;
    color: var(--text-secondary);
}

.donation-list-actions {
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

/* Tax Information Section */
.tax-info-section {
    margin-top: var(--spacing-xl);
    padding: var(--spacing-lg);
    background-color: var(--surface);
    border-radius: var(--border-radius-md);
    border: 1px solid var(--border-color);
    display: flex;
    gap: var(--spacing-lg);
    align-items: center;
}

.tax-info-icon {
    font-size: 2rem;
    color: var(--primary);
}

.tax-info-content h3 {
    margin-top: 0;
    margin-bottom: var(--spacing-sm);
}

.tax-info-content p {
    margin: 0 0 var(--spacing-sm) 0;
    color: var(--text-secondary);
}

.tax-info-content p:last-child {
    margin-bottom: 0;
    font-weight: 600;
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
    .donation-summary {
        grid-template-columns: repeat(2, 1fr);
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

    .filter-group {
        width: 100%;
    }

    .filter-select {
        flex: 1;
    }
}

@media (max-width: 768px) {
    .donations-controls {
        flex-direction: column;
    }

    .view-toggle {
        align-self: flex-end;
    }

    .donation-list-item {
        flex-direction: column;
    }

    .donation-list-image {
        width: 100%;
        height: 150px;
    }

    .donation-list-actions {
        flex-direction: row;
        border-left: none;
        border-top: 1px solid var(--border-color);
    }

    .tax-info-section {
        flex-direction: column;
        text-align: center;
    }
}

@media (max-width: 576px) {
    .donation-summary {
        grid-template-columns: 1fr;
    }

    .filter-group {
        flex-direction: column;
    }

    .donation-actions {
        flex-direction: column;
    }

    .donation-actions .btn {
        width: 100%;
    }

    .pagination {
        flex-direction: column;
        gap: var(--spacing-md);
    }
}
</style>