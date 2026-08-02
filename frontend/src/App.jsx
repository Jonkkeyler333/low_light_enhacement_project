import{
  Routes, Route
} from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import Menu from './components/Menu'
import HomePage from './pages/Home'
import Root from './pages/Root'
import Footer from './components/Footer'


const App = () => {
  return (
    <div>
        <h1>IluminAI</h1>
        <Menu />
        <Routes>
          <Route path="/" element={<Root />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/home" element={<HomePage />} />
        </Routes>
        <Footer />
    </div>   
  )
}

export default App
