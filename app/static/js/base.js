document.addEventListener("DOMContentLoaded", async () => {
    const navigateSignOutHTML = document.querySelector(".navigate_sign_out");

    // Sign Out
    if (navigateSignOutHTML) {
        navigateSignOutHTML.addEventListener("click", async (event) => {
            event.preventDefault();

            confirmResult = confirm("Before Sign Out");

            if (!confirmResult) {
                return;
            }

            try {
                const response = await fetch("/api/sign_out", {
                    method : "POST",
                });

                const signOutResult = await response.json();

                const result = signOutResult.result;
                const error = signOutResult.error;

                if (result === 0) {
                    alert(`Fail to Sign Out : ${error}`);

                    return;
                }

                alert("OK : Success to Sign Out");

                window.location.href = `/`; // Redirect to Main
            } catch (e) {
                console.error(`Fail to Sign Out : ${e}`);

                alert("ERROR : Fail to Sign Out");
            }
        });
    }
});