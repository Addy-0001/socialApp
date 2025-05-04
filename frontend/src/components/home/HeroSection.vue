<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">Make a difference in the world</h1>
          <p class="hero-description">
            Join our platform to raise awareness about social causes and connect
            with like-minded individuals and businesses.
          </p>
          <div class="hero-actions">
            <router-link to="/campaigns/create">
              <button class="btn btn-primary btn-lg">Start a Campaign</button>
            </router-link>
            <router-link to="/campaigns">
              <button class="btn btn-outline btn-lg">Explore Causes</button>
            </router-link>
          </div>
        </div>
        <div class="hero-image-container">
          <img
            src="https://placehold.co/600x500"
            alt="People working together on social causes"
            class="hero-image"
          />
        </div>
      </div>
    </div>
  </section>
</template>
  
  <script>
export default {
  name: "HeroSection",
};
</script>
  
  <style scoped>
.hero-section {
  width: 100%;
  padding: 3rem 0;
  background-color: var(--color-background-muted);
}

.hero-content {
  display: grid;
  gap: 1.5rem;
}

.hero-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
}

.hero-title {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.025em;
}

.hero-description {
  max-width: 600px;
  color: var(--color-text-muted);
  font-size: 1.125rem;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.hero-image-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 0.5rem;
}

@media (min-width: 400px) {
  .hero-actions {
    flex-direction: row;
  }
}

@media (min-width: 768px) {
  .hero-section {
    padding: 6rem 0;
  }

  .hero-title {
    font-size: 3rem;
  }

  .hero-image {
    height: 400px;
  }
}

@media (min-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr 400px;
    gap: 3rem;
  }

  .hero-section {
    padding: 8rem 0;
  }

  .hero-image {
    height: 500px;
  }
}

@media (min-width: 1280px) {
  .hero-content {
    grid-template-columns: 1fr 600px;
  }

  .hero-title {
    font-size: 3.75rem;
  }
}
</style>
  