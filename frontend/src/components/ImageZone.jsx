import { useCallback, useEffect, useState, useMemo } from "react"
import { useDropzone } from "react-dropzone"
// import modelService from "../services/model"
import { Button, Container, Paper } from "@mui/material"

const ImageZone = () => {
    const [file, setFile] = useState(null)

    const onDrop = useCallback((acceptedFiles) => {
        const image = acceptedFiles[0]
        if (!image) return
        setFile(image)
    }, [])

    const preview = useMemo(() => {
        if (!file) return null
        return URL.createObjectURL(file)
    }, [file])

    useEffect(() => {
        if (!preview) return
        return () => URL.revokeObjectURL(preview)
    }, [preview])

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: {
            "image/jpeg": [".jpeg", ".jpg"],
            "image/png": [".png"],
            "image/webp": [".webp"]
        },
        multiple: false,
    })

    const handleReset = () => {
        setFile(null)
    }

    return (
        <div>
            {!file && (
                <Container>
                    <Paper sx={{p: 2, border: "2px dashed",  textAlign: "center"}}>
                        <div {...getRootProps({className: "dropzone"})}>
                            <input {...getInputProps() } />
                            <p>Drag your image here or click to select</p>
                        </div>
                    </Paper>

                </Container>
            )}
            {preview && (
                <Container>
                    <img src={preview} alt="Preview" style={{ width: "500px", height: "500px", objectFit: "contain", marginTop: "10px" }} />
                </Container>
            )}
            <Button onClick={handleReset} variant="contained" color="error" sx={{ mt: 2 }}  >Reset File</Button>
        </div>
    )
}

export default ImageZone