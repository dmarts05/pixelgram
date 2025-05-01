import { JSX, useState } from "react";
import { MdAutoFixHigh } from "react-icons/md";
import { fetchApi } from "../services/fetch-api";
import { API_URL } from "../utils/constants";

interface Props {
    imageUrl: string;
    isOpen: boolean;
    onClose: () => void;
}

const DescriptionField = ({
    value,
    isLoading,
    onChange,
    onGenerate,
    errorPlaceholder,
}: {
    value: string;
    isLoading: boolean;
    onChange: (val: string) => void;
    onGenerate: () => void;
    errorPlaceholder?: string;
}): JSX.Element => {
    return (
        <div className="mt-4 flex items-center gap-2">
            <div className="flex-1">
                {isLoading ? (
                    <div className="skeleton textarea border-none h-10 mt-4 w-full rounded"></div>
                ) : (
                    <textarea
                        className={`textarea w-full resize-none h-10 mt-4`}
                        placeholder={errorPlaceholder || "Description"}
                        value={value}
                        onChange={(e) => {
                            onChange(e.target.value);
                        }}
                    />
                )}
            </div>
            <button
                className="btn btn-circle btn-ghost"
                onClick={onGenerate}
                disabled={isLoading}
            >
                {isLoading ? (
                    <span className="loading loading-spinner"></span>
                ) : (
                    <MdAutoFixHigh />
                )}
            </button>
        </div>
    );
};

const PixelartPreview = ({ src }: { src: string }): JSX.Element => (
    <div className="mt-4 justify-center flex">
        <img
            src={src}
            alt="Pixelart"
            className="w-32 h-32 object-cover border rounded"
        />
    </div>
);

const ModalActions = ({
    onClose,
    onPublish,
    disabled,
}: {
    onClose: () => void;
    onPublish: () => void;
    disabled: boolean;
}): JSX.Element => (
    <div className="modal-actions flex justify-center gap-4 mt-8">
        <button className="btn btn-outline" onClick={onClose}>
            Cancel
        </button>
        <button
            className="btn btn-primary"
            onClick={onPublish}
            disabled={disabled}
        >
            Publish
        </button>
    </div>
);

export default function PublishPixelartModal({
    imageUrl,
    isOpen,
    onClose,
}: Props): JSX.Element | null {
    const [description, setDescription] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [errorPlaceholder, setErrorPlaceholder] = useState<string | null>(
        null
    );

    const handleAutogenerate = async (): Promise<void> => {
        setLoading(true);
        setErrorPlaceholder(null);
        try {
            // Convertir el dataURL a un Blob
            const response = await fetch(imageUrl);
            const blob = await response.blob();

            // Crear un FormData y agregar el blob como archivo
            const formData = new FormData();
            formData.append("file", blob, "image.png"); // 'file' debe coincidir con el parámetro del backend

            // Enviar como multipart/form-data
            const apiResponse = await fetchApi(`${API_URL}/captions`, {
                method: "POST",
                // No establecer Content-Type, FormData lo establece automáticamente
                body: formData,
            });

            if (!apiResponse.ok) {
                const errorData = await apiResponse.json();
                throw new Error(
                    `Error while fetching the caption: ${errorData.detail || apiResponse.statusText}`
                );
            }

            const data = await apiResponse.json();
            setDescription(data.caption);
        } catch (error: unknown) {
            console.error("Error:", error);
            let errorMessage = "An unknown error occurred";

            if (error instanceof Error) {
                errorMessage = error.message;
            }

            setErrorPlaceholder(errorMessage);
            setDescription("");
        } finally {
            setLoading(false);
        }
    };

    const handlePublish = (): void => {
        // Aquí podrías hacer un fetch/post a tu backend
        console.log("Publish pixelart:", { description, imageUrl });
    };

    if (!isOpen) return null;

    return (
        <dialog className="modal modal-open">
            <div className="modal-box">
                <form method="dialog">
                    <button
                        className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
                        onClick={onClose}
                    >
                        ✕
                    </button>
                </form>
                <h3 className="font-bold text-lg">Publish pixelart</h3>
                <PixelartPreview src={imageUrl} />
                <DescriptionField
                    value={description}
                    isLoading={loading}
                    onChange={setDescription}
                    onGenerate={handleAutogenerate}
                    errorPlaceholder={errorPlaceholder || undefined}
                />
                <ModalActions
                    onClose={onClose}
                    onPublish={handlePublish}
                    disabled={!description || loading}
                />
            </div>
            <form method="dialog" className="modal-backdrop">
                <button onClick={onClose}>close</button>
            </form>
        </dialog>
    );
}
