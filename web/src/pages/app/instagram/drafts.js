import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { API_ACCOUNT_POSTS } from '../../../assets/consts';

import App from '../../../layouts/app';
import PrimaryButton from '../../../components/buttons/primary';
import SecondaryButton from '../../../components/buttons/secondary';
import Popup from '../../../components/popup';
import Form from '../../../components/form';
import TextInput from '../../../components/inputs/text';
import TextAreaInput from '../../../components/inputs/text-area';
import PostCard from '../../../components/post';

const DraftsInstagramAppPage = () => {
    const [posts, setPosts] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [currentEditingPostId, setCurrentEditingPostId] = useState('');
    const [editingImage, setEditingImage] = useState('');
    const [editingContent, setEditingContent] = useState('');
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    const navigate = useNavigate();

    const fetchData = async () => {
        const token = localStorage.getItem('token');
        try {
            const response = await fetch(API_ACCOUNT_POSTS + "?allowed=false", {
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

    const handleAllowPostClick = async (id) => {
        const token = localStorage.getItem('token');
        try {
            let post = posts.find(x => x.id === id);
            post.allowed = 1;

            const response = await fetch(API_ACCOUNT_POSTS + "/" + id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ ...post }),
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }

            navigate("/app/instagram/drafts?notify=Post%20updated%20correctly&notify-type=success");
            window.location.reload();
        } catch (error) {
            navigate("/app/instagram/drafts?notify=The%20post%20couldn't%20be%20updated&notify-type=error");
            window.location.reload();
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

            navigate("/app/instagram/drafts?notify=Post%20deleted%20correctly&notify-type=success");
            window.location.reload();
        } catch (error) {
            navigate("/app/instagram/drafts?notify=The%20post%20could't%20be%20deleted&notify-type=error");
            window.location.reload();
        }
    };

    const handleUpdatePostClick = async () => {
        const token = localStorage.getItem('token');
        try {
            let post = posts.find(x => x.id === currentEditingPostId);
            post.url = editingImage;
            post.content = editingContent;

            const response = await fetch(API_ACCOUNT_POSTS + "/" + currentEditingPostId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ ...post }),
            });
            if (!response.ok) {
                const { message } = await response.json();
                throw new Error(message);
            }

            navigate("/app/instagram/drafts?notify=Post%20updated%20correctly&notify-type=success");
            window.location.reload();
        } catch (error) {
            setError(true);
            setErrorMessage(error.message);
        }
    };

    function handleOpenPopup(id) {
        const post = posts.find(x => x.id === id);
        setEditingImage(post.url);
        setEditingContent(post.content);
        setCurrentEditingPostId(post.id);
        setShowModal(true);
    }

    const handleEditingContentChange = (e) => setEditingContent(e.target.value);
    const handleEditingImageChange = (e) => setEditingImage(e.target.value);

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <App>
            <h1 className="text-white text-2xl font-bold mb-8">Drafts</h1>
            <div className="w-full mx-auto flex flex-col gap-8 overflow-hidden max-h-screen ">
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-6 w-full max-w-full p-2 justify-center overflow-y-auto max-h-[85vh] scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                    {Array.isArray(posts) && posts.map((post) => (
                        <PostCard
                            key={post.id}
                            post={post}
                            onDelete={handleDeletePostClick}
                            onEdit={handleOpenPopup}
                            onAllow={handleAllowPostClick}
                        />
                    ))}
                </div>
            </div>

            {showModal && (
                <Popup handleCloseAction={() => setShowModal(false)}>
                    <Form title="Modify post" subtitle="" className="max-w-[700px] w-full">
                        <TextInput
                            id="image"
                            label="Image URL"
                            value={editingImage}
                            onChange={handleEditingImageChange}
                            placeholder="test"
                        />
                        <TextAreaInput
                            id="content"
                            label="Content"
                            value={editingContent}
                            onChange={handleEditingContentChange}
                            placeholder="test"
                            rows={10}
                        />
                        {error && <p className="text-sm text-red-500 text-center">{errorMessage}</p>}
                        <div className="flex flex-row gap-4">
                            <SecondaryButton text="Cancel" onClick={() => setShowModal(false)} />
                            <div className="w-full" />
                            <PrimaryButton text="Update" onClick={handleUpdatePostClick} />
                        </div>
                    </Form>
                </Popup>
            )}
        </App>
    );
};

export default DraftsInstagramAppPage;
