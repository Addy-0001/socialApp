import axios from 'axios';

// Create axios instance with base URL
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/v1/',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// Add a request interceptor to include auth token
apiClient.interceptors.request.use(
    config => {
        // Get token from localStorage
        const token = localStorage.getItem('accessToken');

        // If token exists, add to headers
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }

        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle token refresh (can be expanded)
apiClient.interceptors.response.use(
    response => response,
    async error => {
        // Handle 401 errors (token expired)
        if (error.response && error.response.status === 401) {
            // Could implement token refresh logic here

            // For now, just redirect to login
            localStorage.removeItem('accessToken');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }

        return Promise.reject(error);
    }
);

export default apiClient;