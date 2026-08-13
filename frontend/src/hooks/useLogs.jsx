import { useQuery } from "@tanstack/react-query"
import logService from "../services/logs"

const useLogs = (page, limit) => {
    const skip = page * limit

    const query = useQuery({
        queryKey: ["logs", page, limit],
        queryFn: async () => await logService.getUserLogs(skip, limit)
    })

    return {
        data: query.data,
        isLoading: query.isLoading,
        isError: query.isError,
        error: query.error
    }
}

export default useLogs