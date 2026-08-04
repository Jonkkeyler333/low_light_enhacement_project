import { Container, TextField, Button } from "@mui/material"
import { useField } from "../hooks"
import authService from "../services/auth"
import { useNavigate } from "react-router-dom"


const RegisterForm = () => {
    const { reset: resetEmail, ...emailField} = useField("email")
    const { reset: resetPassword, ...passwordField} = useField("password")
    const { reset: resetName, ...nameField} = useField("name")
    const { reset: resetLastName, ...lastNameField} = useField("last_name")
    const { reset: resetConfirmPassword, ...confirmPasswordField} = useField("confirm_password")
    const navigate = useNavigate()

    const handleSubmit = async (event) => {
        event.preventDefault()
        if (passwordField.value !== confirmPasswordField.value) {
            alert("Passwords do not match!")
            resetEmail()
            resetPassword()
            resetConfirmPassword()
            return
        }
        try {
            const payload = {
                name: nameField.value,
                last_name: lastNameField.value,
                email: emailField.value,
                plain_password: passwordField.value
            }
            console.log("Enviando:", payload)
            const response = await authService.register(payload)
            console.log("Registration successful:", response)
            navigate("/login", { replace: true, state: { showLoginForm: true } })
        } catch (error) {
            console.error("Error during registration:", error.response?.data?.detail || error.message)
        }
    }

    const handleReset = () => {
        resetEmail()
        resetPassword()
        resetConfirmPassword()
        resetName()
        resetLastName()
    }

    return (
        <Container maxWidth="sm">
            <form onSubmit={handleSubmit}>
                <TextField {...nameField} fullWidth margin="normal" label="Name"/>
                <TextField {...lastNameField} fullWidth margin="normal" label="Last Name"/>
                <TextField {...emailField} fullWidth margin="normal" label="Email"/>
                <TextField {...passwordField} fullWidth margin="normal" label="Password"/>
                <TextField {...confirmPasswordField} fullWidth margin="normal" label="Confirm Password"/>
                <Button type="submit" variant="contained" sx={{ mt: 2, mr: 1 }}> Register </Button>
                <Button type="button" onClick={handleReset} variant="outlined" color="error" sx={{ mt: 2 }}> Reset </Button>
            </form>
        </Container>
    )
}

export default RegisterForm