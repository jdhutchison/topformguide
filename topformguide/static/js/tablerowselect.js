$(document).ready(function() {
    $('tbody').on('mouseover', 'td', function(event) { console.log(event.target.parentNode); $(event.target.parentNone).addClass('hover'); });
    $('tbody').on('mouseout', 'td', function(event) { $(event.target.parentNode).removeClass('hover'); });
    $('tbody').on('click', 'tr', function(event) { window.location = '/car/' + event.target.parentNode.dataset.carid; });
});