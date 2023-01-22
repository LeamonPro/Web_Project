let image=document.getElementById("img1");
let image2=document.getElementById("img2");
let image3=document.getElementById("img3");
image.addEventListener('click', function() {
    this.classList.add('go');
    image2.classList.remove('go');
    image3.classList.remove('go');
});

image2.addEventListener('click', function() {
    this.classList.add('go');
    image.classList.remove('go');
    image3.classList.remove('go');
});

image3.addEventListener('click', function() {
    this.classList.add('go');
    image.classList.remove('go');
    image2.classList.remove('go');
});
