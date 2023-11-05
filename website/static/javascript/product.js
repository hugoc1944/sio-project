// Change the main image when the user clicks on a small image
var MainImage = document.getElementById("MainImage");
var smallimg = document.getElementsByClassName("small-img");
smallimg[0].onclick = function(){
    MainImage.src = smallimg[0].src;
}
smallimg[1].onclick = function(){
    MainImage.src = smallimg[1].src;
}
smallimg[2].onclick = function(){
    MainImage.src = smallimg[2].src;
}
smallimg[3].onclick = function(){
    MainImage.src = smallimg[3].src;
}
