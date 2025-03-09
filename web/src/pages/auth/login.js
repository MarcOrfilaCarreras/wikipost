import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Centered from '../../layouts/centered';
import Background from "../../components/background";
import Form from '../../components/form';
import PrimaryButton from '../../components/buttons/primary';
import TextInput from '../../components/inputs/text';

import { API_AUTH_LOGIN_URL, API_AUTH_CHECK_URL } from '../../assets/consts';
import { validateEmail, validatePassword } from '../../utils/validation';

const LoginAuthPage = () => {
    const [email, setEmail] = useState('');
    const [emailError, setEmailError] = useState(false);
    const [emailErrorMessage, setEmailErrorMessage] = useState('');

    const [password, setPassword] = useState('');
    const [passwordError, setPasswordError] = useState(false);
    const [passwordErrorMessage, setPasswordErrorMessage] = useState('');

    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    const navigate = useNavigate();

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
        setEmailError(false);
        setEmailErrorMessage('');
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
        setPasswordError(false);
        setPasswordErrorMessage('');
    };

    const handleSubmitClick = async (event) => {
        event.preventDefault();

        setError(false);
        setErrorMessage('');

        if (!validateEmail(email)) {
            setEmailError(true);
            setEmailErrorMessage('Please enter a valid email.');
            return;
        }

        if (!validatePassword(password)) {
            setPasswordError(true);
            setPasswordErrorMessage('Please enter a valid password.');
            return;
        }

        try {
            const response = await fetch(API_AUTH_LOGIN_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.message);
            }

            const data = await response.json();
            localStorage.setItem('token', data.data.token);
            navigate('/app/dashboard/overview?notify=Welcome%20back!&notify-type=information');
        } catch (error) {
            setError(true);
            setErrorMessage(error.message);
        }
    };

    useEffect(() => {
        const verifyToken = async () => {
            const token = localStorage.getItem('token');

            if (token === null || token === undefined) {
                return;
            }

            try {
                const response = await fetch(API_AUTH_CHECK_URL, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
                });

                if (!response.ok) {
                    throw new Error('Token verification failed');
                }

                navigate('/app/dashboard/overview');
            } catch (error) {
                localStorage.removeItem('token');
            }
        };

        verifyToken()
    }, [navigate]);

    return (
        <Centered className="bg-gray-950">
            <Background />
            <Form
                title="Welcome back"
                subtitle="Please sign in to continue to the Dashboard"
                className="max-w-[500px] w-full"
            >
                <TextInput
                    id="email"
                    label="Email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={handleEmailChange}
                    error={emailError}
                    errorMessage={emailErrorMessage}
                />
                <TextInput
                    id="password"
                    type="password"
                    label="Password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={handlePasswordChange}
                    error={passwordError}
                    errorMessage={passwordErrorMessage}
                />
                <PrimaryButton text="Login" onClick={handleSubmitClick} />
                {error && (
                    <p className="text-sm text-red-500 text-center">{errorMessage}</p>
                )}

                <div className="mt-4 text-center">
                    <span className="text-sm text-gray-300">Don't have an account? </span>
                    <a href="/auth/register" className="text-sm text-blue-500 hover:underline">
                        Register
                    </a>
                </div>
            </Form>
        </Centered>
    );
};

export default LoginAuthPage;
