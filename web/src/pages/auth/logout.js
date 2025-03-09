import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutAuthPage = () => {
    const navigate = useNavigate();

    useEffect(() => {
        localStorage.removeItem('token');
        navigate('/auth/login?notify=You%20have%20successfully%20logged%20out!&notify-type=success');
    }, [navigate]);

    return null;
};

export default LogoutAuthPage;
