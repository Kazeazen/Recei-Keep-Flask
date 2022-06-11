import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';
import styles from "./cssModules/Homepage.module.css";
import {Container, Label, Button} from 'reactstrap';
import jwtDecode from 'jwt-decode';
const Settings = () => {
    let {user, authToken} = useContext(AuthContext)
    let {email} = jwtDecode(localStorage.getItem("authToken"))["sub"]
    
    return (
        <div className={styles.profileContainer}>
            <h1> {user}'s profile</h1>
            <Container className={styles.innerProfileContainer}>                
                <h2>Username:</h2><span>{user}</span>
                <br></br>
                <h2>Email: </h2> <span>{email}</span>
                <br></br>
                <br></br>
                <Button type="button">Reset Password</Button>
                
            </Container>
        </div>
       
    )
}

export default Settings;