import "./profilePage.css";
import avatarImg from "../../assets/foto-do-perfil.png";

function ProfilePage() {
    return (
        <div className="profile-container">
            <header className="profile-header">
                <div className="avatar-container">
                    <img src={avatarImg} alt="Foto de perfil" className="avatar-img" />
                </div>
                <div className="profile-info">
                    <h2>Nome do usuário</h2>
                    <a href="#" className="edit-link">Editar perfil &gt;</a>
                </div>
            </header>

            <section className="info-section">
                <div className="info-item">
                    <p className="info-label">CPF</p>
                    <p className="info-value">000000000-00</p>
                </div>
                <div className="info-item">
                    <p className="info-label">Endereço</p>
                    <p className="info-value">rua dos Tabajaras, 123</p>
                </div>
                <div className="info-item">
                    <p className="info-label">Telefone</p>
                    <p className="info-value">(00)00000-0000</p>
                </div>
            </section>

            <section className="actions-section">
                <div className="action-item">
                    <div className="action-icon">
                        <svg className="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                    </div>
                    <span>Histórico</span>
                </div>

                <div className="action-item">
                    <div className="action-icon">
                        {/* Cancel Icon (Document with X) */}
                        <svg className="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                           <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                           <polyline points="14 2 14 8 20 8"></polyline>
                           <line x1="9" y1="15" x2="15" y2="15"></line>
                           <line x1="10" y1="18" x2="14" y2="12"></line> 
                        </svg>
                    </div>
                    <span>Cancelar agenda</span>
                </div>

                <div className="action-item">
                    <div className="action-icon">
                        {/* Help Icon (Question Mark) */}
                        <svg className="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                            <line x1="12" y1="17" x2="12.01" y2="17"></line>
                        </svg>
                    </div>
                    <span>Ajuda</span>
                </div>
            </section>
        </div>
    );
}

export default ProfilePage;