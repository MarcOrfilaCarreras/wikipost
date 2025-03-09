import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { API_ACCOUNT_POSTS } from '../../../assets/consts';

import App from '../../../layouts/app';
import PostCard from '../../../components/post';

const PublishedInstagramAppPage = () => {
    const [posts, setPosts] = useState([]);

    const navigate = useNavigate();

    const fetchData = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(API_ACCOUNT_POSTS + "?allowed=true&published=true", {
                method: 'GET',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }
            const { data } = await response.json();
            setPosts(data || []);
        } catch (error) {

        }
    };

    const handleDeletePostClick = async (id) => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(API_ACCOUNT_POSTS + "/" + id, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }

            navigate("/app/instagram/published?notify=Post%20deleted%20correctly&notify-type=success");
            window.location.reload();
        } catch (error) {
            navigate("/app/instagram/published?notify=The%20post%20could't%20be%20deleted&notify-type=error");
            window.location.reload();
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <App>
            <h1 className="text-white text-2xl font-bold mb-8">Published</h1>
            <div className="w-full mx-auto flex flex-col gap-8 overflow-hidden max-h-screen ">
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-6 w-full max-w-full p-2 justify-center overflow-y-auto max-h-[85vh] scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                    {Array.isArray(posts) && posts.map((post, index) => (
                        <PostCard
                        key={post.id}
                        post={post}
                        onDelete={handleDeletePostClick}
                    />
                    ))}
                </div>
            </div>
        </App>



    );
};

export default PublishedInstagramAppPage;
