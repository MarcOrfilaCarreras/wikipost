const CTAButton = ({ text, url, className }) => (
    <a href={url} className={`flex items-center justify-center ${className}`}>
        <div className="w-full rounded-full bg-gradient-to-r from-purple-500 to-green-400 p-0.5 animate-glowing-loop shadow-[0_0_5px_rgba(128,0,255,0.3),0_0_8px_rgba(0,255,128,0.3)]">
            <div className="flex rounded-full items-center justify-center bg-gray-950 px-6 py-3">
                <span className="text-white font-semibold">{text}</span>
            </div>
        </div>
    </a>
);

export default CTAButton;
