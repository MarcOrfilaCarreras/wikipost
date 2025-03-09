const SecondaryButton = ({ text, onClick }) => (
    <button
        type="button"
        onClick={onClick}
        className="w-full px-4 py-3 text-sm font-medium text-white border border-gray-600 rounded-lg bg-gray-700 hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:ring-offset-2 focus:ring-offset-gray-800 transition duration-200"
    >
        {text}
    </button>
);

export default SecondaryButton;
