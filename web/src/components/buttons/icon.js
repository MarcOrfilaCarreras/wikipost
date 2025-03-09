const IconButton = ({onClick, children }) => (
    <button
        type="button"
        onClick={onClick}
        className="w-full h-full text-white flex items-center justify-center hover:scale-125 transition-all duration-300"
    >
        {children}
    </button>
);

export default IconButton;
