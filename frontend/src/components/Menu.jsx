import { Link } from 'react-router-dom'
import authService from '../services/auth'
import useUser from '../hooks/useUser'
import { useNavigate } from 'react-router-dom'

const Menu = () => {
    const padding = { paddingRight: 5 }
    const { user, logout } = useUser()
    const navigate = useNavigate()

    const handleLogout = async () => {
        await logout()
        navigate("/")
    }

    return (
        <div>
            <Link style={padding} to="/home">Home</Link>
            {!user && <Link style={padding} to="/login">Login</Link>}
            {user && <span style={padding}>Logged in as: {user.name}</span>}
            {user && (
                <button style={padding} onClick={() => handleLogout()}>
                    Logout
                </button>
            )}
        </div>
    )
    
}

export default Menu