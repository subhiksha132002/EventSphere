console.log("DOMContentLoaded event fired");
let quantityInput; // Define quantityInput globally

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOMContentLoaded event listener executing");
  quantityInput = document.getElementById("quantity"); // Define quantityInput here
  console.log("quantityInput:", quantityInput); // Log quantityInput to verify it's defined

  const incrementBtn = document.querySelector(".increment-btn");
  const decrementBtn = document.querySelector(".decrement-btn");
  const registrationQuantityInput = document.getElementById(
    "registration_quantity"
  );
  const ticketPrice = parseFloat(
    document.getElementById("ticket-price").innerText
  );
  const totalPriceElement = document.getElementById("total-price");
  const registrationForm = document.getElementById("registration-form");

  registrationForm.addEventListener("submit", function (event) {
    // Prevent the default form submission behavior
    event.preventDefault();
    showModal(ticketPrice);
  });

  function updateTotalPrice(quantity) {
    const totalPrice = ticketPrice * quantity;
    totalPriceElement.innerText = totalPrice.toFixed(2);
  }

  incrementBtn.addEventListener("click", function () {
    quantityInput.value = parseInt(quantityInput.value) + 1;
    updateTotalPrice(quantityInput.value);
    updateRegistrationQuantity();
  });

  decrementBtn.addEventListener("click", function () {
    if (parseInt(quantityInput.value) > 0) {
      quantityInput.value = parseInt(quantityInput.value) - 1;
      updateTotalPrice(quantityInput.value);
      updateRegistrationQuantity();
    }
  });

  quantityInput.addEventListener("input", function () {
    if (parseInt(quantityInput.value) < 0) {
      quantityInput.value = 0;
    }
    updateTotalPrice(quantityInput.value);
    updateRegistrationQuantity();
  });

  function updateRegistrationQuantity() {
    registrationQuantityInput.value = quantityInput.value;
  }
});

window.showModal = function (ticketPrice) {
  const quantity = parseInt(quantityInput.value);
  console.log("quantity:", quantity); // Log quantity to verify it's correct
  if (quantity > 0) {
    document.getElementById("total_price_modal").value = `₹${(
      ticketPrice * quantity
    ).toFixed(2)}`;
    document.getElementById("modal_quantity").value = quantity;
    // Enable the Register button
    document.querySelector(".register-btn").removeAttribute("disabled");
    // Show the modal
    $("#registrationModal").modal("show");
  }
};
