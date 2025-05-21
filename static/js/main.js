document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
          behavior: 'smooth'
      });
  });
});

// Add active state to current navigation item
document.addEventListener('DOMContentLoaded', function() {
  const currentLocation = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
      if (link.getAttribute('href') === currentLocation) {
          link.classList.add('active');
      }
  });
});

window.showUploadForm = function() {
    const uploadFormContainer = document.getElementById('uploadFormContainer');
    if (uploadFormContainer) {
        uploadFormContainer.classList.toggle('hidden');
    } else {
        console.error("Upload form container not found.");
    }
};