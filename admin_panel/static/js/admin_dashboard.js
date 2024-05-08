$(document).ready(function () {
  // Get the current URL path
  var path = window.location.pathname;

  // Check if the current page is within the Events section
  if (path.includes("/events/")) {
    // Add the 'active' class to the Events sidebar option
    $(".side-menu.top li").removeClass("active"); // Remove active class from all sidebar options
    $(".side-menu.top li").each(function () {
      if ($(this).find("a").attr("href") === '{% url "admin_panel:events" %}') {
        $(this).addClass("active");
      }
    });
  }
});
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

    // Check if the sidebar is currently hidden before toggling
    if (isSidebarHidden) {
      sidebar.classList.toggle("hide");
      isSidebarHidden = !isSidebarHidden;
    }

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
