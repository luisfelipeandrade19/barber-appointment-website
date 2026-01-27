import logoImg from "../../assets/logoSite.png"
import exemplo from "../../assets/foto-do-perfil.png"
import "./appointment.css"
import { Link, useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"

function Appointment() {

    const [appointments, setAppointments] = useState<any[]>([])
    const [cancelId, setCancelId] = useState<number | null>(null);
    const navigate = useNavigate();

    const fetchAppointments = async () => {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            console.error("No access token found");
            return;
        }

        try {
            const response = await fetch('/api/agendamentos', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                
                const dataWithImage = data.map((item: any) => ({
                    ...item,
                    image: exemplo 
                })).filter((item: any) => item.status !== 'cancelado' && item.status !== 'recusado');
                setAppointments(dataWithImage);
            } else if (response.status === 401) {
                console.error("Unauthorized. Redirecting to login.");
                localStorage.removeItem('accessToken');
                navigate('/');
            } else {
                console.error("Failed to fetch appointments:", response.status);
            }
        } catch (error) {
            console.error("Error fetching appointments:", error);
        }
    };

    useEffect(() => {
        fetchAppointments();
    }, []);

    const handleDelete = async () => {
        if (cancelId !== null) {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                alert("Você precisa estar logado.");
                return;
            }

            try {
                const response = await fetch(`/api/agendamentos/${cancelId}/status`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ status: 'cancelado' })
                });

                if (response.ok) {
                    setAppointments(appointments.filter(app => app.id !== cancelId));
                } else {
                    alert("Erro ao cancelar agendamento.");
                }
            } catch (error) {
                console.error("Erro ao cancelar:", error);
                alert("Erro ao cancelar agendamento.");
            } finally {
                setCancelId(null);
            }
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