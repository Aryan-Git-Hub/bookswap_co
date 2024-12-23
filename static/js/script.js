let logout = document.getElementsByClassName("logout");
for (let index = 0; index < logout.length; index++) {
    logout[index].addEventListener("click", () => {
      let logout_user_bool = confirm("Are you sure, You wanna logout?");
      if (logout_user_bool === true) {
        location.href = "/accounts/logout/";
      }
    });
}
