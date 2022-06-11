import React from 'react'
import { Link } from 'react-router-dom'
import { useContext } from 'react'
import styles from "./cssModules/Header.module.css"
import AuthContext from '../context/AuthContext';
const Header = () => {
    let {authToken, logoutUser} = useContext(AuthContext)
    
    return (
        <div className={styles.headers}>
            { authToken ? (
                <div className={styles.headers}>
                <span> | </span>
                <Link to="/">Home</Link>
                <span> | </span>
                <Link to="/settings">Settings</Link>
                <span> | </span>
                <Link to="#" onClick={logoutUser}> Logout</Link>
                </div>
            ) : (
                <div className={styles.headers}>
                <span> | </span>
                <Link to="/login"> Login</Link>
                <span> | </span>
                <Link to="/register">Register</Link>
                <span> | </span>
                </div>
            )}
        </div>

    )
}
export default Header;