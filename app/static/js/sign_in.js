document.addEventListener("DOMContentLoaded", async () => {
    const signInFormHTML = document.querySelector(".sign_in_form");
    const signInFormNameHTML = document.querySelector(".sign_in_form_name");
    const signInFormPasswordHTML = document.querySelector(".sign_in_form_password");

    signInFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = signInFormNameHTML.value;
        const password = signInFormPasswordHTML.value;

        // Check : Require
        if (!name || !password) {
            alert("Require : All Fields ( Name / Password )");

            return;
        }

        // Request
        try {
            const response = await fetch("/api/sign_in", {
                method : "POST",
                headers : {
                    "Content-Type" : "application/json", // Flask : Request with JSON
                },
                body : JSON.stringify({name, password}),
            });

            // Check : Response
            if (!response.ok) {
                throw new Error("[ ERROR ] Fail to Fetch \"Sign In\"");
            }

            const signInResult = await response.json();

            const result = signInResult.result; // Get Result ( 1 : Success / 0 : Fail )
            const account_id = signInResult.account_id // Get Account ID
            const error = signInResult.error // Get Error

            if (result === 0) {
                alert(`Fail to Sign In : ${error}`);

                return;
            }

            alert("OK : Success to Sign In");
            
            window.location.href = `/profile/${account_id}`; // Redirect with Account ID
        } catch (e) {
            console.error(`Fail to Sign In : ${e}`);

            alert("ERROR : Fail to Sign In");
        }
    });
});