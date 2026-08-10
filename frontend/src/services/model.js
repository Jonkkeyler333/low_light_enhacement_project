import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api"

export const checkModel = async () => {
    const response = await axios.get(`${API_URL}/enhance/check`)
    return response.data
}

export const inference = async (file) => {
    const formData = new FormData()
    formData.append('image', file)
    const response = await axios.post(`${API_URL}/enhance/`, 
        formData,
        {responseType: "blob", withCredentials: true})
    return response.data
}

export default { checkModel, inference }