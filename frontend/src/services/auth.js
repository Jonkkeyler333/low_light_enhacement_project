import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const login = async (credentials) => {
    const response = await axios.post(`${API_URL}/api/auth/login`, credentials ,{ withCredentials: true })
    return response.data
}

export default{
    login
}