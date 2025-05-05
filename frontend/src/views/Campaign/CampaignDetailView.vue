<template>
  <div class="campaign-detail-page">
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
      <button @click="fetchCampaignDetails" class="btn btn-primary">
        Try Again
      </button>
      <router-link to="/campaigns" class="btn btn-outline mt-2">Back to Campaigns</router-link>
    </div>

    <!-- Campaign Details -->
    <div v-else-if="campaign" class="campaign-content">
      <!-- Campaign Header -->
      <section class="campaign-header">
        <div class="container">
          <div class="breadcrumbs">
            <router-link to="/">Home</router-link> &gt;
            <router-link to="/campaigns">Campaigns</router-link> &gt;
            <span>{{ campaign.title }}</span>
          </div>

          <div class="campaign-header-content">
            <div class="campaign-header-info">
              <div class="campaign-badges">
                <span class="campaign-category">{{
                  campaign.category.name
                  }}</span>
                <span v-if="campaign.is_featured" class="featured-badge">Featured</span>
                <span v-if="campaign.is_business" class="business-badge">Business</span>
              </div>
              <h1 class="campaign-title">{{ campaign.title }}</h1>
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
            </div>
          </div>
        </div>
      </section>

      <!-- Campaign Main Content -->
      <section class="campaign-main">
        <div class="container">
          <div class="campaign-grid">
            <!-- Left Column: Campaign Image and Description -->
            <div class="campaign-left-column">
              <div class="campaign-image-container">
                <img :src="campaign.cover_image" :alt="campaign.title" @error="handleImageError"
                  class="campaign-image" />
              </div>

              <div class="campaign-tabs">
                <button class="tab-button" :class="{ active: activeTab === 'about' }" @click="activeTab = 'about'">
                  About
                </button>
              </div>

              <div class="campaign-tab-content">
                <!-- About Tab -->
                <div v-if="activeTab === 'about'" class="tab-panel">
                  <div class="campaign-description">
                    <h2>About this Campaign</h2>
                    <p>{{ campaign.description }}</p>

                    <!-- For demo purposes, adding more content -->
                    <h3>Our Mission</h3>
                    <p>
                      This campaign aims to address critical social and
                      environmental challenges in our community. Through
                      collective action and targeted initiatives, we can create
                      meaningful change and build a more sustainable future.
                    </p>

                    <h3>How Your Support Helps</h3>
                    <p>
                      Your contribution directly supports our efforts to
                      implement sustainable solutions, engage community members,
                      and drive positive outcomes. Every donation, regardless of
                      size, makes a difference in our ability to achieve our
                      goals.
                    </p>
                  </div>
                </div>

                <!-- Updates Tab -->


                <!-- Comments Tab -->

              </div>
            </div>

            <!-- Right Column: Campaign Stats and Actions -->
            <div class="campaign-right-column">
              <div class="campaign-stats card">
                <div class="funding-stats">
                  <div class="funding-amount">

                    <span class="goal-amount">raised of ${{
                      formatNumber(campaign.funding_goals)
                    }}
                      goal</span>
                  </div>
                </div>

                <div class="campaign-stats-grid">
                  <div class="stat-item">
                    <div class="stat-value">
                      {{ getDaysLeft(campaign.deadline) }}
                    </div>
                    <div class="stat-label">Days Left</div>
                  </div>

                  <div class="stat-item">
                    <div class="stat-value">
                      {{ formatDate(campaign.created_at, true) }}
                    </div>
                    <div class="stat-label">Started</div>
                  </div>
                </div>

                <div class="campaign-actions">
                  <button class="btn btn-primary btn-lg btn-block">
                    Donate Now
                  </button>
                  <div class="share-buttons">
                    <button class="btn btn-outline btn-sm" @click="shareCampaign('facebook')">
                      <i class="fab fa-facebook-f"></i> Share
                    </button>
                    <button class="btn btn-outline btn-sm" @click="shareCampaign('twitter')">
                      <i class="fab fa-twitter"></i> Tweet
                    </button>
                    <button class="btn btn-outline btn-sm" @click="shareCampaign('email')">
                      <i class="fas fa-envelope"></i> Email
                    </button>
                  </div>
                </div>
              </div>

              <div class="campaign-creator-card card">
                <h3>Campaign Organizer</h3>
                <div class="creator-info">
                  <div class="creator-avatar">
                    <div class="avatar-placeholder">
                      {{ campaign.created_by.full_name.charAt(0) }}
                    </div>
                  </div>
                  <div class="creator-details">
                    <div class="creator-name">
                      {{ campaign.created_by.full_name }}
                    </div>
                    <div class="creator-role">
                      {{ campaign.created_by.role }}
                    </div>
                  </div>
                </div>
                <button class="btn btn-outline btn-block mt-3">
                  <a :href="'mailto:' + campaign.created_by.email">
                    Contact Organizer
                  </a>
                </button>
              </div>

              <div class="campaign-report card">
                <p>See something wrong with this campaign?</p>
                <button class="btn btn-sm btn-outline" @click="reportCampaign">
                  Report Campaign
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Related Campaigns -->
      <section class="related-campaigns">
        <div class="container">
          <h2>Similar Campaigns</h2>
          <div class="campaign-grid">
            <div v-for="relatedCampaign in relatedCampaigns" :key="relatedCampaign.id" class="campaign-card">
              <div class="campaign-image">
                <img :src="relatedCampaign.cover_image" :alt="relatedCampaign.title" @error="handleImageError" />
              </div>
              <div class="campaign-content">
                <div class="campaign-category">
                  {{ relatedCampaign.category.name }}
                </div>
                <h3 class="campaign-title">{{ relatedCampaign.title }}</h3>
                <p class="campaign-description">
                  {{ truncateText(relatedCampaign.description, 100) }}
                </p>

                <div class="campaign-progress">
                  <div class="progress-bar">
                  </div>
                  <div class="progress-stats">
                    <span class="funding-goal">${{
                      formatNumber(relatedCampaign.funding_goals)
                    }}
                      Goal</span>

                  </div>
                </div>

                <div class="campaign-footer">
                  <router-link :to="`/campaigns/${relatedCampaign.id}`" class="btn btn-sm btn-primary">
                    View Details
                  </router-link>
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
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import apiClient from "@/axios";

