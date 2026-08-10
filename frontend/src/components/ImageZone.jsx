import { useCallback } from "react"
import { useDropzone } from "react-dropzone"
// import modelService from "../services/model"
import { Container, Paper } from "@mui/material"

const ImageZone = ({handleFileChange, file}) => {
    
    const onDrop = useCallback((acceptedFiles) => {
        const image = acceptedFiles[0]
        if (!image) return
        handleFileChange(image)
    }, [handleFileChange])

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        accept: {
            "image/jpeg": [".jpeg", ".jpg"],
            "image/png": [".png"],
            "image/webp": [".webp"]
        },
        multiple: false,
    })

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
        </div>
    )
}

export default ImageZone