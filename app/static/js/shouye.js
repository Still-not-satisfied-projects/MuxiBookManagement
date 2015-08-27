
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
