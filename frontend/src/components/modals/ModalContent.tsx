import React from "react";

interface ModalContentProps {
    children: React.ReactNode;
    className?: string;
}

const ModalContent: React.FC<ModalContentProps> = ({
    children,
    className = "",
}) => {
    return <div className={`modal-box ${className}`}>{children}</div>;
};

export default ModalContent;
