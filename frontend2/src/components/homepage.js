import axios from 'axios'
import React, {useState,useEffect,useContext} from 'react'
import AuthContext from '../context/AuthContext'


const HomePage = () => {
    let [images, setImages] = useState([])
    let [authToken, logoutUser] = useContext(AuthContext)
}