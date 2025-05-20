import React, { createContext } from "react";

interface ModalContextType {
    isOpen: boolean;
    onClose: () => void;
    dialogRef: React.RefObject<HTMLDialogElement | null>;
}

const ModalContext = createContext<ModalContextType | null>(null);

export default ModalContext;
