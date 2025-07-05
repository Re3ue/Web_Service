document.addEventListener("DOMContentLoaded", async () => {
    const changeFormHTML = document.querySelector(".change_form");

    changeFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        changePassword();
    });
});

async function changePassword() {
    const changeFormNameHTML = document.querySelector(".change_form_name");
    const changeFormDisplayNameHTML = document.querySelector(".change_form_display_name");

    const name = changeFormNameHTML.value;
    const displayName = changeFormDisplayNameHTML.value;

    // Check : Require
    if (!name || !displayName) {
        alert("Require : All Fields ( Name / Display Name )");

        return;
    }

    // Request
    try {
        const response = await fetch("/api/change_password_1", {
            method : "POST",
            headers : {
                "Content-Type" : "application/json", // Flask : Request with JSON
            },
            body : JSON.stringify({name, displayName}),
        });

        // Check : Response
        if (!response.ok) {
            throw new Error("[ ERROR ] Fail to Fetch \"Change Password\"");
        }

        const changePasswordResult = await response.json();

        const result = changePasswordResult.result; // Get Result ( 1 : Success / 0 : Fail )
        const accountId = changePasswordResult.account_id // Get Account ID
        const error = changePasswordResult.error // Get Error

        if (result === 0) {
            alert(`Fail to Change Password : ${error}`);

            return;
        }
        
        window.location.href = `/change_password_2/${accountId}`; // Redirect to Change Password with Account ID
    } catch (e) {
        console.error(`Fail to Change Password : ${e}`);

        alert("[ ERROR ] Fail to Change Password");
    }
}