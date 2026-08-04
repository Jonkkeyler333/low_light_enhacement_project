import { Box, Divider, Link, Typography } from '@mui/material'

const Footer = () => {
    return (
        <Box component="footer" sx={{ pt: 2 }}>
            <Divider sx={{ mb: 2.5 }} />
            <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', pb: 2 }}>
                © 2026 IluminAI. All rights reserved. Made with ♡{' '}
                <Link href="https://github.com/Jonkkeyler333" target="_blank" rel="noopener noreferrer" underline="hover">
                    Keyler
                </Link>
            </Typography>
        </Box>
    )
}

export default Footer