export default {
  name: "CampaignDetailPage",
  setup() {
    const route = useRoute();
    const campaign = ref(null);
    const loading = ref(true);
    const error = ref(null);
    const activeTab = ref("about");
    const newComment = ref("");

    // Mock data for demo purposes
    const updates = ref([
      {
        title: "Campaign Launch Success!",
        date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
        content:
          "We're thrilled to announce the successful launch of our campaign! Thank you to everyone who has supported us so far. We've already reached 15% of our funding goal in just the first week.",
      },
      {
        title: "New Partnership Announcement",
        date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
        content:
          "We're excited to share that we've partnered with Local Green Initiative to expand our impact. This collaboration will help us reach more communities and implement sustainable solutions more effectively.",
      },
    ]);

    const comments = ref([
      {
        author: "Jane Smith",
        date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), // 5 days ago
        content:
          "This is such an important initiative! I've shared it with my network and hope more people will support it.",
      },
      {
        author: "Michael Johnson",
        date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
        content:
          "I've been following this issue for years and am glad to see someone taking action. Count me in as a supporter!",
      },
    ]);

    const relatedCampaigns = ref([]);

    // Fetch campaign details
    const fetchCampaignDetails = async () => {
      const campaignId = route.params.id;
      loading.value = true;
      error.value = null;

      try {
        // In a real app, you would fetch the specific campaign
        // const response = await apiClient.get(`/campaigns/campaigns/${campaignId}`);
        // campaign.value = response.data;

        // For demo purposes, we'll simulate an API call with a timeout
        setTimeout(async () => {
          try {
            const response = await apiClient.get("/campaigns/campaigns");
            const campaigns = response.data;

            // Find the campaign with the matching ID
            campaign.value = campaigns.find(
              (c) => c.id.toString() === campaignId.toString()
            );

            if (!campaign.value) {
              error.value = "Campaign not found";
            } else {
              // Get related campaigns (same category)
              relatedCampaigns.value = campaigns
                .filter(
                  (c) =>
                    c.id !== campaign.value.id &&
                    c.category.id === campaign.value.category.id
                )
                .slice(0, 3);

              // If not enough related campaigns, add some others
              if (relatedCampaigns.value.length < 3) {
                const otherCampaigns = campaigns
                  .filter(
                    (c) =>
                      c.id !== campaign.value.id &&
                      c.category.id !== campaign.value.category.id
                  )
                  .slice(0, 3 - relatedCampaigns.value.length);

                relatedCampaigns.value = [
                  ...relatedCampaigns.value,
                  ...otherCampaigns,
                ];
              }
            }
          } catch (err) {
            console.error("Error fetching campaigns:", err);
            error.value =
              "Failed to load campaign details. Please try again later.";
          } finally {
            loading.value = false;
          }
        }, 800); // Simulate network delay
      } catch (err) {
        console.error("Error fetching campaign details:", err);
        error.value =
          "Failed to load campaign details. Please try again later.";
        loading.value = false;
      }
    };

    // Format date
    const formatDate = (dateString, shortFormat = false) => {
      const date = new Date(dateString);

      if (shortFormat) {
        return date.toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
        });
      }

      return date.toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    };

    // Format deadline date
    const formatDeadline = (dateString) => {
      const deadline = new Date(dateString);
      const now = new Date();
      const diffTime = deadline - now;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays < 0) {
        return "Campaign ended";
      } else if (diffDays === 0) {
        return "Ends today";
      } else if (diffDays === 1) {
        return "1 day left";
      } else {
        return `${diffDays} days left`;
      }
    };

    // Get days left
    const getDaysLeft = (dateString) => {
      const deadline = new Date(dateString);
      const now = new Date();
      const diffTime = deadline - now;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      return diffDays > 0 ? diffDays : 0;
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

    // Add a comment
    const addComment = () => {
      if (newComment.value.trim()) {
        comments.value.unshift({
          author: "You", // In a real app, this would be the logged-in user
          date: new Date(),
          content: newComment.value.trim(),
        });
        newComment.value = "";
      }
    };

    // Share campaign
    const shareCampaign = (platform) => {
      const url = window.location.href;
      const title = campaign.value
        ? campaign.value.title
        : "Check out this campaign";

      switch (platform) {
        case "facebook":
          window.open(
            `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
              url
            )}`,
            "_blank"
          );
          break;
        case "twitter":
          window.open(
            `https://twitter.com/intent/tweet?text=${encodeURIComponent(
              title
            )}&url=${encodeURIComponent(url)}`,
            "_blank"
          );
          break;
        case "email":
          window.open(
            `mailto:?subject=${encodeURIComponent(
              title
            )}&body=${encodeURIComponent(`Check out this campaign: ${url}`)}`,
            "_blank"
          );
          break;
      }
    };

    // Report campaign
    const reportCampaign = () => {
      alert(
        "Thank you for your concern. This campaign has been reported to our team for review."
      );
    };

    // Fetch campaign when component mounts
    onMounted(() => {
      fetchCampaignDetails();
    });

    return {
      campaign,
      loading,
      error,
      activeTab,
      updates,
      comments,
      newComment,
      relatedCampaigns,
      fetchCampaignDetails,
      formatDate,
      formatDeadline,
      getDaysLeft,
      formatNumber,
      truncateText,
      handleImageError,
      addComment,
      shareCampaign,
      reportCampaign,
    };
  },
};
</script>

