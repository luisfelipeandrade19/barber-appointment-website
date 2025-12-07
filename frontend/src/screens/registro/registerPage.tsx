import person from "../../assets/ft.jpg";
import GoogleLoginButton from "../../lib/components/googleLoginButton";
import FacebookLoginButton from "../../lib/components/FacebookLoginButton";

function RegisterPage() {
  return (
    <>
      <div className="container">
        {/* Adicionado o / no final */}
        <img id="userImage" src={person} width={180} alt="User" />

        <form action="get">
          <h2 className="userTitle">Nome de usuário</h2>
          <input type="text" id="userNamer" placeholder="Digite seu nome" />

          <h2 className="userTitle">Email</h2>
          <input type="email" id="inputUsername" placeholder="Digite seu email" />

          <h2 className="userTitle">Senha</h2>
          <input type="password" id="inputPassword" placeholder="******" />

          <h2 className="userTitle">Confirmar Senha</h2>
          {/* Corrigido: password e fechamento /> */}
          <input type="password" id="confirmPassword" placeholder="******" />

          <button id="registerButton" type="submit">REGISTRAR</button>

          {/* O form agora engloba tudo que pertence a ele */}
          <div className="socialLogin">
            <h2 id="titleSocialLogin">Cadastrar com</h2>
            <GoogleLoginButton />
            <FacebookLoginButton />
          </div>

          <footer>
            <p>Já tem uma conta?</p>
            <p 
              onClick={() => { window.location.href = "/login" }} 
              style={{ cursor: 'pointer', color: 'blue' }}
            >
              Fazer Login
            </p>
          </footer>
        </form> {/* O form fecha por último */}
      </div>
    </>
  );
}

export default RegisterPage;