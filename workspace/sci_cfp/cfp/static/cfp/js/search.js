$(document).ready(function() {
    $('#sci-cfp-search-btn').click(function() {
        window.location.href = '/cfp/search?q=' + $('#sci-cfp-search-in').val();
    });
});
