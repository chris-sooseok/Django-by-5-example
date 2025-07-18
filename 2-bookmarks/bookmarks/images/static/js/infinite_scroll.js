export function initInfiniteScroll() {
    let page = 1;
    let emptyPage = false;
    let blockRequest = false;
    // ? attach event listener to scroll
    window.addEventListener('scroll', function (e) {
        // ? total scrollable distance on page = document.body.clientHeight - window.innerHeight
        // ? start loading before the user hits the bottom = - 200
        let margin = document.body.clientHeight - window.innerHeight - 200;
        if (window.pageYOffset > margin && !emptyPage && !blockRequest) {
            // ? prevents additional HTTP requests from scroll event
            blockRequest = true;
            page += 1;
            fetch('?images_only=1&page=' + page)
                .then(response => response.text())
                .then(html => {
                    if (html === '') {
                        emptyPage = true;
                    } else {
                        let imageList = document.getElementById('image-list');
                        imageList.insertAdjacentHTML('beforeEnd', html);
                        blockRequest = false;
                    }
                })
        }
    });
    // initial scroll event when the page is loaded
    window.dispatchEvent(new Event('scroll'));
}
