
// ! bookmark button basically contains this code
// ! we implement this launcher to allow any updates that can be made to bookmarklet code itself

(function() {
  if (!window.bookmarklet) {
    const bookmarklet_js = document.body.appendChild(document.createElement('script'));
    // ! ?r= random is used to prevent loading from cache
    // ! this makes sure to load updated bookmarklet in case of it has been previously loaded
    bookmarklet_js.src = '//127.0.0.1:8000/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 9999999999999999);
    bookmarklet_js.onload = () => {
      window.bookmarklet = true;
    };
  } else {
    bookmarkletLaunch();
  }
})();
