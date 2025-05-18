<template>
  <footer class="footer">
    <div class="footer-container">
      <!-- Main Footer Content -->
      <div class="footer-content">
        <!-- Brand Section -->
        <div class="footer-brand">
          <router-link to="/" class="footer-logo">EcoImpact</router-link>
          <p class="footer-tagline">
            Empowering communities to create sustainable change together.
          </p>
          <div class="footer-social">
            <a href="#" aria-label="Facebook" class="social-icon">
              <i class="fab fa-facebook-f"></i>
            </a>
            <a href="#" aria-label="Twitter" class="social-icon">
              <i class="fab fa-twitter"></i>
            </a>
            <a href="#" aria-label="Instagram" class="social-icon">
              <i class="fab fa-instagram"></i>
            </a>
            <a href="#" aria-label="LinkedIn" class="social-icon">
              <i class="fab fa-linkedin-in"></i>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="footer-links">
          <h3 class="footer-heading">Quick Links</h3>
          <ul class="footer-nav">
            <li><router-link to="/campaigns">Campaigns</router-link></li>
            <li><router-link to="/about">About Us</router-link></li>
          </ul>
        </div>
      </div>

      <!-- Contact Info -->
      <div class="footer-contact">
        <div class="contact-item">
          <i class="fas fa-map-marker-alt"></i>
          <span>123 Impact Street, Eco City, EC 12345</span>
        </div>
        <div class="contact-item">
          <i class="fas fa-phone"></i>
          <span>+1 (555) 123-4567</span>
        </div>
        <div class="contact-item">
          <i class="fas fa-envelope"></i>
          <span>info@ecoimpact.org</span>
        </div>
      </div>

      <!-- Bottom Footer -->
      <div class="footer-bottom">
        <div class="footer-copyright">
          &copy; {{ currentYear }} EcoImpact. All rights reserved.
        </div>
        <div class="footer-legal">
          <router-link to="/privacy">Privacy Policy</router-link>
          <router-link to="/terms">Terms of Service</router-link>
          <router-link to="/accessibility">Accessibility</router-link>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      email: "",
      currentYear: new Date().getFullYear(),
    };
  },
  methods: {
    subscribeNewsletter() {
      // Handle newsletter subscription
      alert(`Thank you for subscribing with: ${this.email}`);
      this.email = "";
      // In a real app, you would send this to your backend
    },
  },
};
</script>

<script setup>
// If you prefer Composition API:
// import { ref, computed } from 'vue'
//
// const email = ref('')
// const currentYear = computed(() => new Date().getFullYear())
//
// function subscribeNewsletter() {
//   alert(`Thank you for subscribing with: ${email.value}`)
//   email.value = ''
// }
</script>

<style>
.footer {
  background-color: var(--surface);
  color: var(--text-primary);
  padding: var(--spacing-xl) 0 var(--spacing-md);
  margin-top: var(--spacing-xxl);
  border-top: 1px solid var(--border-color);
}

.footer-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.footer-brand {
  display: flex;
  flex-direction: column;
}

.footer-logo {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
  margin-bottom: var(--spacing-sm);
}

.footer-tagline {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.6;
}

.footer-social {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-sm);
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-full);
  background-color: var(--primary);
  color: var(--text-on-primary);
  transition: all 0.2s ease;
}

.social-icon:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

/* For Font Awesome icons */
.fab,
.fas {
  font-size: var(--font-size-md);
}

.footer-heading {
  font-size: var(--font-size-md);
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
}

.footer-nav {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-nav li {
  margin-bottom: var(--spacing-sm);
}

.footer-nav a {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-nav a:hover {
  color: var(--primary);
  text-decoration: none;
}

.footer-newsletter p {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
}

.newsletter-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.newsletter-form .form-group {
  margin-bottom: 0;
}

.footer-contact {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: var(--spacing-md);
  padding: var(--spacing-lg) 0;
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
  margin-bottom: var(--spacing-md);
}

.contact-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--text-secondary);
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-md);
}

.footer-copyright {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.footer-legal {
  display: flex;
  gap: var(--spacing-md);
}

.footer-legal a {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-legal a:hover {
  color: var(--primary);
}

/* Responsive Styles */
@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }

  .footer-contact {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .footer-bottom {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }

  .footer-legal {
    flex-wrap: wrap;
    justify-content: center;
  }
}

/* Note: This component uses Font Awesome icons. You'll need to include Font Awesome in your project.
     Add this to your index.html:
     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  */
</style>