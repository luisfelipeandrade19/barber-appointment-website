import { useState } from 'react';

interface LoginButtonProps {
    onClick: () => Promise<void>;
}

const LoginButton = ({ onClick }: LoginButtonProps) => {
    const [loading, setLoading] = useState(false);

    const handleButtonClick = async () => {
        setLoading(true);

        try {
            await onClick();
        } catch (error) {
            console.error("Erro capturado pelo botao", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <button
            id="loginButton"
            onClick={handleButtonClick}
            disabled={loading}
            style={{ cursor: loading ? 'wait' : 'pointer', color: 'white' }}
        >
            {loading ? 'Entrando...' : 'Login'}
        </button>
    );
};

export default LoginButton;