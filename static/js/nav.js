$(document).on("click", 'nav div div ul li a', function(){
    $(this).addClass("active").siblings().removeClass('active')
    ;
 });