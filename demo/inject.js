var imageData;

function getHeroUrl(accommodationId) {
    var filteredJson = imageData.filter(item => item.hotel_name == accommodationId);
    if (filteredJson.length == 0) return "";
    return filteredJson[0].image_url
}

function getGalleryUrls(accommodationId) {
    var filteredJson = imageData.filter(item => item.hotel_name == accommodationId);
    var galleryImages = [];
    var itemUrls = filteredJson.slice(1).map(item => item.image_url);
    galleryImages.push(...itemUrls);
    return galleryImages
}

function alterImages() {
    clearTimeout(timer);

    var accommodations = document.querySelectorAll("[data-testid='accommodation-list-element']");
    accommodations.forEach(function (accommodation) {
        var accommodationId = accommodation.getAttribute('data-accommodation');
        heroImage = getHeroUrl(accommodationId);
        if (heroImage != "") {
            var mainImage = accommodation.querySelector("[data-testid='accommodation-main-image']");
            mainImage.src = heroImage;

            var galleryImages = accommodation.querySelectorAll("[data-testid='tile-gallery-image-container'] img");
            var galleryUrls = getGalleryUrls(accommodationId);
            if (galleryUrls.length > 0) {
                galleryImages.forEach(function (galleryImage, i) {
                    if (i < galleryUrls.length) {
                        galleryImage.src = galleryUrls[i]
                    }
                });
            }
        }
        console.log(heroImage);
    });
}

let timer = null;
if (window.location.href.includes("&optilens_")) {
    console.log("Optilens active");
    var dataUrl = null;
    if (window.location.href.includes("&optilens_nima")) {
        console.log("Using NIMA data");
        dataUrl = 'https://raw.githack.com/kapil-verma/ImageQualityScore/colab/demo/data_nima.json';
    } else if (window.location.href.includes("&optilens_trinima")) {
        console.log("Using triNIMA data");
        dataUrl = 'https://raw.githack.com/kapil-verma/ImageQualityScore/colab/demo/data_trinima.json';
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