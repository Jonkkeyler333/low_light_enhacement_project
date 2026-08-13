import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api"

const getUserLogs = async (skip, limit) => {
    const response = await axios.get(`${API_URL}/logs/me`, {
        params: { skip, limit },
        withCredentials: true
    })
    console.log(response.data)
    return response.data
}

export default { getUserLogs }