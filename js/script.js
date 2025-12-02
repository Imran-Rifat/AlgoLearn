// =======================
// NAVBAR & ACCOUNT PANEL
// =======================

const navbar      = document.querySelector('.header .navbar');
const accountForm = document.querySelector('.account-form');

const menuBtn     = document.querySelector('#menu-btn');
const closeNavbar = document.querySelector('#close-navbar');
const accountBtn  = document.querySelector('#account-btn');
const closeForm   = document.querySelector('#close-form');

if (menuBtn && navbar) {
  menuBtn.onclick = () => {
    navbar.classList.add('active');
  };
}

if (closeNavbar && navbar) {
  closeNavbar.onclick = () => {
    navbar.classList.remove('active');
  };
}

if (accountBtn && accountForm) {
  accountBtn.onclick = () => {
    accountForm.classList.add('active');
  };
}

if (closeForm && accountForm) {
  closeForm.onclick = () => {
    accountForm.classList.remove('active');
  };
}

// =======================
// SLIDERS
// =======================

// Home hero slider
if (document.querySelector('.home-slider')) {
  var homeSwiper = new Swiper(".home-slider", {
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    loop: true,
    grabCursor: true,
  });
}

// Home courses slider (only if used)
if (document.querySelector('.home-courses-slider')) {
  var coursesSwiper = new Swiper(".home-courses-slider", {
    loop: true,
    grabCursor: true,
    spaceBetween: 20,
    breakpoints: {
      0:   { slidesPerView: 1 },
      768: { slidesPerView: 2 },
      991: { slidesPerView: 3 },
    },
  });
}

// Reviews slider
if (document.querySelector('.reviews-slider')) {
  var reviewSwiper = new Swiper(".reviews-slider", {
    loop: true,
    grabCursor: true,
    spaceBetween: 20,
    breakpoints: {
      0:   { slidesPerView: 1 },
      768: { slidesPerView: 2 },
      991: { slidesPerView: 3 },
    },
  });
}

// =======================
// INLINE COURSE EXPAND INFO
// =======================
document.querySelectorAll('.show-info').forEach(btn => {
  btn.addEventListener('click', function () {
    const infoBox = document.getElementById(this.dataset.target);
    if (!infoBox) return;

    if (infoBox.style.display === "block") {
      infoBox.style.display = "none";
      this.textContent = "read more";
    } else {
      infoBox.style.display = "block";
      this.textContent = "show less";
    }
  });
});

// =======================
// GREETING FROM LOGIN DATA
// =======================

const userGreeting = document.getElementById("user-greeting");

(function updateGreeting() {
  const loggedInUser = JSON.parse(localStorage.getItem("algolearn_user") || "null");
  const isLoggedIn   = localStorage.getItem("isLoggedIn") === "true";

  if (userGreeting && isLoggedIn && loggedInUser && loggedInUser.username) {
    userGreeting.textContent = "Hi, " + loggedInUser.username;
  } else if (userGreeting) {
    userGreeting.textContent = "";
  }
})();
