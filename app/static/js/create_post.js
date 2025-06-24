document.addEventListener("DOMContentLoaded", async () => {
    const postForm = document.querySelector(".post_form");
    const postFormTitle = document.querySelector(".post_form_title");
    const postFormContent = document.querySelector(".post_form_content");
    const postFormDate = document.querySelector(".post_form_date");

    // Submit : Create Post
    postForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const title = postFormTitle.value;
        const content = postFormContent.value;
        const date = postFormDate.value;

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

            console.log(`[ DEBUG ] Response Status : ${response.status}`);

            // Check : Respones (Create Post to Server)
            if (!response.ok) {
                throw new Error("[ ERROR ] Fail to Fetch \"Create Post\"");
            }

            const create_post_result = await response.json();

            const result = create_post_result.result; // Get Result ( 1 : Success / 0 : Fail )
            const post_id = create_post_result.post_id; // Get Post ID

            alert("OK : Success to Create Post");

            window.location.href = `/post/${post_id}`; // Redirect with Post ID
        } catch (error) {
            console.log("[ ERROR ] Fail to Create Post");

            alert("ERROR : Fail to Create Post");
        }
    })
})