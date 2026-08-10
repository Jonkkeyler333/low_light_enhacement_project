import { useQuery } from "@tanstack/react-query"
import logService from "../services/logs"

export const useLogs = (page, limit) => {
    const skip = page * limit

    const query = useQuery({
        queryKey: ["logs", page, limit],
        queryFn: () => logService.getUserLogs(skip, limit)
    })

    return {
        logs: query.data,
        isLoading: query.isLoading,
        isError: query.isError,
        error: query.error
    }

}