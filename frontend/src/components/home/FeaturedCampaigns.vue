<template>
  <section class="featured-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">Featured Campaigns</h2>
        <p class="section-description">
          Join these impactful campaigns and help make a difference.
        </p>
      </div>
      <div class="campaigns-grid">
        <div
          v-for="campaign in campaigns"
          :key="campaign.id"
          class="campaign-card"
        >
          <div class="campaign-image-container">
            <img
              :src="campaign.image"
              :alt="campaign.title"
              class="campaign-image"
            />
            <span class="campaign-badge">{{ campaign.category }}</span>
          </div>
          <div class="campaign-header">
            <h3 class="campaign-title">{{ campaign.title }}</h3>
          </div>
          <div class="campaign-content">
            <p class="campaign-description">{{ campaign.description }}</p>
            <div class="campaign-progress-container">
              <div class="campaign-progress-info">
                <span>${{ campaign.raised }}</span>
                <span class="campaign-goal">of ${{ campaign.goal }}</span>
              </div>
              <div class="progress-bar">
                <div
                  class="progress-bar-fill"
                  :style="{ width: campaign.progress + '%' }"
                ></div>
              </div>
              <p class="campaign-supporters">
                {{ campaign.supporters }} supporters
              </p>
            </div>
          </div>
          <div class="campaign-footer">
            <router-link
              :to="`/campaigns/${campaign.id}`"
              class="campaign-link"
            >
              <button class="btn btn-primary btn-block">
                Support This Cause
              </button>
            </router-link>
          </div>
        </div>
      </div>
      <div class="view-all-container">
        <router-link to="/campaigns">
          <button class="btn btn-outline">View All Campaigns</button>
        </router-link>
      </div>
    </div>
  </section>
</template>
  
  <script>
export default {
  name: "FeaturedCampaigns",
  data() {
    return {
      campaigns: [
        {
          id: 1,
          title: "Clean Water Initiative",
          description:
            "Providing clean water to communities in need around the world.",
          category: "Environment",
          image: "https://placehold.co/400x200",
          progress: 75,
          supporters: 1243,
          goal: "50,000",
          raised: "37,500",
        },
        {
          id: 2,
          title: "Education for All",
          description:
            "Supporting education programs for underprivileged children.",
          category: "Education",
          image: "https://placehold.co/400x200",
          progress: 45,
          supporters: 876,
          goal: "25,000",
          raised: "11,250",
        },
        {
          id: 3,
          title: "Mental Health Awareness",
          description:
            "Raising awareness about mental health issues and providing support.",
          category: "Health",
          image: "https://placehold.co/400x200",
          progress: 90,
          supporters: 2156,
          goal: "30,000",
          raised: "27,000",
        },
      ],
    };
  },
};
</script>
  
  <style scoped>
.featured-section {
  padding: 3rem 0;
  background-color: var(--color-background-alt);
}

.section-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.025em;
  margin-bottom: 0.5rem;
}

.section-description {
  max-width: 900px;
  color: var(--color-text-muted);
}

.campaigns-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.campaign-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  background-color: var(--color-background);
}

.campaign-image-container {
  position: relative;
  aspect-ratio: 16 / 9;
}

.campaign-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.campaign-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 0.25rem 0.625rem;
  border-radius: 9999px;
  background-color: var(--color-background);
  font-size: 0.75rem;
  font-weight: 500;
}

.campaign-header {
  padding: 1rem;
}

.campaign-title {
  font-size: 1.25rem;
  font-weight: 700;
}

.campaign-content {
  padding: 0 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.campaign-description {
  font-size: 0.875rem;
  color: var(--color-text-muted);
}

.campaign-progress-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.campaign-progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}

.campaign-goal {
  color: var(--color-text-muted);
}

.progress-bar {
  width: 100%;
  height: 0.5rem;
  background-color: var(--color-background-muted);
  border-radius: 9999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: var(--color-primary);
  border-radius: 9999px;
}

.campaign-supporters {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.campaign-footer {
  padding: 1rem;
}

.campaign-link {
  display: block;
  width: 100%;
}

.view-all-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

@media (min-width: 768px) {
  .featured-section {
    padding: 6rem 0;
  }

  .campaigns-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .section-title {
    font-size: 2.25rem;
  }
}
</style>
  