<style scoped>
/* Campaign Detail Page Styles */
.campaign-detail-page {
  min-height: 100vh;
}

/* Campaign Header */
.campaign-header {
  background-color: var(--surface);
  padding: var(--spacing-lg) 0;
  border-bottom: 1px solid var(--border-color);
}

.breadcrumbs {
  font-size: var(--font-size-sm);
  margin-bottom: var(--spacing-md);
  color: var(--text-secondary);
}

.breadcrumbs a {
  color: var(--text-secondary);
  text-decoration: none;
}

.breadcrumbs a:hover {
  color: var(--primary);
  text-decoration: underline;
}

.campaign-header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.campaign-badges {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.campaign-category {
  display: inline-block;
  background-color: var(--primary-light);
  color: var(--text-on-primary);
  padding: 2px 8px;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
}

.featured-badge {
  display: inline-block;
  background-color: var(--accent);
  color: white;
  padding: 2px 8px;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
}

.business-badge {
  display: inline-block;
  background-color: var(--secondary);
  color: white;
  padding: 2px 8px;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-xs);
}

.campaign-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  line-height: 1.2;
}

.campaign-meta {
  display: flex;
  gap: var(--spacing-md);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.campaign-location,
.campaign-deadline {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Campaign Main Content */
.campaign-main {
  padding: var(--spacing-xl) 0;
}

.campaign-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-xl);
}

