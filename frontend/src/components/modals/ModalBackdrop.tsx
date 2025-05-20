import React from "react";
import useModalContext from "../../hooks/useModalContext";

interface ModalBackdropProps {
    className?: string;
}

const ModalBackdrop: React.FC<ModalBackdropProps> = ({ className = "" }) => {
    const { onClose } = useModalContext();

    return (
        <form method="dialog" className={`modal-backdrop ${className}`}>
            <button aria-label="Close modal" onClick={onClose}></button>
        </form>
    );
};

export default ModalBackdrop;
