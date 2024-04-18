var imageData;

function alterImages() {
    clearTimeout(timer);

    var accommodations = document.querySelectorAll("[data-testid='accommodation-list-element']");
    accommodations.forEach(function (accommodation) {
        var accommodationId = accommodation.getAttribute('data-accommodation');

        imageData.accommodations.forEach(imageData => {
            if (imageData.id == accommodationId) {
                var mainImage = accommodation.querySelector("[data-testid='accommodation-main-image']");
                mainImage.src = imageData.heroImage;

                var galleryImages = accommodation.querySelectorAll("[data-testid='tile-gallery-image-container'] img");
                galleryImages.forEach(function (galleryImage, index) {
                    if (index < imageData.galleryImages.length) {
                        galleryImage.src = imageData.galleryImages[index];
                    }
                });
            }
        });
    });
}

let timer = null;
if (window.location.href.includes("&optilens_")) {
    console.log("Optilens active");
    var dataUrl = null;
    if (window.location.href.includes("&optilens_nima")) {
        console.log("Using Nima data");
        dataUrl = 'https://raw.githack.com/kapil-verma/ImageQualityScore/colab/demo/data_nima.json';
    } else if (window.location.href.includes("&optilens_gemini")) {
        console.log("Using Gemini data");
        dataUrl = 'https://raw.githack.com/kapil-verma/ImageQualityScore/colab/demo/data_gemini.json';
    }
    if (dataUrl != null) {
        fetch(dataUrl).then(response => {
            if (!response.ok) throw new Error('Could not read image data file: ' + dataUrl);
            return response.json();
        }).then(data => {
            imageData = data;
            const observer = new MutationObserver(() => {
                if (timer) clearTimeout(timer);
                timer = setTimeout(alterImages, 500);
            });
            observer.observe(document, { childList: true, subtree: true });
        }).catch(error => console.error('There has been a problem with your fetch operation:', error));
    }
}