$(function(){
  $(window).scroll(function(){
    $('.year').each(function(){
      var year = $(this).find('h2').first().text();
      if($(this).offset().top < $(document).scrollTop() +100){
        $(this).find('.date').addClass('activeYear');
           $('#dataYear').html(year);
        }else{
          $(this).find('.date').removeClass('activeYear');
        }
    });
  });
});
$(document).ready(function(){
  var year = $('.year').find('h2').first().text();
    $('#dataYear').html(year); 
  $('.year').first().find('.date').addClass('activeYear');
});