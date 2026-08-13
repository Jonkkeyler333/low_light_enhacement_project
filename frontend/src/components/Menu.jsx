import { Link } from 'react-router-dom'
import { Box, Button, Stack, Typography, Avatar } from '@mui/material'
import { Person as PersonIcon } from "@mui/icons-material"
import useUser from '../hooks/useUser'
import { useNavigate } from 'react-router-dom'
import { useNotifyActions } from '../store/notifyStore'
import LogoutIcon from '@mui/icons-material/Logout'

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
                alignitems: 'center',
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
                {user && (
                    <Button component={Link} to="/history" variant="text">
                        History
                    </Button>
                )}
                {!user && (
                    <Button component={Link} to="/login" variant="contained">
                        Login
                    </Button>
                )}
                {user && (
                    <Box sx={{ display: "flex", alignItems: "center"}}>
                        <Avatar sx={{ bgcolor: 'primary.main', width: 48, height: 48 }}>
                            {user?.name ? user.name[0].toUpperCase() : <PersonIcon />}
                        </Avatar>
                        <Typography variant="body2" color="text.secondary" sx={{ display: 'inline-flex', alignItems: 'center', mx: 1 }}> Logged in as {user.name} </Typography>
                    </Box>  
                )}
                {user && (
                    <Button onClick={handleLogout} startIcon={<LogoutIcon />} variant="outlined" color="error">
                        Logout
                    </Button>
                )}
            </Stack>            
        </Box>
    )
}

export default Menu