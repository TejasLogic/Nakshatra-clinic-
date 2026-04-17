
import os

files = [
    r"d:\new-nakshatra\nakshatra-website\index.html",
    r"d:\new-nakshatra\nakshatra-website\contact.html",
    r"d:\new-nakshatra\nakshatra-website\book-appointment.html",
    r"d:\new-nakshatra\nakshatra-website\appointment-page.html"
]

inline_script = """  <script>
    (function () {
      const API_ENDPOINT = "https://www.forms.thedigitechsolutions.com/api/forms/submit/09f77c2c-a501-4b0b-b96d-552efe7145d5";

      function handleFormSubmit(event) {
        event.preventDefault();
        const form = event.target;

        // Check for validity
        if (form.checkValidity && !form.checkValidity()) {
          form.reportValidity();
          return;
        }

        const submitButton = form.querySelector('button[type="submit"], input[type="submit"], button:not([type]), #realSubmitBtn');
        const originalButtonText = submitButton ? submitButton.innerText : "";

        if (submitButton) {
          submitButton.disabled = true;
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
              if (typeof window.fbq === "function") {
                window.fbq("track", "Lead");
                console.log("Meta Pixel Lead event triggered successfully");
              } else {
                console.warn("Meta Pixel Lead event NOT triggered: window.fbq is not a function");
              }
              showMessage(form, "Message Sent Successfully!", "success");
            } else {
              showMessage(form, "Submission failed. Please retry.", "error");
            }
          })
          .catch((error) => {
            console.error("Form submission error:", error);
            showMessage(form, "Error submitting form. Please try again later.", "error");
          })
          .finally(() => {
            if (submitButton) {
              submitButton.disabled = false;
              if (submitButton.getAttribute("data-original-text")) {
                submitButton.innerText = submitButton.getAttribute("data-original-text");
              }
            }
          });
      }

      function showMessage(form, message, type) {
        let msgContainer = form.querySelector("#msgSubmit");
        if (!msgContainer) {
          msgContainer = document.createElement("div");
          msgContainer.id = "msgSubmit";
          msgContainer.className = "h3 hidden";
          form.appendChild(msgContainer);
        }
        msgContainer.innerText = message;
        msgContainer.classList.remove("hidden", "d-none");
        msgContainer.style.display = "block";
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
          form.removeAttribute("action");
          form.removeEventListener("submit", handleFormSubmit);
          form.addEventListener("submit", handleFormSubmit);
        });
      }

      if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
      } else {
        init();
      }
    })();
  </script>
</body>"""

for filepath in files:
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove external script reference
            if '<script src="js/form-integration.js"></script>' in content:
                content = content.replace('<script src="js/form-integration.js"></script>', '')
                print(f"Removed external script from {filepath}")
            
            # Remove any previously existing matching inline script (naively)
            # Or just replace the body closing tag with the script + body closing tag
            if "const API_ENDPOINT" in content and "handleFormSubmit" in content:
                 print(f"Inline script seems to already exist in {filepath}, replacing it...")
                 # Regex to remove old inline script block if present?
                 # ideally we find the block and replace it.
                 # Let's clean up old appended scripts if they exist at the end
                 import re
                 content = re.sub(r'<script>\s*\(function\s*\(\)\s*\{.*?\}\)\(\);\s*</script>\s*</body>', '</body>', content, flags=re.DOTALL)

            # Append new inline script
            content = content.replace('</body>', inline_script)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added inline script to {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
