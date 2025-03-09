const Card = ({ title = "Title", subtitle = "Subtitle", children }) => (
    <div className="bg-gradient-to-br from-gray-800/50 via-gray-800/30 to-gray-800/50 backdrop-blur-xl border border-gray-700/50 rounded-2xl p-8 md:p-12 shadow-xl">
        <div className="mb-4 flex items-center justify-center">
            {children}
        </div>
        <h3 className="text-xl font-semibold text-white">{title}</h3>
        <p className="text-gray-400 mt-2">
            {subtitle}
        </p>
    </div>
);

export default Card;
