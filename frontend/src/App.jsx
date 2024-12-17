import { useState } from 'react'
import './App.css'
import Home from './components/Home'
import Register from './components/Register'
import Login from './components/Login'
import About from './components/About'
import Chat from './components/Chat'
import {Routes, Route, useLocation} from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoutes'
import NotFound from './components/NotFound';


function App() {
  const location = useLocation();
  return (
    <>
      {
        <Routes>
          <Route path="login/" element={<Login />}/>
          <Route path="register/" element={<Register />}/>
          <Route path="/" element={<Home />}/>
          <Route path="home/" element={<Home />}/>
          <Route path="about/" element={<About />}/>

          <Route element={<ProtectedRoute />}>
            <Route path="chat/" element={<Chat />}/>
          </Route> 
          <Route path="*" element={<NotFound />} />  
        </Routes>
      }     
    </>
  )
}

export default App