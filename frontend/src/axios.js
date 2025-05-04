// axios config for project with django rest framework, jwt
import axios from "axios";

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
});

// Add a request interceptor
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    }
)


export default apiClient;