import { Link } from 'react-router-dom'
import { Box, Button, Stack, Typography } from '@mui/material'
import useUser from '../hooks/useUser'
import { useNavigate } from 'react-router-dom'

const Menu = () => {
    const { user, logout } = useUser()
    const navigate = useNavigate()

    const handleLogout = async () => {
        await logout()
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
            </Stack>

            {user && (
                <Typography variant="body2" color="text.secondary">
                    Logged in as <Box component="span" sx={{ fontWeight: 700, color: 'text.primary' }}>{user.name}</Box>
                </Typography>
            )}

            {user && (
                <Button onClick={handleLogout} variant="outlined">
                    Logout
                </Button>
            )}
        </Box>
    )
    
}

export default Menu