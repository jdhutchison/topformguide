$(document).ready(function() {
    $('tbody').on('mouseenter', 'td', function(event) {
        $(event.target.parentNode).addClass('hover');
    });
    $('tbody').on('mouseout', 'td', function(event) {
        $(event.target.parentNode).removeClass('hover');
    });
    $('tbody').on('click', 'tr', function(event) {
        window.location = '/car/' + event.target.parentNode.dataset.carid;
    });
});