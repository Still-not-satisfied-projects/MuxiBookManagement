
$(document).ready(function(){
var $imgs = $(".book");
var count = 0;
var bar = document.getElementById("bar");
var length = $imgs.length;
 console.log($imgs,length);
for(var i = 0;i<length;i++){
    $imgs.eq(i).bind("load",function(){
        count += 1;
        console.log("load");
        change_bar();
      	if (count == length){
      		bar.style.display = "none"
      	}
      })  
    }

window.onload = function (){
	 bar.firstElementChild.style.width = "100%";
	
	bar.style.display = "none"

}
function change_bar(){
    bar.firstElementChild.style.width = (count/length)*100 +"%";
}

})
function showBorder(){
	document.getElementById('content').style.display = 'block' ;
	document.getElementById('fade').style.display = 'block' ;
	document.getElementById('close').style.display = 'block' ;
}
function hideBorder(){
	document.getElementById('content').style.display = 'none' ;
	document.getElementById('fade').style.display = 'none' ;
	document.getElementById('close').style.display = 'none' ;
}

function showBorderLog(){
	document.getElementById('content_log').style.display = 'block' ;
	document.getElementById('fade_log').style.display = 'block' ;
}
function hideBorderLog(){
	document.getElementById('content_log').style.display = 'none' ;
	document.getElementById('fade_log').style.display = 'none' ;
}
/*首页新增图书导航*/
$(document).ready(function(){
var boxwidth;
var boxheight;
var leftnum;
var current;
var left;
current = 0;
boxwidth = $(".showbox").css("width");
boxheight = $(".showbox").css("height");
boxwidthnum = $(".showbox").width();
$(".box").css("height",boxheight);
$(".box").css("width",boxwidth);
$(".slide").width(boxwidthnum*($(".box").length));
$(".slide").css("height",boxheight);
$("#prev").bind("click",function(){
	prev(current);
});
$("#next").bind("click",function(){
	next(current);
});
function next(num){
	if (current == ($(".box").length-1))
  {
  current = 0;
  $(".slide").animate({left:current*(-boxwidthnum) + 'px'});
  }
else
  {
  current += 1;
  $(".slide").animate({left:current*(-boxwidthnum) + 'px'});
 }
};
	function prev(num){
	
	if (current == 0)
  {
  current = $(".box").length-1;
  $(".slide").animate({left:current*(-boxwidthnum) + 'px'});
  }
else
  {
  current -= 1;
  $(".slide").animate({left:current*(-boxwidthnum) + 'px'});
 
  }
	
};
});


