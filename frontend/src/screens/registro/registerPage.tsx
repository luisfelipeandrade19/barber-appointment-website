import person from "../../assets/ft.jpg";
import GoogleLoginButton from "../../lib/components/googleLoginButton";
import FacebookLoginButton from "../../lib/components/FacebookLoginButton";
import "./registerPage.css";

function RegisterPage() {
  return (
    <>

           
       
      <div className="container">

        <header>
            <h1>
                Criar conta
            </h1>
        </header>
        
        <form action="get">
          <h2 className="userTitle">Nome de usuário</h2>
          <input type="text" id="userNamer" placeholder="Digite seu nome" />

          <h2 className="userTitle">Email</h2>
          <input type="email" id="inputUsername" placeholder="Digite seu email" />

          <h2 className="userTitle">Senha</h2>
          <input type="password" id="inputPassword" placeholder="******" />

          <h2 className="userTitle">Confirmar Senha</h2>
          <input type="password" id="confirmPassword" placeholder="******" />

          <button id="registerButton" type="submit">
            REGISTRAR
          </button>

          {/* Seção de Login Social */}
          <div className="socialLogin">
            <h2 id="titleSocialLogin">Cadastrar com</h2>
            <GoogleLoginButton />
            <FacebookLoginButton />
          </div>

          {/* Rodapé com link para login */}
          <footer>
            <p>Já tem uma conta?</p>
            <p 
              onClick={() => { window.location.href = "/login" }} 
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