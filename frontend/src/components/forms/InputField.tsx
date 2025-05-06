import {
    FieldError,
    FieldValues,
    Path,
    RegisterOptions,
    UseFormRegister,
} from "react-hook-form";

type InputFieldProps<T extends FieldValues> = {
    name: Path<T>;
    label: string;
    type?: string;
    register: UseFormRegister<T>;
    error?: FieldError;
    rules?: RegisterOptions<T>;
    disabled?: boolean;
};

function InputField<T extends FieldValues>({
    name,
    label,
    type = "text",
    register,
    error,
    rules = {},
    disabled = false,
}: InputFieldProps<T>): React.ReactNode {
    return (
        <div className="flex flex-col gap-2">
            <label className="floating-label">
                <input
                    type={type}
                    placeholder={`${label}${rules?.required ? " *" : ""}`}
                    className={`input w-full ${error ? "input-error" : ""}`}
                    {...register(name, rules)}
                    disabled={disabled}
                />
                <span>
                    {label}
                    {rules?.required && <span className="text-error"> *</span>}
                </span>
            </label>
            {error && <span className="text-error">{error.message}</span>}
        </div>
    );
}

export default InputField;
