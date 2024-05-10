document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("create-event-form");
  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": "{{ csrf_token }}",
        },
      });
      const data = await response.json();
      if (response.ok && data.success) {
        // Show success message pop-up
        alert(data.message);
        // Redirect to a success page or do other actions as needed
        window.location.href = "/success_url";
      } else {
        // Show failure message pop-up with form errors
        let errorMessage = "Failed to create event.";
        if (data.errors) {
          errorMessage += "\n" + Object.values(data.errors).flat().join("\n");
        }
        alert(errorMessage);
      }
    } catch (error) {
      console.error("Error:", error);
      // Show error message pop-up
      alert("An error occurred. Please try again later.");
    }
  });
});
