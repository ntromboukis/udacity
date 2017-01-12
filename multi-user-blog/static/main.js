var modal = document.getElementById('myModal');
var btn = document.getElementById("loginBtn");
var span = document.getElementsByClassName("close")[0];
var signup = document.getElementById("signup");
var topFields = document.getElementById("top-fields");
var u_error = document.getElementById("username_error");
var p_error = document.getElementById("password_error");
var e_error = document.getElementById("e_error");
var val = 0;
btn.onclick = function() {
    modal.style.display = "block";
}
span.onclick = function() {
    modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function signupFunction() {
    if (val % 2 == 0) {
        signup.style.display = "block";
        topFields.style.paddingBottom = "1em";
        val++;
    } else {
        signup.style.display = "none";
        topFields.style.paddingBottom = "5em";
        val++;
    }
}

function infoErrorFunction() {
    if (u_error || p_error || e_error) {
        modal.style.display = "block";
    }
}