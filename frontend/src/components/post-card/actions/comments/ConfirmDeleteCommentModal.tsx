import React from "react";
import Modal from "../../../modals/Modal";
import ModalButton from "../../../modals/ModalButton";

interface ConfirmDeleteCommentModalProps {
    isOpen: boolean;
    onCancel: () => void;
    onConfirm: () => void;
    isLoading: boolean;
    commentId: string;
}

const ConfirmDeleteCommentModal: React.FC<ConfirmDeleteCommentModalProps> = ({
    isOpen,
    onCancel,
    onConfirm,
    isLoading,
    commentId,
}) => (
    <Modal
        isOpen={isOpen}
        onClose={onCancel}
        ariaLabel="Confirm comment deletion dialog"
        id={`confirm-delete-comment-modal-${commentId}`}
    >
        {isOpen && (
            <>
                <Modal.Content>
                    <Modal.Header>Confirm Comment Deletion</Modal.Header>

                    <p>Are you sure you want to delete this comment?</p>

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
            </>
        )}
    </Modal>
);

export default ConfirmDeleteCommentModal;
