<template>
  <section class="business-section">
    <div class="container">
      <div class="business-content">
        <div class="business-text">
          <h2 class="business-title">Small Businesses Making a Difference</h2>
          <p class="business-description">
            Discover and support small businesses that are committed to social
            causes and making a positive impact in their communities.
          </p>
          <div class="business-actions">
            <router-link to="/businesses/register">
              <button class="btn btn-primary">Register Your Business</button>
            </router-link>
            <router-link to="/businesses">
              <button class="btn btn-outline">Explore All Businesses</button>
            </router-link>
          </div>
        </div>
        <div class="business-grid">
          <router-link
            v-for="business in businesses"
            :key="business.id"
            :to="`/businesses/${business.id}`"
            class="business-card"
          >
            <div class="business-card-content">
              <div class="business-image-container">
                <img
                  :src="business.image"
                  :alt="business.name"
                  class="business-image"
                />
              </div>
              <div class="business-info">
                <div class="business-header">
                  <h3 class="business-name">{{ business.name }}</h3>
                </div>
                <span class="business-category">{{ business.category }}</span>
                <p class="business-card-description">
                  {{ business.description }}
                </p>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>
  
  <script>
export default {
  name: "BusinessSection",
  data() {
    return {
      businesses: [
        {
          id: 1,
          name: "Green Earth Cafe",
          category: "Food & Beverage",
          description:
            "Sustainable coffee shop supporting environmental causes",
          image: "https://placehold.co/100x100",
        },
        {
          id: 2,
          name: "Community Bookstore",
          category: "Retail",
          description: "Local bookstore supporting literacy programs",
          image: "https://placehold.co/100x100",
        },
        {
          id: 3,
          name: "Healthy Bites",
          category: "Restaurant",
          description: "Organic restaurant supporting local farmers",
          image: "https://placehold.co/100x100",
        },
        {
          id: 4,
          name: "Eco Consulting",
          category: "Services",
          description: "Business consulting with a focus on sustainability",
          image: "https://placehold.co/100x100",
        },
      ],
    };
  },
};
</script>
  
  <style scoped>
.business-section {
  padding: 3rem 0;
}

.business-content {
  display: grid;
  gap: 2.5rem;
}

.business-text {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.business-title {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.025em;
}

.business-description {
  max-width: 600px;
  color: var(--color-text-muted);
}

.business-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.business-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.business-card {
  height: 100%;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  text-decoration: none;
  color: var(--color-text);
}

.business-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.business-card-content {
  padding: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.business-image-container {
  width: 3rem;
  height: 3rem;
  border-radius: 9999px;
  overflow: hidden;
  flex-shrink: 0;
}

.business-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.business-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.business-name {
  font-weight: 500;
}

.business-category {
  display: inline-flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: 9999px;
  padding: 0.125rem 0.625rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.business-card-description {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (min-width: 400px) {
  .business-actions {
    flex-direction: row;
  }
}

@media (min-width: 640px) {
  .business-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) {
  .business-section {
    padding: 6rem 0;
  }

  .business-content {
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
  }

  .business-title {
    font-size: 2.25rem;
  }

  .business-description {
    font-size: 1.125rem;
  }
}
</style>
  