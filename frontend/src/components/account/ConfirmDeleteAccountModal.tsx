import React from "react";
import Modal from "../modals/Modal";
import ModalButton from "../modals/ModalButton";

interface ConfirmDeleteAccountModalProps {
    isOpen: boolean;
    onCancel: () => void;
    onConfirm: () => void;
    isLoading: boolean;
}

export const CONFIRM_DELETE_ACCOUNT_MODAL_ID = "confirm-delete-account-modal";

const ConfirmDeleteAccountModal: React.FC<ConfirmDeleteAccountModalProps> = ({
    isOpen,
    onCancel,
    onConfirm,
    isLoading,
}) => (
    <Modal
        isOpen={isOpen}
        onClose={onCancel}
        ariaLabel="Confirm account deletion dialog"
        id={CONFIRM_DELETE_ACCOUNT_MODAL_ID}
    >
        <Modal.Content>
            <Modal.Header>Confirm delete account</Modal.Header>
            <p>
                Are you sure you want to delete your account? This action cannot
                be undone.
            </p>
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
                    Delete Account
                </ModalButton>
            </Modal.Footer>
        </Modal.Content>
        <Modal.Backdrop />
    </Modal>
);

export default ConfirmDeleteAccountModal;
