import React from "react";

interface ConfirmDeleteModalProps {
    isOpen: boolean;
    onCancel: () => void;
    onConfirm: () => void;
    isLoading: boolean;
}

function ConfirmDeleteModal({
    isOpen,
    onCancel,
    onConfirm,
    isLoading,
}: ConfirmDeleteModalProps): React.ReactNode {
    if (!isOpen) return null;

    return (
        <dialog className="modal modal-open">
            <div className="modal-box">
                <button
                    className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
                    onClick={onCancel}
                >
                    ✕
                </button>
                <h3 className="font-bold text-lg">Confirm Deletion</h3>
                <p>Are you sure you want to delete this post?</p>
                <div className="modal-action">
                    <button
                        className="btn"
                        onClick={onCancel}
                        disabled={isLoading}
                    >
                        Cancel
                    </button>
                    <button
                        className="btn btn-error w-18.75"
                        onClick={onConfirm}
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <span className="loading loading-spinner loading-xs" />
                        ) : (
                            "Delete"
                        )}
                    </button>
                </div>
            </div>
            <form method="dialog" className="modal-backdrop">
                <button onClick={onCancel} />
            </form>
        </dialog>
    );
}

export default ConfirmDeleteModal;
