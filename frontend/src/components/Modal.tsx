import { useEffect } from "react";

interface ModalProps {
    id: string;
    children: React.ReactNode;
    responsive?: boolean;
    modalBoxClassName?: string;
    onClose?: () => void;
}

function Modal({
    id,
    children,
    responsive = true,
    modalBoxClassName = "",
    onClose = (): void => {},
}: ModalProps): React.ReactNode {
    useEffect(() => {
        const modal = document.getElementById(id) as HTMLDialogElement;
        if (modal) {
            modal.addEventListener("close", onClose);
        }
        return (): void => {
            if (modal) {
                modal.removeEventListener("close", onClose);
            }
        };
    }, [id, onClose]);

    return (
        <dialog
            id={id}
            className={`modal ${responsive && "modal-bottom sm:modal-middle"}`}
        >
            <div className={`modal-box ${modalBoxClassName}`}>{children}</div>

            {/* Clicking outside (backdrop) closes the modal */}
            <form method="dialog" className="modal-backdrop">
                <button></button>
            </form>
        </dialog>
    );
}

export default Modal;
