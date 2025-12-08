import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import LoginPage from "../../screens/login/loginPage";
import RegisterPage from "../../screens/registro/registerPage";
import Home from "../../screens/home/home";
import NavBar from "../components/navBar/navBar";
import Agendar from "../../screens/agendar/agendar";

 import { GoogleOAuthProvider } from '@react-oauth/google';
import Appointment from "../../screens/agendamento/appointment";
import HistoryPage from "../../screens/historico/historyPage";

function Layout() {
  const location = useLocation();
  const hideNavBarPaths = ['/', '/register'];
  const showNavBar = !hideNavBarPaths.includes(location.pathname);

  return (
    <>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/agendar" element={<Agendar/>} />
        <Route path="/home" element={<Home/>}/>
        <Route path="/agendamentos" element={<Appointment/>}/>
        <Route path="/historico" element={<HistoryPage/>}/>
      </Routes>
      {showNavBar && <NavBar/>}
    </>
  );
}

function RoutesApp() {

  const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  return (
    <GoogleOAuthProvider clientId={CLIENT_ID}>
      <BrowserRouter>
        <Layout />
      </BrowserRouter>
    </GoogleOAuthProvider>
        
  );
}

export default RoutesApp;
