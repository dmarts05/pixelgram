import React, { useEffect, useRef } from "react";

/**
 * Best practices for daisyUI modals:
 * - Use <dialog> for all modals.
 * - The opener button should have aria-haspopup="dialog" and aria-expanded.
 * - Use aria-label for modal accessibility.
 */

interface BaseModalProps {
    isOpen: boolean;
    onClose: () => void;
    children: React.ReactNode;
    showCloseButton?: boolean;
    modalBoxClassName?: string;
    backdropClassName?: string;
    ariaLabel?: string;
    id?: string; // Optional id for accessibility or testing
}

const BaseModal: React.FC<BaseModalProps> = ({
    isOpen,
    onClose,
    children,
    showCloseButton = true,
    modalBoxClassName = "",
    backdropClassName = "",
    ariaLabel = "Modal dialog",
    id,
}) => {
    const dialogRef = useRef<HTMLDialogElement>(null);

    useEffect(() => {
        const dialog = dialogRef.current;
        if (!dialog) return;
        if (isOpen && !dialog.open) {
            dialog.showModal();
        } else if (!isOpen && dialog.open) {
            dialog.close();
        }
    }, [isOpen]);

    useEffect(() => {
        const dialog = dialogRef.current;
        if (!dialog) return;
        const handleClose = (): void => onClose();
        dialog.addEventListener("close", handleClose);
        return (): void => { dialog.removeEventListener("close", handleClose); };
    }, [onClose]);

    // Trap focus inside modal
    useEffect(() => {
        const dialog = dialogRef.current;
        if (!dialog || !isOpen) return;
        const previouslyFocused = document.activeElement as HTMLElement;
        dialog.focus();
        return (): void => {
            previouslyFocused?.focus();
        };
    }, [isOpen]);

    return (
        <dialog
            ref={dialogRef}
            className={`modal ${isOpen ? "modal-open" : ""}`}
            aria-label={ariaLabel}
            id={id}
        >
            <div className={`modal-box ${modalBoxClassName}`}>
                {showCloseButton && (
                    <button
                        className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
                        onClick={onClose}
                        aria-label="Close modal"
                        type="button"
                    >
                        ✕
                    </button>
                )}
                {children}
            </div>
            <form method="dialog" className={`modal-backdrop ${backdropClassName}`}> 
                <button aria-label="Close modal" onClick={onClose}></button>
            </form>
        </dialog>
    );
};

export default BaseModal;
