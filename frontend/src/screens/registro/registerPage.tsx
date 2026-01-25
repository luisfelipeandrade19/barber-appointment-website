import GoogleLoginButton from "../../lib/components/googleButton/googleLoginButton";
import FacebookLoginButton from "../../lib/components/facebookButton/FacebookLoginButton";
import "./registerPage.css";

function RegisterPage() {
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