import React, {useState, useEffect, useContext} from 'react'
import axios from 'axios'
import Row from 'react-bootstrap/Row';
import AuthContext from '../context/AuthContext';
import Col from 'react-bootstrap/Col';
import {Card, CardHeader, CardMedia, CardContent, CardActions, Typography} from '@material-ui/core'
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from "./cssModules/Homepage.module.css"

const ImageGrid = () => {
    let {authToken, getImages, images} = useContext(AuthContext)

    useEffect(() => {
        getImages()
    }, [])

    let deleteImage = async(e) => {
        e.preventDefault()
        await axios.delete("http://localhost:5000/images/" + e.target.id, {
            headers: {
                "Authorization":`Bearer ${authToken.access_token}`
            },
            data: {
                'id': e.target.id
            }
        })
        .then((res) => {
            console.log(res)
            getImages()
        })
        .catch((err) => {
            console.error(err)
        })
    }
    return (
        <div>
            <Row>
                {images.map(images => {
                    return (
                        <Col xs={12} md={6} lg={true} key={images.id}>
                            <Card style={{width: '20rem', height:'18rem'}} key= {images.id} className={styles.cards}>
                                <CardHeader></CardHeader>
                                <CardMedia
                                    component="img"
                                    height="145"
                                    alt={`Receipt #${images.id}`}
                                    image={require("../../../backend/" + images.img)}
                                />
                                <CardContent>
                                    <Typography component="span">
                                        {images.name}
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    <button type="button" size="small" className="btn btn-danger" onClick={deleteImage} id={images.id}>Delete</button>
                                </CardActions>
                            </Card>
                        </Col>
                    )
                })}
            </Row>
        </div>
    )
}
export default ImageGrid;