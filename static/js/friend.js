let searchInput = document.getElementById("search-friend");
const searchResults = document.getElementById("results");

document.addEventListener("keypress", async function (e) {
  if (e.key === "Enter") {
    const search = searchInput.value;
    if (search.length > 0) {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/search/user/${search}`,
        );
        const results = await response.json();
        searchResults.innerHTML = "";
        searchResults.innerHTML = "";
        searchResults.innerHTML += `
                <div class="search-result">
                    <img src="${results.profile_img}" alt="avatar" />
                    <p>${results.username}</p>
                    <button class="button is-link" onclick="addFriends('${results.username}')">Add to friends</button>
                </div>
            `;
      } catch (error) {
        console.error(error);
      }
    }
  }
});

async function addFriends(username) {
  console.log(username);
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/user/${username}/friends`,
      {
        method: "POST",
      },
    );

    if (response.status === 200) {
      window.location.assign("/friends");
    } else {
      window.location.assign("/");
    }
  } catch (error) {
    console.error(error);
  }
}
