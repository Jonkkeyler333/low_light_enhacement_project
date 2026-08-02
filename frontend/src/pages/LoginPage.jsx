import LoginForm from "../components/LoginForm"
import RegisterForm from "../components/RegisterForm"
import { useState } from "react"
import { useLocation } from "react-router-dom"

const LoginPage = () => {
    const location = useLocation()
    const [showLoginForm, setShowLoginForm] = useState(location.state?.showLoginForm ?? true)

    return (
        <div>
            <h2>Welcome to the Login Page</h2>
            {showLoginForm ? (
                <div>
                    <h3>Please enter your credentials to log in.</h3>
                    <LoginForm />
                    <button onClick={() => setShowLoginForm(false)}>Don't have an account? Register here</button>
                </div>
                ) : (
                <div>
                    <RegisterForm />
                    <button onClick={() => setShowLoginForm(true)}>Already have an account? Log in here</button>
                </div>
                )
            }            
        </div>
    )
}

export default LoginPage