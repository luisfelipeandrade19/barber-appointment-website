import FacebookLogin from '@greatsumini/react-facebook-login';
import facebook from "../../../assets/facebook.png"

const FacebookLoginButton = () => {
  const appId = import.meta.env.VITE_FACEBOOK_APP_ID;

  return (
    <FacebookLogin
      appId={appId}
      onSuccess={(response) => {
        console.log('Login Success!', response);
      }}
      onFail={(error) => {
        console.log('Login Failed!', error);
      }}
      onProfileSuccess={(response) => {
        console.log('Get Profile Success!', response);
      }}
      style={{
        backgroundColor: '#ffffffff',
        width: 50,
        height: 50,
        borderRadius: 100,
        borderStyle: 'none'
      }}
    >
      <img src={facebook} id='imgFacebook' style={{
        width: 50,
        height: 50,
        cursor: 'pointer',
        padding: 5,
        display: 'flex'
      }} />
    </FacebookLogin>
  );

};

export default FacebookLoginButton;
