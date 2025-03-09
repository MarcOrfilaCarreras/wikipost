import React, { useEffect, useState } from 'react';

import { API_ACCOUNT_ARTICLES, API_ACCOUNT_POSTS } from '../../../assets/consts';

import App from '../../../layouts/app';

import Card from "../../../components/card";
import Table from '../../../components/table';

const OverviewDashboardAppPage = () => {
    const [articleCounter, setArticleCounter] = useState(0);
    const [draftsPostsCounter, setDraftsPostsCounter] = useState(0);
    const [scheduledPostsCounter, setScheduledPostsCounter] = useState(0);
    const [publishedPostsCounter, setPublishedPostsCounter] = useState(0);

    const [articles, setArticles] = useState([]);
    const articlesColumns = ['title', 'url'];

    const [publishedPosts, setPublishedPosts] = useState([]);
    const publishedPostsColumns = ['content'];

    const fetchData = async (url) => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
            return await response.json();
        } catch (error) {
            return {};
        }
    };

    const fetchArticles = async () => {
        const data = await fetchData(API_ACCOUNT_ARTICLES);
        if (!("data" in data)) {
            setArticleCounter(0);
            setArticles([]);
            return;
        }

        const sortedArticles = data.data.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );

        setArticleCounter(data.data == null ? 0 : data.data.length);
        setArticles(sortedArticles);
    }

    const fetchDraftsPosts = async () => {
        const data = await fetchData(API_ACCOUNT_POSTS + "?allowed=false");
        if (!("data" in data)) {
            setDraftsPostsCounter(0);
            return;
        }

        setDraftsPostsCounter(data.data == null ? 0 : data.data.length);
    }

    const fetchScheduledPosts = async () => {
        const data = await fetchData(API_ACCOUNT_POSTS + "?allowed=true&published=false");
        if (!("data" in data)) {
            setScheduledPostsCounter(0);
            return;
        }

        setScheduledPostsCounter(data.data == null ? 0 : data.data.length);
    }

    const fetchPublishedPosts = async () => {
        const data = await fetchData(API_ACCOUNT_POSTS + "?published=true");
        if (!("data" in data)) {
            setPublishedPostsCounter(0);
            return;
        }

        setPublishedPostsCounter(data.data == null ? 0 : data.data.length);
        setPublishedPosts(data.data);
    }

    useEffect(() => {
        fetchArticles();
        fetchDraftsPosts();
        fetchScheduledPosts();
        fetchPublishedPosts();
    }, []);

    return (
        <App>
            <h1 className="text-white text-2xl font-bold mb-8">Overview</h1>
            <div className='flex flex-col gap-8'>
                <div className='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 [&>div]:mb-4 [&>div]:sm:mr-4'>
                    <Card title="" subtitle='Total Articles'>
                        <h1 className='text-white text-4xl font-bold text-left w-full'>{articleCounter}</h1>
                    </Card>
                    <Card title="" subtitle='Drafts'>
                        <h1 className='text-white text-4xl font-bold text-left w-full'>{draftsPostsCounter}</h1>
                    </Card>
                    <Card title="" subtitle='Scheduled'>
                        <h1 className='text-white text-4xl font-bold text-left w-full'>{scheduledPostsCounter}</h1>
                    </Card>
                    <Card title="" subtitle='Published'>
                        <h1 className='text-white text-4xl font-bold text-left w-full'>{publishedPostsCounter}</h1>
                    </Card>
                </div>

                <div className='hidden sm:grid grid-cols-1 xl:grid-cols-2 gap-8'>
                    <div className='flex flex-col gap-4'>
                        <h2 className="text-white text-xl font-bold">Latest articles</h2>
                        <Table columns={articlesColumns} data={articles} rowsPerPage={8} />
                    </div>
                    <div className='flex flex-col gap-4'>
                        <h2 className="text-white text-xl font-bold">Published posts</h2>
                        <Table columns={publishedPostsColumns} data={publishedPosts} rowsPerPage={8} />
                    </div>
                </div>
            </div>
        </App>
    );
};

export default OverviewDashboardAppPage;
