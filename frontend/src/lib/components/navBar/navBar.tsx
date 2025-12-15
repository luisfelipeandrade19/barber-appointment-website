import { Link } from "react-router-dom";
import  homebtn  from "../../../assets/botao-home.png"
import  appointmentbtn  from "../../../assets/calendar.png"
import  profilebtn  from "../../../assets/do-utilizador.png"

import  "./navBar.css"

function NavBar(){

    return(
        <>
        <div className="navBar-container">
            <nav>
                <Link to="/home"><img id="imgs-nav" className="home-btn" 
                src={homebtn} alt="Botao home" /></Link>

                <Link to="/agendamentos"><img id="imgs-nav" className="appointment-btn" 
                src={appointmentbtn} alt="Botao agendamentos" /></Link>

                <Link to="/perfil"><img id="imgs-nav" className="profile-btn" 
                src={profilebtn} alt="Botao perfil" /></Link>
            </nav>
        </div>
        </>
    )
}

export default NavBar;