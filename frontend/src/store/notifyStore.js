import { create } from 'zustand'

const useNotifyStore = create( (set) => ({
    message: '',
    open: false,
    severity: 'success',
    actions: {
        showSuccess: (message) => set({ message, open: true, severity: 'success' }),
        showError: (message) => set({ message, open: true, severity: 'error' }),
        showInfo: (message) => set({ message, open: true, severity: 'info' }),
        close: () => set({ open: false })
    }
}))

export const useMessage = () => useNotifyStore(state => state.message)
export const useOpen = () => useNotifyStore(state => state.open)
export const useSeverity = () => useNotifyStore(state => state.severity)
export const useNotifyActions = () => useNotifyStore(state => state.actions)