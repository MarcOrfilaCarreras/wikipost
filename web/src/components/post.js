import React from 'react';
import IconButton from './buttons/icon';
import AcceptIcon from '../assets/icons/buttons/accept';
import BinIcon from '../assets/icons/buttons/bin';
import EditIcon from '../assets/icons/buttons/edit';

const PostCard = ({ post, onDelete, onEdit, onAllow }) => {
    return (
        <div
            key={post.id}
            className="border border-gray-700 rounded-2xl shadow-xl bg-gradient-to-br from-gray-800 to-gray-900 text-gray-100 w-full max-w-xs flex flex-col min-h-0"
        >
            <img src={post.url} alt="Post" className="w-full h-48 object-cover rounded-t-2xl" />

            <div className="p-4 flex-grow h-[150px] overflow-y-auto text-sm scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                <p className="text-gray-300 leading-snug break-words">
                    {post.content}
                </p>
            </div>

            <div className="p-4 border-t border-gray-700 flex justify-between text-sm text-gray-400">
                <div className="flex flex-row gap-4">
                    <IconButton onClick={() => onDelete(post.id)}>
                        <BinIcon />
                    </IconButton>
                    {onEdit && (
                        <IconButton onClick={() => onEdit(post.id)}>
                            <EditIcon />
                        </IconButton>
                    )}
                </div>
                <div className="w-full flex items-center justify-between [&>button]:w-auto">
                    <div className="flex-grow items-center"></div>
                    {onAllow && (
                        <IconButton className="w-auto" onClick={() => onAllow(post.id)}>
                            <AcceptIcon />
                        </IconButton>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PostCard;
