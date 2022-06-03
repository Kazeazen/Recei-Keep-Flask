import axios from 'axios'
import React, {useState,useEffect,useContext} from 'react'
import AuthContext from '../context/AuthContext'


const HomePage = () => {
    let [images, setImages] = useState([])
    let {logoutUser, user} = useContext(AuthContext)

    return (
        <h3>Hello {user}</h3> 
    )
}

export default HomePage;