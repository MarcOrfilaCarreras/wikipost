const Form = ({ title = "Title", subtitle = "Subtitle", children, className }) => (
    <div className={`bg-gray-800 rounded-lg shadow-xl p-6 space-y-6 border border-gray-700 ${className}`}>
        <div className="text-center space-y-2">
            <h1 className="text-2xl font-bold text-white">{title}</h1>
            <p className="text-gray-400 text-sm">{subtitle}</p>
        </div>
        <form className="space-y-6">
        </form>

        {children}
    </div>
);

export default Form;