/* Left Column */
.campaign-left-column {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.campaign-image-container {
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
}

.campaign-image {
  width: 100%;
  height: auto;
  display: block;
}

.campaign-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
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

.campaign-tab-content {
  padding: var(--spacing-md) 0;
}

.tab-panel h2 {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-md);
}

.tab-panel h3 {
  font-size: 1.25rem;
  margin: var(--spacing-lg) 0 var(--spacing-sm);
}

.campaign-description p {
  margin-bottom: var(--spacing-md);
  line-height: 1.6;
}

.timeline {
  list-style: none;
  padding: 0;
  margin: var(--spacing-md) 0;
  position: relative;
}

.timeline::before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 15px;
  width: 2px;
  background-color: var(--border-color);
}

.timeline li {
  position: relative;
  padding-left: 40px;
  margin-bottom: var(--spacing-md);
}

.timeline li::before {
  content: "";
  position: absolute;
  left: 8px;
  top: 5px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: var(--primary);
}

.timeline-date {
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

/* Updates Tab */
.update-item {
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-color);
}

.update-item:last-child {
  border-bottom: none;
}

.update-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.update-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.update-date {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* Comments Tab */
.comment-form {
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-md);
  background-color: var(--surface);
  border-radius: var(--border-radius-md);
}

.comment-form h3 {
  margin-bottom: var(--spacing-sm);
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.comment-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background-color: var(--surface);
  border-radius: var(--border-radius-md);
}

.comment-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.comment-content {
  flex-grow: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-xs);
}

.comment-author {
  font-weight: 600;
}

.comment-date {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.empty-updates,
.empty-comments {
  padding: var(--spacing-lg);
  text-align: center;
  color: var(--text-secondary);
  background-color: var(--surface);
  border-radius: var(--border-radius-md);
}

/* Right Column */
.campaign-right-column {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.card {
  background-color: var(--background);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-lg);
}

.funding-stats {
  margin-bottom: var(--spacing-lg);
}

.funding-amount {
  margin-bottom: var(--spacing-sm);
}

.current-amount {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary);
}

.goal-amount {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-left: var(--spacing-xs);
}

.funding-progress {
  display: flex;
  justify-content: flex-end;
  font-size: var(--font-size-sm);
  margin-top: 4px;
}

.campaign-stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.stat-item {
  padding: 10px;
}

.stat-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.campaign-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.btn-block {
  width: 100%;
}

.btn-lg {
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-md);
}

.share-buttons {
  display: flex;
  justify-content: space-between;
}

.creator-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin: var(--spacing-md) 0;
}

.creator-details {
  display: flex;
  flex-direction: column;
}

.creator-name {
  font-weight: 600;
}

.creator-role {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.campaign-report {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

/* Related Campaigns */
.related-campaigns {
  background-color: var(--surface);
  padding: var(--spacing-xl) 0;
  margin-top: var(--spacing-xl);
}

.related-campaigns h2 {
  margin-bottom: var(--spacing-lg);
}

.related-campaigns .campaign-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.related-campaigns .campaign-card {
  background-color: var(--background);
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
  min-height: 50vh;
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
  .campaign-grid {
    grid-template-columns: 1fr;
  }

  .campaign-right-column {
    order: -1;
  }

  .campaign-stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .campaign-title {
    font-size: 1.75rem;
  }

  .campaign-meta {
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .tab-button {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-sm);
  }

  .share-buttons {
    flex-wrap: wrap;
    gap: var(--spacing-sm);
  }

  .share-buttons .btn {
    flex: 1;
    min-width: 80px;
  }
}

@media (max-width: 576px) {
  .campaign-stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .comment-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .comment-avatar {
    margin-bottom: var(--spacing-sm);
  }
}
</style>