import React, {useContext} from 'react'
import {Label, Input, Form, Button, FormGroup} from 'reactstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom'
import styles from "./cssModules/LoginComponent.module.css"
import AuthContext from '../context/AuthContext';

const LoginComponent = () => {
    let {loginUser} = useContext(AuthContext)

    return (
        <div className={styles.outsideContainer}>
            <div className={styles.textContainer}>
                <Form onSubmit={loginUser}>
                    <FormGroup>
                        <Label for="usernameInput">Username</Label>
                        <Input type='text' name='username' placeholder='Enter Username' id="usernameInput"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="passwordInput">Password</Label>
                        <Input type='password' name='password' placeholder = '**********' id="passwordInput"/>
                    </FormGroup>
                    <a href="#" className={styles.forgotPassword}>Forgot Password?</a>
                    <input type='submit' id = {styles.submitButton}/>
                </Form>
                <Link to="/register" className={styles.registerNewAccount}>Register</Link>
            </div>
        </div>
    )
}

export default LoginComponent;