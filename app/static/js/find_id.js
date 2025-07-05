document.addEventListener("DOMContentLoaded", async () => {
    const findFormHTML = document.querySelector(".find_form");

    findFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        findId();
    });
});

async function findId() {
    const findFormDisplayNameHTML = document.querySelector(".find_form_display_name");

    const displayName = findFormDisplayNameHTML.value;

    // Check : Require
    if (!displayName) {
        alert("Require : All Fields ( Display Name )");

        return;
    }

    // Request
    try {
        const response = await fetch("/api/find_id", {
            method : "POST",
            headers : {
                "Content-Type" : "application/json", // Flask : Request with JSON
            },
            body : JSON.stringify({displayName}),
        });

        // Check : Response
        if (!response.ok) {
            throw new Error("[ ERROR ] Fail to Fetch \"Find ID\"");
        }

        const findIdResult = await response.json();

        const result = findIdResult.result; // Get Result ( 1 : Success / 0 : Fail )
        const accountName = findIdResult.account_name // Get Account Name
        const error = findIdResult.error // Get Error

        if (result === 0) {
            alert(`Fail to Find ID : ${error}`);

            return;
        }

        alert(`[ OK ] Success to Find ID : ${accountName}`);
        
        window.location.href = `/sign_in`; // Redirect to Sign In
    } catch (e) {
        console.error(`Fail to Find ID : ${e}`);

        alert("[ ERROR ] Fail to Find ID");
    }
}