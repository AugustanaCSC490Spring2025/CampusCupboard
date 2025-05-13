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

  const fileInput = document.getElementById('fileInput');
  if (fileInput) {
      fileInput.addEventListener('change', function () {
          document.getElementById('uploadForm').submit(); // Automatically submit the form
      });
  } else {
      console.error("fileInput element not found in the DOM.");
  }
});

function triggerFileInput() {
  const fileInput = document.getElementById('imageUpload');
  fileInput.click(); // Trigger the hidden file input

  fileInput.addEventListener('change', function () {
      // Automatically submit the form when a file is selected
      document.getElementById('uploadForm').submit();
  });
}

function showUploadForm() {
  const uploadFormContainer = document.getElementById('uploadFormContainer');
  if (uploadFormContainer) {
      uploadFormContainer.classList.toggle('hidden'); // Toggle visibility of the upload form
  } else {
      console.error("Upload form container not found.");
  }
}

function addImage() {
  const imageInput = document.getElementById('imageInput');
  const descriptionInput = document.getElementById('descriptionInput');
  const uploadedImagesContainer = document.getElementById('uploadedImagesContainer');

  if (imageInput.files.length === 0) {
      alert("Please select an image.");
      return;
  }

  if (!descriptionInput.value.trim()) {
      alert("Please enter a description.");
      return;
  }

  // Create a new image container
  const imageContainer = document.createElement('div');
  imageContainer.classList.add('image-container');

  // Create the image element
  const img = document.createElement('img');
  img.src = URL.createObjectURL(imageInput.files[0]); // Use a temporary URL for the uploaded image
  img.alt = "Uploaded Image";
  img.style.maxWidth = "100%";
  img.style.borderRadius = "10px";

  // Create the description element
  const description = document.createElement('div');
  description.classList.add('image-description');
  description.innerHTML = `<p>${descriptionInput.value}</p>`;

  // Append the image and description to the image container
  imageContainer.appendChild(img);
  imageContainer.appendChild(description);

  // Append the image container to the uploaded images container
  uploadedImagesContainer.appendChild(imageContainer);

  // Clear the form inputs
  imageInput.value = "";
  descriptionInput.value = "";

  // Hide the upload form
  document.getElementById('uploadFormContainer').classList.add('hidden');
}

document.getElementById('messageForm').addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent the default form submission

  const formData = new FormData(this);
  fetch(this.action, {
      method: 'POST',
      body: formData
  })
  .then(response => response.text())
  .then(data => {
      // Update the message list dynamically
      const messageList = document.getElementById('messageList');
      const newMessage = document.createElement('li');
      newMessage.innerHTML = `
          <div class="message-text">${formData.get('message')}</div>
          <div class="message-timestamp">${new Date().toLocaleString()}</div>
      `;
      messageList.appendChild(newMessage);

      // Clear the input field
      document.getElementById('messageInput').value = '';
  })
  .catch(error => console.error('Error:', error));
});