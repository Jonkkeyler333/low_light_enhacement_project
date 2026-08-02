import { useField } from "../hooks"
import authService from "../services/auth"
import { useNavigate } from "react-router-dom"

// campos name: str = Field(min_length = 1, max_length = 50)
    // last_name: str = Field(min_length = 1, max_length = 50)
    // email: EmailStr
    // plain_password: str = Field(min_length = 1)

const RegisterForm = () => {
    const { reset: resetEmail, ...emailField} = useField("email")
    const { reset: resetPassword, ...passwordField} = useField("password")
    const { ...nameField} = useField("name")
    const { ...lastNameField} = useField("last_name")
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

    return (
        <div>
            <h3>Welcome to the Registration Form </h3>
            <span role="img" aria-label="waving man" aria-hidden="true">
                👋
            </span>
            <p>Fill in the fields below to register.</p>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name  </label>
                    <input {...nameField} />
                </div>
                <div>
                    <label>Last Name  </label>
                    <input {...lastNameField} />
                </div>
                <div>
                    <label>Email  </label>
                    <input {...emailField} />
                </div>
                <div>
                    <label>Password  </label>
                    <input {...passwordField} />
                </div>
                <div>
                    <label>Confirm Password  </label>
                    <input {...confirmPasswordField} />
                </div>
                <button type="submit">Register</button>
            </form>
        </div>
    )
}

export default RegisterForm