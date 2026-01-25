import GoogleLoginButton from "../../lib/components/googleButton/googleLoginButton";
import FacebookLoginButton from "../../lib/components/facebookButton/FacebookLoginButton";
import "./registerPage.css";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

function RegisterPage() {
  const navigate = useNavigate()
  const [usuario, setUsuario] = useState("")
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")
  const [confSenha, setConfSenha] = useState("")

  const [loading, setLoading] = useState(false)

  const handleRegister = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setLoading(true)

    if (senha !== confSenha) {
      alert("As senhas não coincidem!");
      setLoading(false);
      return;

    }

    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nome: usuario,
          email: email,
          senha: senha,
          confirmar_senha: confSenha
        }),
      })
      // const data = await response.json()

      // if (!response.ok) {
      //   throw new Error(data.detail || "Erro de registro")
      // }

      // --- MUDANÇA AQUI ---
      console.log("Status da resposta:", response.status); // Vai mostrar 200, 404, 500, etc.

      const text = await response.text(); // Lê como texto primeiro
      console.log("Corpo da resposta:", text); // Mostra o que veio (pode ser vazio ou HTML de erro)

      if (!text) {
        throw new Error(`O servidor respondeu com status ${response.status} mas sem conteúdo.`);
      }

      const data = JSON.parse(text); // Tenta converter manualmente
      // --------------------

      if (!response.ok) {
        throw new Error(data.detail || "Erro de registro")
      }

      localStorage.setItem('accessToken', data.access_token);
      localStorage.setItem('refreshToken', data.refresh_token);

      console.log("Registrado com sucesso!");
      navigate('/home');


    } catch (error: any) {

      console.error("DETALHES DO ERRO:", error);
      alert(`Erro ao tentar registrar-se: ${error.message}`)
    } finally {
      setLoading(false);
    }
  }


  return (
    <>
      <div className="register-container">

        <header className="register-header">
          <p className="title-create-account">Criar Conta</p>
          <div className="register-socialLogin">
            <GoogleLoginButton />
            <FacebookLoginButton />
          </div>
          <div className="ou-registre">
            <p>ou</p>
            <p>Registre-se com email</p>
          </div>
        </header>

        <form>
          <h2 className="userTitle">Nome de usuário</h2>
          <input type="text" id="userNamer" placeholder="Digite seu nome" onChange={(e) => setUsuario(e.target.value)} />

          <h2 className="userTitle">Email</h2>
          <input type="email" id="inputUsername" placeholder="Digite seu email" onChange={(e) => setEmail(e.target.value)} />

          <h2 className="userTitle">Senha</h2>
          <input type="password" id="inputPassword" placeholder="******" onChange={(e) => setSenha(e.target.value)} />

          <h2 className="userTitle">Confirmar Senha</h2>
          <input type="password" id="confirmPassword" placeholder="******" onChange={(e) => setConfSenha(e.target.value)} />

          <button id="registerButton" type="submit" onClick={handleRegister}>
            REGISTRAR
          </button>

          <footer className="register-footer">
            <p>Já tem uma conta?</p>
            <p
              onClick={() => { window.location.href = "/" }}
              style={{ cursor: 'pointer', color: 'blue' }}
            >
              Fazer Login
            </p>
          </footer>
        </form>
      </div>
    </>
  );
}

export default RegisterPage;