
import GoogleLoginButton from "../../lib/components/googleLoginButton";
import FacebookLoginButton from "../../lib/components/FacebookLoginButton";
import profile from "../../assets/foto-do-perfil.png"
import "./loginPage.css"

function LoginPage(){

  
    return(
    <>
      <div className="login-container">
        <img className="profile-img" src={profile} width={180}/>
        <form action="get">
            <div className="inputs">
              <p className="input-label">Email</p>
              <input type="email" id="inputUsername" placeholder="Digite seu email"/>
              <p className="input-label">Senha</p>
              <input type="password" id="inputPassword" placeholder="******" />
              <button id="loginButton">Login</button>
            </div>
            <div className="socials">
              <h2 id="titleSocialLogin">Logar com</h2>
              <div className="socialLogin">
                <GoogleLoginButton/>
                <FacebookLoginButton/>
              </div>
              <footer>
                <p>Não tem conta ainda?</p>
                <p onClick={() =>{
                  window.location.href = "/register"}} 
                  style={{ cursor: 'pointer', color: 'blue'}}
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