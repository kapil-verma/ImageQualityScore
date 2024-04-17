function alterImages() {
    clearTimeout(timer);
    var accommodations = document.querySelectorAll("[data-testid='accommodation-list-element']");
    accommodations.forEach(function(accommodation) {
        var accommodationId = accommodation.getAttribute('data-accommodation');
        console.log("accommodationId: " + accommodationId);
        var mainImage = accommodation.querySelector("[data-testid='accommodation-main-image']");
        mainImage.src = "https://cdn.pixabay.com/photo/2024/03/15/22/12/ai-generated-8635876_1280.png";
    });
}

let timer = null;
const observer = new MutationObserver(() => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(alterImages, 3000);
});

if (window.location.href.includes("&optilens"))
    observer.observe(document, { childList: true, subtree: true });

