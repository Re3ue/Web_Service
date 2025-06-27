document.addEventListener("DOMContentLoaded", async () => {
    // Event of "Edit" Button => Route : Edit Post
    const eidtPostId = document.querySelector(".edit_button").dataset.postId; // Get Post ID
    console.log(`[ DEBUG ] Post ID : ${eidtPostId}`);
    const editButtonHTML = document.querySelector(".edit_button").addEventListener("click", () => {
        routeEditPost(eidtPostId);
    });
    
    // Event of "Delete" Button => Route : Delete Post
    const deletePostId = document.querySelector(".delete_button").dataset.postId; // Get Post ID
    console.log(`[ DEBUG ] Post ID : ${deletePostId}`);
    const deleteButtonHTML = document.querySelector(".delete_button").addEventListener("click", () => {
        deletePost(deletePostId);
    });
})

// Route to Edit Post
function routeEditPost(postId) {
    window.location.href = `/edit_post_get/${postId}`;
}

// Delete Post
async function deletePost(postId) {
    confirmResult = confirm("Before Delete");

    if (!confirmResult) {
        return;
    }

    try {
        const response = await fetch(`/api/delete_post/${postId}`, {
            method: "DELETE",
        });

        // Check : Response (Delete Post to Server)
        if (!response.ok) {
            throw new Error("[ ERROR ] Fail to Fetch \"Delete Post\"");
        }

        const deletePostResult = await response.json();

        const result = deletePostResult.result;
        const error = deletePostResult.error

        if (result === 0) {
            alert(`Fail to Delete Post : ${error}`);

            return;
        }

        alert("OK : Success to Delete Post");

        window.location.href = `/`; // Redirect to Main
    } catch (e) {
        console.error(`Fail to Delete Post : ${e}`);

        alert("ERROR : Fail to Delete Post");
    }
}