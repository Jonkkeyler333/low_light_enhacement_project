import { Link } from 'react-router-dom'
import { Box, Button, Stack, Typography } from '@mui/material'

const Root = () => {
    return (
        <Box
            sx={{
                display: 'grid',
                gridTemplateColumns: { xs: '1fr', md: '1.1fr 0.9fr' },
                gap: { xs: 3, md: 4 },
                alignItems: 'center',
                minHeight: { xs: 'auto', md: '60vh' },
                py: { xs: 2, md: 4 },
            }}
        >
            <Box>
                <Typography variant="overline" color="primary" sx={{ letterSpacing: '0.18em' }}>
                    AI IMAGE ENHANCEMENT
                </Typography>
                <Typography variant="h2" component="h2" sx={{ mt: 1.5, mb: 2 }}>
                    Bring low-light photos back to life.
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 620, lineHeight: 1.8 }}>
                    IluminAI improves visibility, balance and clarity in dark images using advanced enhancement pipelines. The interface is designed to stay calm, clear and focused while the model does the heavy lifting.
                </Typography>
                <Stack direction="row" spacing={1.5} sx={{ mt: 3, flexWrap: 'wrap' }}>
                    <Button variant="contained" component={Link} to="/login">
                        Start now
                    </Button>
                    <Button variant="outlined" component={Link} to="/home">
                        View workspace
                    </Button>
                </Stack>
            </Box>

            <Box
                sx={{
                    borderRadius: 2,
                    border: '1px solid',
                    borderColor: 'divider',
                    background:
                        'linear-gradient(145deg, rgba(43,108,176,0.08), rgba(15,118,110,0.06))',
                    p: { xs: 3, md: 4 },
                    minHeight: 280,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    boxShadow: '0 24px 80px rgba(16, 32, 51, 0.08)',
                }}
            >
                <Box>
                    <Typography variant="subtitle2" color="text.secondary">
                        First pass of the UI
                    </Typography>
                    <Typography variant="h5" component="p" sx={{ mt: 1.2, fontWeight: 700 }}>
                        Clean layout, subtle contrast, and a focus on the image workflow.
                    </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 4, maxWidth: 360 }}>
                    Next steps can add upload, preview, and inference status sections without changing this visual language.
                </Typography>
            </Box>
        </Box>
    )
}

export default Root