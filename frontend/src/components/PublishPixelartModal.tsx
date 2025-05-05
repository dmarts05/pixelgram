import React, { useState } from "react";
import { MdAutoFixHigh } from "react-icons/md";
import { useNavigate } from "react-router";
import { fetchApi } from "../services/fetch-api";

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
}): React.ReactNode => {
    return (
        <div className="mt-4 flex items-center gap-2">
            <div className="flex-1">
                {isLoading ? (
                    <div className="skeleton textarea border-none h-10 mt-4 w-full rounded"></div>
                ) : (
                    <textarea
                        className={`textarea w-full resize-none h-10 mt-4`}
                        maxLength={1000}
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

const PixelartPreview = ({ src }: { src: string }): React.ReactElement => (
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
}): React.ReactElement => (
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

const SuccessView = ({
    onDone,
}: {
    onDone: () => void;
}): React.ReactElement => (
    <div className="flex flex-col items-center gap-6 py-4">
        <div role="alert" className="alert alert-success">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 shrink-0 stroke-current"
                fill="none"
                viewBox="0 0 24 24"
            >
                <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
            </svg>
            <span>Your pixelart has been successfully uploaded!</span>
        </div>
        <button className="btn btn-primary w-32" onClick={onDone}>
            Done
        </button>
    </div>
);

export default function PublishPixelartModal({
    imageUrl,
    isOpen,
    onClose,
}: Props): React.ReactElement | null {
    const [description, setDescription] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [errorPlaceholder, setErrorPlaceholder] = useState<string | null>(
        null
    );
    const [isPublished, setIsPublished] = useState<boolean>(false);
    const navigate = useNavigate();

    const handleAutogenerate = async (): Promise<void> => {
        setLoading(true);
        setErrorPlaceholder(null);
        try {
            // Convert dataURL to Blob
            const response = await fetch(imageUrl);
            const blob = await response.blob();

            // Create FormData and add blob
            const formData = new FormData();
            formData.append("file", blob, "image.png");

            // Send as multipart/form-data
            const apiResponse = await fetchApi("captions", {
                method: "POST",
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

    const handlePublish = async (): Promise<void> => {
        setLoading(true);
        try {
            // Convert dataURL to Blob
            const response = await fetch(imageUrl);
            const blob = await response.blob();

            // Create FormData and add blob and description
            const formData = new FormData();
            formData.append("file", blob, "image.png");
            formData.append("description", description);

            const apiResponse = await fetchApi("posts", {
                method: "POST",
                body: formData,
            });

            if (!apiResponse.ok) {
                const errorData = await apiResponse.json();
                throw new Error(
                    `Error while publishing the pixelart: ${errorData.detail || apiResponse.statusText}`
                );
            }

            // Set published state to true on success
            setIsPublished(true);
        } catch (error: unknown) {
            console.error("Error publishing pixelart:", error);
            let errorMessage = "Ocurrió un error al publicar tu pixelart";

            if (error instanceof Error) {
                errorMessage = error.message;
            }

            setErrorPlaceholder(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleDone = (): void => {
        onClose();
        navigate("/feed");
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

                {isPublished ? (
                    <SuccessView onDone={handleDone} />
                ) : (
                    <>
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
                    </>
                )}
            </div>
            <form method="dialog" className="modal-backdrop">
                <button onClick={onClose}>close</button>
            </form>
        </dialog>
    );
}
