var imageData = {
    "accommodations": [
        {
            "id": 6365,
            "heroImage": "https://cdn.pixabay.com/photo/2024/03/15/22/12/ai-generated-8635876_1280.png",
            "galleryImages": [
                "https://cdn.pixabay.com/photo/2017/07/20/03/52/chicken-2521141_1280.png",
                "https://cdn.pixabay.com/photo/2017/07/20/03/52/chicken-2521141_1280.png"
            ]
        }
    ]
};

function alterImages() {
    clearTimeout(timer); 

    fetch('https://raw.githubusercontent.com/json-iterator/test-data/master/large-file.json')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

    var accommodations = document.querySelectorAll("[data-testid='accommodation-list-element']");
    accommodations.forEach(function(accommodation) {
        var accommodationId = accommodation.getAttribute('data-accommodation');

        imageData.accommodations.forEach(imageData => {
            if (imageData.id == accommodationId) {
                console.log('New image data for ' + accommodationId);
                var mainImage = accommodation.querySelector("[data-testid='accommodation-main-image']");
                mainImage.src = imageData.heroImage;

                var galleryImages = accommodation.querySelectorAll("[data-testid='grid-image'] img");
                galleryImages.forEach(function(galleryImage, index) {
                    if (index < imageData.galleryImages.length) {
                        galleryImage.src = imageData.galleryImages[index];
                    }
                });
            }
        });
    });
}

let timer = null;
const observer = new MutationObserver(() => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(alterImages, 500);
});

if (window.location.href.includes("&optilens")) {
    observer.observe(document, { childList: true, subtree: true });
}