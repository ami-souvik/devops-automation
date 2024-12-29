import axios from 'axios'
import { useEnvars } from '@/hooks/use-envars'

const { VITE_API_BASE_URL } = useEnvars()

// Create an Axios instance
const api = axios.create({
    baseURL: VITE_API_BASE_URL, // Use Vite environment variable
    timeout: 30000,
});

// Request interceptor to add Authorization header
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken'); // Retrieve token from storage
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle errors globally
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Handle unauthorized access (e.g., token expired)
            localStorage.removeItem('authToken'); // Clear the token
            window.location.href = '/login'; // Redirect to login
        }
        return Promise.reject(error);
    }
);

export default api;