

// ? adding link into head to load css file that styles bookarklet
const minWidth = 250;
const minHeight = 250;
let link = document.createElement('link'); // Create new link Element
link.rel = 'stylesheet'; // set the attributes for link element
link.type = 'text/css';
// ? '?r=' r stands for random is used to prevent from loading a cached version file
const siteUrl = '//127.0.0.1:8000/'
link.href = siteUrl + 'static/css/bookmarklet.css?r=' + Math.floor(Math.random() * 9999999999999999);
let head = document.getElementsByTagName('head')[0];  // Get HTML head element
head.appendChild(link);  // Append link element to HTML head

// ? create bookmarklet and append it into body
let body = document.getElementsByTagName('body')[0];
const bookmarkletBox = `
  <div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <!-- ! below is where images found on a website will be displayed -->
    <div class="images"></div>
  </div>`;
body.innerHTML += bookmarkletBox;

// display all images found on a website and let users choose the image they want to share
function bookmarkletLaunch() {
    const bookmarklet = document.getElementById('bookmarklet');
    // selects element that has images as class
    let imagesFound = bookmarklet.querySelector('.images');
    // clear images found
    imagesFound.innerHTML = '';
    // display bookmarklet DOM element
    bookmarklet.style.display = 'block';
    // connect close event to close DOM element
    bookmarklet.querySelector('#close')
        .addEventListener('click', function () {
            bookmarklet.style.display = 'none'
        });

    // find images on a website with the minimum dimensions
    const images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"],img[src$=".png"]');
    images.forEach(image => {
        if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
            var imageFound = document.createElement('img');
            imageFound.src = image.src;
            // append each created image element into images element
            imagesFound.append(imageFound);
        }
    })

    // select image event
    imagesFound.querySelectorAll('img').forEach(image => {
        // ? for each image, add a listener
        image.addEventListener('click', function(event){
            imageSelected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteUrl + 'images/create/?url='
            + encodeURIComponent(imageSelected.src)
            + '&title='
            + encodeURIComponent(document.title),
                '_blank');
        })
    })
}

// launch the bookmkarklet
bookmarkletLaunch();