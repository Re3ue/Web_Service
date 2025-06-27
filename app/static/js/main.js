let allPost = [];

const postsPerPage = 10;
const pagesPerGroup = 10;

let currentPage = 1;
let currentPageGroup = 1;

let allPostCount = 0;
let allPageCount = 0;
let allGroupCount = 0;

document.addEventListener("DOMContentLoaded", async () => {
    // Get All Post
    getAllPost();

    // Event of "Search" Button => Search Post
    const searchButtonHTML = document.querySelector(".search_button").addEventListener("click", searchPost);
})

async function getAllPost() {
    try {
        const response = await fetch("/api/get_all_post");
        const getAllPostResult = await response.json();

        const result = getAllPostResult.result;
        allPost = getAllPostResult.all_post;
        const error = getAllPostResult.error;

        if (result === 0) {
            alert(`Fail to Get All Post : ${error}`);

            return;
        }

        renderAllPost(currentPage)
    } catch (e) {
        console.error(`Fail to Get All Post : ${e}`);
    }
}

function renderAllPost(currentPage) {
    const allPostHTML = document.querySelector(".all_post");
    allPostHTML.innerHTML = "";

    allPostCount = allPost.length;
    allPageCount = Math.ceil(allPostCount / postsPerPage);
    allGroupCount = Math.ceil(allPageCount / pagesPerGroup);

    const startPost = (currentPage - 1) * postsPerPage;
    const endPost = startPost + postsPerPage;
    const posts = allPost.slice(startPost, endPost); // Get Posts ( Current Page )

    if (posts.length == 0) {
        allPostHTML.innerHTML = "<div>Not Exist : All Post</div>"

        return;
    }

    // Render : Page
    posts.forEach(postElement => {
        const div = document.createElement("div");

        div.className = "all_post_element_container";
        div.innerHTML = `
            <div class="all_post_element_title">
                <a href="/post/${postElement.post_id}">${postElement.post_title}</a>
            </div>
            <div class="all_post_element_content">${postElement.post_content}</div>
            <div class="all_post_element_information">Date : ${postElement.post_date} | Up Vote : ${postElement.post_upvote}</div>
        `;

        allPostHTML.appendChild(div);
    });

    renderAllPage(allPageCount, allGroupCount)
}

function renderAllPage(allPageCount, allGroupCount) {
    const allPageHTML = document.querySelector(".all_page");
    allPageHTML.innerHTML = "";

    const startPage = (currentPageGroup - 1) * pagesPerGroup + 1;
    const endPage = Math.min(startPage + pagesPerGroup, allPageCount);

    for (let i = startPage; i < endPage + 1; i++) {
        const button = document.createElement("button");

        button.textContent = i;

        if (i == currentPage) {
            button.style.fontWeight = "bold";
        }

        // Event => Render : Page
        button.onclick = () => {
            currentPage = i;

            renderAllPost(currentPage);
        }

        allPageHTML.appendChild(button);
    }
}

// Event : Previous Button
function previousPage() {
    if (currentPage > 1) {
        currentPage--;

        if (currentPage % pagesPerGroup === 0) {
            currentPageGroup--;
        }

        renderAllPost(currentPage);
    }
}

// Event : Next Button
function nextPage() {
    if (currentPage < allPageCount) {
        currentPage++;

        if ((currentPage - 1) % pagesPerGroup === 0) {
            currentPageGroup++;
        }

        renderAllPost(currentPage);
    }
}

// Search
async function searchPost() {
    const searchInput = document.querySelector(".search_input").value;

    try {
        const response = await fetch(`/api/search_post?search_input=${encodeURIComponent(searchInput)}`);
        const searchPostResult = await response.json();

        const result = searchPostResult.result;
        searchPost = searchPostResult.search_post;
        const error = searchPostResult.error;

        if (result === 0) {
            alert(`Fail to Search Post : ${error}`);

            return;
        }

        allPost = searchPost;

        let currentPage = 1;
        let currentPageGroup = 1;

        renderAllPost(currentPage);
    } catch (e) {
        console.error(`Fail to Search Post : ${e}`);
    }
}