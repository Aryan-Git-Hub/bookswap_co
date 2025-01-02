let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
function edit_user_posted_ad(book_id) {
  $.ajax({
    url: "/user-ads/", // Django view URL
    type: "POST",
    headers: {
      "X-CSRFToken": csrf_token, // Include CSRF token in headers
    },
    data: {
      book_id: book_id,
      action: "edit",
    },
    success: function (response) {
      $("#edit_user_posted_ad_form").html(response.form);
    },
    error: function (xhr, status, error) {
        // console.error(xhr.responseText);
    },
  });
}


$("#id_form").submit(function (e) {
  e.preventDefault();
  let form = $(this);
  let data = form.serialize();

  $.ajax({
    url: "/user-ads/", // Django view URL
    type: "POST",
    headers: {
      "X-CSRFToken": csrf_token, // Include CSRF token in headers
    },
    data: data,
    success: function (response) {
        if(response.success) location.href = "/user-ads/";
        else $("#edit_user_posted_ad_form").html(response.form);
    },
    error: function (xhr, status, error) {
      // console.error(xhr.responseText);
    },
  });
});