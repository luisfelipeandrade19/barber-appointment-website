
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "../../screens/login/loginPage";
import RegisterPage from "../../screens/registro/registerPage";
import Home from "../../screens/home/home";
import NavBar from "../components/navBar";
 import { GoogleOAuthProvider } from '@react-oauth/google';
import Appointment from "../../screens/agendamento/appointment";


function RoutesApp() {

  const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  return (
    <GoogleOAuthProvider clientId={CLIENT_ID}>
      <BrowserRouter>
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/home" element={<Home/>}/>
            <Route path="/agendamentos" element={<Appointment/>}/>
          </Routes>
          <NavBar/>
        </BrowserRouter>
    </GoogleOAuthProvider>
        
  );
}

export default RoutesApp;
