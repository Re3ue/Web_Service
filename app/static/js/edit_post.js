document.addEventListener("DOMContentLoaded", async () => {
    const postFormHTML = document.querySelector(".post_form");
    const postFormTitleHTML = document.querySelector(".post_form_title");
    const postFormContentHTML = document.querySelector(".post_form_content");
    const postFormDateHTML = document.querySelector(".post_form_date");

    const eidtPostId = document.querySelector(".post_form_button").dataset.postId; // Get Post ID
    console.log(`[ DEBUG ] Post ID : ${eidtPostId}`);

    // Submit : Edit Post
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

        // Request : Edit Post to Server
        try {
            const response = await fetch(`/api/edit_post_post/${eidtPostId}`, {
                method : "POST",
                headers : {
                    "Content-Type" : "application/json", // Flask : Request with JSON
                },
                body : JSON.stringify({title, content, date}),
            });

            // Check : Response (Edit Post to Server)
            if (!response.ok) {
                throw new Error("[ ERROR ] Fail to Fetch \"Edit Post\"");
            }

            const editPostResult = await response.json();

            const result = editPostResult.result; // Get Result ( 1 : Success / 0 : Fail )
            const post_id = editPostResult.post_id; // Get Post ID
            const error = editPostResult.error; // Get Error

            if (result === 0) {
                alert(`Fail to Edit Post : ${error}`);

                return;
            }

            alert("OK : Success to Edit Post");

            window.location.href = `/post/${post_id}`; // Redirect with Post ID
        } catch (e) {
            console.error(`Fail to Edit Post : {e}`);

            alert("ERROR : Fail to Edit Post");
        }
    })
});