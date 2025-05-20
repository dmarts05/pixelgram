import React from "react";
import useModalContext from "../../hooks/useModalContext";

interface ModalHeaderProps {
    children?: React.ReactNode;
    showCloseButton?: boolean;
    className?: string;
}

const ModalHeader: React.FC<ModalHeaderProps> = ({
    children,
    showCloseButton = true,
    className = "",
}) => {
    const { onClose } = useModalContext();

    return (
        <div className={`flex justify-between items-center mb-4 ${className}`}>
            {typeof children === "string" ? (
                <h3 className="font-bold text-lg">{children}</h3>
            ) : (
                children
            )}

            {showCloseButton && (
                <form method="dialog">
                    <button
                        className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
                        onClick={onClose}
                        aria-label="Close modal"
                        type="button"
                    >
                        ✕
                    </button>
                </form>
            )}
        </div>
    );
};

export default ModalHeader;
