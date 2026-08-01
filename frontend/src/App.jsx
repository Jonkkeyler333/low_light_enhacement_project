import { useState } from 'react'
import{
  Routes, Route, Link, useMatch, useNavigate
} from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import Menu from './components/Menu'
import Home from './pages/Home'


const App = () => {
  return (
    <div>
        <h1>Welcome to the App xd</h1>
        <Menu />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
    </div>   
  )
}

export default App
