const sidebarToggle = document.querySelector("#content nav .bx.bx-menu");
const sidebar = document.getElementById("sidebar");
const sidebarItems = document.querySelectorAll("#sidebar .side-menu.top li a");

// Flag to track sidebar visibility
let isSidebarHidden = false;

// Toggle sidebar on menu bar click
sidebarToggle.addEventListener("click", () => {
  sidebar.classList.toggle("hide");
  isSidebarHidden = !isSidebarHidden;
});

// Add click event listener to sidebar items
sidebarItems.forEach((item) => {
  item.addEventListener("click", (e) => {
    // Prevent default link behavior
    e.preventDefault();

    // Remove active class from all sidebar items
    sidebarItems.forEach((i) => i.parentElement.classList.remove("active"));

    // Add active class to the clicked sidebar item
    item.parentElement.classList.add("active");

    // Navigate to the respective page
    const href = item.getAttribute("href");
    window.location.href = href;
  });
});

// Close sidebar when clicking outside
document.addEventListener("click", (e) => {
  const isClickInsideSidebar = sidebar.contains(e.target);
  const isClickInsideToggle = sidebarToggle.contains(e.target);
  const isClickInsideEvent = e.target.closest(".events");

  // If clicked outside sidebar and toggle, hide the sidebar
  if (!isClickInsideSidebar && !isClickInsideToggle && !isClickInsideEvent) {
    sidebar.classList.add("hide");
    isSidebarHidden = true;
  }
});

// JavaScript code for enabling multi-select functionality
var select = document.getElementById("events_attending");
select.addEventListener("change", function () {
  // Count the number of selected options
  var selectedCount = select.selectedOptions.length;
  // If more than one option is selected, allow multiple selection
  if (selectedCount > 1) {
    select.setAttribute("multiple", "multiple");
  } else {
    // If only one option is selected, disable multiple selection
    select.removeAttribute("multiple");
  }
});

// Get the modals and their elements
var errorModal = document.getElementById("errorModal");
var successModal = document.getElementById("successModal");
var spans = document.getElementsByClassName("close");
var errorMessage = document.getElementById("errorMessage");
var successMessage = document.getElementById("successMessage");

// When the user clicks on the close button, close the modal
for (var i = 0; i < spans.length; i++) {
  spans[i].onclick = function () {
    errorModal.style.display = "none";
    successModal.style.display = "none";
  };
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == errorModal) {
    errorModal.style.display = "none";
  } else if (event.target == successModal) {
    successModal.style.display = "none";
  }
};

// Function to show the error modal
function showErrorModal(message) {
  errorMessage.textContent = message;
  errorModal.style.display = "block";
}

// Function to show the success modal
function showSuccessModal(message) {
  successMessage.textContent = message;
  successModal.style.display = "block";
}
