document.addEventListener("DOMContentLoaded", async () => {
    // Event of "Edit" Button => Route : Edit Account
    const editAccountId = document.querySelector(".edit_button").dataset.accountId; // Get Account ID
    console.log(`[ DEBUG ] Account ID : ${editAccountId}`);
    const editButtonHTML = document.querySelector(".edit_button").addEventListener("click", () => {
        routeEditAccount(editAccountId);
    });
    
    // Event of "Delete" Button => Route : Delete Account
    const deleteAccountId = document.querySelector(".delete_button").dataset.accountId; // Get Account ID
    console.log(`[ DEBUG ] Account ID : ${deleteAccountId}`);
    const deleteButtonHTML = document.querySelector(".delete_button").addEventListener("click", () => {
        deleteAccount(deleteAccountId);
    });
});

// Route to Edit Account
function routeEditAccount(accountId) {
    window.location.href = `/edit_account_get/${accountId}`;
}

// Delete Account
async function deleteAccount(accountId) {
    confirmResult = confirm("Before Delete");

    if (!confirmResult) {
        return;
    }

    try {
        const response = await fetch(`/api/delete_account/${accountId}`, {
            method: "DELETE",
        });

        // Check : Response (Delete Account to Server)
        if (!response.ok) {
            throw new Error("[ ERROR ] Fail to Fetch \"Delete Account\"");
        }

        const deleteAccountResult = await response.json();

        const result = deleteAccountResult.result;
        const error = deleteAccountResult.error

        if (result === 0) {
            alert(`Fail to Delete Account : ${error}`);

            return;
        }

        alert("OK : Success to Delete Account");

        window.location.href = `/`; // Redirect to Main
    } catch (e) {
        console.error(`Fail to Delete Account : ${e}`);

        alert("ERROR : Fail to Delete Account");
    }
}