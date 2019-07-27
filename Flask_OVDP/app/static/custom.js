$(document).ready(function() {
    $('li.active').removeClass('active');
    $('a[href="' + location.pathname + '"]').closest('li').addClass('active');

    $('a').removeClass('active');
    $('a[href="' + location.pathname + '"]').closest('a').addClass('active');
});
