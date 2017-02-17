// JS needed to simulate the "sticky" focus state, aka stay pressed down, in chrome:

$(".mm-item").click(function() {
  $(this).focus();
});