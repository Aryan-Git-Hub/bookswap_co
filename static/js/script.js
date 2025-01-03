// for logout()
let logout = document.getElementsByClassName("logout");
for (let index = 0; index < logout.length; index++) {
  logout[index].addEventListener("click", () => {
    // let logout_user_bool = confirm("Are you sure, You wanna logout?");
    let logout_user_bool = Swal.fire({
          title: "Are you sure?",
          text: "You will be logged out from your account",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Yes, log out!"
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire({
          title: "Logged Out!",
          text: "You are logged out from your bookswap account",
          icon: "success"
        });
        location.href = "/accounts/logout/"
      }
    });
    // if (logout_user_bool === true) {
    //   location.href = "/accounts/logout/";
    // }
  });
}


// for search_results
const search_for_1 = document.getElementById("search_for_1");
const search_for_2 = document.getElementById("search_for_2");
let search_btn = document.getElementsByClassName("search_btn");
let search_logo = document.getElementsByClassName("search_logo");



function disable_search() {
  if ((search_for_1.value == "" || search_for_1.value == null) && (search_for_2.value == "" || search_for_2 == null)) {
    for (let j = 0; j < search_btn.length; j++) {
      const element = search_btn[j];
      element.disabled = true;
    }
    for (let i = 0; i < search_logo.length; i++) {
      const element = search_logo[i];
      element.classList.remove("icon_transform");
      element.title = "Please type something to Search...";
    }
  } else {
    for (let j = 0; j < search_btn.length; j++) {
      const element = search_btn[j];
      element.disabled = false;
    }
    for (let i = 0; i < search_logo.length; i++) {
      const element = search_logo[i];
      element.classList.add("icon_transform");
      element.removeAttribute("title");
    }
  }
}
disable_search();
search_for_1.addEventListener('input', disable_search);
search_for_2.addEventListener('input', disable_search);
