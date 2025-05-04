<template>
  <div class="campaigns-list-page">
    <!-- Page Header -->
    <section class="page-header">
      <div class="container">
        <div class="page-header-content">
          <div>
            <h1 class="page-title">Explore Campaigns</h1>
            <p class="page-description">
              Discover and support campaigns that are making a difference in
              communities around the world.
            </p>
          </div>
          <router-link to="/campaigns/create" class="btn btn-primary"
            >Start a Campaign</router-link
          >
        </div>
      </div>
    </section>

    <!-- Filters and Controls -->
    <section class="filters-section">
      <div class="container">
        <div class="filters-container">
          <!-- Search Bar -->
          <div class="search-container">
            <div class="search-input-wrapper">
              <i class="fas fa-search search-icon"></i>
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Search campaigns..."
                class="search-input"
                @input="handleSearch"
              />
              <button
                v-if="searchQuery"
                @click="clearSearch"
                class="search-clear-btn"
                aria-label="Clear search"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>

          <!-- Filter Controls -->
          <div class="filter-controls">
            <div class="filter-dropdown">
              <label for="category-filter">Category</label>
              <select
                id="category-filter"
                v-model="selectedCategory"
                class="form-control"
                @change="applyFilters"
              >
                <option value="">All Categories</option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div class="filter-dropdown">
              <label for="status-filter">Status</label>
              <select
                id="status-filter"
                v-model="selectedStatus"
                class="form-control"
                @change="applyFilters"
              >
                <option value="">All Statuses</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="featured">Featured</option>
              </select>
            </div>

            <div class="filter-dropdown">
              <label for="sort-by">Sort By</label>
              <select
                id="sort-by"
                v-model="sortBy"
                class="form-control"
                @change="applyFilters"
              >
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="goal-high">Highest Goal</option>
                <option value="goal-low">Lowest Goal</option>
                <option value="deadline">Deadline (Soonest)</option>
              </select>
            </div>
          </div>

          <!-- View Toggle -->
          <div class="view-toggle">
            <button
              @click="viewMode = 'grid'"
              class="view-toggle-btn"
              :class="{ active: viewMode === 'grid' }"
              aria-label="Grid view"
            >
              <i class="fas fa-th-large"></i>
            </button>
            <button
              @click="viewMode = 'list'"
              class="view-toggle-btn"
              :class="{ active: viewMode === 'list' }"
              aria-label="List view"
            >
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>

        <!-- Active Filters -->
        <div v-if="hasActiveFilters" class="active-filters">
          <div class="active-filters-label">Active Filters:</div>
          <div class="filter-tags">
            <div v-if="selectedCategory" class="filter-tag">
              Category: {{ getCategoryName(selectedCategory) }}
              <button
                @click="removeFilter('category')"
                class="filter-tag-remove"
                aria-label="Remove category filter"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div v-if="selectedStatus" class="filter-tag">
              Status: {{ formatStatus(selectedStatus) }}
              <button
                @click="removeFilter('status')"
                class="filter-tag-remove"
                aria-label="Remove status filter"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div v-if="searchQuery" class="filter-tag">
              Search: "{{ searchQuery }}"
              <button
                @click="removeFilter('search')"
                class="filter-tag-remove"
                aria-label="Remove search filter"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
          <button @click="resetFilters" class="btn btn-sm btn-outline">
            Clear All
          </button>
        </div>
      </div>
    </section>

    <!-- Campaigns List -->
    <section class="campaigns-section">
      <div class="container">
        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading campaigns...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-container">
          <div class="error-icon">!</div>
          <h3>Oops! Something went wrong</h3>
          <p>{{ error }}</p>
          <button @click="fetchCampaigns" class="btn btn-primary">
            Try Again
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredCampaigns.length === 0" class="empty-container">
          <div class="empty-icon">📋</div>
          <h3>No Campaigns Found</h3>
          <p v-if="hasActiveFilters">
            Try adjusting your filters or search criteria
          </p>
          <p v-else>There are no campaigns available at the moment</p>
          <button
            v-if="hasActiveFilters"
            @click="resetFilters"
            class="btn btn-primary"
          >
            Clear Filters
          </button>
        </div>

        <!-- Grid View -->
        <div v-else-if="viewMode === 'grid'" class="campaigns-grid">
          <div
            v-for="campaign in paginatedCampaigns"
            :key="campaign.id"
            class="campaign-card"
          >
            <div class="campaign-image">
              <img
                :src="campaign.cover_image"
                :alt="campaign.title"
                @error="handleImageError"
              />
              <div v-if="campaign.is_featured" class="featured-badge">
                Featured
              </div>
              <div v-if="campaign.is_business" class="business-badge">
                Business
              </div>
            </div>
            <div class="campaign-content">
              <div class="campaign-category">{{ campaign.category.name }}</div>
              <h3 class="campaign-title">{{ campaign.title }}</h3>
              <p class="campaign-description">
                {{ truncateText(campaign.description, 100) }}
              </p>

              <div class="campaign-meta">
                <div class="campaign-location">
                  <i class="fas fa-map-marker-alt"></i>
                  {{ campaign.location }}
                </div>
                <div class="campaign-deadline">
                  <i class="fas fa-clock"></i>
                  {{ formatDeadline(campaign.deadline) }}
                </div>
              </div>

              <div class="campaign-progress">
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: calculateProgress(campaign) + '%' }"
                  ></div>
                </div>
                <div class="progress-stats">
                  <span class="funding-goal"
                    >${{ formatNumber(campaign.funding_goals) }} Goal</span
                  >
                  <span class="funding-progress"
                    >{{ calculateProgress(campaign) }}%</span
                  >
                </div>
              </div>

              <div class="campaign-footer">
                <div class="campaign-creator">
                  <span>By {{ campaign.created_by.full_name }}</span>
                </div>
                <router-link
                  :to="`/campaigns/${campaign.id}`"
                  class="btn btn-sm btn-primary"
                >
                  View Details
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- List View -->
        <div v-else class="campaigns-list">
          <div
            v-for="campaign in paginatedCampaigns"
            :key="campaign.id"
            class="campaign-list-item"
          >
            <div class="campaign-list-image">
              <img
                :src="campaign.cover_image"
                :alt="campaign.title"
                @error="handleImageError"
              />
              <div v-if="campaign.is_featured" class="featured-badge">
                Featured
              </div>
            </div>
            <div class="campaign-list-content">
              <div class="campaign-list-header">
                <div class="campaign-category">
                  {{ campaign.category.name }}
                </div>
                <div class="campaign-deadline">
                  {{ formatDeadline(campaign.deadline) }}
                </div>
              </div>
              <h3 class="campaign-list-title">{{ campaign.title }}</h3>
              <p class="campaign-list-description">
                {{ truncateText(campaign.description, 200) }}
              </p>

              <div class="campaign-list-meta">
                <div class="campaign-location">
                  <i class="fas fa-map-marker-alt"></i>
                  {{ campaign.location }}
                </div>
                <div class="campaign-creator">
                  <i class="fas fa-user"></i>
                  {{ campaign.created_by.full_name }}
                </div>
                <div v-if="campaign.is_business" class="business-indicator">
                  <i class="fas fa-briefcase"></i>
                  Business Campaign
                </div>
              </div>

              <div class="campaign-list-progress">
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: calculateProgress(campaign) + '%' }"
                  ></div>
                </div>
                <div class="progress-stats">
                  <span class="funding-goal"
                    >${{ formatNumber(campaign.funding_goals) }} Goal</span
                  >
                  <span class="funding-progress"
                    >{{ calculateProgress(campaign) }}%</span
                  >
                </div>
              </div>

              <div class="campaign-list-footer">
                <router-link
                  :to="`/campaigns/${campaign.id}`"
                  class="btn btn-sm btn-primary"
                >
                  View Campaign
                </router-link>
                <button class="btn btn-sm btn-outline">Share</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div
          v-if="!loading && !error && filteredCampaigns.length > 0"
          class="pagination"
        >
          <button
            @click="prevPage"
            class="pagination-btn"
            :disabled="currentPage === 1"
            aria-label="Previous page"
          >
            <i class="fas fa-chevron-left"></i>
          </button>

          <div class="pagination-info">
            Page {{ currentPage }} of {{ totalPages }}
          </div>

          <button
            @click="nextPage"
            class="pagination-btn"
            :disabled="currentPage === totalPages"
            aria-label="Next page"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>
  
  <script>
