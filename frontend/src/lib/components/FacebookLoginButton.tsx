import FacebookLogin from '@greatsumini/react-facebook-login';

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
        backgroundColor: '#4267b2',
        color: '#fff',
        fontSize: '16px',
        padding: '12px 24px',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer'
      }}
    >
      Login via Facebook
    </FacebookLogin>
  );

};

export default FacebookLoginButton;
