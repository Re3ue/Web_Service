document.addEventListener("DOMContentLoaded", async () => {
    const postPasswordFormHTML = document.querySelector(".post_password_form");

    postPasswordFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        checkPostPassword();
    });
});

async function checkPostPassword() {
    const postId = document.querySelector(".post_password_form_button").dataset.postId; // Get Post ID

    const postPasswordFormPasswordHTML = document.querySelector(".post_password_form_password");

    const postPassword = postPasswordFormPasswordHTML.value;

    // Check : Require
    if (!postPassword) {
        alert("Require : All Fields ( Post Password )");

        return;
    }

    // Request
    try {
        const response = await fetch(`/api/post_password/${postId}`, {
            method : "POST",
            headers : {
                "Content-Type" : "application/json", // Flask : Request with JSON
            },
            body : JSON.stringify({postPassword}),
        });

        // Check : Response
        if (!response.ok) {
            throw new Error("[ ERROR ] Fail to Fetch \"Post Password\"");
        }

        const findIdResult = await response.json();

        const result = findIdResult.result; // Get Result ( 1 : Success / 0 : Fail )
        // const postId = findIdResult.post_id // Get Post ID
        const error = findIdResult.error // Get Error

        if (result === 0) {
            alert(`Fail to Check - Post Password : ${error}`);

            return;
        }

        alert(`[ OK ] Success to Check - Post Password`);
        
        window.location.href = `/post/${postId}`; // Redirect to Post
    } catch (e) {
        console.error(`Fail to Check - Post Password : ${e}`);

        alert("[ ERROR ] Fail to Check - Post Password");
    }
}