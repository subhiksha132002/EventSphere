document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".increment-btn").forEach((button) => {
    button.addEventListener("click", function () {
      let quantityInput = this.previousElementSibling;
      let currentValue = parseInt(quantityInput.value);
      quantityInput.value = currentValue + 1;
    });
  });

  document.querySelectorAll(".decrement-btn").forEach((button) => {
    button.addEventListener("click", function () {
      let quantityInput = this.nextElementSibling;
      let currentValue = parseInt(quantityInput.value);
      if (currentValue > 0) {
        quantityInput.value = currentValue - 1;
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Get the quantity input field and buttons
  const quantityInput = document.getElementById("quantity");
  const incrementBtn = document.querySelector(".increment-btn");
  const decrementBtn = document.querySelector(".decrement-btn");
  const registrationQuantityInput = document.getElementById(
    "registration_quantity"
  );

  // Event listener for increment button
  incrementBtn.addEventListener("click", function () {
    quantityInput.value = parseInt(quantityInput.value) + 1;
    updateRegistrationQuantity();
  });

  // Event listener for decrement button
  decrementBtn.addEventListener("click", function () {
    if (parseInt(quantityInput.value) > 0) {
      quantityInput.value = parseInt(quantityInput.value) - 1;
      updateRegistrationQuantity();
    }
  });

  function updateRegistrationQuantity() {
    const quantityInput = document.getElementById("quantity");
    const registrationQuantityInput = document.getElementById(
      "registration_quantity"
    );
    registrationQuantityInput.value = quantityInput.value;
  }
});
