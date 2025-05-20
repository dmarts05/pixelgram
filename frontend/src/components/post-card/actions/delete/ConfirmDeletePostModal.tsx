import React from "react";
import Modal from "../../../modals/Modal";
import ModalButton from "../../../modals/ModalButton";

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
    postId,
}: ConfirmDeleteModalProps & { postId: string }): React.ReactNode {
    return (
        <Modal
            isOpen={isOpen}
            onClose={onCancel}
            ariaLabel="Confirm deletion dialog"
            id={`confirm-delete-modal-${postId}`}
        >
            <Modal.Content>
                <Modal.Header>Confirm Deletion</Modal.Header>
                <p>Are you sure you want to delete this post?</p>
                <Modal.Footer>
                    <ModalButton
                        onClick={onCancel}
                        disabled={isLoading}
                        variant="outline"
                    >
                        Cancel
                    </ModalButton>
                    <ModalButton
                        onClick={onConfirm}
                        disabled={isLoading}
                        variant="error"
                        loading={isLoading}
                    >
                        Delete
                    </ModalButton>
                </Modal.Footer>
            </Modal.Content>
            <Modal.Backdrop />
        </Modal>
    );
}

export default ConfirmDeleteModal;
