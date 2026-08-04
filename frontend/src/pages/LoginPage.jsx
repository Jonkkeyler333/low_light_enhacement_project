import LoginForm from "../components/LoginForm"
import RegisterForm from "../components/RegisterForm"
import { useState } from "react"
import { useLocation } from "react-router-dom"
import { Box, Button, Stack, Typography } from "@mui/material"

const LoginPage = () => {
    const location = useLocation()
    const [showLoginForm, setShowLoginForm] = useState(true)
    const activeShowLoginForm = location.state?.showLoginForm ?? showLoginForm

    return (
        <Box
            sx={{
                display: 'grid',
                gridTemplateColumns: { xs: '1fr', md: '0.9fr 1.1fr' },
                gap: { xs: 3, md: 4 },
                alignItems: 'start',
                py: { xs: 1, md: 2 },
            }}
        >
            <Box
                sx={{
                    borderRadius: 2,
                    border: '1px solid',
                    borderColor: 'divider',
                    backgroundColor: 'background.paper',
                    p: { xs: 3, md: 4 },
                }}
            >
                <Typography variant="overline" color="primary" sx={{ letterSpacing: '0.18em' }}>
                    ACCESS
                </Typography>
                <Typography variant="h4" component="h2" sx={{ mt: 1, mb: 1.5 }}>
                    Welcome to the Login Page
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.8 }}>
                    Use your account to access the enhancement workspace.
                </Typography>
                <Stack direction="row" spacing={1.5} sx={{ mt: 3, flexWrap: 'wrap' }}>
                    <Button variant={activeShowLoginForm ? 'contained' : 'outlined'} onClick={() => setShowLoginForm(true)}>
                        Log in
                    </Button>
                    <Button variant={!activeShowLoginForm ? 'contained' : 'outlined'} onClick={() => setShowLoginForm(false)}>
                        Register
                    </Button>
                </Stack>
            </Box>

            <Box
                sx={{
                    borderRadius: 2,
                    border: '1px solid',
                    borderColor: 'divider',
                    backgroundColor: 'background.paper',
                    p: { xs: 3, md: 4 },
                }}
            >
                {activeShowLoginForm ? (
                    <Stack spacing={2.5}>
                        <Box>
                            <Typography variant="h5" component="h3">
                                Sign in
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                                Enter your credentials to continue.
                            </Typography>
                        </Box>
                        <LoginForm />
                        <Button variant="text" onClick={() => setShowLoginForm(false)} sx={{ alignSelf: 'flex-start', px: 0 }}>
                            Don't have an account? Register here
                        </Button>
                    </Stack>
                ) : (
                    <Stack spacing={2.5}>
                        <Box>
                            <Typography variant="h5" component="h3">
                                Create account
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                                Register to start enhancing images.
                            </Typography>
                        </Box>
                        <RegisterForm />
                        <Button variant="text" onClick={() => setShowLoginForm(true)} sx={{ alignSelf: 'flex-start', px: 0 }}>
                            Already have an account? Log in here
                        </Button>
                    </Stack>
                )}
            </Box>
        </Box>
    )
}

export default LoginPage