import Notification from "../components/notification";

const Main = ({children, className}) => (
    <div className={`w-screen h-screen ${className}`}>
        <Notification />
        {children}
    </div>
);

export default Main;
