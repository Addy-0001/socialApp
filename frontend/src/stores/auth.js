import { defineStore } from 'pinia';
import apiClient from '@/axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        accessToken: null,
        refreshToken: null,
        isAuthenticated: false,
        loading: false,
    }),

    getters: {
        // Get current user
        currentUser: (state) => state.user,

        // Check if user is authenticated
        userIsAuthenticated: (state) => state.isAuthenticated,

        // Check if user has a specific role
        hasRole: (state) => (role) => {
            return state.user && state.user.role === role;
        },

        // Get user's full name
        userFullName: (state) => {
            return state.user ? state.user.full_name : '';
        },

        // Get auth token for API requests
        authToken: (state) => state.accessToken,
    },

    actions: {
        // Set auth data after successful login
        setAuth(authData) {
            this.accessToken = authData.access;
            this.refreshToken = authData.refresh || null;
            this.user = authData.user;
            this.isAuthenticated = true;

            // Store token in localStorage for persistence
            localStorage.setItem('accessToken', this.accessToken);
            if (this.refreshToken) {
                localStorage.setItem('refreshToken', this.refreshToken);
            }
            localStorage.setItem('user', JSON.stringify(this.user));

            // Set auth header for future API requests
            apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`;
        },

        // Login user
        async login(credentials) {
            this.loading = true;

            try {
                const response = await apiClient.post('auth/login/', credentials);
                this.setAuth(response.data);
                return { success: true, data: response.data };
            } catch (error) {
                console.error('Login error:', error);
                return {
                    success: false,
                    error: error.response?.data || 'An error occurred during login'
                };
            } finally {
                this.loading = false;
            }
        },

        // Logout user
        logout() {
            this.user = null;
            this.accessToken = null;
            this.refreshToken = null;
            this.isAuthenticated = false;

            // Remove from localStorage
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');

            // Remove auth header
            delete apiClient.defaults.headers.common['Authorization'];
        },

        // Initialize auth state from localStorage (on app start)
        initAuth() {
            const accessToken = localStorage.getItem('accessToken');
            const refreshToken = localStorage.getItem('refreshToken');
            const user = localStorage.getItem('user');

            if (accessToken && user) {
                this.accessToken = accessToken;
                this.refreshToken = refreshToken || null;
                this.user = JSON.parse(user);
                this.isAuthenticated = true;

                // Set auth header for API requests
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`;
            }
        },

        // Check if token is valid (can be expanded to verify with backend)
        checkAuth() {
            return this.isAuthenticated;
        }
    }
});