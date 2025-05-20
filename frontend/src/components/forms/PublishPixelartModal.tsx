import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { MdAutoFixHigh } from "react-icons/md";
import { useNavigate } from "react-router";
import { autogenerateCaption, publishPost } from "../../services/posts-service";
import Modal from "../modals/Modal";
import ModalButton from "../modals/ModalButton";

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
    disabled = false,
}: {
    value: string;
    isLoading: boolean;
    onChange: (val: string) => void;
    onGenerate: () => void;
    errorPlaceholder?: string;
    disabled?: boolean;
}): React.ReactNode => {
    const [userHasTyped, setUserHasTyped] = useState(false);

    return (
        <div className="mt-4 flex items-center gap-2">
            <div className="flex-1">
                {isLoading ? (
                    <div className="skeleton textarea border-none h-10 mt-4 w-full rounded"></div>
                ) : (
                    <textarea
                        className={`textarea w-full resize-none h-10 mt-4 ${errorPlaceholder && !userHasTyped ? "textarea-error" : ""}`}
                        maxLength={1000}
                        placeholder={errorPlaceholder || "Description"}
                        value={value}
                        onChange={(e) => {
                            setUserHasTyped(e.target.value.length > 0);
                            onChange(e.target.value);
                        }}
                    />
                )}
            </div>
            <button
                className="btn btn-circle btn-ghost"
                onClick={onGenerate}
                disabled={isLoading || disabled}
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

const PixelartPreview = ({ src }: { src: string }): React.ReactNode => (
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
    loading = false,
}: {
    onClose: () => void;
    onPublish: () => void;
    disabled: boolean;
    loading?: boolean;
}): React.ReactNode => (
    <div className="modal-actions flex justify-center gap-4 mt-8">
        <ModalButton variant="outline" onClick={onClose}>
            Cancel
        </ModalButton>
        <ModalButton
            variant="primary"
            onClick={onPublish}
            disabled={disabled}
            loading={loading}
        >
            Publish
        </ModalButton>
    </div>
);

const SuccessView = ({ onDone }: { onDone: () => void }): React.ReactNode => (
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
}: Props): React.ReactNode | null {
    const [description, setDescription] = useState<string>("");
    const [generating, setGenerating] = useState<boolean>(false);
    const [publishing, setPublishing] = useState<boolean>(false);
    const [errorPlaceholder, setErrorPlaceholder] = useState<string | null>(
        null
    );
    const [isPublished, setIsPublished] = useState<boolean>(false);
    const navigate = useNavigate();

    const autogenerateMutation = useMutation({
        mutationFn: async () => {
            return await autogenerateCaption(imageUrl);
        },
        onSuccess: (data: string) => {
            setDescription(data);
            setGenerating(false);
        },
        onError: (error: Error) => {
            setDescription("");
            setErrorPlaceholder(error.message);
            setGenerating(false);
        },
    });

    const publishMutation = useMutation({
        mutationFn: async () => {
            await publishPost(imageUrl, description);
        },
        onSuccess: () => {
            setIsPublished(true);
            setPublishing(false);
        },
        onError: (error: Error) => {
            setErrorPlaceholder(error.message);
            setPublishing(false);
        },
    });

    const handleAutogenerate = async (): Promise<void> => {
        setGenerating(true);
        setErrorPlaceholder(null);
        autogenerateMutation.mutate();
    };

    const handlePublish = async (): Promise<void> => {
        setPublishing(true);
        publishMutation.mutate();
    };

    const handleDone = (): void => {
        onClose();
        navigate("/feed");
    };

    if (!isOpen) return null;

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            ariaLabel="Publish pixelart dialog"
        >
            <Modal.Content>
                <Modal.Header>Publish pixelart</Modal.Header>
                {isPublished ? (
                    <SuccessView onDone={handleDone} />
                ) : (
                    <>
                        <PixelartPreview src={imageUrl} />
                        <DescriptionField
                            value={description}
                            isLoading={generating}
                            onChange={setDescription}
                            onGenerate={handleAutogenerate}
                            errorPlaceholder={errorPlaceholder || undefined}
                            disabled={publishing}
                        />
                        <ModalActions
                            onClose={onClose}
                            onPublish={handlePublish}
                            disabled={!description || generating || publishing}
                            loading={publishing}
                        />
                    </>
                )}
            </Modal.Content>
            <Modal.Backdrop />
        </Modal>
    );
}
