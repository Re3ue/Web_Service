document.addEventListener("DOMContentLoaded", async () => {
    const changeFormHTML = document.querySelector(".change_form");

    const accountId = document.querySelector(".change_form_button").dataset.accountId; // Get Account ID
    
    console.log(`[ DEBUG ] Account ID : ${accountId}`);

    changeFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        changePassword(accountId);
    });
});

async function changePassword(accountId) {
    const changeFormNewPasswordHTML = document.querySelector(".change_form_new_password");

    const newPassword = changeFormNewPasswordHTML.value;

    // Check : Require
    if (!newPassword) {
        alert("Require : All Fields ( New Password )");

        return;
    }

    // Request
    try {
        const response = await fetch(`/api/change_password_2/${accountId}`, {
            method : "POST",
            headers : {
                "Content-Type" : "application/json", // Flask : Request with JSON
            },
            body : JSON.stringify({newPassword}),
        });

        // Check : Response
        if (!response.ok) {
            throw new Error("[ ERROR ] Fail to Fetch \"Change Password\"");
        }

        const changePasswordResult = await response.json();

        const result = changePasswordResult.result; // Get Result ( 1 : Success / 0 : Fail )
        const newPasswordRaw = changePasswordResult.new_password_raw // Get Account New Password ( Raw )
        const error = changePasswordResult.error // Get Error

        if (result === 0) {
            alert(`Fail to Change Password : ${error}`);

            return;
        }

        alert(`[ OK ] Success to Change Password : ${newPasswordRaw}`);
        
        window.location.href = `/sign_in`; // Redirect to Sign In
    } catch (e) {
        console.error(`Fail to Change Password : ${e}`);

        alert("[ ERROR ] Fail to Change Password");
    }
}