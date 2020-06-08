function sendemail() {
	var max_price = document.getElementById("max_price").value
	var email = document.getElementById("email").value
	if (max_price=="" && email==""){
		alert('Please enter Max price and Email')
		return
	} else if (email==""){
		alert('Please enter correct E-mail')
		return
	} else if (max_price==""){
		alert('Please enter Max price')
		return
	} else if (!window.category){
		alert('Please select a category')
		return
	}
	document.getElementById("message").textContent = 'Searching...'
	eel.selector(window.category, max_price)
	eel.sendemail(max_price, email)(message)
}

function message() {
	document.getElementById("message").textContent = 'Hey, email has sent'
}

function save() {
	document.getElementById("bar_para").style.display="none"
	document.getElementById("bar1").style.display="none"
	document.getElementById("bar2").style.display="none"
	var max_price = document.getElementById("max_price").value
	var email = document.getElementById("email").value
	if (max_price==""){
		alert('Please enter Max price')
		return
	} else if (!window.category){
		alert('Please select a category')
		return
	}
	document.getElementById("message2").textContent = 'downloading...'
	eel.selector(window.category, max_price)
	eel.save(max_price)(message2)
}

function message2() {
	document.getElementById("message2").textContent = 'Saved'
	document.getElementById("bar_para").style.display="block"
	document.getElementById("bar1").style.display="block"
	document.getElementById("bar2").style.display="block"
}

function pricebar(){
	eel.bar('Price')
}

function ratingbar(){
	eel.bar('Rating')
}

function laptop(){
	document.getElementById("laptop").src = "img/laptoptick.jpg"
	document.getElementById("camera").src = "img/camera.jpg"
	document.getElementById("mobile").src = "img/mobile.jpg"
	window.category = 'laptop'
}

function camera(){
	document.getElementById("laptop").src = "img/laptop.jpg"
	document.getElementById("camera").src = "img/cameratick.jpg"
	document.getElementById("mobile").src = "img/mobile.jpg"
	window.category = 'camera'
}

function mobile(){
	document.getElementById("laptop").src = "img/laptop.jpg"
	document.getElementById("camera").src = "img/camera.jpg"
	document.getElementById("mobile").src = "img/mobiletick.jpg"
	window.category = 'mobile'
}

