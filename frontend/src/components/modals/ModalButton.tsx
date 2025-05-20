import React from "react";

export interface ModalButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "primary" | "outline" | "error";
    loading?: boolean;
    children: React.ReactNode;
}

const variantClass: Record<string, string> = {
    primary: "btn btn-primary",
    outline: "btn btn-outline",
    error: "btn btn-error",
};

const ModalButton: React.FC<ModalButtonProps> = ({
    variant = "primary",
    loading = false,
    children,
    className = "",
    ...props
}) => {
    return (
        <button
            className={`${variantClass[variant]} ${className} relative`}
            disabled={props.disabled || loading}
            {...props}
        >
            <span className={loading ? "invisible" : "visible"}>
                {children}
            </span>
            {loading && (
                <span className="loading loading-spinner loading-xs absolute inset-0 m-auto"></span>
            )}
        </button>
    );
};

export default ModalButton;
