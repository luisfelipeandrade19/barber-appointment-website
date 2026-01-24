import { useState } from "react";
import "./profilePage.css";
import profileIcon from "../../assets/do-utilizador.png"; // Using existing profile icon as avatar placeholder
import historyIcon from "../../assets/calendar.png"; // Reusing calendar icon for history
// You might need a specific icon for "history clock", checking available assets later or using SVG

function ProfilePage() {
    const [showHistory, setShowHistory] = useState(false);

    // Mock Data for History - replicating what was in HistoryPage
    const historyData = [
        {
            id: 1,
            barberName: "Felipe",
            date: "12/12/2025",
            services: "Barba e cabelo",
        },
        {
            id: 2,
            barberName: "João",
            date: "13/12/2025",
            services: "Corte Social",
        },
        {
            id: 3,
            barberName: "Alisson",
            date: "12/12/2025",
            services: "Barba e cabelo",
        }
    ];

    return (
        <div className="profile-container">
            <header className="profile-header">
                <div className="profile-avatar-container">
                    <img src={profileIcon} alt="User Avatar" className="auth-icon" />
                </div>
                <div className="profile-info">
                    <h2>Nome do usuário</h2>
                    <a href="#" className="edit-link">Editar perfil &gt;</a>
                </div>
            </header>

            <div className="details-box">
                <div className="detail-item">
                    <label>CPF</label>
                    <span>000000000-00</span>
                </div>
                <div className="detail-item">
                    <label>Endereço</label>
                    <span>rua dos Tabajaras, 123</span>
                </div>
                <div className="detail-item">
                    <label>Telefone</label>
                    <span>(00)00000-0000</span>
                </div>
            </div>

            <div className="menu-options">
                <div className="menu-item" onClick={() => setShowHistory(true)}>
                    {/* Using an SVG for the history clock icon similar to the mockup */}
                    <svg className="menu-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M12 20a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"></path>
                        <path d="M12 6v6l4 2"></path>
                    </svg>
                    <span>Histórico</span>
                </div>

                {/* 
                <div className="menu-item">
                     <span>Cancelar agenda</span>
                </div>
                <div className="menu-item">
                     <span>Ajuda</span>
                </div> 
                */}
            </div>

            {showHistory && (
                <div className="modal-overlay" onClick={() => setShowHistory(false)}>
                    <div className="modal-content history-modal-content" onClick={e => e.stopPropagation()}>
                        <button className="close-modal-btn" onClick={() => setShowHistory(false)}>&times;</button>
                        <h2 className="history-title">Histórico de Agendamento</h2>
                        <ul className="history-list">
                            {historyData.map(item => (
                                <li key={item.id} className="history-item">
                                    <p><span>Barbeiro:</span> {item.barberName}</p>
                                    <p><span>Data:</span> {item.date}</p>
                                    <p><span>Serviços:</span> {item.services}</p>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ProfilePage;