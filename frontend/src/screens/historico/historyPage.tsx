import voltar from "../../assets/volte.png"
import exemplo from "../../assets/foto-do-perfil.png"
import "./historyPage.css"


interface BarberHistoryItem {
    id: number;
    barberName: string;
    contact: string;
    email?: string;
    date: string;
    time: string;
    services: string;
    image: string;
    status: string;
}

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function HistoryPage() {
    const [listHistory, setListHistory] = useState<BarberHistoryItem[]>([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchHistory = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                navigate('/');
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

                    const mappedData: BarberHistoryItem[] = data.map((item: any) => ({
                        id: item.id,
                        barberName: item.barberName,
                        contact: item.contact,
                        email: "", // Backend doesn't return email yet
                        date: item.date,
                        time: item.time,
                        services: item.services,
                        image: exemplo, // Default image
                        status: item.status
                    }));
                    setListHistory(mappedData);
                } else if (response.status === 401) {
                    localStorage.removeItem('accessToken');
                    navigate('/');
                }
            } catch (error) {
                console.error("Error fetching history:", error);
            }
        };

        fetchHistory();
    }, [navigate]);

    return (
        <>
            <div className="history-container">
                <header className="history-header">
                    <p onClick={() => {
                        window.location.href = "/home"
                    }}
                        style={{ margin: 0, display: 'flex', alignItems: 'center' }}
                    ><img src={voltar} alt="Botao voltar" /></p>
                    <h1>
                        Histórico
                    </h1>
                </header>
                <div className="history-content">
                    <ol id="history-list">
                        {listHistory.length === 0 ? (
                            <li className="empty-message">
                                Você não tem agendamentos
                            </li>
                        ) : (
                            listHistory.map((item, index) => (
                                <li key={index} className="history-item">
                                    <div className="history-item-content">
                                        <div className="history-img-container">
                                            <img src={item.image} alt="Foto do barbeiro" />
                                        </div>
                                        <div className="history-info">
                                            <p className="name">
                                                <span>Nome:</span> {item.barberName}
                                            </p>
                                            <p className="contact">
                                                <span>Contato:</span> {item.contact}
                                            </p>
                                            {item.email && (
                                                <p className="email">
                                                    <span>Email:</span> {item.email}
                                                </p>
                                            )}
                                            <p className="date">
                                                <span>Data:</span> {item.date} - {item.time}
                                            </p>
                                            <p className="services">
                                                <span>Serviços:</span> {item.services}
                                            </p>
                                            <p className="status">
                                                <span>Status:</span> {item.status}
                                            </p>
                                        </div>
                                    </div>
                                </li>
                            ))
                        )}
                    </ol>
                </div>
            </div>
        </>
    )
}

export default HistoryPage