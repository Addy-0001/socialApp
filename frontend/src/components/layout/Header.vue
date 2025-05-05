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
      <button class="navbar-toggle" @click="isMenuOpen = !isMenuOpen" aria-label="Toggle navigation menu">
        <span class="navbar-toggle-icon" :class="{ 'open': isMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </button>

      <!-- Center: Navigation Links -->
      <div class="navbar-menu" :class="{ 'active': isMenuOpen }">
        <div class="navbar-links">
          <router-link to="/campaigns" class="navbar-link">Campaigns</router-link>
          <router-link to="/businesses" class="navbar-link">Businesses</router-link>
          <router-link to="/about" class="navbar-link">About Us</router-link>
          <router-link to="/contact" class="navbar-link">Contact</router-link>
        </div>

        <!-- Right: Authentication Buttons or User Menu -->
        <div class="navbar-auth">
          <!-- Unauthenticated User -->
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="btn btn-outline navbar-btn">Log In</router-link>
            <router-link to="/signup" class="btn btn-primary navbar-btn">Sign Up</router-link>
          </template>

          <!-- Authenticated User -->
          <template v-else>
            <!-- Create Campaign Button (Always Visible) -->
            <router-link to="/campaigns/create" class="btn btn-primary navbar-btn create-campaign-btn">
              <i class="fas fa-plus"></i>
              <span>Create Campaign</span>
            </router-link>

            <!-- User Dropdown -->
            <div class="navbar-user-dropdown">
              <button class="user-dropdown-toggle" @click="toggleUserDropdown" aria-label="User menu">
                <div v-if="authStore.user?.profile_image" class="user-avatar">
                  <img :src="authStore.user.profile_image" :alt="authStore.userFullName" />
                </div>
                <div v-else class="user-avatar-placeholder">
                  {{ userInitials }}
                </div>
                <span class="user-name">{{ authStore.userFullName }}</span>
                <i class="fas fa-chevron-down dropdown-arrow"></i>
              </button>

              <!-- User Dropdown Content -->
              <div class="dropdown-menu user-dropdown" :class="{ 'active': showUserDropdown }">
                <div class="dropdown-user-info">
                  <div v-if="authStore.user?.profile_image" class="dropdown-user-avatar">
                    <img :src="authStore.user.profile_image" :alt="authStore.userFullName" />
                  </div>
                  <div v-else class="dropdown-user-avatar-placeholder">
                    {{ userInitials }}
                  </div>
                  <div class="dropdown-user-details">
                    <div class="dropdown-user-name">{{ authStore.userFullName }}</div>
                    <div class="dropdown-user-email">{{ authStore.user?.email }}</div>
                  </div>
                </div>

                <div class="dropdown-divider"></div>

                <router-link to="/profile" class="dropdown-item">
                  <i class="fas fa-user"></i>
                  <span>My Profile</span>
                </router-link>

                <router-link to="/my-campaigns" class="dropdown-item">
                  <i class="fas fa-bullhorn"></i>
                  <span>My Campaigns</span>
                </router-link>

                <router-link to="/donations" class="dropdown-item">
                  <i class="fas fa-hand-holding-heart"></i>
                  <span>My Donations</span>
                </router-link>

                <router-link to="/settings" class="dropdown-item">
                  <i class="fas fa-cog"></i>
                  <span>Settings</span>
                </router-link>

                <div class="dropdown-divider"></div>

                <button @click="handleLogout" class="dropdown-item logout-item">
                  <i class="fas fa-sign-out-alt"></i>
                  <span>Logout</span>
                </button>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, watch, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();

    // Menu state
    const isMenuOpen = ref(false);
    const showUserDropdown = ref(false);
    const showNotifications = ref(false);

    // Mock notifications (replace with real data in production)
    const notifications = ref([
      {
        text: 'Your campaign "Clean Ocean Initiative" has received a new donation of $50',
        time: '2 hours ago',
        read: false,
        icon: 'fas fa-donate'
      },
      {
        text: 'John Smith commented on your campaign',
        time: '1 day ago',
        read: false,
        icon: 'fas fa-comment'
      },
      {
        text: 'Your campaign has reached 50% of its funding goal!',
        time: '3 days ago',
        read: true,
        icon: 'fas fa-chart-line'
      }
    ]);

    // Computed properties
    const notificationCount = computed(() => {
      return notifications.value.filter(notification => !notification.read).length;
    });

    const userInitials = computed(() => {
      if (!authStore.user || !authStore.userFullName) return '';

      const names = authStore.userFullName.split(' ');
      if (names.length >= 2) {
        return `${names[0][0]}${names[1][0]}`.toUpperCase();
      }
      return names[0][0].toUpperCase();
    });

    // Toggle dropdowns
    const toggleUserDropdown = () => {
      showUserDropdown.value = !showUserDropdown.value;
      if (showUserDropdown.value) {
        showNotifications.value = false;
      }
    };

    const toggleNotifications = () => {
      showNotifications.value = !showNotifications.value;
      if (showNotifications.value) {
        showUserDropdown.value = false;
      }
    };

    // Close dropdowns when clicking outside
    const handleClickOutside = (event) => {
      const userDropdown = document.querySelector('.navbar-user-dropdown');
      const notificationsDropdown = document.querySelector('.navbar-notifications');

      if (userDropdown && !userDropdown.contains(event.target)) {
        showUserDropdown.value = false;
      }

      if (notificationsDropdown && !notificationsDropdown.contains(event.target)) {
        showNotifications.value = false;
      }
    };

    // Add click outside listener
    window.addEventListener('click', handleClickOutside);

    // Clean up listener on component unmount
    onUnmounted(() => {
      window.removeEventListener('click', handleClickOutside);
    });

    // Close mobile menu when route changes
    watch(() => router.currentRoute.value.path, () => {
      isMenuOpen.value = false;
    });

    // Notification functions
    const markAllAsRead = () => {
      notifications.value.forEach(notification => {
        notification.read = true;
      });
    };

    // Logout function
    const handleLogout = () => {
      authStore.logout();
      router.push('/');
      isMenuOpen.value = false;
      showUserDropdown.value = false;
    };

    return {
      isMenuOpen,
      showUserDropdown,
      showNotifications,
      notifications,
      notificationCount,
      userInitials,
      authStore,
      toggleUserDropdown,
      toggleNotifications,
      markAllAsRead,
      handleLogout
    };
  }
};
</script>

