const PrimaryButton = ({ text, onClick }) => (
    <button
        type="button"
        onClick={onClick}
        className="w-full px-4 py-3 text-sm font-medium text-white bg-blue-500 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800 transition duration-200"
    >
        {text}
    </button>
);

export default PrimaryButton;
