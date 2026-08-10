import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const login = async (credentials) => {
    const response = await axios.post(`${API_URL}/auth/login`, credentials ,{ withCredentials: true })
    return response.data
}

const logout = async () => {
    const response = await axios.post(`${API_URL}/auth/logout`, {}, { withCredentials: true })
    return response.data
}

const getMe = async () => {
    const response = await axios.get(`${API_URL}/auth/me`, { withCredentials: true })
    return response.data
}

const register = async (userData) => {
    const response = await axios.post(`${API_URL}/auth/register`, userData)
    return response.data
}

export default {
    login,
    logout,
    getMe,
    register
}   