    $(document).ready(function(){
    $('.book_information').mouseleave(function(){
        $(this).find('.book_information_1').slideUp('fast');
    })
    $('.book_information').mousemove(function(){
        $(this).find('.book_information_1').slideDown('1000');
    })
})