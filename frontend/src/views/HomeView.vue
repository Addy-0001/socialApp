<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-container">
        <h1 class="hero-title">Make a Difference Today</h1>
        <p class="hero-subtitle">
          Join our community of changemakers and support campaigns that matter.
        </p>
        <div class="hero-actions">
          <router-link to="/campaigns/create" class="btn btn-primary"
            >Start a Campaign</router-link
          >
          <router-link to="/campaigns" class="btn btn-outline"
            >Explore All Campaigns</router-link
          >
        </div>
      </div>
    </section>

    <!-- Featured Campaigns Section -->
    <section class="featured-campaigns">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Featured Campaigns</h2>
          <router-link to="/campaigns" class="section-link"
            >View All</router-link
          >
        </div>

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
        <div v-else-if="featuredCampaigns.length === 0" class="empty-container">
          <div class="empty-icon">📋</div>
          <h3>No Featured Campaigns Yet</h3>
          <p>Check back soon or explore all campaigns</p>
          <router-link to="/campaigns" class="btn btn-primary"
            >Browse All Campaigns</router-link
          >
        </div>

        <!-- Campaign Cards -->
        <div v-else class="campaign-grid">
          <div
            v-for="campaign in featuredCampaigns"
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
      </div>
    </section>

    <!-- Recent Campaigns Section -->
    <section class="recent-campaigns">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Recent Campaigns</h2>
          <router-link to="/campaigns" class="section-link"
            >View All</router-link
          >
        </div>

        <!-- Campaign List -->
        <div
          v-if="!loading && !error && campaigns.length > 0"
          class="campaign-list"
        >
          <div
            v-for="campaign in recentCampaigns"
            :key="campaign.id"
            class="campaign-list-item"
          >
            <div class="campaign-list-image">
              <img
                :src="campaign.cover_image"
                :alt="campaign.title"
                @error="handleImageError"
              />
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
                {{ truncateText(campaign.description, 150) }}
              </p>

              <div class="campaign-list-progress">
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: calculateProgress(campaign) + '%' }"
                  ></div>
                </div>
                <div class="progress-stats">
                  <span class="funding-goal"
                    >${{ formatNumber(campaign.funding_goals) }}</span
                  >
                  <span class="funding-progress"
                    >{{ calculateProgress(campaign) }}%</span
                  >
                </div>
              </div>

              <div class="campaign-list-footer">
                <div class="campaign-creator">
                  <span>By {{ campaign.created_by.full_name }}</span>
                </div>
                <router-link
                  :to="`/campaigns/${campaign.id}`"
                  class="btn btn-sm btn-outline"
                >
                  Learn More
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State for Recent Campaigns -->
        <div
          v-else-if="!loading && !error && campaigns.length === 0"
          class="empty-container"
        >
          <p>No recent campaigns available.</p>
        </div>
      </div>
    </section>

    <!-- Call to Action Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>Ready to Make an Impact?</h2>
          <p>
            Start your own campaign or support existing ones to drive positive
            change in your community.
          </p>
          <div class="cta-buttons">
            <router-link to="/campaigns/create" class="btn btn-primary"
              >Start a Campaign</router-link
            >
            <router-link to="/about" class="btn btn-outline"
              >Learn More</router-link
            >
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
  
<script>
import { ref, computed, onMounted } from "vue";
import apiClient from "@/axios";

export default {
  name: "HomePage",
  setup() {
    const campaigns = ref([]);
    const loading = ref(true);
    const error = ref(null);

    // Computed properties for different campaign lists
    const featuredCampaigns = computed(() => {
      return campaigns.value
        .filter((campaign) => campaign.is_featured || campaign.is_active)
        .slice(0, 3);
    });

    const recentCampaigns = computed(() => {
      return [...campaigns.value]
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .slice(0, 4);
    });

    // Fetch campaigns from API
    const fetchCampaigns = async () => {
      loading.value = true;
      error.value = null;

      try {
        const response = await apiClient.get("/campaigns/campaigns");
        campaigns.value = response.data;
      } catch (err) {
        console.error("Error fetching campaigns:", err);
        error.value = "Failed to load campaigns. Please try again later.";
      } finally {
        loading.value = false;
      }
    };

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

    // Calculate funding progress (dummy calculation since we don't have actual funding data)
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

    // Fetch campaigns when component mounts
    onMounted(() => {
      fetchCampaigns();
    });

    return {
      campaigns,
      loading,
      error,
      featuredCampaigns,
      recentCampaigns,
      fetchCampaigns,
      formatDeadline,
      calculateProgress,
      formatNumber,
      truncateText,
      handleImageError,
    };
  },
};
</script>
  
<style scoped>
/* Hero Section */
.hero {
  background-color: var(--primary);
  color: var(--text-on-primary);
  padding: var(--spacing-xxl) 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.2) 0%,
    rgba(0, 0, 0, 0) 100%
  );
  z-index: 1;
}

.hero-container {
  position: relative;
  z-index: 2;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: var(--spacing-md);
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: var(--spacing-xl);
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

.hero-actions .btn {
  padding: var(--spacing-sm) var(--spacing-xl);
}

/* Section Styling */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.section-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

.section-link {
  color: var(--primary);
  font-weight: 500;
  text-decoration: none;
}

.section-link:hover {
  text-decoration: underline;
}

.featured-campaigns,
.recent-campaigns {
  padding: var(--spacing-xxl) 0;
}

.featured-campaigns {
  background-color: var(--background);
}

.recent-campaigns {
  background-color: var(--surface);
}

/* Campaign Grid */
.campaign-grid {
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
  margin-bottom: var(--spacing-sm);
  line-height: 1.3;
}

.campaign-description {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.5;
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

/* Campaign List */
.campaign-list {
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
}

.campaign-list-image {
  flex: 0 0 200px;
  height: 200px;
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

.campaign-list-progress {
  margin-bottom: var(--spacing-md);
}

.campaign-list-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* CTA Section */
.cta-section {
  background-color: var(--primary-dark);
  color: var(--text-on-primary);
  padding: var(--spacing-xxl) 0;
  text-align: center;
}

.cta-content {
  max-width: 700px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.cta-content h2 {
  font-size: 2rem;
  margin-bottom: var(--spacing-md);
}

.cta-content p {
  font-size: 1.1rem;
  margin-bottom: var(--spacing-xl);
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

/* Loading, Error, and Empty States */
.loading-container,
.error-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xxl) 0;
  text-align: center;
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
  color: var(--error);
}

/* Responsive Styles */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .hero-actions .btn {
    width: 100%;
    max-width: 300px;
  }

  .campaign-list-item {
    flex-direction: column;
  }

  .campaign-list-image {
    flex: 0 0 auto;
    height: 200px;
    width: 100%;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .cta-buttons .btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>