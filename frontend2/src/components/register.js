import React, {useContext} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import {Label, Input, Form, Button, FormGroup} from 'reactstrap'
import { Link } from 'react-router-dom'
import styles from "./cssModules/Register.module.css"
import AuthContext from '../context/AuthContext';
const RegisterComponent = () => {
    let {registerUser} = useContext(AuthContext)
    return(
        <div className={styles.outsideContainer}>
            <div className={styles.textContainer}>
                <Form onSubmit={registerUser}>
                    <FormGroup>
                        <Label for="usernameInput">Username</Label>
                        <Input type='text' name='username' placeholder='Enter Username' id="usernameInput"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="passwordInput">Password</Label>
                        <Input type='password' name='password' placeholder = '**********' id="passwordInput"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="registerEmailInput">Email</Label>
                        <Input type="email" name="email" placeholder='example@example.com' id="registerEmailInput" />
                    </FormGroup>
                    <input type='submit' id = {styles.submitButton}/>
                </Form>
            </div>
        </div>
    )
}
export default RegisterComponent;