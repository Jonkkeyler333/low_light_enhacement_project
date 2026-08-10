import { 
  Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper, TablePagination, CircularProgress, Container, Typography, Box, Divider
} from '@mui/material'
import { useState } from 'react'
import { useLogs } from '../hooks/useLogs'
import { useNotifyActions } from '../store/notifyStore'

const HistoryPage = () => {
    const [page, setPage] = useState(0)
    const [limit, setLimit] = useState(10)
    const { logs, isLoading, isError, error } = useLogs(page, limit)
    const { showError, showInfo } = useNotifyActions()
    const totalLogs = logs.length

    const handleChangePage = (event, newPage) => {
        setPage(newPage)
    }

    const handleChangeRowsPerPage = (event) => {
        setLimit(parseInt(event.target.value, 10));
        setPage(0)
    }

  if (isLoading) {
    showInfo("Loading audit logs...")
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    )
  }
  if (isError) {
    showError(`Error loading audit logs: ${error.message}`)
    return (
      <Container>
        <Typography variant="h6" color="error">
          Error loading audit logs: {error.message}
        </Typography>
      </Container>
    )
  }

  return (
    <Paper sx={{ width: '100%' }}>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Acción</TableCell>
              <TableCell>Usuario</TableCell>
              <TableCell>Fecha</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {logs.map((log) => (
              <TableRow key={log.id}>
                <TableCell>{log.id}</TableCell>
                <TableCell>{log.action}</TableCell>
                <TableCell>{log.user}</TableCell>
                <TableCell>{log.createdAt}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Control de paginación de Material UI */}
      <TablePagination
        component="div"
        count={totalLogs} // Total global de registros en la BD
        page={page}
        onPageChange={handleChangePage}
        rowsPerPage={limit}
        onRowsPerPageChange={handleChangeRowsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </Paper>
  )
}

export default HistoryPage