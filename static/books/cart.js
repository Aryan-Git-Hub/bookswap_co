// for post request, using of fetch API
function data_options(inc_or_dec_or_rem, book_id, total_price, qty = 0) {
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
            total_price:total_price,
            qty:qty
        }),
    };
    return options;
}


const cart_val = document.getElementById("cart_val");
const total_price = document.getElementById("total-price");


// to delete book from cart
async function deleteBook(element, book_id) {
  response = await fetch(window.location.href, data_options("deleteBook", book_id, total_price.innerText));
  let data = await response.json();
  cart_val.innerHTML = Number(cart_val.innerHTML)-1;
  const row = element.closest('.cart-details');
  row.remove();
  total_price.innerText = data.total_price;
  // if cart is empty
  if(cart_val.innerHTML==0){
    const cart_items_container = document.getElementById("cart_items_container");
    const total_price_container = document.getElementById("total_price_container");
    cart_items_container.innerHTML = `<p class="empty-cart">Your cart is empty. Explore amazing books on <span class="highlight">Book Swap</span>!</p>`;
    total_price_container.innerHTML = "";
  }
}



// // to increase quantity
// async function increaseQuantity(element, book_id, qty) {
//   const response = await fetch(window.location.href, data_options("increaseQuantity", book_id, total_price.innerText, qty));
//   let data = await response.json();
//   const input = element.previousElementSibling;
//   res = data.qty;
//   input.value = res;
//   cart_val.innerHTML = Number(cart_val.innerHTML)+1;
//   total_price.innerText = data.total_price
// }

// // to decrease quantity
// async function decreaseQuantity(element, book_id, qty) {
//   const response = await fetch(window.location.href, data_options("decreaseQuantity", book_id, total_price.innerText, qty));
//   let data = await response.json();
//   const input = element.nextElementSibling;
//   res = data.qty;
//   cart_val.innerHTML = Number(cart_val.innerHTML)-1;
//   if(res<=0) {
//     const row = element.closest('tr');
//     row.remove();
//   }
//   input.value = res;
//   total_price.innerText = data.total_price
// }

