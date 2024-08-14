function getDocumentDimensions() {
	const body = document.body;
	const html = document.documentElement;

	// Calculate the full height and width of the page, including scrollable areas
	const height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);
	const width = Math.max(body.scrollWidth, body.offsetWidth, html.clientWidth, html.scrollWidth, html.offsetWidth);

	return { width, height };
}

function setGradientHeight() {
    const body = document.body;
    const html = document.documentElement;

    // Calculate the full height of the page, including content that extends beyond the viewport
    const height = Math.max(body.scrollHeight, body.offsetHeight, html.clientHeight, html.scrollHeight, html.offsetHeight);

    // Apply the height to the body
    body.style.height = height + 'px';
}


function addDecorativeImages() {
	const documentSize = getDocumentDimensions();

    const img_density = 0.000035;
    const img_quantity = Math.floor(documentSize.width * documentSize.height * img_density);
    let imagesLoaded = 0

	for (let i = 0; i < img_quantity; i++) {
		const img = document.createElement('img');
		const imgNumber = Math.floor(Math.random() * img_count) + 1;
		img.src = `/static/imgs/${imgNumber}.png`; // Sequentially generate the image URLs

		// Randomly position the image across the entire document
		img.style.position = 'absolute';
		img.style.top = Math.random() * documentSize.height + 'px';
		img.style.left = Math.random() * documentSize.width + 'px';

		// Randomly size the image
		const size = Math.random() * 50 + 75; // Between 75px and 125px
		img.style.width = size + 'px';
		img.style.height = 'auto';

		// Randomly rotate the image
		const rotation = Math.random() * 90 - 45; // Between -45deg and 45deg
		img.style.transform = `rotate(${rotation}deg)`;

		// Set a lower z-index so images don't overlap important content
		img.style.zIndex = -1;

		// Append the image to the body
		document.body.appendChild(img);

				// Track when the image has fully loaded
		img.onload = () => {
			imagesLoaded++;
			if (imagesLoaded === img_quantity) {
				// Once all images have loaded, adjust the gradient height
				setGradientHeight();
			}
        };
	}
}

// Call the functions on page load and resize
window.onload = function() {
    addDecorativeImages();
    setGradientHeight();
};

window.onresize = setGradientHeight;
