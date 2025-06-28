document.addEventListener("DOMContentLoaded", async () => {
    const signUpFormHTML = document.querySelector(".sign_up_form");
    const signUpFormNameHTML = document.querySelector(".sign_up_form_name");
    const signUpFormPasswordHTML = document.querySelector(".sign_up_form_password");

    signUpFormHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = signUpFormNameHTML.value;
        const password = signUpFormPasswordHTML.value;

        // Check : Require
        if (!name || !password) {
            alert("Require : All Fields ( Name / Password )");

            return;
        }

        // Request : Create Account to Server
        try {
            const response = await fetch("/api/create_account", {
                method : "POST",
                headers : {
                    "Content-Type" : "application/json", // Flask : Request with JSON
                },
                body : JSON.stringify({name, password}),
            });

            // Check : Response (Create Account to Server)
            if (!response.ok) {
                throw new Error("[ ERROR ] Fail to Fetch \"Create Account\"");
            }

            const createAccountResult = await response.json();

            const result = createAccountResult.result; // Get Result ( 1 : Success / 0 : Fail )
            const account_id = createAccountResult.account_id // Get Account ID
            const error = createAccountResult.error // Get Error

            if (result === 0) {
                alert(`Fail to Create Account : ${error}`);

                return;
            }

            alert("OK : Success to Create Account");
            
            window.location.href = `/profile/${account_id}`; // Redirect with Account ID
        } catch (e) {
            console.error(`Fail to Create Account : ${e}`);

            alert("ERROR : Fail to Create Account");
        }
    });
});