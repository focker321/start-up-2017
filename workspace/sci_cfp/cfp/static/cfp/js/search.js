$(document).ready(function () {
    $('#sci-cfp-search-btn').click(function () {
        window.location.href = '/cfp/search?q=' + $('#sci-cfp-search-in').val();
    });

    $("#sci-cfp-search-in").bind("keypress", {}, keypressInBox);

    function keypressInBox(e) {

        var code = (e.keyCode ? e.keyCode : e.which);
        if (code == 13) { //Enter keycode                        
            e.preventDefault();
            window.location = "/cfp/search?q=" + $('#sci-cfp-search-in').val();
        }
    }
});