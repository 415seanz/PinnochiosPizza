// set variable to determine whether onblur event requires validation - prevents double alert
var validating = true;
// if username is already set, just display username
document.addEventListener('DOMContentLoaded', () => {

  // on username change, check whether username is taken
  document.querySelector('#username').onblur = () => {
    var taken = 0;

    let username = document.querySelector('#username').value;
    for (i=0; i<users.length; i++) {
      if (users[i] == username) {
        taken = 1;
        if (validating == true) {
            validating = false;
            alert(`Username ${username} is already taken!`);
            //have to wait a brief moment before re-focusing on username field - prevents double warning
            setTimeout(function(){
                document.getElementById("username").focus();
                validating = true;
            }, 1);
        }
      }
    }
  };

  // password entry validation
  document.querySelector('#registrationForm').onsubmit = () => {

    // check if password and validation match. if not, alert user
    let password = document.querySelector('#password').value;
    let validation = document.querySelector('#validation').value;
    if (password != validation) {
      alert('Passwords do not match. Please try again.');
      return false;
    }
  };


});
