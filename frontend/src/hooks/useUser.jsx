import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query"
import authService from "../services/auth"

export const useUser = () => {
  const queryClient = useQueryClient()

  const query = useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      try {
        return await authService.getMe()
      } catch (error) {
        if (error.response?.status === 401) {
          queryClient.setQueryData(["user"], null)
        }
        throw error
      }
    },
    retry: false,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    staleTime: 1000 * 60 * 5, //datos frescos por 5 minutos
    gcTime: 1000 * 60 * 30,   //La cache se elimina a los 30 minutos
  })

  const logoutMutation = useMutation({
    mutationFn: authService.logout,
    onSuccess: () => {
        // queryClient.invalidateQueries({ queryKey: ["user"]})
        queryClient.setQueryData(["user"], null)
    }
  })

  return {
    user: query.data,
    isLoading: query.isLoading,
    isError: query.isError,
    isAuthenticated: !!query.data && !query.isError,
    error: query.error,
    logout: () => logoutMutation.mutate()
  }
}

export default useUser