<script setup>

</script>

<style>
/* Existing Navbar Styles */
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

/* New Styles for Authentication UI */

/* Create Campaign Button */
.create-campaign-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

/* User Dropdown */
.navbar-user-dropdown,
.navbar-notifications {
  position: relative;
}

.user-dropdown-toggle {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-md);
  transition: background-color 0.2s ease;
}

.user-dropdown-toggle:hover {
  background-color: var(--surface);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: var(--font-size-sm);
}

.user-name {
  font-weight: 500;
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-arrow {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  transition: transform 0.2s ease;
}

.user-dropdown-toggle:hover .dropdown-arrow {
  color: var(--text-primary);
}

.navbar-user-dropdown:has(.user-dropdown.active) .dropdown-arrow {
  transform: rotate(180deg);
}

/* Notifications */
.notifications-toggle {
  position: relative;
  background: none;
  border: none;
  cursor: pointer;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
}

.notifications-toggle:hover {
  background-color: var(--surface);
}

.notifications-toggle i {
  font-size: var(--font-size-md);
  color: var(--text-secondary);
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: var(--error);
  color: white;
  font-size: 10px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Dropdown Menus */
.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background-color: var(--background);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  min-width: 240px;
  max-width: 320px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
  z-index: 1000;
  overflow: hidden;
}

.dropdown-menu.active {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
}

.dropdown-user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.dropdown-user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.dropdown-user-avatar-placeholder {
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

.dropdown-user-details {
  overflow: hidden;
}

.dropdown-user-name {
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-user-email {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-primary);
  text-decoration: none;
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: var(--surface);
}

.dropdown-item i {
  width: 16px;
  color: var(--text-secondary);
}

.logout-item {
  color: var(--error);
  border: none;
  background: none;
  width: 100%;
  text-align: left;
}

.logout-item i {
  color: var(--error);
}

/* Notifications Dropdown */
.notifications-dropdown {
  width: 320px;
  max-height: 400px;
  display: flex;
  flex-direction: column;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.dropdown-header h3 {
  font-size: var(--font-size-md);
  margin: 0;
}

.mark-all-read {
  background: none;
  border: none;
  color: var(--primary);
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.notifications-list {
  max-height: 300px;
  overflow-y: auto;
}

.notification-item {
  display: flex;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  transition: background-color 0.2s ease;
}

.notification-item:hover {
  background-color: var(--surface);
}

.notification-item.unread {
  background-color: rgba(46, 125, 50, 0.05);
}

.notification-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--surface);
  color: var(--primary);
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-text {
  margin: 0 0 4px 0;
  font-size: var(--font-size-sm);
}

.notification-time {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

.empty-notifications {
  padding: var(--spacing-md);
  text-align: center;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.dropdown-footer {
  padding: var(--spacing-sm) var(--spacing-md);
  text-align: center;
  border-top: 1px solid var(--border-color);
}

.view-all {
  color: var(--primary);
  font-size: var(--font-size-sm);
  text-decoration: none;
}

.view-all:hover {
  text-decoration: underline;
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
    justify-content: flex-start;
    background-color: var(--background);
    transition: all 0.3s ease;
    margin-left: 0;
    z-index: 1000;
    padding-top: 70px;
    overflow-y: auto;
  }

  .navbar-menu.active {
    right: 0;
  }

  .navbar-links {
    flex-direction: column;
    align-items: center;
    margin-bottom: var(--spacing-xl);
    width: 100%;
  }

  .navbar-link {
    font-size: var(--font-size-lg);
    padding: var(--spacing-md);
    width: 100%;
    text-align: center;
  }

  .navbar-auth {
    flex-direction: column;
    width: 100%;
    gap: var(--spacing-md);
    padding: 0 var(--spacing-md);
  }

  .navbar-btn {
    width: 100%;
    text-align: center;
    padding: var(--spacing-md);
  }

  /* Mobile authenticated user UI */
  .create-campaign-btn {
    order: -1;
    margin-bottom: var(--spacing-md);
  }

  .navbar-user-dropdown {
    width: 100%;
  }

  .user-dropdown-toggle {
    width: 100%;
    justify-content: center;
    padding: var(--spacing-md);
    background-color: var(--surface);
  }

  .dropdown-menu {
    position: static;
    opacity: 1;
    visibility: visible;
    transform: none;
    box-shadow: none;
    max-width: 100%;
    width: 100%;
    margin-top: var(--spacing-md);
    display: none;
  }

  .dropdown-menu.active {
    display: block;
  }

  .navbar-notifications {
    width: 100%;
    margin-bottom: var(--spacing-md);
  }

  .notifications-toggle {
    width: 100%;
    height: auto;
    border-radius: var(--border-radius-md);
    padding: var(--spacing-md);
    background-color: var(--surface);
    justify-content: center;
  }

  .notification-badge {
    top: var(--spacing-md);
    right: calc(50% - 50px);
  }
}
</style>