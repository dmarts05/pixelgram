import React, { useState } from "react";
import BaseModal from "../BaseModal";

type PostCardImageProps = {
    postId: string;
    imageUrl: URL;
    imageAlt: string;
    height: number;
};

function PostCardImage({
    postId,
    imageUrl,
    imageAlt,
    height,
}: PostCardImageProps): React.ReactNode {
    const [isModalOpen, setIsModalOpen] = useState(false);

    function handleOpenModal(): void {
        setIsModalOpen(true);
    }
    function handleCloseModal(): void {
        setIsModalOpen(false);
    }

    return (
        <>
            <figure
                onClick={handleOpenModal}
                className="relative border-y border-base-200 cursor-pointer overflow-hidden select-none"
                style={{ height: `${height}px` }}
            >
                {/* Blurred background layer */}
                <div
                    className="absolute inset-0 bg-cover bg-center blur-md scale-x-150"
                    style={{
                        backgroundImage: `url(${String(imageUrl)})`,
                    }}
                />

                {/* Foreground image with white background */}
                <img
                    src={String(imageUrl)}
                    alt={imageAlt}
                    className="relative mx-auto bg-white border-r-1 border-l-1 border-base-200"
                    style={{
                        minWidth: height,
                        minHeight: height,
                    }}
                    tabIndex={0}
                    role="button"
                    aria-label="Open image preview"
                    onClick={handleOpenModal}
                    onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ")
                            handleOpenModal();
                    }}
                />
            </figure>

            <BaseModal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                modalBoxClassName="p-0"
                ariaLabel="Image preview dialog"
                id={`image-preview-modal-${postId}`}
            >
                <h3 className="sr-only">Image preview</h3>
                <div>
                    <img
                        src={String(imageUrl)}
                        alt={imageAlt}
                        className="w-full"
                        height={height}
                    />
                </div>
            </BaseModal>
        </>
    );
}

export default PostCardImage;
