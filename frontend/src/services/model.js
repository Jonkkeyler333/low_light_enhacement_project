import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export const checkModel = async () => {
    const response = await axios.get(`${API_URL}/api/enhance/check`)
    return response.data
}

export default { checkModel }