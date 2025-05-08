import Modal from "../Modal";

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
    const modalId = `image-modal-${postId}`;

    function handleOpenModal(): void {
        const modal = document.getElementById(modalId) as HTMLDialogElement;
        modal.showModal();
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
                />
            </figure>

            <Modal id={modalId} responsive={false} modalBoxClassName="p-0">
                <img
                    src={String(imageUrl)}
                    alt={imageAlt}
                    className="w-full"
                    height={height}
                />
            </Modal>
        </>
    );
}

export default PostCardImage;
