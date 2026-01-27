import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./cadastrarBarbeiro.css";

function CadastrarBarbeiro() {
    const navigate = useNavigate();
    const [nome, setNome] = useState("");
    const [telefone, setTelefone] = useState("");
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");

    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        const token = localStorage.getItem('accessToken');
        if (!token) return;

        setLoading(true);
        try {
            const response = await fetch('/api/admin/barbeiros', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    nome,
                    email,
                    telefone,
                    senha,
                    especialidade: "Geral"
                })
            });

            if (response.ok) {
                alert("Barbeiro cadastrado com sucesso!");
                navigate('/perfil');
            } else {
                const errorData = await response.json();
                console.error("Erro detalhado:", errorData);
                const errorMessage = Array.isArray(errorData.detail)
                    ? errorData.detail.map((err: any) => `${err.loc.join('.')} - ${err.msg}`).join('\n')
                    : errorData.detail || "Falha ao cadastrar";
                alert(`Erro:\n${errorMessage}`);
            }
        } catch (error) {
            console.error("Erro ao cadastrar:", error);
            alert("Erro de conexão");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="cadastrar-container">
            <header className="cadastrar-header">
                <button className="back-btn" onClick={() => navigate('/perfil')}>&lt;</button>
                <h1>Cadastrar Barbeiro</h1>
            </header>

            <div className="form-group-cadastrar">
                <div className="input-group">
                    <label htmlFor="nome">Nome:</label>
                    <input
                        type="text"
                        className="input-field"
                        id="nome"
                        value={nome}
                        onChange={(e) => setNome(e.target.value)}
                    />
                </div>

                <div className="input-group">
                    <label htmlFor="telefone">Telefone:</label>
                    <input
                        type="text"
                        className="input-field"
                        id="telefone"
                        value={telefone}
                        onChange={(e) => setTelefone(e.target.value)}
                    />
                </div>

                <div className="input-group">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        className="input-field"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div className="input-group">
                    <label htmlFor="senha">Senha:</label>
                    <input
                        type="password"
                        className="input-field"
                        id="senha"
                        value={senha}
                        onChange={(e) => setSenha(e.target.value)}
                    />
                </div>

                <div className="input-group">
                    <label>Serviços Padrão (Adicionados automaticamente):</label>
                    <ul className="default-services-list">
                        <li>Corte de Cabelo (R$30,00)</li>
                        <li>Barba (R$20,00)</li>
                        <li>Barba + Cabelo (R$45,00)</li>
                    </ul>
                </div>

                <div className="button-app">
                    <button className="cadastrar-btn" onClick={handleSubmit} disabled={loading}>
                        {loading ? "CADASTRANDO..." : "CADASTRAR"}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default CadastrarBarbeiro;