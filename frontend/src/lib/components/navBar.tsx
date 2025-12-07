import { Link } from "react-router-dom";
function NavBar(){

    return(
        <>
        <div className="navBar-container">
            <nav>
                <Link to="/home">Home</Link>
                <Link to="/agendamentos">Agendamentos</Link>
                <Link to="/perfil">Perfil</Link>
            </nav>
        </div>
        </>
    )
}

export default NavBar;