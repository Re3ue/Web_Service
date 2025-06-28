let allAccount = [];
let allPost = [];

document.addEventListener("DOMContentLoaded", async () => {
    // Get All Account
    getAllAccount();

    // Get All Post
    getAllPost();
});

// Escape HTML
function escapeHTML(str) {
    if (typeof str !== "string") {
        return "";
    } 

    return str
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

// ########## ########## ########## ########## //
// Account
// ########## ########## ########## ########## //

// Account - Get
async function getAllAccount() {
    try {
        const response = await fetch("/admin_api/get_all_account");
        const getAllAccountResult = await response.json();

        const result = getAllAccountResult.result;
        allAccount = getAllAccountResult.all_account;
        const error = getAllAccountResult.error;

        if (result === 0) {
            alert(`Admin - Fail to Get All Account : ${error}`);

            return;
        }

        console.log(`[ DEBUG ] Get All Account : Success`);

        renderAllAccount()
    } catch (e) {
        console.error(`Admin - Fail to Get All Post : ${e}`);
    }
}

// Account - Render
function renderAllAccount() {
    const accountListHTML = document.getElementById("account_section_list");
    accountListHTML.innerHTML = "";

    allAccountCount = allAccount.length;

    const accounts = allAccount.slice(0, allAccountCount); // Get Accounts

    if (accounts.length == 0) {
        accountListHTML.innerHTML = "<div>Not Exist : All Account</div>"

        return;
    }

    // Render
    accounts.forEach(accountElement => {
        const div = document.createElement("div");

        div.className = "all_element_container";
        div.innerHTML = `
            <div class="all_element_id">${escapeHTML(accountElement.account_id.toString())}</div>
            <div class="all_element_title">${escapeHTML(accountElement.account_name)}</div>
            <div class="all_element_content">${escapeHTML(accountElement.account_pw)}</div>
            <div class="all_element_information">Date : ${escapeHTML(accountElement.post_date)}</div>
            <button class="all_element_button" onclick="deleteAccount(${accountElement.account_id})">Delete</button>
        `;

        accountListHTML.appendChild(div);
    });
}

// Account - Delete All
async function deleteAllAccount() {
    try {
        const response = await fetch("/admin_api/delete_all_account", {
            method: "DELETE",
        });

        const deleteAllAccountResult = await response.json();

        const result = deleteAllAccountResult.result;
        const error = deleteAllAccountResult.error;

        if (result === 0) {
            alert(`Admin - Fail to Delete All Account : ${error}`);

            return;
        }

        console.log(`[ DEBUG ] Delete All Account : Success`);

        getAllAccount();
    } catch (e) {
        console.error(`Admin - Fail to Delete All Account : ${e}`);
    }
}

// Account - Delete
async function deleteAccount(accountId) {
    try {
        const response = await fetch(`/admin_api/delete_account/${accountId}`, {
            method: "DELETE",
        });

        const deleteAccountResult = await response.json();

        const result = deleteAccountResult.result;
        const error = deleteAccountResult.error;

        if (result === 0) {
            alert(`Admin - Fail to Delete Account : ${error}`);

            return;
        }

        console.log(`[ DEBUG ] Delete Account ( ${accountId} ) : Success`);

        getAllAccount();
    } catch (e) {
        console.error(`Admin - Fail to Delete Account ( ${account_id} ) : ${e}`);
    }
}

// Account - Create 100
async function createAccount100() {
    try {
        const response = await fetch("/admin_api/create_account_100", {
            method: "POST",
        });

        const createAccountResult = await response.json();

        const result = createAccountResult.result;
        const error = createAccountResult.error;

        if (result === 0) {
            alert(`Admin - Fail to Create Account 100 : ${error}`);

            return;
        }

        console.log(`[ DEBUG ] Create 100 Account : Success`);

        getAllAccount();
    } catch (e) {
        console.error(`Admin - Fail to Create Account 100 : ${e}`);
    }
}

// ########## ########## ########## ########## //
// Post
// ########## ########## ########## ########## //

// Post - Get
async function getAllPost() {
    try {
        const response = await fetch("/admin_api/get_all_post");
        const getAllPostResult = await response.json();

        const result = getAllPostResult.result;
        allPost = getAllPostResult.all_post;
        const error = getAllPostResult.error;

        if (result === 0) {
            alert(`Fail to Get All Post : ${error}`);

            return;
        }

        console.log(`[ DEBUG ] Get All Post : Success`);

        renderAllPost()
    } catch (e) {
        console.error(`Fail to Get All Post : ${e}`);
    }
}

// Post - Render
function renderAllPost() {
    const postListHTML = document.getElementById("post_section_list");
    postListHTML.innerHTML = "";

    allPostCount = allPost.length;

    const posts = allPost.slice(0, allPostCount); // Get Posts

    if (posts.length == 0) {
        postListHTML.innerHTML = "<div>Not Exist : All Post</div>"

        return;
    }

    // Render
    posts.forEach(postElement => {
        const div = document.createElement("div");

        div.className = "all_element_container";
        div.innerHTML = `
            <div class="all_element_id">${escapeHTML(postElement.post_id.toString())}</div>
            <div class="all_element_title">${escapeHTML(postElement.post_title)}</div>
            <div class="all_element_content">${escapeHTML(postElement.post_content)}</div>
            <div class="all_element_information">Date : ${escapeHTML(postElement.post_date)} | Up Vote : ${postElement.post_upvote}</div>
            <button class="all_element_button" onclick="deletePost(${postElement.post_id})">Delete</button>
        `;

        postListHTML.appendChild(div);
    });
}

// Post - Delete All
async function deleteAllPost() {
    try {
        const response = await fetch("/admin_api/delete_all_post", {
            method: "DELETE",
        });

        const deletePostResult = await response.json();

        const result = deletePostResult.result;
        const error = deletePostResult.error;

        if (result === 0) {
            alert(`Admin - Fail to Delete All Post : ${error}`);

            return;
        }

        console.log(`[ DEBUG ] Delete All Post : Success`);

        getAllPost();
    } catch (e) {
        console.error(`Admin - Fail to Delete All Post : ${e}`);
    }
}

// Post - Delete
async function deletePost(postId) {
    try {
        const response = await fetch(`/admin_api/delete_post/${postId}`, {
            method: "DELETE",
        });

        const deletePostResult = await response.json();

        const result = deletePostResult.result;
        const error = deletePostResult.error;

        if (result === 0) {
            alert(`Admin - Fail to Delete Post : ${error}`);

            return;
        }

        console.log(`[ DEBUG ] Delete Post ( ${postId} ) : Success`);

        getAllPost();
    } catch (e) {
        console.error(`Admin - Fail to Delete Post ( ${postId} ) : ${e}`);
    }
}

// Post - Create 100
async function createPost100() {
    try {
        const response = await fetch("/admin_api/create_post_100", {
            method: "POST",
        });

        const createPostResult = await response.json();

        const result = createPostResult.result;
        const error = createPostResult.error;

        if (result === 0) {
            alert(`Admin - Fail to Create Post 100 : ${error}`);

            return;
        }

        console.log(`[ DEBUG ] Create 100 Post : Success`);

        getAllPost();
    } catch (e) {
        console.error(`Admin - Fail to Create Post 100 : ${e}`);
    }
}
