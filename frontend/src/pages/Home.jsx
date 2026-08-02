import useUser from "../hooks/useUser"

const HomePage = () => {
    const { user, isLoading, isError, isAuthenticated, error } = useUser()

    if (isLoading) {
        return <div>Loading...</div>
    }

    // if (isError) {
    //     return <div>Error: {error.message}</div>
    // }

    if (!isAuthenticated) {
        return <div>You are not authenticated. Please log in.</div>
    }

    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            <h2>Hiii {user?.name}</h2>
            <p>This is the home page of the application.</p>
        </div>
    )
}

export default HomePage