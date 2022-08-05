import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import styles from "./cssModules/Homepage.module.css";
import {Container, Button} from 'reactstrap';
import jwtDecode from 'jwt-decode';
const Settings = () => {
    let {user} = useContext(AuthContext);
    let {email} = jwtDecode(localStorage.getItem("authToken"))["sub"];
    
    return (
        <div>
            <h1 className={styles.profileHeader}> {user}'s profile</h1>
            <div className={styles.profileContainer}>
                <div className={styles.innerProfileContainer}>                
                    <h2>Username: {user}</h2> 
                    <h2>Email: {email}</h2>
                    <Button type="button">Reset Password</Button>
                </div>
            </div>
        </div>
       
    )
}

export default Settings;