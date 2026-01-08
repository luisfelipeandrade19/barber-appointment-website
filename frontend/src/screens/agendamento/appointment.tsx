import logoImg from "../../assets/logoSite.png"
import exemplo from "../../assets/foto-do-perfil.png"
import "./appointment.css"
import { Link } from "react-router-dom"

function Appointment(){

    const listAppointments = [
        {
            id: 1,
            barberName: "Felipe",
            contact: "(88) 99999-1111",
            date: "12/12/2025",
            time: "14:30h",
            services: "Barba e cabelo",
            image: exemplo 
         }
        ,
        {
            id: 2,
            barberName: "João",
            contact: "(88) 99999-2222",
            date: "13/12/2025",
            time: "09:00h",
            services: "Corte Social",
            image: exemplo
        },
        {
            id: 3,
            barberName: "Carlos",
            contact: "(88) 99999-3333",
            date: "13/12/2025",
            time: "10:00h",
            services: "Barba",
            image: exemplo
        },
        {
            id: 4,
            barberName: "Carlos",
            contact: "(88) 99999-3333",
            date: "13/12/2025",
            time: "10:00h",
            services: "Barba",
            image: exemplo
        },
        {
            id: 5,
            barberName: "Carlos",
            contact: "(88) 99999-3333",
            date: "13/12/2025",
            time: "10:00h",
            services: "Barba",
            image: exemplo
        },
        {
            id: 6,
            barberName: "Carlos",
            contact: "(88) 99999-3333",
            date: "13/12/2025",
            time: "10:00h",
            services: "Barba",
            image: exemplo
        }

    ]
    
    return(
        <>
        <div className="appointment-container">
            <header className="appointment-header">
                <img className="img-logo" src={logoImg} alt="logo site" />
            </header>
            <div className="appointment-content-main">
                <Link to="/agendar"><button className="appointment-page-btn"  >AGENDAR AGORA</button></Link>
                <div className="appoiments">
                    <h1 className="title-appointments">Meus Agendamentos:</h1>
                    <ol id="appoiments-list">
                       {listAppointments.map((item)=>(
                        <li className="item-list">
                            <div className={`div-list ${item.barberName}`}>
                                <img id="img-list" src={item.image} alt="logo site" width={120}/>
                                <div className="appointment-info">
                                    <p className="name">
                                        <span>Barbeiro:</span> {item.barberName}
                                    </p>
                                    <p className="contact">
                                        <span>Contato:</span> {item.contact}
                                    </p>
                                    <p className="date">
                                        <span>Data:</span> {item.date}
                                    </p>
                                    <p className="time">
                                        <span>Horário:</span> {item.time}
                                    </p>
                                    <p className="services">
                                        <span>Serviços:</span> {item.services}
                                    </p>
                                </div>
                            </div>
                        </li>
                       ))}
                    </ol>
                </div>
            </div>
        </div>
        </>
    )
}

export default Appointment