// for logout()
let logout = document.getElementsByClassName("logout");
for (let index = 0; index < logout.length; index++) {
    logout[index].addEventListener("click", () => {
      let logout_user_bool = confirm("Are you sure, You wanna logout?");
      if (logout_user_bool === true) {
        location.href = "/accounts/logout/";
      }
    });
}


// for search_results
const search_for = document.getElementsByName("search_for");
const search_btn = document.getElementById("search_btn");
const search_logo = document.getElementById("search_logo");
if (search_for.value=="" || search_for.value==null) {
    search_btn.disabled==true;
    search_logo.classList.remove("search_logo_transform");
    console.log("Hello")
} else {
    search_btn.disabled==false;
    search_logo.classList.add("search_logo_transform");
}