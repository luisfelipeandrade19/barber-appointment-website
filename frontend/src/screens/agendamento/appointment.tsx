import logoImg from "../../assets/logoSite.png"
import exemplo from "../../assets/foto-do-perfil.png"
import "./appointment.css"
import { Link } from "react-router-dom"
import { useState } from "react"

function Appointment() {

    const [appointments, setAppointments] = useState([
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

    ])

    const [cancelId, setCancelId] = useState<number | null>(null);

    const handleDelete = () => {
        if (cancelId !== null) {
            setAppointments(appointments.filter(app => app.id !== cancelId));
            setCancelId(null);
        }
    };

    const closeModal = () => {
        setCancelId(null);
    };

    return (
        <>
            <div className="appointment-container">
                <header className="header">
                    <img className="img-logo" src={logoImg} alt="logo site" />
                </header>
                <div className="appointment-content-main">
                    <Link to="/agendar"><button className="appointment-page-btn"  >AGENDAR AGORA</button></Link>
                    <div className="appoiments">
                        <h1 className="title-appointments">Meus Agendamentos:</h1>
                        <ol id="appoiments-list">
                            {appointments.map((item) => (
                                <li className="item-list" key={item.id}>
                                    <div className={`div-list ${item.barberName}`}>
                                        <button className="delete-btn" onClick={() => setCancelId(item.id)}>
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                                <line x1="6" y1="6" x2="18" y2="18"></line>
                                            </svg>
                                        </button>
                                        <img id="img-list" src={item.image} alt="logo site" width={120} />
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

                {cancelId !== null && (
                    <div className="modal-overlay">
                        <div className="modal-content">
                            <h2>Deseja mesmo cancelar?</h2>
                            <div className="modal-actions">
                                <button className="modal-btn confirm" onClick={handleDelete}>Sim</button>
                                <button className="modal-btn cancel" onClick={closeModal}>Não</button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    )
}

export default Appointment