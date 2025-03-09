const Window = ({ url }) => (
    <div className="relative w-full max-w-7xl">
        <div className="bg-gray-900 rounded-2xl overflow-hidden">
            <div
                className="px-4 py-3 bg-gray-800/50 border-b border-gray-700/50 flex items-center gap-2"
            >
                <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
                </div>
            </div>
            <img src={url} className="w-full h-auto" alt={`Window ${url}`} />
        </div>
    </div>
);

export default Window;
