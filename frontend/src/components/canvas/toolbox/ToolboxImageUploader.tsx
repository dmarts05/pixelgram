import { MdOutlineUploadFile } from "react-icons/md";

interface ToolboxImageUploaderProps {
    inputId: string;
    handleImageUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

function ToolboxImageUploader({
    inputId,
    handleImageUpload,
}: ToolboxImageUploaderProps): React.ReactNode {
    return (
        <>
            <input
                type="file"
                accept="image/*"
                id="image-input"
                onChange={handleImageUpload}
                className="hidden"
            />
            <button
                onClick={() => {
                    const input = document.getElementById(
                        inputId
                    ) as HTMLInputElement;
                    input.click();
                }}
                className="btn btn-circle w-8 h-8 border-white border-2"
            >
                {<MdOutlineUploadFile />}
            </button>
        </>
    );
}

export default ToolboxImageUploader;
