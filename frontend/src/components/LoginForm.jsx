import { useState } from "react"
import authService from "../services/auth"
import { useField } from "../hooks"
import { useNavigate } from "react-router-dom"
import useUser from "../hooks/useUser"
import { Container, TextField, Button } from "@mui/material"

const LoginForm = () => {
    const { reset: resetEmail, ...emailField} = useField("email")
    const { reset: resetPassword, ...passwordField} = useField("password")
    const [error, setError] = useState(null)
    const navigate = useNavigate()
    const { user } = useUser()

    const handleLogin = async (event) => {
        event.preventDefault()
        if (user){
            alert("You are already logged in. Please log out first.")
            return
        }
        if (!emailField.value || !passwordField.value) {
            alert("Please fill in both email and password fields.")
            return
        }
        const payload = {
            email: emailField.value, 
            plain_password: passwordField.value
        }
        console.log("Enviando:", payload)
        try {
            const response = await authService.login(payload)
            console.log("Login successful:", response)
            // const me = await authService.getMe()
            // console.log("User info:", me)
            navigate("/home")
        } catch (err) {
            console.log("Error:", err.response?.data?.detail)
            setError(err.response?.data?.detail || "Invalid Credentials")
        }
    }

    const handleReset = () => {
        resetEmail()
        resetPassword()
    }

    return (
        <Container maxWidth="sm">
            <form onSubmit={handleLogin}>
                <TextField {...emailField} fullWidth margin="normal" label="Email"/>
                <TextField {...passwordField} fullWidth margin="normal" label="Password"/>
                <Button type="submit" variant="contained" sx={{ mt: 2, mr: 1 }}>
                    Login
                </Button>
                <Button type="button" onClick={() => handleReset()} variant="outlined" color="error" sx={{ mt: 2 }}> Reset </Button>
            </form>
            {error && <p>{error}</p>}
        </Container>
    )
}

export default LoginForm