import person from "../../assets/ft.jpg"
import GoogleLoginButton from "../../lib/components/googleLoginButton";
import FacebookLoginButton from "../../lib/components/FacebookLoginButton";

function LoginPage(){

  
    return(
    <>
      <div className="container">
        <img id="userImage" src={person} width={180}/>

        <form action="get">
            <h2 id="userTitle">Usuário</h2>
            <div className="inputs">
              <input type="email" id="inputUsername" placeholder="Digite seu email"/>
              <input type="password" id="inputPassword" placeholder="******" />
              <button id="loginButton">LOGIN</button>
            </div>
            <div className="socialLogin">
              <h2 id="titleSocialLogin">Logar com</h2>
              <GoogleLoginButton/>
              <FacebookLoginButton/>
            </div>
            <footer>
              <p>Não tem conta ainda?</p>
              <p onClick={() =>{
                window.location.href = "/register"}} 
                style={{ cursor: 'pointer', color: 'blue'}}
                >Cadastrar-se</p>
                
            </footer>
        </form>
      </div>
    </>
)
}



export default LoginPage;