<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- Left: App Name -->
      <div class="navbar-brand">
        <router-link to="/" class="navbar-logo">
          <span>EcoImpact</span>
        </router-link>
      </div>

      <!-- Mobile Menu Toggle -->
      <button
        class="navbar-toggle"
        @click="isMenuOpen = !isMenuOpen"
        aria-label="Toggle navigation menu"
      >
        <span class="navbar-toggle-icon" :class="{ open: isMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </button>

      <!-- Center: Navigation Links -->
      <div class="navbar-menu" :class="{ active: isMenuOpen }">
        <div class="navbar-links">
          <router-link to="/campaigns" class="navbar-link"
            >Campaigns</router-link
          >
          <router-link to="/businesses" class="navbar-link"
            >Businesses</router-link
          >
          <router-link to="/about" class="navbar-link">About Us</router-link>
          <router-link to="/contact" class="navbar-link">Contact</router-link>
        </div>

        <!-- Right: Authentication Buttons -->
        <div class="navbar-auth">
          <router-link to="/login" class="btn btn-outline navbar-btn"
            >Log In</router-link
          >
          <router-link to="/signup" class="btn btn-primary navbar-btn"
            >Sign Up</router-link
          >
        </div>
      </div>
    </div>
  </nav>
</template>
  
  <script>
export default {
  name: "Navbar",
  data() {
    return {
      isMenuOpen: false,
    };
  },
  watch: {
    // Close menu when route changes
    $route() {
      this.isMenuOpen = false;
    },
  },
};
</script>
  
  <script setup>
// If you prefer Composition API:
// import { ref, watch } from 'vue'
// import { useRoute } from 'vue-router'
//
// const route = useRoute()
// const isMenuOpen = ref(false)
//
// watch(() => route.path, () => {
//   isMenuOpen.value = false
// })
</script>
  
  <style>
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  background-color: var(--background);
  box-shadow: var(--shadow-sm);
  height: 70px;
  display: flex;
  align-items: center;
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
  height: 100%;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.navbar-logo {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
}

.navbar-logo:hover {
  text-decoration: none;
}

.navbar-menu {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  margin-left: var(--spacing-xl);
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.navbar-link {
  color: var(--text-primary);
  font-weight: 500;
  text-decoration: none;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  transition: all 0.2s ease;
}

.navbar-link:hover {
  color: var(--primary);
  text-decoration: none;
}

.navbar-link.router-link-active {
  color: var(--primary);
  font-weight: 600;
}

.navbar-auth {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.navbar-btn {
  padding: var(--spacing-xs) var(--spacing-md);
}

.navbar-toggle {
  display: none;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: var(--spacing-xs);
}

.navbar-toggle-icon {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 24px;
  height: 18px;
}

.navbar-toggle-icon span {
  display: block;
  height: 2px;
  width: 100%;
  background-color: var(--text-primary);
  transition: all 0.3s ease;
}

.navbar-toggle-icon.open span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}

.navbar-toggle-icon.open span:nth-child(2) {
  opacity: 0;
}

.navbar-toggle-icon.open span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

/* Responsive Styles */
@media (max-width: 768px) {
  .navbar-toggle {
    display: flex;
    z-index: 1001;
  }

  .navbar-menu {
    position: fixed;
    top: 0;
    right: -100%;
    width: 100%;
    height: 100vh;
    flex-direction: column;
    justify-content: center;
    background-color: var(--background);
    transition: all 0.3s ease;
    margin-left: 0;
    z-index: 1000;
  }

  .navbar-menu.active {
    right: 0;
  }

  .navbar-links {
    flex-direction: column;
    align-items: center;
    margin-bottom: var(--spacing-xl);
  }

  .navbar-link {
    font-size: var(--font-size-lg);
    padding: var(--spacing-md);
  }

  .navbar-auth {
    flex-direction: column;
    width: 80%;
    gap: var(--spacing-md);
  }

  .navbar-btn {
    width: 100%;
    text-align: center;
    padding: var(--spacing-md);
  }
}
</style>