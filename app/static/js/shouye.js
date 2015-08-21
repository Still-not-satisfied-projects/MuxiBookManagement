    $(document).ready(function(){
    $('.book_information').mouseleave(function(){
        $(this).find('.book_information_1').slideUp('fast');
    })
    $('.book_information').mousemove(function(){
        $(this).find('.book_information_1').slideDown('1000');
    })
})

    function showBorder(){
	document.getElementById('content').style.display = 'block' ;
	document.getElementById('fade').style.display = 'block' ;
}
function hideBorder(){
	document.getElementById('content').style.display = 'none' ;
	document.getElementById('fade').style.display = 'none' ;
}