$( function() {

    $("h1,div").hide().fadeIn(200);

    $("#submit").click(function(event){ // this is very similar to newevent as they basically do same thing
        now = new Date (Date.now());
        old = new Date(($('#dob').val()));
        if ($('#username').val().length === 0) {
            alert('Enter a username!');
            return false
        }
        if ($.trim($('#username').val())== "" ){
            alert("Enter a correct username");
            return false
        }
        if ($('#password').val().length === 0) {
            alert('Enter a password!');
            return false
        }
        if ($('#dob').val().length == 0) {
            alert('Enter a date of birth!');
            return false
        }
        if (!Date.parse($('#dob').val())) {
          alert('Enter a valid date of birth!');
          return false
        }
        if ($('#email').val().length == 0) {
            alert('Enter an email!');
            return false
        }
        if (now <= old){
            alert("This date has already passed!");
            return false
            }
 })
});
