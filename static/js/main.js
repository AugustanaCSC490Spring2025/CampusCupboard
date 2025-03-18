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

function triggerFileInput() {
    const fileInput = document.getElementById('imageUpload');
    fileInput.click(); // Trigger the hidden file input

    fileInput.addEventListener('change', function () {
        // Automatically submit the form when a file is selected
        document.getElementById('uploadForm').submit();
    });
}
