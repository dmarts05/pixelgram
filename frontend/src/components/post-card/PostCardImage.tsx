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
                className="border-y border-base-200 cursor-pointer"
            >
                <img
                    src={String(imageUrl)}
                    alt={imageAlt}
                    style={{
                        minWidth: `${height}px`,
                        minHeight: `${height}px`,
                    }}
                />
            </figure>

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
