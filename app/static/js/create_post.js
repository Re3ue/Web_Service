document.addEventListener("DOMContentLoaded", async () => {
    const postFormHTML = document.querySelector(".post_form");
    const postFormTitleHTML = document.querySelector(".post_form_title");
    const postFormContentHTML = document.querySelector(".post_form_content");
    const postFormDateHTML = document.querySelector(".post_form_date");

    // Submit : Create Post
    postFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        const title = postFormTitleHTML.value;
        const content = postFormContentHTML.value;
        const date = postFormDateHTML.value;

        // Check : Require
        if (!title || !content || !date) {
            alert("Require : All Fields ( Title / Content / Date");

            return;
        }

        // Request : Create Post to Server
        try {
            const response = await fetch("/api/create_post", {
                method : "POST",
                headers : {
                    "Content-Type" : "application/json", // Flask : Request with JSON
                },
                body : JSON.stringify({title, content, date}),
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
            console.error(`Fail to Create Post : {e}`);

            alert("ERROR : Fail to Create Post");
        }
    })
});