import { JSX, useState } from "react";
import { fetchApi } from "../services/fetch-api";
import { API_URL } from "../utils/constants";

interface Props {
    imageUrl: string; // Cambiado de ImageData a string, ya que es un dataURL
    isOpen: boolean;
    onClose: () => void;
}

export default function PublishPixelartModal({
    imageUrl,
    isOpen,
    onClose,
}: Props): JSX.Element | null {
    const [description, setDescription] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);

    const handleAutogenerate = async (): Promise<void> => {
        setLoading(true);
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
            setDescription(data.description);
        } catch (error) {
            console.error("Error:", error);
            // Manejar el error, tal vez mostrar un mensaje al usuario
        } finally {
            setLoading(false);
        }
    };

    const handlePublish = (): void => {
        // Aquí podrías hacer un fetch/post a tu backend
        console.log("Publicar pixelart:", { description, imageUrl });
    };

    if (!isOpen) return null;

    // Subcomponentes internos

    const PixelartPreview = ({ src }: { src: string }): JSX.Element => (
        <div className="mt-4">
            <img
                src={src}
                alt="Pixelart"
                className="w-32 h-32 object-cover border rounded"
            />
        </div>
    );

    const DescriptionField = ({
        value,
        isLoading,
        onChange,
        onGenerate,
    }: {
        value: string;
        isLoading: boolean;
        onChange: (val: string) => void;
        onGenerate: () => void;
    }): JSX.Element => (
        <div className="mt-4 flex items-start gap-2">
            <div className="flex-1">
                {isLoading ? (
                    <div className="skeleton animate-pulse h-24 w-full rounded"></div>
                ) : (
                    <textarea
                        className="textarea textarea-bordered w-full resize-none h-24"
                        value={value}
                        onChange={(e) => onChange(e.target.value)}
                    />
                )}
            </div>
            <button
                className="btn btn-secondary"
                onClick={onGenerate}
                disabled={isLoading}
            >
                Autogenerar
            </button>
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
        <div className="modal-action">
            <button className="btn btn-outline" onClick={onClose}>
                Cancelar
            </button>
            <button
                className="btn btn-primary"
                onClick={onPublish}
                disabled={disabled}
            >
                Publicar
            </button>
        </div>
    );

    return (
        <div className="modal modal-open">
            <div className="modal-box">
                <h3 className="font-bold text-lg">Publicar pixelart</h3>
                <PixelartPreview src={imageUrl} />
                <DescriptionField
                    value={description}
                    isLoading={loading}
                    onChange={setDescription}
                    onGenerate={handleAutogenerate}
                />
                <ModalActions
                    onClose={onClose}
                    onPublish={handlePublish}
                    disabled={!description || loading}
                />
            </div>
        </div>
    );
}
