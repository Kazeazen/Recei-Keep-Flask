
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import LoginComponent from './components/login';
import Header from './components/header';
import RegisterComponent from './components/register';
import HomePage from './components/homepage';
import 'bootstrap/dist/css/bootstrap.min.css';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './utils/PrivateRoute';
function App() {
  return (
    <div className="center">
      
      <Router>
        <AuthProvider>
        <Header />
        <Routes>
          <Route path="/" element={
            <PrivateRoute>
              <HomePage />
            </PrivateRoute>
          } />
          <Route element={<LoginComponent />} path="/login"  />
          <Route element={<RegisterComponent />} path="/register"  />
        </Routes>
        </AuthProvider>
      </Router>
      
    </div>
  );
}

export default App;
