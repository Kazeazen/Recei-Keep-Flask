import { Route, Navigate} from 'react-router-dom'
import { useContext } from 'react';
import AuthContext from '../context/AuthContext';
const PrivateRoute = ({children}) => {
    let {authToken} = useContext(AuthContext)
    
    return authToken ? children : <Navigate to="/login" />
}

export default PrivateRoute;