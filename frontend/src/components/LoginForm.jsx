import { useState } from "react"
import authService from "../services/auth"
import { useField } from "../hooks"
import { useNavigate } from "react-router-dom"

const LoginForm = () => {
    const { reset: resetEmail, ...emailField} = useField("email")
    const { reset: resetPassword, ...passwordField} = useField("password")
    const [error, setError] = useState(null)
    const navigate = useNavigate()

    const handleLogin = async (event) => {
        event.preventDefault()
        const payload = {
            email: emailField.value, 
            plain_password: passwordField.value
        }
        console.log("Enviando:", payload)
        try {
            const response = await authService.login(payload)
            console.log("Login successful:", response.data)
            navigate("/")
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
        <div>
            <form onSubmit={handleLogin}>
                <div>
                    <label>Email</label>
                    <input {...emailField} />
                </div>
                <div>
                    <label>Password</label>
                    <input {...passwordField} />
                </div>
                <button type="submit">Login</button>
            </form>
            <button onClick={() => handleReset()}>Reset</button>
            {error && <p>{error}</p>}
        </div>
    )
}

export default LoginForm