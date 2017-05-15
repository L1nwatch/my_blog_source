$(document).ready(function () {
    var number_of_choices = $('.spinner').children('.choice').length;

    $('.spinner .choice').each(function (index) {
        var angle = 2 * Math.PI / number_of_choices;
        var small_angle = (Math.PI - angle) / 2;

        var radius = $('.spinner').width() / 2;

        var width = Math.ceil(radius * Math.sin(angle) / Math.sin(small_angle));
        var triangle_height = Math.ceil(radius * Math.sin(small_angle));

        var hue = 360 / number_of_choices * index;
        var color = 'hsl(' + hue + ', 80%, 70%)';

        $(this).css({
            'left': (radius - width / 2) + 'px',
            'background': color,
            'width': width + 'px',
            'height': (radius - triangle_height) + 'px',
            'transform-origin': width / 2 + 'px ' + radius + 'px',
            'transform': 'rotate(' + (angle * 180 / Math.PI * index) + 'deg)'
        });

        $(this).children('span').css({
            'top': (radius - triangle_height - 5) + 'px',
            'border-top-color': color,
            'border-width': triangle_height + 'px ' + width / 2 + 'px 0px ' + width / 2 + 'px '
        });
    });

    $('button#id_spin_me').click(function () {
        spin();
    });

});

function spin() {

    var number_of_choices = $('.spinner').children('.choice').length;
    var angle = 360 / number_of_choices;
    rotate(angle, 0, (Math.random() * number_of_choices) + number_of_choices);

    function rotate(degree_incr, index, total) {
        if (index >= total) {
            return;
        }

        $('.spinner .pointer').css({
            'transform': 'rotate(' + degree_incr * index + 'deg)',
        });

        setTimeout(function () {
            var color = 'hsl(' + angle * (index % number_of_choices) + ', 100%, 60%)';

            $('.spinner .choice').each(function (i) {
                if (i == index % number_of_choices) {
                    $(this).css('background', color);
                    $(this).children('span').css('border-top-color', color);
                } else {
                    var old_color = 'hsl(' + angle * (i % number_of_choices) + ', 80%, 70%)';
                    $(this).css('background', old_color);
                    $(this).children('span').css('border-top-color', old_color);
                }
            });

            $('.spinner .pointer span').css('background', color);

            rotate(degree_incr, index + 1, total);
        }, 200);
    }
}