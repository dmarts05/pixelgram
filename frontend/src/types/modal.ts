export type ModalContextType = {
    isOpen: boolean;
    onClose: () => void;
    dialogRef: React.RefObject<HTMLDialogElement | null>;
};
