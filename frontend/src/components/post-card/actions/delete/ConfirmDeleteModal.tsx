import React from "react";
import BaseModal from "../../../BaseModal";

interface ConfirmDeleteModalProps {
    isOpen: boolean;
    onCancel: () => void;
    onConfirm: () => void;
    isLoading: boolean;
}

export const CONFIRM_DELETE_MODAL_ID = "confirm-delete-modal";

function ConfirmDeleteModal({
    isOpen,
    onCancel,
    onConfirm,
    isLoading,
}: ConfirmDeleteModalProps): React.ReactNode {
    return (
        <BaseModal
            isOpen={isOpen}
            onClose={onCancel}
            ariaLabel="Confirm deletion dialog"
        >
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
        </BaseModal>
    );
}

export default ConfirmDeleteModal;