import { ref, computed, onMounted, watch } from "vue";
import apiClient from "@/axios";

export default {
  name: "CampaignsListPage",
  setup() {
    // State variables
    const campaigns = ref([]);
    const categories = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const viewMode = ref("grid");
    const searchQuery = ref("");
    const selectedCategory = ref("");
    const selectedStatus = ref("");
    const sortBy = ref("newest");
    const currentPage = ref(1);
    const itemsPerPage = ref(9);
    const searchTimeout = ref(null);

    // Fetch campaigns from API
    const fetchCampaigns = async () => {
      loading.value = true;
      error.value = null;

      try {
        const response = await apiClient.get("/campaigns/campaigns");
        campaigns.value = response.data;

        // Extract unique categories
        const uniqueCategories = new Map();
        campaigns.value.forEach((campaign) => {
          if (
            campaign.category &&
            !uniqueCategories.has(campaign.category.id)
          ) {
            uniqueCategories.set(campaign.category.id, campaign.category);
          }
        });
        categories.value = Array.from(uniqueCategories.values());
      } catch (err) {
        console.error("Error fetching campaigns:", err);
        error.value = "Failed to load campaigns. Please try again later.";
      } finally {
        loading.value = false;
      }
    };

    // Filter campaigns based on search and filters
    const filteredCampaigns = computed(() => {
      let result = [...campaigns.value];

      // Apply search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        result = result.filter(
          (campaign) =>
            campaign.title.toLowerCase().includes(query) ||
            campaign.description.toLowerCase().includes(query) ||
            campaign.location.toLowerCase().includes(query)
        );
      }

      // Apply category filter
      if (selectedCategory.value) {
        result = result.filter(
          (campaign) =>
            campaign.category &&
            campaign.category.id.toString() ===
              selectedCategory.value.toString()
        );
      }

      // Apply status filter
      if (selectedStatus.value) {
        switch (selectedStatus.value) {
          case "active":
            result = result.filter(
              (campaign) => campaign.is_active && !campaign.is_completed
            );
            break;
          case "completed":
            result = result.filter((campaign) => campaign.is_completed);
            break;
          case "featured":
            result = result.filter((campaign) => campaign.is_featured);
            break;
        }
      }

      // Apply sorting
      switch (sortBy.value) {
        case "newest":
          result.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
          );
          break;
        case "oldest":
          result.sort(
            (a, b) => new Date(a.created_at) - new Date(b.created_at)
          );
          break;
        case "goal-high":
          result.sort(
            (a, b) => parseFloat(b.funding_goals) - parseFloat(a.funding_goals)
          );
          break;
        case "goal-low":
          result.sort(
            (a, b) => parseFloat(a.funding_goals) - parseFloat(b.funding_goals)
          );
          break;
        case "deadline":
          result.sort((a, b) => new Date(a.deadline) - new Date(b.deadline));
          break;
      }

      return result;
    });

    // Pagination
    const totalPages = computed(() => {
      return Math.ceil(filteredCampaigns.value.length / itemsPerPage.value);
    });

    const paginatedCampaigns = computed(() => {
      const startIndex = (currentPage.value - 1) * itemsPerPage.value;
      const endIndex = startIndex + itemsPerPage.value;
      return filteredCampaigns.value.slice(startIndex, endIndex);
    });

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++;
        scrollToTop();
      }
    };

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--;
        scrollToTop();
      }
    };

    const scrollToTop = () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    };

    // Check if there are active filters
    const hasActiveFilters = computed(() => {
      return (
        selectedCategory.value || selectedStatus.value || searchQuery.value
      );
    });

    // Format deadline date
    const formatDeadline = (dateString) => {
      const deadline = new Date(dateString);
      const now = new Date();
      const diffTime = deadline - now;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays < 0) {
        return "Ended";
      } else if (diffDays === 0) {
        return "Ends today";
      } else if (diffDays === 1) {
        return "1 day left";
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
      return parseFloat(num).toLocaleString("en-US");
    };

    // Truncate text with ellipsis
    const truncateText = (text, maxLength) => {
      if (text.length <= maxLength) return text;
      return text.substring(0, maxLength) + "...";
    };

    // Handle image loading errors
    const handleImageError = (event) => {
      event.target.src = "/placeholder.jpg"; // Fallback image
    };

    // Get category name by ID
    const getCategoryName = (categoryId) => {
      const category = categories.value.find(
        (cat) => cat.id.toString() === categoryId.toString()
      );
      return category ? category.name : "Unknown Category";
    };

    // Format status for display
    const formatStatus = (status) => {
      return status.charAt(0).toUpperCase() + status.slice(1);
    };

    // Handle search with debounce
    const handleSearch = () => {
      clearTimeout(searchTimeout.value);
      searchTimeout.value = setTimeout(() => {
        applyFilters();
      }, 300);
    };

    // Clear search
    const clearSearch = () => {
      searchQuery.value = "";
      applyFilters();
    };

    // Apply filters
    const applyFilters = () => {
      currentPage.value = 1; // Reset to first page when filters change
    };

    // Remove a specific filter
    const removeFilter = (filterType) => {
      switch (filterType) {
        case "category":
          selectedCategory.value = "";
          break;
        case "status":
          selectedStatus.value = "";
          break;
        case "search":
          searchQuery.value = "";
          break;
      }
      applyFilters();
    };

    // Reset all filters
    const resetFilters = () => {
      selectedCategory.value = "";
      selectedStatus.value = "";
      searchQuery.value = "";
      sortBy.value = "newest";
      applyFilters();
    };

    // Watch for changes in filtered campaigns to update pagination
    watch(filteredCampaigns, () => {
      if (currentPage.value > totalPages.value && totalPages.value > 0) {
        currentPage.value = totalPages.value;
      }
    });

    // Fetch campaigns when component mounts
    onMounted(() => {
      fetchCampaigns();
    });

    return {
      campaigns,
      categories,
      loading,
      error,
      viewMode,
      searchQuery,
      selectedCategory,
      selectedStatus,
      sortBy,
      currentPage,
      filteredCampaigns,
      paginatedCampaigns,
      totalPages,
      hasActiveFilters,
      fetchCampaigns,
      formatDeadline,
      calculateProgress,
      formatNumber,
      truncateText,
      handleImageError,
      getCategoryName,
      formatStatus,
      handleSearch,
      clearSearch,
      applyFilters,
      removeFilter,
      resetFilters,
      nextPage,
      prevPage,
    };
  },
};
</script>
  
  <style>
