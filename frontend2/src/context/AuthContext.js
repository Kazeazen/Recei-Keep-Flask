import { createContext, useState} from 'react'
import axios from "axios";
import { useNavigate } from 'react-router-dom'
import jwtDecode from 'jwt-decode';

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({children}) => {

    const [authToken, setAuthToken] = useState(() => localStorage.getItem('authToken') ? JSON.parse(localStorage.getItem('authToken')) : null)
    const [user, setUser] = useState(() => localStorage.getItem("authToken") ? jwtDecode(localStorage.getItem("authToken"))["sub"]["username"] : null)
    const navigate = useNavigate();
    
    let loginUser = async(e) => {
        e.preventDefault()
        let data = await axios.post("http://localhost:5000/login", {
            headers: {
                "Content-Type":"application/json"
            },
            username: e.target.username.value, password: e.target.password.value
        })
        if (data.status === 200) {
            setAuthToken(data.data)
            setUser(data.data.access_token)
            localStorage.setItem("authToken", JSON.stringify(data.data))
            navigate("/")
        }
        else {
            alert("Something went wrong.")
        }
    }

    // let registerUser {handles user registration, redirects back to login}

    let registerUser = async(e) => {
        e.preventDefault()
        let data = await axios.post("http://localhost:5000/register", {
            headers: {
                "Content-Type":"application/json"
            },
            username: e.target.username.value, password: e.target.password.value, email: e.target.email.value
        })
        if (data.status === 200) {
            setAuthToken(data.data)
            setUser(data.data.access_token)
            localStorage.setItem("authToken", JSON.stringify(data.data))
            navigate("/")
        }
        else {
            alert("Something went wrong...")
            console.log(data)
        }
    }
    let logoutUser = () => {
        setAuthToken(null)
        setUser(null)
        localStorage.removeItem("authToken")
        navigate("/login")
    }

    let contextData = {
        loginUser:loginUser,
        authToken:authToken,
        logoutUser:logoutUser,
        registerUser:registerUser,
        user: user
    }


    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
}