const enlargedImageContainer = document.getElementById("enlarged-image-container");
const enlargedImage = document.getElementById("enlarged-image");
const closeBtn = document.getElementById("close-btn");
const images = document.querySelectorAll("img.opener"); // This will select all the images with the 'opener' class.

function openImage(src) {
    enlargedImageContainer.style.display = "flex";
    enlargedImage.src = src;
}

function closeImage() {
    enlargedImageContainer.style.display = "none";
}

images.forEach((image) => {
    image.addEventListener("click", () => {
        openImage(image.src);
    });
});

closeBtn.addEventListener("click", closeImage);

// Close the enlarged image when clicking outside the image
enlargedImageContainer.addEventListener("click", (event) => {
    if (event.target === enlargedImage) {
        return;
    }
    closeImage();
});

// Close the enlarged image when pressing the Escape key
document.addEventListener("keydown", (event) => {
    if (enlargedImageContainer.style.display === "flex" && event.key === "Escape") {
        closeImage();
    }
});