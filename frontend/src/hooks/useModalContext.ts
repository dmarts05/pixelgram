import { useContext } from "react";
import ModalContext from "../stores/modal-context";
import type { ModalContextType } from "../types/modal";

const useModalContext = (): ModalContextType => {
    const context = useContext(ModalContext);
    if (!context) {
        throw new Error("useModalContext must be used inside a Modal");
    }
    return context;
};

export default useModalContext;
