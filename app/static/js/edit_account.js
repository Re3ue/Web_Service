document.addEventListener("DOMContentLoaded", async () => {
    const profileAccountContainerHTML = document.querySelector(".profile_account_container");
    const profileAccountNameHTML = document.querySelector(".profile_account_name");
    const profileAccountPasswordHTML = document.querySelector(".profile_account_password");

    const eidtAccountId = document.querySelector(".profile_account_button").dataset.accountId; // Get Account ID
    console.log(`[ DEBUG ] Account ID : ${eidtAccountId}`);

    // Submit : Edit Account
    profileAccountContainerHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = profileAccountNameHTML.value;
        const password = profileAccountPasswordHTML.value;

        // Check : Require
        if (!name || !password) {
            alert("Require : All Fields ( Name / Password )");

            return;
        }

        // Request : Edit Account to Server
        try {
            const response = await fetch(`/api/edit_account_post/${eidtAccountId}`, {
                method : "POST",
                headers : {
                    "Content-Type" : "application/json", // Flask : Request with JSON
                },
                body : JSON.stringify({name, password}),
            });

            // Check : Response (Edit Account to Server)
            if (!response.ok) {
                throw new Error("[ ERROR ] Fail to Fetch \"Edit Account\"");
            }

            const editPostResult = await response.json();

            const result = editPostResult.result; // Get Result ( 1 : Success / 0 : Fail )
            const accountId = editPostResult.account_id; // Get Account ID
            const error = editPostResult.error; // Get Error

            if (result === 0) {
                alert(`Fail to Edit Account : ${error}`);

                return;
            }

            alert("OK : Success to Edit Account");

            window.location.href = `/profile/${accountId}`; // Redirect with Account ID
        } catch (e) {
            console.error(`Fail to Edit Account : ${e}`);

            alert("ERROR : Fail to Edit Account");
        }
    });
});