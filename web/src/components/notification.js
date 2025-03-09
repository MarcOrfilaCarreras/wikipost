import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import InformationIcon from "../assets/icons/notifications/information";
import SuccessIcon from "../assets/icons/notifications/success";
import ErrorIcon from "../assets/icons/notifications/error";

const checkNotification = (searchParams) => {
    return searchParams.has("notify");
};

const Notification = () => {
    const [searchParams] = useSearchParams();
    const [show, setShow] = useState(false);
    const [message, setMessage] = useState("");
    const [type, setType] = useState("information");

    useEffect(() => {
        if (checkNotification(searchParams)) {
            setMessage(searchParams.get("notify") || "You have a new notification!");
            setType(searchParams.get("notify-type") || "information");
            setShow(true);
        }
    }, [searchParams]);

    useEffect(() => {
        if (show) {
            const timer = setTimeout(() => {
                setShow(false);
            }, 5000);

            return () => clearTimeout(timer);
        }
    }, [show]);

    if (!show) return null;

    let Icon = InformationIcon;
    if (type === "success") {
        Icon = SuccessIcon;
    }

    if (type === "error") {
        Icon = ErrorIcon;
    }

    return (
        <div className="animate-fade-in-up fixed flex items-center w-full max-w-sm p-4 space-x-4 rounded-lg shadow-sm top-5 right-5 text-gray-400 divide-gray-700 bg-gray-800 border border-gray-700">
            <Icon></Icon>
            <div className="ms-3 text-sm font-normal">{message}</div>
        </div>
    );
};

export default Notification;
