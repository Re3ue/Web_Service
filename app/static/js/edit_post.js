document.addEventListener("DOMContentLoaded", async () => {
    const postFormHTML = document.querySelector(".post_form");

    const eidtPostId = document.querySelector(".post_form_button").dataset.postId; // Get Post ID
    
    console.log(`[ DEBUG ] Post ID : ${eidtPostId}`);

    // Submit : Edit Post
    postFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        editPost(eidtPostId);
    });
});

async function editPost(eidtPostId) {
    const postFormTitleHTML = document.querySelector(".post_form_title");
    const postFormContentHTML = document.querySelector(".post_form_content");
    const postFormFileHTML = document.querySelector(".post_form_file");
    const postFormPasswordHTML = document.querySelector(".post_form_password");

    const title = postFormTitleHTML.value;
    const content = postFormContentHTML.value;
    const file = postFormFileHTML.files[0];
    const password = postFormPasswordHTML.value;

    // Check : Require
    if (!title || !content) {
        alert("Require : All Fields ( Title / Content )");

        return;
    }

    // Form Data
    const formData = new FormData();

    formData.append("title", title);
    formData.append("content", content);
    if (file) formData.append("file", file);
    if (password) formData.append("password", password);

    // Request : Edit Post to Server
    try {
        const response = await fetch(`/api/edit_post_post/${eidtPostId}`, {
            method : "POST",
            body : formData,
        });

        // Check : Response (Edit Post to Server)
        if (!response.ok) {
            throw new Error("[ ERROR ] Fail to Fetch \"Edit Post\"");
        }

        const editPostResult = await response.json();

        const result = editPostResult.result; // Get Result ( 1 : Success / 0 : Fail )
        const postId = editPostResult.post_id; // Get Post ID
        const error = editPostResult.error; // Get Error

        if (result === 0) {
            alert(`Fail to Edit Post : ${error}`);

            return;
        }

        alert("OK : Success to Edit Post");

        window.location.href = `/post/${postId}`; // Redirect with Post ID
    } catch (e) {
        console.error(`Fail to Edit Post : ${e}`);

        alert("ERROR : Fail to Edit Post");
    }
}