document.addEventListener("DOMContentLoaded", async () => {
    const postFormHTML = document.querySelector(".post_form");

    postFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        createPost();
    });
});

async function createPost() {
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

    // Request : Create Post to Server
    try {
        const response = await fetch("/api/create_post", {
            method : "POST",
            body : formData,
        });

        // Check : Response (Create Post to Server)
        if (!response.ok) {
            throw new Error("[ ERROR ] Fail to Fetch \"Create Post\"");
        }

        const createPostResult = await response.json();

        const result = createPostResult.result; // Get Result ( 1 : Success / 0 : Fail )
        const post_id = createPostResult.post_id; // Get Post ID
        const error = createPostResult.error; // Get Error

        if (result === 0) {
            alert(`Fail to Create Post : ${error}`);

            return;
        }

        alert("OK : Success to Create Post");

        window.location.href = `/post/${post_id}`; // Redirect with Post ID
    } catch (e) {
        console.error(`Fail to Create Post : ${e}`);

        alert("ERROR : Fail to Create Post");
    }
}