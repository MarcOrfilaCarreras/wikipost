import Main from './main';

const Centered = ({ children, className }) => (
    <Main>
        <div className={`w-full h-full flex justify-center items-center ${className}`}>
            {children}
        </div>
    </Main>
);

export default Centered;
