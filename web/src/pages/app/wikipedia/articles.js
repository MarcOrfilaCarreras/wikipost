import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { API_ACCOUNT_ARTICLES, API_ACCOUNT_ARTICLES_GENERATE } from '../../../assets/consts';

import App from '../../../layouts/app';
import TextInput from '../../../components/inputs/text';
import Form from '../../../components/form';
import PrimaryButton from '../../../components/buttons/primary';
import SecondaryButton from '../../../components/buttons/secondary';
import Table from '../../../components/table';
import Popup from '../../../components/popup';

import SpinnerIcon from '../../../assets/icons/spinner';

const ArticlesAccountAppPage = () => {
    const [showLoading, setShowLoading] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [url, setUrl] = useState('');
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [articles, setArticles] = useState([]);
    const [selectedArticles, setSelectedArticles] = useState([]);

    const columns = ['id', 'title', 'url', 'created_at'];

    const navigate = useNavigate();

    const fetchData = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(API_ACCOUNT_ARTICLES, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
            const { data } = await response.json();
            setArticles(data || []);
        } catch (error) {

        }
    };

    useEffect(() => {
        fetchData();
    }, [navigate]);

    const handleOpenModal = () => setShowModal(true);
    const handleCloseModal = () => {
        setUrl('');
        setShowLoading(false);
        setShowModal(false);
        setError(false);
        setErrorMessage('');
    };

    const handleUrlChange = (e) => setUrl(e.target.value);

    const handleCreateArticle = async (event) => {
        event.preventDefault();
        setShowLoading(true);
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(API_ACCOUNT_ARTICLES, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
                body: JSON.stringify({ url }),
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
            handleCloseModal();
            fetchData();
        } catch (error) {
            setError(true);
            setErrorMessage(error.message);
        } finally {
            setShowLoading(false);
        }
    };

    const handleGenerateArticles = async () => {
        if (selectedArticles.length === 0) return;
        setShowLoading(true);
        try {
            const token = localStorage.getItem('token');
            await Promise.all(
                selectedArticles.map((article) =>
                    fetch(`${API_ACCOUNT_ARTICLES_GENERATE.replace("{{id}}", article.id)}`, {
                        method: 'POST',
                        headers: { Authorization: `Bearer ${token}` }
                    }).then((response) => {
                        if (!response.ok) {
                            return response.json().then(({ message }) => {
                                throw new Error(message);
                            });
                        }
                    })
                )
            );
            navigate("/app/instagram/drafts?notify=Posts%20generated%20correctly&notify-type=success");
        } catch (error) {
            navigate("/app/wikipedia/articles?notify=An%20article%20could't%20be%20generated&notify-type=error");
        } finally {
            setShowLoading(false);
        }
    };

    const handleDeleteArticles = async () => {
        if (selectedArticles.length === 0) return;
        setShowLoading(true);
        try {
            const token = localStorage.getItem('token');
            await Promise.all(
                selectedArticles.map((article) =>
                    fetch(`${API_ACCOUNT_ARTICLES}/${article.id}`, {
                        method: 'DELETE',
                        headers: { Authorization: `Bearer ${token}` },
                    }).then((response) => {
                        if (!response.ok) {
                            return response.json().then(({ message }) => {
                                throw new Error(message);
                            });
                        }
                    })
                )
            );
            fetchData();
        } catch (error) {
            navigate("/app/wikipedia/articles?notify=An%20article%20could't%20be%20deleted&notify-type=error");
        } finally {
            setShowLoading(false);
        }
    };

    const handleRowSelect = (selectedRows) => setSelectedArticles(selectedRows);

    return (
        <App>
            <h1 className="text-white text-2xl font-bold mb-8">Articles</h1>
            <div className="w-full flex flex-col gap-8">
                <div className="flex flex-col gap-4">
                    <div className="grid grid-cols-3 max-w-44 gap-x-4">
                        <PrimaryButton text="+" onClick={handleOpenModal} />
                        <SecondaryButton text="-" onClick={handleDeleteArticles} />
                        <SecondaryButton text="*" onClick={handleGenerateArticles} />
                    </div>
                    <Table columns={columns} data={articles} onRowSelect={handleRowSelect} rowsPerPage={12} />
                </div>
            </div>
            {showModal && (
                <Popup handleCloseAction={handleCloseModal}>
                    <Form title="New article" subtitle="" className="max-w-[500px] w-full">
                        <TextInput
                            id="url"
                            label="New url"
                            value={url}
                            onChange={handleUrlChange}
                            placeholder="https://wikipedia.org/wiki"
                        />
                        {error && <p className="text-sm text-red-500 text-center">{errorMessage}</p>}
                        <div className="flex flex-row gap-4">
                            <SecondaryButton text="Cancel" onClick={handleCloseModal} />
                            <div className="w-full" />
                            <PrimaryButton text="Create" onClick={handleCreateArticle} />
                        </div>
                    </Form>
                </Popup>
            )}
            {showLoading && (
                <Popup handleCloseAction={handleCloseModal}>
                    <SpinnerIcon />
                </Popup>
            )}
        </App>
    );
};

export default ArticlesAccountAppPage;