/* Campaigns List Page Styles */
.campaigns-list-page {
  min-height: 100vh;
}

/* Page Header */
.page-header {
  background-color: var(--primary);
  color: var(--text-on-primary);
  padding: var(--spacing-xl) 0;
}

.page-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
}

.page-description {
  max-width: 600px;
  opacity: 0.9;
}

/* Filters Section */
.filters-section {
  background-color: var(--surface);
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 10;
}

.filters-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.search-container {
  flex: 1;
  min-width: 250px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: var(--spacing-sm);
  color: var(--text-secondary);
}

.search-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-sm) var(--spacing-sm)
    var(--spacing-xl);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-md);
}

.search-clear-btn {
  position: absolute;
  right: var(--spacing-sm);
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
}

.filter-controls {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.filter-dropdown {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.filter-dropdown label {
  font-size: var(--font-size-sm);
  margin-bottom: 4px;
  color: var(--text-secondary);
}

.view-toggle {
  display: flex;
  gap: var(--spacing-xs);
}

.view-toggle-btn {
  background: none;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-sm);
  cursor: pointer;
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.view-toggle-btn.active {
  background-color: var(--primary);
  color: var(--text-on-primary);
  border-color: var(--primary);
}

.active-filters {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.active-filters-label {
  font-weight: 600;
  color: var(--text-secondary);
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.filter-tag {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  background-color: var(--background);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-full);
  padding: 4px var(--spacing-sm);
  font-size: var(--font-size-sm);
}

.filter-tag-remove {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Campaigns Section */
.campaigns-section {
  padding: var(--spacing-xl) 0;
}

/* Grid View */
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
  height: 100%;
  display: flex;
  flex-direction: column;
}

.campaign-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.campaign-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.campaign-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.campaign-card:hover .campaign-image img {
  transform: scale(1.05);
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
  z-index: 1;
}

.business-badge {
  position: absolute;
  top: var(--spacing-sm);
  left: var(--spacing-sm);
  background-color: var(--secondary);
  color: white;
  padding: 4px 8px;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 600;
  z-index: 1;
}

.campaign-content {
  padding: var(--spacing-md);
  display: flex;
  flex-direction: column;
  flex-grow: 1;
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
  margin-bottom: var(--spacing-sm);
  line-height: 1.3;
}

.campaign-description {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.5;
  flex-grow: 1;
}

.campaign-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.campaign-location,
.campaign-deadline {
  display: flex;
  align-items: center;
  gap: 4px;
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

.campaign-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--border-color);
}

.campaign-creator {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* List View */
.campaigns-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.campaign-list-item {
  display: flex;
  background-color: var(--background);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.campaign-list-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.campaign-list-image {
  flex: 0 0 200px;
  height: 200px;
  position: relative;
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
  margin-bottom: var(--spacing-sm);
}

.campaign-list-title {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-sm);
}

.campaign-list-description {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
  flex-grow: 1;
}

.campaign-list-meta {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  flex-wrap: wrap;
}

.campaign-list-meta > div {
  display: flex;
  align-items: center;
  gap: 4px;
}

.business-indicator {
  color: var(--secondary);
  font-weight: 500;
}

.campaign-list-progress {
  margin-bottom: var(--spacing-md);
}

.campaign-list-footer {
  display: flex;
  gap: var(--spacing-md);
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: var(--spacing-xl);
  gap: var(--spacing-md);
}

.pagination-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-md);
  border: 1px solid var(--border-color);
  background-color: var(--background);
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background-color: var(--primary);
  color: var(--text-on-primary);
  border-color: var(--primary);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* Loading, Error, Empty States */
.loading-container,
.error-container,
.empty-container {
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
  font-size: 2rem;
  margin-bottom: var(--spacing-md);
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
  font-weight: 700;
}

/* Responsive Styles */
@media (max-width: 992px) {
  .page-header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-controls {
    order: 2;
  }

  .view-toggle {
    order: 3;
    align-self: flex-end;
  }
}

@media (max-width: 768px) {
  .campaign-list-item {
    flex-direction: column;
  }

  .campaign-list-image {
    flex: 0 0 auto;
    height: 200px;
    width: 100%;
  }

  .filter-controls {
    flex-direction: column;
  }
}

@media (max-width: 576px) {
  .active-filters {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .filter-tags {
    width: 100%;
  }
}
</style>