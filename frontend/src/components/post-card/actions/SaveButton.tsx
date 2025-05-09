import {useMutation} from "@tanstack/react-query";
import { savePost, unsavePost } from "../../../services/posts-service";
import {FaBookmark, FaRegBookmark} from "react-icons/fa";
interface SavedButtonProps {
    postId: string;
    savedByUser: boolean;
}

function SaveButton({ postId,savedByUser }: SavedButtonProps): React.ReactNode {
    
    const savePostMutation = useMutation({
        mutationFn: async () => {
            if (!savedByUser) {
                await savePost(postId);
            } else {
                await unsavePost(postId);
            }
        },
    });
    
    return (
        <button
            onClick={() => savePostMutation.mutate()}
            className="rounded-full text-lg hover:text-primary transition-colors cursor-pointer"
        >
            {savedByUser ? <FaBookmark/> : <FaRegBookmark/>}
        </button>
    );
}
export default SaveButton;