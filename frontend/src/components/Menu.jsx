import { Link } from 'react-router-dom'
import { Box, Button, Stack, Typography } from '@mui/material'
import useUser from '../hooks/useUser'
import { useNavigate } from 'react-router-dom'
import { useNotifyActions } from '../store/notifyStore'

const Menu = () => {
    const { user, logout } = useUser()
    const navigate = useNavigate()
    const { showSuccess } = useNotifyActions()

    const handleLogout = async () => {
        await logout()
        showSuccess("Logout successful")
        navigate("/")
    }

    return (
        <Box
            sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: 2,
                width: '100%',
                flexWrap: 'wrap',
            }}
        >
            <Stack direction="row" spacing={1} alignItems="center">
                {user && (
                    <Button component={Link} to="/home" variant="text">
                        Home
                    </Button>
                )}
                {!user && (
                    <Button component={Link} to="/login" variant="contained">
                        Login
                    </Button>
                )}
                {user && (
                    <Typography variant="body2" color="text.secondary" sx={{ display: 'inline-flex', alignItems: 'center', mx: 1 }}> Logged in as {user.name} </Typography>
                )}
                {user && (
                    <Button onClick={handleLogout} variant="outlined">
                        Logout
                    </Button>
                )}
            </Stack>            
        </Box>
    )
}

export default Menu