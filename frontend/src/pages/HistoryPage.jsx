import { 
  Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper, TablePagination, CircularProgress, Container, Typography, Box
} from '@mui/material'
import { useState, useEffect } from 'react'
import useLogs from '../hooks/useLogs'
import { useNotifyActions } from '../store/notifyStore'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import CloseIcon from '@mui/icons-material/Close'

const HistoryPage = () => {
  const [page, setPage] = useState(0)
  const [limit, setLimit] = useState(10)
  const { data, isLoading, isError, error } = useLogs(page, limit)
  const { showError} = useNotifyActions()

  const handleChangePage = (event, newPage) => {
      setPage(newPage)
  }

  const handleChangeRowsPerPage = (event) => {
      setLimit(parseInt(event.target.value, 10))
      setPage(0)
  }

  useEffect(() => {
    if (isError) {
      showError(`Error loading audit logs: ${error.message}`)
    }
  }, [isError, error, showError])

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    )
  }
  if (isError) {
    return (
      <Container>
        <Typography variant="h6" color="error">
          Error loading audit logs: {error.message}
        </Typography>
      </Container>
    )
  }

  return (
    <Container>
      <Paper sx={{ width: "100%" }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>{<Typography variant="h6" fontWeight="bold">ID</Typography>}</TableCell>
                <TableCell>{<Typography variant="h6" fontWeight="bold">File Name</Typography>}</TableCell>
                <TableCell>{<Typography variant="h6" fontWeight="bold">Processing Time (s)</Typography>}</TableCell>
                <TableCell>{<Typography variant="h6" fontWeight="bold">TimeStamp</Typography>}</TableCell>
                <TableCell>{<Typography variant="h6" fontWeight="bold">Status</Typography>}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.logs.map((log) => (
                <TableRow key={log.id}>
                  <TableCell>{log.id}</TableCell>
                  <TableCell>{log.input_filename}</TableCell>
                  <TableCell>{log.processing_time.toFixed(3)}</TableCell>
                  <TableCell>{new Date(log.created_at).toLocaleString('es-CO')}</TableCell>
                  <TableCell>{log.status === 'completed' ? 
                    <CheckCircleIcon color="success"/> 
                    : 
                    <CloseIcon color="error"/> }
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          component="div"
          count={data.count}
          page={page}
          onPageChange={handleChangePage}
          rowsPerPage={limit}
          onRowsPerPageChange={handleChangeRowsPerPage}
          rowsPerPageOptions={[5, 10, 25]}
        />
      </Paper>
    </Container>
  )
}

export default HistoryPage