
import GoogleLoginButton from "../../lib/components/googleButton/googleLoginButton";
import FacebookLoginButton from "../../lib/components/facebookButton/FacebookLoginButton";
import profile from "../../assets/foto-do-perfil.png"
import "./loginPage.css"
import { useNavigate } from 'react-router-dom';
import { useState } from "react";
import LoginButton from "../../lib/components/loginButton/loginButton";

function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")





  const handleLogin = async () => {
    try {

      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, senha: senha }),
      });

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || "Erro ao fazer login")
      }

      localStorage.setItem('accessToken', data.access_token);

      localStorage.setItem('refreshToken', data.refreshToken);

      localStorage.setItem('usuario', JSON.stringify(data.usuario));

      console.log("Login realizado com sucesso!");
      navigate('/home');

    } catch (error) {

      alert("Falha no login. Verifique suas credenciais.");
      console.error(error);
    } finally {
    }
  }


  return (
    <>
      <div className="login-container">
        <img className="profile-img" src={profile} width={180} />
        <form action="get">
          <div className="inputs">
            <p className="input-label">Email</p>
            <input type="email" id="inputUsername" placeholder="Digite seu email" onChange={(e) => setEmail(e.target.value)} />
            <p className="input-label">Senha</p>
            <input type="password" id="inputPassword" placeholder="******" onChange={(e) => setSenha(e.target.value)} />
            <LoginButton onClick={handleLogin} />
          </div>
          <div className="socials">
            <h2 id="titleSocialLogin">Logar com</h2>
            <div className="socialLogin">
              <GoogleLoginButton />
              <FacebookLoginButton />
            </div>
            <footer>
              <p>Não tem conta ainda?</p>
              <p onClick={() => {
                window.location.href = "/register"
              }}
                style={{ cursor: 'pointer', color: 'blue' }}
              >Cadastrar-se
              </p>
            </footer>
          </div>
        </form>
      </div>
    </>
  )
}



export default LoginPage;