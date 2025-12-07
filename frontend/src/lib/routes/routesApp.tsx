
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "../../screens/login/loginPage";
import RegisterPage from "../../screens/registro/registerPage";
import Home from "../../screens/home/home";
import NavBar from "../components/navBar";


function RoutesApp() {

  return (
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/home" element={<Home/>}/>
          </Routes>
          <NavBar/>
        </BrowserRouter>
  );
}

export default RoutesApp;
