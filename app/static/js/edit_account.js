document.addEventListener("DOMContentLoaded", async () => {
    const profileAccountContainerHTML = document.querySelector(".profile_account_container");

    const editAccountId = document.querySelector(".profile_account_button").dataset.accountId; // Get Account ID
    
    console.log(`[ DEBUG ] Account ID : ${editAccountId}`);

    // Submit : Edit Account
    profileAccountContainerHTML.addEventListener("submit", async (event) => {
        event.preventDefault();

        editAccountPost(editAccountId);
    });

    // Image - Change
    document.querySelector(".profile_account_image_file").addEventListener("change", (event) => {
        imageFileChange(event);
    });
});

async function editAccountPost(editAccountId) {
    // HTML
    const profileAccountImageFileHTML = document.querySelector(".profile_account_image_file");

    const profileAccountNameHTML = document.querySelector(".profile_account_name");
    const profileAccountPasswordHTML = document.querySelector(".profile_account_password");
    const profileAccountDisplayNameHTML = document.querySelector(".profile_account_display_name");
    
    const profileAccountBirthHTML = document.querySelector(".profile_account_birth");
    const profileAccountCountryHTML = document.querySelector(".profile_account_country");

    // Data
    const image = profileAccountImageFileHTML.files[0];

    const name = profileAccountNameHTML.value;
    const password = profileAccountPasswordHTML.value;
    const displayName = profileAccountDisplayNameHTML.value;

    const birth = profileAccountBirthHTML.value;
    const country = profileAccountCountryHTML.value;

    // Check : Require
    if (!name || !password || !displayName) {
        alert("Require : All Fields ( Name / Password / Display Name )");

        return;
    }

    // Form Data
    const formData = new FormData();

    if (image) formData.append("image", image);
    formData.append("name", name);
    formData.append("password", password);
    formData.append("displayName", displayName);
    if (birth) formData.append("birth", birth);
    if (country) formData.append("country", country);

    // Request : Edit Account to Server
    try {
        const response = await fetch(`/api/edit_account_post/${editAccountId}`, {
            method : "POST",
            body : formData,
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
}

function imageFileChange(event) {        
    const fileReader = new FileReader();

    fileReader.onload = function () {
        const profileAccountImageViewHTML = document.querySelector(".profile_account_image_view")
        
        const imageFile = fileReader.result; // Get Data ( Image File )

        profileAccountImageViewHTML.src = imageFile // Set Data ( Image File )
    };

    fileReader.readAsDataURL(event.target.files[0]);
}