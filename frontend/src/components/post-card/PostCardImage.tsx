type PostCardImageProps = {
    imageUrl: URL;
    imageAlt: string;
    height: number;
};

function PostCardImage({
    imageUrl,
    imageAlt,
    height,
}: PostCardImageProps): React.ReactNode {
    const dialogId = `image-modal-${imageUrl}`;

    function openModal(): void {
        const dialog = document.getElementById(dialogId) as HTMLDialogElement;
        dialog.showModal();
    }

    return (
        <>
            <figure
                onClick={openModal}
                className="relative border-y border-base-200 cursor-pointer overflow-hidden"
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

            {/* Modal dialog for full image */}
            <dialog id={dialogId} className="modal">
                <div className="modal-box p-0">
                    <img
                        src={String(imageUrl)}
                        alt={imageAlt}
                        className="w-full"
                        height={height}
                    />
                </div>
                <form method="dialog" className="modal-backdrop">
                    <button>close</button>
                </form>
            </dialog>
        </>
    );
}

export default PostCardImage;
