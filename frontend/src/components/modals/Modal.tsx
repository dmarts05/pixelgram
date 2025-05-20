import React, { useEffect, useRef } from "react";
import ModalContext from "../../stores/modal-context";
import ModalHeader from "./ModalHeader";
import ModalContent from "./ModalContent";
import ModalFooter from "./ModalFooter";
import ModalBackdrop from "./ModalBackdrop";

interface ModalProps {
    isOpen: boolean;
    onClose: () => void;
    children: React.ReactNode;
    ariaLabel?: string;
    id?: string;
}

const Modal: React.FC<ModalProps> & {
    Header: typeof ModalHeader;
    Content: typeof ModalContent;
    Footer: typeof ModalFooter;
    Backdrop: typeof ModalBackdrop;
} = ({ isOpen, onClose, children, ariaLabel = "Modal dialog", id }) => {
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

        return (): void => {
            dialog.removeEventListener("close", handleClose);
        };
    }, [onClose]);

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
        <ModalContext.Provider value={{ isOpen, onClose, dialogRef }}>
            <dialog
                ref={dialogRef}
                className={`modal ${isOpen ? "modal-open" : ""}`}
                aria-label={ariaLabel}
                id={id}
            >
                {children}
            </dialog>
        </ModalContext.Provider>
    );
};

Modal.Header = ModalHeader;
Modal.Content = ModalContent;
Modal.Footer = ModalFooter;
Modal.Backdrop = ModalBackdrop;

export default Modal;
