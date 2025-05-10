import {useState} from "react";
import {useMutation} from "@tanstack/react-query";
import { savePost, unsavePost } from "../../../services/posts-service";
import {FaBookmark, FaRegBookmark} from "react-icons/fa";
interface SavedButtonProps {
    postId: string;
    savedByUser: boolean;
}

function SaveButton({ postId,savedByUser }: SavedButtonProps): React.ReactNode {
    
    const [isSaved, setIsSaved] = useState<boolean>(savedByUser);

    const savePostMutation = useMutation({
        mutationFn: async () => {
            if (!isSaved) {
                setIsSaved(true);
                await savePost(postId);
                
            } else {
                setIsSaved(false);
                await unsavePost(postId);
                
            }
        },

    });
    
    return (
        <button
            onClick={() => {savePostMutation.mutate();}}
            className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
        >
            {isSaved ? <FaBookmark/> : <FaRegBookmark/>}
        </button>
    );
}
export default SaveButton;