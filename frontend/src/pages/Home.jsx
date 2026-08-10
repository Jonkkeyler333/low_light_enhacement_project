import { useEffect, useRef } from "react"
import { useState } from "react"
import modelService from "../services/model"
import useUser from "../hooks/useUser"
import ImageZone from "../components/ImageZone"
import { useNotifyActions } from "../store/notifyStore"
import { Container, Typography, Paper, Chip, Box, CircularProgress, Grid, Avatar, Divider, Alert, CardContent, Card } from "@mui/material"
import {
    AutoAwesome as AutoAwesomeIcon,
    CheckCircle as CheckCircleIcon,
    Person as PersonIcon,
    CloudUpload as CloudUploadIcon
} from "@mui/icons-material"

const HomePage = () => {
    const { user, isLoading, isError, isAuthenticated, error } = useUser()
    const { showError, showInfo } = useNotifyActions()
    const [modelData, setModelData] = useState(null)
    const lastMessageRef = useRef("")

    useEffect(() => {
        if (isLoading) {
            const message = "Loading user data"
            if (lastMessageRef.current !== message) {
                lastMessageRef.current = message
                showInfo(message)
            }
            return
        }

        if (isError) {
            const message = `Error: ${error?.message || "Unknown error"}`
            if (lastMessageRef.current !== message) {
                lastMessageRef.current = message
                showError(message)
            }
        }
    }, [isLoading, isError, error, showInfo, showError])

    useEffect(() => {
        const fetchModelData = async () => {
            try {
                const data = await modelService.checkModel()
                console.log("Model data fetched:", data)
                setModelData(data)
            } catch (error) {
                console.error("Error fetching model data:", error)
            }
        }
        fetchModelData()
    }, [])

    if (isLoading) {
        return (
            <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" minHeight="60vh">
                <CircularProgress size={50} thickness={4} />
                <Typography variant="body1" color="text.secondary" sx={{ mt: 2 }}>
                    Loading user data...
                </Typography>
            </Box>
        )
    }

    if (!isAuthenticated) {
        return (
            <Container maxWidth="sm" sx={{ mt: 8 }}>
                <Alert severity="warning" variant="outlined" sx={{ borderRadius: 2 }}>
                    You're not logged in. Please log in to access the enhancement workspace.
                </Alert>
            </Container>
        )
    }

    return (
        <Container maxWidth="lg">
            <Paper
                elevation={0}
                sx={{
                    p: { xs: 3, md: 4 },
                    mb: 4,
                    borderRadius: 2 ,
                    background: (theme) =>
                        `linear-gradient(135deg, ${theme.palette.primary.main}15 0%, ${theme.palette.secondary.main}15 100%)`,
                    border: '1px solid',
                    borderColor: 'divider',
                    position: 'relative',
                    overflow: 'hidden'
                }}
            >
                <Box display="flex" alignItems="center" gap={2} mb={2}>
                    <Avatar sx={{ bgcolor: 'primary.main', width: 48, height: 48 }}>
                        {user?.name ? user.name[0].toUpperCase() : <PersonIcon />}
                    </Avatar>
                    <Box>
                        <Typography variant="h4" component="h1" fontWeight="bold">
                            ¡Welcome, {user?.name || "Usuario"}!
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Main Panel
                        </Typography>
                    </Box>
                </Box>

                <Typography variant="body1" color="text.secondary" sx={{ maxWidth: '600px', mb: 2 }}>
                    Enhance your low-light images
                </Typography>
                
                <Divider sx={{ my: 2 }} />

                <Box display="flex" alignItems="center" gap={1} color="primary.main">
                    <CloudUploadIcon fontSize="small" />
                    <ImageZone />
                </Box>
            </Paper>


            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Card variant="outlined" sx={{ borderRadius: 2 }}>
                        <CardContent sx={{ p: 3 }}>
                            <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={2}>
                                <Box display="flex" alignItems="center" gap={1.5}>
                                    <AutoAwesomeIcon color="primary" fontSize="medium" />
                                    <Box>
                                        <Typography variant="h6" fontWeight="bold">
                                            Model Status
                                        </Typography>
                                    </Box>
                                </Box>

                                { modelData?.model_loaded ? (
                                    <Chip
                                        icon={<CheckCircleIcon />}
                                        label="Modelo activo y listo"
                                        color="success"
                                        variant="soft"
                                        sx={{ fontWeight: 'bold' }}
                                    />
                                ) : (
                                    <Chip
                                        label="Modelo fuera de línea"
                                        color="error"
                                        variant="outlined"
                                    />
                                )}
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Container>
    )
}

export default HomePage