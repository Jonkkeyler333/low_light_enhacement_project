import { useState, useEffect, useMemo } from 'react'
import { Container, Typography, Button, Divider, Box, Paper } from '@mui/material'
import ImageZone from '../components/ImageZone'
import modelService from '../services/model'
import { useNotifyActions } from '../store/notifyStore'
import { AutoAwesome as AutoAwesomeIcon  } from '@mui/icons-material'
import RestartAltIcon from '@mui/icons-material/RestartAlt'
import DownloadIcon from '@mui/icons-material/Download'

const Enhancement = () => {
    const [file, setFile] = useState(null)
    const [result, setResult] = useState(null)
    const { showError, showSuccess, showInfo } = useNotifyActions()

    const handleFileChange = (newFile) => {
        setFile(newFile)
    }

    const handleEnhance = async () => {
        try {
            showInfo("Enhancing the image, please wait...")
            const resultBlob = await modelService.inference(file)
            setResult(resultBlob)
            showSuccess("Image enhanced successfully!")
        } catch (error) {
            showError("Error enhancing the image.")
            console.error(error.response.data.details || error.message || error)
        }        
    }

    const preview = useMemo(() => {
        if (!file) return null
        return URL.createObjectURL(file)
    }, [file])

    const resultPreview = useMemo(() => {
        if (!result) return null
        return URL.createObjectURL(result)
    }, [result])

    useEffect(() => {
        if (!preview || !resultPreview) return
        return () => {
            URL.revokeObjectURL(preview)
            URL.revokeObjectURL(resultPreview)
        }
    }, [preview, resultPreview])

    const handleReset = () => {
        setFile(null)
        setResult(null)
    }

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Low Light Image Enhancement
            </Typography>
            <ImageZone handleFileChange={handleFileChange} file={file} />
            {(preview || resultPreview) && <Divider sx={{ my: 4 }} />}
            <Box 
                sx={{ 
                    display: 'flex', 
                    flexDirection: { xs: 'column', md: 'row' },
                    gap: 3, 
                    justifyContent: 'center', 
                    alignItems: 'stretch',
                    my: 2
                }}
            >
                {preview && (
                    <Paper 
                        elevation={2} 
                        sx={{ 
                            p: 2, 
                            flex: 1, 
                            display: 'flex', 
                            flexDirection: 'column', 
                            alignItems: 'center',
                            maxWidth: { md: '50%' }
                        }}
                    >
                        <Typography variant="h6" color="text.primary" gutterBottom sx={{ fontWeight: 'medium' }}>
                            Your Current Image
                        </Typography>
                        <Divider flexItem sx={{ mb: 2 }} />
                        <Box sx={{ width: '100%', height: '350px', display: 'flex', justifyContent: 'center' }}>
                            <img 
                                src={preview} 
                                alt="Current" 
                                style={{ width: "100%", height: "100%", objectFit: "contain", borderRadius: '4px' }} 
                            />
                        </Box>
                        {file && (
                            <Typography variant="body1" color="text.secondary">
                                Selected file: {file.name}
                                Size: {(file.size / 1024).toFixed(2)} KB
                            </Typography>
                        )}
                    </Paper>
                )}

                {resultPreview && (
                    <Paper 
                        elevation={2} 
                        sx={{ 
                            p: 2, 
                            flex: 1, 
                            display: 'flex', 
                            flexDirection: 'column', 
                            alignItems: 'center',
                            maxWidth: { md: '50%' }
                        }}
                    >
                        <Typography variant="h6" color="primary" gutterBottom sx={{ fontWeight: 'bold' }}>
                            Your Enhanced Image
                        </Typography>
                        <Divider flexItem sx={{ mb: 2 }} />
                        <Box sx={{ width: '100%', height: '350px', display: 'flex', justifyContent: 'center' }}>
                            <img 
                                src={resultPreview} 
                                alt="Enhanced Result" 
                                style={{ width: "100%", height: "100%", objectFit: "contain", borderRadius: '4px' }} 
                            />
                        </Box>
                    </Paper>
                )}
            </Box>
            <Divider />
            <Button onClick={handleEnhance} startIcon={<AutoAwesomeIcon />} variant="contained" color="primary" sx={{ mt: 2, mr: 2 }} disabled={!file || result}>Enhance Image </Button>
            {resultPreview && (
                <Button startIcon={<DownloadIcon/>} variant='contained' color='success' sx={{ mt: 2, mr: 2 }} component='a' href={resultPreview} download={file ? `enhanced_${file.name}` : 'enhanced_image.png'}>
                    Download Result</Button>
            )}
            <Button onClick={handleReset} startIcon={<RestartAltIcon />} variant="contained" color="error" sx={{ mt: 2 }}>Reset File</Button>            
        </Container>
    )
}

export default Enhancement