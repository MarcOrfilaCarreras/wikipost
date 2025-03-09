import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Centered from "./centered";
import Navbar from '../components/navbar';

import { API_AUTH_CHECK_URL } from '../assets/consts';

const App = ({ children }) => {
    const navigate = useNavigate();

    useEffect(() => {
        const verifyToken = async () => {
            const token = localStorage.getItem('token');

            if (token === null || token === undefined) {
                navigate('/auth/login');
            }

            try {
                const response = await fetch(API_AUTH_CHECK_URL, {
                    method: 'GET',
                    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
                });

                if (!response.ok) {
                    throw new Error('Token verification failed');
                }
            } catch (error) {
                localStorage.removeItem('token');
                navigate('/auth/login');
            }
        };

        verifyToken();
    }, [navigate]);

    return (
        <Centered className="bg-gray-950">
            <main className="w-full h-full flex overflow-hidden">
                <Navbar className="w-64 h-full">
                    <li>
                        Dashboard
                        <ul>
                            <li>
                                <a href="/app/dashboard/overview">
                                    📊 Overview
                                </a>
                            </li>
                        </ul>
                    </li>
                    <li>
                        Wikipedia
                        <ul>
                            <li>
                                <a href="/app/wikipedia/articles">
                                    🔍 Scrape & Manage
                                </a>
                            </li>
                        </ul>
                    </li>
                    <li>
                        Instagram
                        <ul>
                            <li>
                                <a href="/app/instagram/drafts">
                                    📌 Drafts
                                </a>
                            </li>
                            <li>
                                <a href="/app/instagram/scheduled">
                                    🚀 Scheduled Posts
                                </a>
                            </li>
                            <li>
                                <a href="/app/instagram/published">
                                    ✅ Published Posts
                                </a>
                            </li>
                        </ul>
                    </li>
                    <li>
                        Settings
                        <ul>
                            <li>
                                <a href="/app/settings/profile">
                                    👤 User Profile
                                </a>
                            </li>
                        </ul>
                    </li>
                </Navbar>

                <div className="flex-1 overflow-auto mt-8 mb-2 mx-8 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                    {children}
                </div>
            </main>
        </Centered>
    );
};

export default App;
