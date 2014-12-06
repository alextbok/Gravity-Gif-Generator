
$(window).load(function() {
	var c = document.getElementById("canvas");
	var ctx = c.getContext("2d");
	var img = document.getElementById("grav_png");
	
	var word = ctx.drawImage(img,10,10);
	word.id = "gravtext"
});