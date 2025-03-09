import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import PrimaryButton from "./buttons/primary";

import MenuIcon from "../assets/icons/menu";
import CloseIcon from "../assets/icons/close";

const Navbar = ({ children }) => {
    const navigate = useNavigate();
    const [isOpen, setIsOpen] = useState(false);

    const handleLogoutClick = () => {
        navigate('/auth/logout');
    };

    const toggleSidebar = () => setIsOpen(!isOpen);

    const getFirstLetter = (child) => {
        if (!React.isValidElement(child)) return '';

        const childArray = React.Children.toArray(child.props.children);
        const textNode = childArray.find(c => typeof c === 'string' && c.trim().length > 0);

        if (textNode) return textNode.trim().slice(0, 2);

        return '';
    };

    const mobileNavButtons = [];
    let firstSubmenu = true;

    React.Children.forEach(children, child => {
        if (!React.isValidElement(child)) return;

        const subMenu = React.Children.toArray(child.props.children).find(c => React.isValidElement(c) && c.type === 'ul');

        if (subMenu) {
            if (!firstSubmenu) {
                mobileNavButtons.push(
                    <span key={`separator-${mobileNavButtons.length}`} className="border border-gray-700/50 mt-4 mb-4"></span>
                );
            }
            firstSubmenu = false;

            React.Children.forEach(subMenu.props.children, subItem => {
                if (!React.isValidElement(subItem)) return;

                const link = React.Children.toArray(subItem.props.children).find(c => React.isValidElement(c) && c.type === 'a');

                if (link) {
                    const href = link.props.href;
                    const subLetter = getFirstLetter(link);
                    if (subLetter) {
                        mobileNavButtons.push(
                            <button
                                key={subLetter}
                                className="w-10 h-10 bg-gray-600 text-white rounded flex items-center justify-center"
                                onClick={() => navigate(href)}
                            >
                                {subLetter}
                            </button>
                        );
                    }
                }
            });
        }
    });

    return (
        <>
            <div className="xl:hidden p-4 bg-gray-800 flex flex-col gap-8">
                <button onClick={toggleSidebar} className="text-white focus:outline-none flex justify-center">
                    <MenuIcon></MenuIcon>
                </button>
                <div className="flex flex-col gap-4">
                    {mobileNavButtons}
                </div>
            </div>

            <aside
                className={`
                    bg-gray-800 shadow-xl space-y-6 border-r border-gray-700
                    flex flex-col h-screen p-4 fixed xl:static z-50
                    transform transition-transform duration-200 ease-in-out
                    ${isOpen ? "translate-x-0" : "-translate-x-full"}
                    xl:translate-x-0 xl:w-72
                `}
            >
                <div className="p-4 bg-gray-800">
                    <p className="text-xl text-white font-bold border-b border-gray-700 pb-4 flex flex-row">
                        <span className='w-full'>Wikipost</span>

                        <button onClick={toggleSidebar} className="xl:hidden text-white focus:outline-none">
                            <CloseIcon></CloseIcon>
                        </button>
                    </p>
                </div>

                <nav>
                    <ul className={`pl-6 space-y-10 w-64 xl:w-48 lg:w-
                        [&>li]:text-white [&>li]:font-bold
                        [&>li>button]:px-4 [&>li>button]:py-2 [&>li>button]:text-white
                        [&>li>ul]:pl-4 [&>li>ul]:mt-2 [&>li>ul]:space-y-4
                        [&>li>a]:px-4 [&>li>a]:py-2 [&>li>a]:text-white
                        [&>li>ul>li>a]:text-sm [&>li>ul>li>a]:font-normal [&>li>ul>li>a]:text-white
                    `}>
                        {children}
                    </ul>
                </nav>

                <div className="flex-grow p-4 flex items-end">
                    <PrimaryButton text="Logout" onClick={handleLogoutClick} />
                </div>
            </aside>
        </>
    );
};

export default Navbar;
