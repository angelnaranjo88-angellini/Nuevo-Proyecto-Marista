document.addEventListener("DOMContentLoaded", () => {
  const header = document.getElementById("site-header");
  const navToggle = document.getElementById("nav-toggle");
  const mainNav = document.getElementById("main-nav");
  const yearEl = document.getElementById("year");

  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const onScroll = () => {
    if (window.scrollY > 8) header.classList.add("scrolled");
    else header.classList.remove("scrolled");
  };
  onScroll();
  window.addEventListener("scroll", onScroll);

  navToggle.addEventListener("click", () => {
    const isOpen = mainNav.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
    navToggle.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
  });

  mainNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mainNav.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });

  document.querySelectorAll(".faq-question").forEach((btn) => {
    btn.addEventListener("click", () => {
      const item = btn.closest(".faq-item");
      const answer = item.querySelector(".faq-answer");
      const isOpen = btn.getAttribute("aria-expanded") === "true";

      document.querySelectorAll(".faq-question").forEach((otherBtn) => {
        if (otherBtn !== btn) {
          otherBtn.setAttribute("aria-expanded", "false");
          otherBtn.closest(".faq-item").querySelector(".faq-answer").style.maxHeight = null;
        }
      });

      btn.setAttribute("aria-expanded", String(!isOpen));
      answer.style.maxHeight = isOpen ? null : answer.scrollHeight + "px";
    });
  });

  const form = document.getElementById("booking-form");
  const successBox = document.getElementById("form-success");

  const todayInput = document.getElementById("fecha");
  if (todayInput) {
    todayInput.min = new Date().toISOString().split("T")[0];
  }

  const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  const isValidPhone = (value) => /^[0-9()+\-\s]{7,}$/.test(value);

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    let valid = true;

    const fields = [
      { el: document.getElementById("nombre"), check: (v) => v.trim().length > 1 },
      { el: document.getElementById("telefono"), check: isValidPhone },
      { el: document.getElementById("email"), check: isValidEmail },
      { el: document.getElementById("servicio"), check: (v) => v !== "" },
      { el: document.getElementById("fecha"), check: (v) => v !== "" },
    ];

    fields.forEach(({ el, check }) => {
      const wrapper = el.closest(".form-row") || el.parentElement;
      const passed = check(el.value);
      wrapper.classList.toggle("invalid", !passed);
      if (!passed) valid = false;
    });

    if (!valid) return;

    successBox.classList.add("visible");
    form.reset();
    setTimeout(() => successBox.classList.remove("visible"), 6000);
  });
});
