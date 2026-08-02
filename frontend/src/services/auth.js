import axios from 'axios'

// const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const login = async (credentials) => {
    const response = await axios.post(`/api/auth/login`, credentials ,{ withCredentials: true })
    return response.data
}

const logout = async () => {
    const response = await axios.post(`/api/auth/logout`, {}, { withCredentials: true })
    return response.data
}

const getMe = async () => {
    const response = await axios.get(`/api/auth/me`, { withCredentials: true })
    return response.data
}

const register = async (userData) => {
    const response = await axios.post(`/api/auth/register`, userData)
    return response.data
}

export default {
    login,
    logout,
    getMe,
    register
}   