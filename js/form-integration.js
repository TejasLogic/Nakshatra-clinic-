(function () {
  const API_ENDPOINT =
    "https://www.forms.thedigitechsolutions.com/api/forms/submit/09f77c2c-a501-4b0b-b96d-552efe7145d5";

  function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;

    // Check for validity
    if (form.checkValidity && !form.checkValidity()) {
      // If browser validation fails, we stop here.
      // reportValidity shows the browser's native error bubbles.
      form.reportValidity();
      return;
    }

    // Find submit button
    const submitButton = form.querySelector(
      'button[type="submit"], input[type="submit"], button:not([type]), #realSubmitBtn'
    );
    const originalButtonText = submitButton ? submitButton.innerText : "";

    if (submitButton) {
      submitButton.disabled = true;
      // Only change text if it's not an icon-only button and has text
      if (submitButton.innerText.trim().length > 0) {
        submitButton.setAttribute("data-original-text", originalButtonText);
        submitButton.innerText = "Sending...";
      }
    }

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    fetch(API_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (response.ok) {
          form.reset();
          // Track Meta Pixel Lead event
          // Track Meta Pixel Lead event
          if (typeof window.fbq === "function") {
            window.fbq("track", "Lead");
            console.log("Meta Pixel Lead event triggered successfully");
          } else {
            console.warn(
              "Meta Pixel Lead event NOT triggered: window.fbq is not a function"
            );
          }
          showMessage(form, "Message Sent Successfully!", "success");
        } else {
          showMessage(form, "Submission failed. Please retry.", "error");
        }
      })
      .catch((error) => {
        console.error("Form submission error:", error);
        showMessage(
          form,
          "Error submitting form. Please try again later.",
          "error"
        );
      })
      .finally(() => {
        if (submitButton) {
          submitButton.disabled = false;
          if (submitButton.getAttribute("data-original-text")) {
            submitButton.innerText =
              submitButton.getAttribute("data-original-text");
          }
        }
      });
  }

  function showMessage(form, message, type) {
    let msgContainer = form.querySelector("#msgSubmit");

    // If not found by ID, look for class or create one
    if (!msgContainer) {
      // Some forms might use a different ID or structure?
      // Based on files seen, #msgSubmit is common.
      // If not present, append to form end.
      msgContainer = document.createElement("div");
      msgContainer.id = "msgSubmit";
      msgContainer.className = "h3 hidden"; // Maintain existing classes if possible
      form.appendChild(msgContainer);
    }

    msgContainer.innerText = message;
    // Ensure visibility
    msgContainer.classList.remove("hidden", "d-none");
    msgContainer.style.display = "block";

    // Apply coloring classes based on bootstrap/custom css
    msgContainer.classList.remove("text-success", "text-danger");
    if (type === "success") {
      msgContainer.classList.add("text-success");
    } else {
      msgContainer.classList.add("text-danger");
    }
  }

  function init() {
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
      // Remove Action Attribute
      form.removeAttribute("action");

      // We need to ensure our listener is attached.
      // Since we are loading this script, we can just attach it.
      // If other scripts attach listeners, multiple might run.
      // Ideally we remove others, but without nuking logic it's hard.
      // However, modifying function.js will remove the main conflicting ones.

      form.addEventListener("submit", handleFormSubmit);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
