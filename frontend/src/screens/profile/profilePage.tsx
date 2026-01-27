import "./profilePage.css";
import avatarImg from "../../assets/foto-do-perfil.png";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

interface UserProfile {
    nome: string;
    email: string;
    telefone: string;
    tipo: string;
    data_cadastro?: string;
    preferencias?: string;
}

function ProfilePage() {
    const [user, setUser] = useState<UserProfile | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            const token = localStorage.getItem('accessToken');
            if (!token) {
                navigate('/');
                return;
            }

            try {
                const response = await fetch('/api/perfil', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    setUser(data);
                } else if (response.status === 401) {
                    localStorage.removeItem('accessToken');
                    navigate('/');
                }
            } catch (error) {
                console.error("Error fetching profile:", error);
            }
        };

        fetchProfile();
    }, [navigate]);

    if (!user) {
        return <div className="profile-container"><p>Carregando...</p></div>;
    }

    const formatDate = (dateString?: string) => {
        if (!dateString) return "";
        return new Date(dateString).toLocaleDateString('pt-BR');
    };

    return (
        <div className="profile-container">
            <header className="profile-header">
                <div className="avatar-container">
                    <img src={avatarImg} alt="Foto de perfil" className="avatar-img" />
                </div>
                <div className="profile-info">
                    <h2>{user.nome}</h2>
                    <a href="#" className="edit-link">Editar perfil &gt;</a>
                </div>
            </header>

            <section className="info-section">
                <div className="info-item">
                    <p className="info-label">Email</p>
                    <p className="info-value">{user.email}</p>
                </div>
                <div className="info-item">
                    <p className="info-label">Tipo</p>
                    <p className="info-value">{user.tipo}</p>
                </div>
                <div className="info-item">
                    <p className="info-label">Telefone</p>
                    <p className="info-value">{user.telefone || "Não informado"}</p>
                </div>
                
                
            </section>

            <section className="actions-section">
                <div className="action-item" onClick={() => navigate('/historico')} style={{ cursor: 'pointer' }}>
                    <div className="action-icon">
                        <svg className="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                    </div>
                    <span>Histórico</span>
                </div>

                <div className="action-item" onClick={() => navigate('/agendamentos')} style={{ cursor: 'pointer' }}>
                    <div className="action-icon">
                        <svg className="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="9" y1="15" x2="15" y2="15"></line>
                            <line x1="10" y1="18" x2="14" y2="12"></line>
                        </svg>
                    </div>
                    <span>Cancelar agenda</span>
                </div>

        
            </section>
        </div>
    );
}

export default ProfilePage;