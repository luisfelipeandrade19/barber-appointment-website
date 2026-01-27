import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./editProfile.css";

function EditProfile() {
    const navigate = useNavigate();
    const [nome, setNome] = useState("");
    const [telefone, setTelefone] = useState("");
    const [loading, setLoading] = useState(false);

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
                    setNome(data.nome);
                    setTelefone(data.telefone || "");
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

    const handleSave = async () => {
        const token = localStorage.getItem('accessToken');
        if (!token) return;

        setLoading(true);
        try {
            const response = await fetch('/api/perfil', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ nome, telefone })
            });

            if (response.ok) {
                navigate('/perfil');
            } else {
                alert("Erro ao atualizar perfil.");
            }
        } catch (error) {
            console.error("Error updating profile:", error);
            alert("Erro ao conectar ao servidor.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="editar-container">
            <header className="editar-header">
                <button className="back-btn" onClick={() => navigate('/perfil')}>&lt;</button>
                <h1>Editar Perfil</h1>
            </header>

            <div className="form-group-edit">
                <div className="name-form-group">
                    <label htmlFor="nome">Nome:</label>
                    <input
                        type="text"
                        className="input-field"
                        id="nome"
                        value={nome}
                        onChange={(e) => setNome(e.target.value)}
                    />
                </div>

                <div className="telefone-form-group">
                    <label htmlFor="telefone">Telefone:</label>
                    <input
                        type="text"
                        className="input-field"
                        id="telefone"
                        value={telefone}
                        onChange={(e) => setTelefone(e.target.value)}
                    />
                </div>

                <div className="button-app">
                    <button className="edit-page-btn" id="btn-edit" onClick={handleSave} disabled={loading}>
                        {loading ? "SALVANDO..." : "SALVAR"}
                    </button>
                </div>
            </div>
        </div>
    );
}
export default EditProfile;