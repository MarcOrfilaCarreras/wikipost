import React, { useState } from 'react';
import IconButton from './buttons/icon';
import AcceptIcon from '../assets/icons/buttons/accept';
import BinIcon from '../assets/icons/buttons/bin';
import EditIcon from '../assets/icons/buttons/edit';
import VerticalSliderIcon from '../assets/icons/verticalSlider';
import LeftArrowIcon from '../assets/icons/leftArrow';

const PostCard = ({ post, onDelete, onEdit, onAllow }) => {
    const [flipped, setFlipped] = useState(false);

    return (
        <div
            key={post.id}
            className="[perspective:1000px] w-full max-w-xs min-h-[400px]"
        >
            <div
                className={`relative w-full h-full transition-transform duration-500 [transform-style:preserve-3d] ${flipped ? '[transform:rotateY(180deg)]' : ''}`}
            >
                {/* Front Side */}
                <div className="absolute inset-0 border border-gray-700 rounded-2xl shadow-xl bg-gradient-to-br from-gray-800 to-gray-900 text-gray-100 flex flex-col" style={{ backfaceVisibility: 'hidden' }}>
                    <img src={post.url} alt="Post" className="w-full h-48 object-cover rounded-t-2xl" />
                    <div className="p-4 flex-grow overflow-y-auto text-sm scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                        <p className="text-gray-300 leading-snug break-words">
                            {post.content}
                        </p>
                    </div>
                    <div className="p-4 border-t border-gray-700 flex justify-between text-sm text-gray-400">
                        <div className="flex flex-row gap-4 items-center">
                            <IconButton onClick={() => onDelete(post.id)}>
                                <BinIcon />
                            </IconButton>
                            {onEdit && (
                                <IconButton onClick={() => onEdit(post.id)}>
                                    <EditIcon />
                                </IconButton>
                            )}
                            {post.questions && (
                                <IconButton onClick={() => setFlipped(!flipped)}>
                                    <VerticalSliderIcon />
                                </IconButton>
                            )}
                        </div>
                        <div className="flex flex-row gap-4 items-center">
                            {onAllow && (
                                <IconButton onClick={() => onAllow(post.id)}>
                                    <AcceptIcon />
                                </IconButton>
                            )}
                        </div>
                    </div>
                </div>

                {/* Back Side */}
                <div className="absolute inset-0 [transform:rotateY(180deg)] border border-gray-700 rounded-2xl shadow-xl bg-gradient-to-br from-gray-900 to-gray-800 text-gray-100 flex flex-col" style={{ backfaceVisibility: 'hidden' }}>
                    <div className="p-4 overflow-y-auto text-sm scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800 flex-grow">
                        {post.questions[0]?.content && (
                            <h3 className="text-md font-semibold mb-4">{post.questions[0].content}</h3>
                        )}
                        {post.questions[0]?.options && (
                            <ul className="space-y-3">
                                {post.questions[0].options.map((option, index) => (
                                    <li
                                        key={index}
                                        className={`p-2 rounded-md cursor-pointer transition-all ease-in-out duration-200 ${option.is_correct ? 'bg-green-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
                                    >
                                        <span className={`flex items-center space-x-2`}>
                                            {option.is_correct ? (
                                                <span className="text-green-400">✔️</span>
                                            ) : (
                                                <span></span>
                                            )}

                                            <span>{option.content}</span>
                                        </span>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                    <div className="p-4 border-t border-gray-700 grid grid-cols-12">
                        <IconButton onClick={() => setFlipped(!flipped)}>
                            <LeftArrowIcon />
                        </IconButton>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default PostCard;
