import axios from 'axios'
import React, {useState,useContext} from 'react'
import AuthContext from '../context/AuthContext'
import {Input, Form, FormGroup, Container} from 'reactstrap'
import styles from "./cssModules/Homepage.module.css"
import ImageGrid from './ImageGrid'
import { TextField } from '@material-ui/core'
const HomePage = () => {
    let [imageUpload, setImageUpload] = useState(null)
    let {authToken, getImages} = useContext(AuthContext)
    const [inputText, setInputText] = useState("")

    let uploadImage = async(e) => {
        e.preventDefault()
        await axios.post("http://localhost:5000/images", {file: imageUpload},
        {
            headers: {
                'Authorization': `Bearer ${authToken.access_token}`,
                'Content-Type':'multipart/form-data'
            },
        })
        .then(() => {
            console.log("Success")
            getImages()
        })
        .catch((error) => {
            console.error(error)
        })
    }

    let inputHandler = (e) => {
        var lower = e.target.value.toLowerCase();
        setInputText(lower)
    }

    return (
        <div>
            <Container>
                <h3 className={styles.welcomeText}>Welcome to Recei-Keep!</h3>
                <hr></hr>
                <Form className={styles.photoUpload} onSubmit={uploadImage} encType='multipart/form-data'>
                    <FormGroup>
                        <p className={styles.uploadText}>Upload Receipt!</p>
                        <Input type="file" name="photo" accept='.jpg, .png, .jpeg' placeholder='upload new photo' id="photoUpload" onChange = { (e) => setImageUpload(e.target.files[0]) }/>
                        <input type="submit" className="btn btn-primary"/>
                    </FormGroup>
                </Form>
            </Container>
            <hr></hr>
            <div className={styles.searchWidth}>
                <TextField
                    id="outlined-basic"
                    onChange={inputHandler}
                    variant="outlined"
                    fullWidth
                    label="Search" 
                    className={styles.searchColor}
                />
            </div>
            <Container>
                <ImageGrid />
            </Container>
        </div>
        
    )
}

export default HomePage;