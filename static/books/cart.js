// for post request, using of fetch API
function data_options(inc_or_dec_or_rem, book_id, qty) {
    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    let options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken":csrf_token
        },
        body: JSON.stringify({
            // data
            inc_or_dec_or_rem:inc_or_dec_or_rem,
            book_id:book_id,
            qty:qty
        }),
    };
    return options;
}

const cart_val = document.getElementById("cart_val")

async function increaseQuantity(element, book_id, qty) {
  const response = await fetch(window.location.href, data_options("increaseQuantity", book_id, qty));
  let data = await response.json();
  const input = element.previousElementSibling;
  res = data.response;
  input.value = res;
  cart_val.innerHTML = Number(cart_val.innerHTML)+1;
}


async function decreaseQuantity(element, book_id, qty) {
  const response = await fetch(window.location.href, data_options("decreaseQuantity", book_id, qty));
  let data = await response.json();
  const input = element.nextElementSibling;
  res = data.response;
  cart_val.innerHTML = Number(cart_val.innerHTML)-1;
  if(res<=0) {
    const row = element.closest('tr');
    row.remove();
  }
  input.value = res;
}
