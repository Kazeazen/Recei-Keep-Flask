import {Navigate} from 'react-router-dom'
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';
const PrivateRoute = ({children}) => {
    let {authToken, user} = useContext(AuthContext)
    
    return authToken && user ? children : <Navigate to="/login" />
}

export default PrivateRoute;