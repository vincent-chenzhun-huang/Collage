(function () {
    if (window.mybookmarklet !== undefined){
        mybookmarklet();
    }
    else{
        document.body.appendChild(document.createElement('script')).src='http://127.0.0.1:8000/static/js/bookmarklet.js';
    }
})();