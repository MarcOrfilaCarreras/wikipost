import { useState, useEffect } from 'react';

import { API_ACCOUNT_SETTINGS } from '../../../assets/consts';

import App from '../../../layouts/app';

import TextInput from '../../../components/inputs/text';
import TextAreaInput from '../../../components/inputs/text-area';
import CronJobGenerator from '../../../components/inputs/cron';
import Form from '../../../components/form';
import PrimaryButton from '../../../components/buttons/primary';
import Popup from '../../../components/popup';

import SpinnerIcon from '../../../assets/icons/spinner';

const ProfileSettingsAppPage = () => {
    const [aiPrompt, setAiPrompt] = useState("");
    const [instagramUsername, setInstagramUsername] = useState("");
    const [instagramPassword, setInstagramPassword] = useState("");
    const [instagramEmail, setInstagramEmail] = useState("");
    const [instagramEmailPassword, setInstagramEmailPassword] = useState("");
    const [cronJob, setCronJob] = useState('* * * * *');

    const [showLoading, setShowLoading] = useState(false);
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    const fetchData = async () => {
        const token = localStorage.getItem('token');

        try {
            const response = await fetch(API_ACCOUNT_SETTINGS, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
            });

            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }

            const { data } = await response.json();

            setAiPrompt(data?.ai_prompt || "");
            setInstagramUsername(data?.instagram_username || "");
            setInstagramPassword(data?.instagram_password || "");
            setInstagramEmail(data?.instagram_email || "");
            setInstagramEmailPassword(data?.instagram_email_password || "");
            setCronJob(data?.scheduler_interval || '* * * * *');
        } catch (error) {
            setErrorMessage("There was a problem retrieving your settings");
            setError(true);
            return;
        }

        setErrorMessage("");
        setError(false);
    };

    const handleAiPromptChange = (e) => setAiPrompt(e.target.value);
    const handleInstagramUsernameChange = (e) => setInstagramUsername(e.target.value);
    const handleInstagramPasswordChange = (e) => setInstagramPassword(e.target.value);
    const handleInstagramEmailChange = (e) => setInstagramEmail(e.target.value);
    const handleInstagramEmailPasswordChange = (e) => setInstagramEmailPassword(e.target.value);

    const handleCronJobGenerated = (generatedCron) => {
        setCronJob(generatedCron);
    };

    const handleSaveChange = async (e) => {
        const token = localStorage.getItem('token');

        e.preventDefault();
        setShowLoading(true);

        try {
            const response = await fetch(API_ACCOUNT_SETTINGS, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
                body: JSON.stringify({ 'ai_prompt': aiPrompt, 'instagram_username': instagramUsername, 'instagram_password': instagramPassword, 'instagram_email': instagramEmail, 'instagram_email_password': instagramEmailPassword, 'scheduler_interval': cronJob }),
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
        } catch (error) {
            setErrorMessage("There was a problem saving your settings");
            setError(true);
            setShowLoading(false);
            return;
        }

        setErrorMessage("");
        setError(false);
        setShowLoading(false);

        fetchData();
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <App>
            <h1 className="text-white text-2xl font-bold mb-8">Profile</h1>
            <div className="w-full mx-auto flex flex-col gap-8 overflow-hidden max-h-screen ">
                <div className="w-full flex flex-col gap-8 overflow-y-auto max-h-[85vh] scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                    <Form title="Settings" subtitle="Configure your account" className="w-full h-full">
                        <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4'>
                            <TextInput
                                id="instagram-username"
                                label="Instagram Username"
                                placeholder="MrBeast@2024"
                                value={instagramUsername}
                                onChange={handleInstagramUsernameChange}
                                error={error}
                                errorMessage={errorMessage}
                            />
                            <TextInput
                                id="instagram-password"
                                type="password"
                                label="Instagram Password"
                                placeholder="mRbE4sT@20O4"
                                value={instagramPassword}
                                onChange={handleInstagramPasswordChange}
                                error={error}
                                errorMessage={errorMessage}
                            />
                            <div>
                                <TextInput
                                    id="instagram-email"
                                    label="Instagram Email"
                                    placeholder="mrbeast@gmail.com"
                                    value={instagramEmail}
                                    onChange={handleInstagramEmailChange}
                                    error={error}
                                    errorMessage={errorMessage}
                                />
                                <p className="text-yellow-400 text-xs pt-2">Only Gmail accounts work right now.</p>
                            </div>
                            <TextInput
                                id="instagram-email-password"
                                type="password"
                                label="Instagram Email Password"
                                placeholder="mRbE4sT@20O4"
                                value={instagramEmailPassword}
                                onChange={handleInstagramEmailPasswordChange}
                                error={error}
                                errorMessage={errorMessage}
                            />
                        </div>
                        <CronJobGenerator
                            label="Scheduler"
                            defaultCronExpression={cronJob}
                            onCronJobGenerated={handleCronJobGenerated} />
                        <TextAreaInput
                            id="ai-prompt"
                            label="AI Prompt"
                            value={aiPrompt}
                            onChange={handleAiPromptChange}
                            placeholder="https://wikipedia.org/wiki"
                        />

                        {error && <p className="text-sm text-red-500 text-center">{errorMessage}</p>}
                        <div className="flex flex-row gap-4">
                            <div className="w-full" />
                            <div>
                                <PrimaryButton text="Save" onClick={handleSaveChange} />
                            </div>
                        </div>
                    </Form>
                </div>
            </div>

            {showLoading && (
                <Popup>
                    <SpinnerIcon />
                </Popup>
            )}

        </App>
    );
};

export default ProfileSettingsAppPage;
