document.addEventListener("DOMContentLoaded", () => {
  const emailInput = document.querySelector("#email");
  const emailStatus = document.querySelector("#email-status");

  if (!emailInput || !emailStatus) {
    return;
  }

  let lastValue = "";
  emailInput.addEventListener("input", () => {
    const email = emailInput.value.trim();
    if (!email || email === lastValue) {
      emailStatus.textContent = "";
      return;
    }
    lastValue = email;

    fetch(`/api/check-email?email=${encodeURIComponent(email)}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.exists) {
          emailStatus.textContent = "This email is already registered.";
          emailStatus.classList.add("error-text");
          emailStatus.classList.remove("success-text");
        } else {
          emailStatus.textContent = "This email is available.";
          emailStatus.classList.add("success-text");
          emailStatus.classList.remove("error-text");
        }
      })
      .catch(() => {
        emailStatus.textContent = "Unable to verify availability right now.";
        emailStatus.classList.add("error-text");
        emailStatus.classList.remove("success-text");
      });
  });
});
