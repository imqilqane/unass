let items = document.querySelectorAll('.item');
let header = document.querySelector('#header');
let overlay = document.querySelector('.overlay');
let links = document.querySelector('.links');

// slid show

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
	showSlides((slideIndex += n));
}

function currentSlide(n) {
	showSlides((slideIndex = n));
}

function showSlides(n) {
	var i;
	var slides = document.getElementsByClassName('mySlides');
	var dots = document.getElementsByClassName('dot');
	if (n > slides.length) {
		slideIndex = 1;
		console.log(slideIndex);
	}
	if (n < 1) {
		slideIndex = slides.length;
		console.log(slideIndex);
	}
	for (i = 0; i < slides.length; i++) {
		slides[i].style.display = 'none';
		console.log('none');
	}
	for (i = 0; i < dots.length; i++) {
		dots[i].className = dots[i].className.replace(' active', '');
		console.log('active');
	}
	slides[slideIndex - 1].style.display = 'block';
	dots[slideIndex - 1].className += ' active';
}
