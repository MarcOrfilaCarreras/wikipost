const Popup = ({ children }) => (
    <div
        className="absolute left-0 top-0 h-full w-full z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center">
        <div className="w-full flex flex-col items-center gap-4">
            {children}
        </div>
    </div>
);

export default Popup;
