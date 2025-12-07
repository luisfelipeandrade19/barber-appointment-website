import { useGoogleLogin } from '@react-oauth/google'
import googleButton from '../../assets/google.png'

function GoogleLoginButton(){

    const login = useGoogleLogin({
        onSuccess: tokenResponse => console.log(tokenResponse),
        onError: error => console.log('Login Failed:', error)
    })

    return(
        <>
        <button onClick={() => login()}
            
        style={{
        backgroundColor: '#ffffffff',
        width: 50,
        height: 50,
        borderRadius: 100,
        borderStyle: 'none'
        }}>
          <img src={googleButton}
          style={
            {
               width: 50,
                height: 50,
                cursor: 'pointer',
                padding: 5
            }
          }
          />
        </button>
        </>
    )
}

export default GoogleLoginButton