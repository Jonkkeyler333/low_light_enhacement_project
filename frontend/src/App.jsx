import { Routes, Route } from 'react-router-dom'
import { Box, Container, CssBaseline, GlobalStyles, ThemeProvider, Typography, createTheme } from '@mui/material'
import LoginPage from './pages/LoginPage'
import Menu from './components/Menu'
import HomePage from './pages/Home'
import Root from './pages/Root'
import Footer from './components/Footer'

const theme = createTheme({
  palette: {
    primary: { main: '#2B6CB0' },
    secondary: { main: '#0F766E' },
    background: { default: '#F4F7FB', paper: '#FFFFFF' },
    text: { primary: '#102033', secondary: '#546375' },
  },
  shape: { borderRadius: 20 },
  typography: {
    fontFamily: '"Segoe UI", "Roboto", sans-serif',
    h1: { fontWeight: 700, letterSpacing: '-0.04em' },
    h2: { fontWeight: 700, letterSpacing: '-0.03em' },
    h3: { fontWeight: 700, letterSpacing: '-0.02em' },
    button: { textTransform: 'none', fontWeight: 600 },
  },
})

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <GlobalStyles
        styles={{
          html: { colorScheme: 'light' },
          body: { margin: 0, minWidth: 320 },
          '#root': { minHeight: '100vh' },
          a: { color: 'inherit', textDecoration: 'none' },
        }}
      />
      <Box
        sx={{
          minHeight: '100vh',
          background:
            'radial-gradient(circle at top left, rgba(43, 108, 176, 0.12), transparent 30%), linear-gradient(180deg, #f7f9fc 0%, #eef3f8 100%)',
          py: { xs: 2, md: 4 },
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: { xs: 3, md: 4 } }}>
            <Box
              sx={{
                display: 'flex',
                alignItems: { xs: 'flex-start', sm: 'center' },
                justifyContent: 'space-between',
                flexDirection: { xs: 'column', sm: 'row' },
                gap: 1.5,
                py: 1,
              }}
            >
              <Box>
                <Typography variant="h3" component="h1">IluminAI</Typography>
                <Typography variant="body2" color="text.secondary">
                  Low-light enhancement for sharper, clearer images.
                </Typography>
              </Box>
              <Menu />
            </Box>

            <Box sx={{ px: { xs: 0, md: 1 }, pb: { xs: 2, md: 3 } }}>
              <Routes>
                <Route path="/" element={<Root />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/home" element={<HomePage />} />
              </Routes>
            </Box>

            <Footer />
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  )
}

export default App
