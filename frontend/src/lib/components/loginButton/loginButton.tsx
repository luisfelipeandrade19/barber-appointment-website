import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginButton = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const handleLogin = async () => {
        setLoading(true);

        try {
            await new Promise(resolve => setTimeout(resolve, 1000));

            console.log("Login realizado com sucesso!");
            navigate('/home');

        } catch (error) {
            alert("Falha no login. Verifique suas credenciais.");
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <button
            id="loginButton"
            onClick={handleLogin}
            disabled={loading}
            style={{ cursor: loading ? 'wait' : 'pointer', color: 'white' }}
        >
            {loading ? 'Entrando...' : 'Login'}
        </button>
    );
};

export default LoginButton;