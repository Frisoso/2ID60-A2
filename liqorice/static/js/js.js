
$( "html").hide().fadeIn(1000);
$( ".socialNetworkNav" ).hide().fadeIn(2000);

displayComments();

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
        }
    }

    document.body.appendChild(form);
    form.submit();
}


function submitComment() {
  if (!validateForms()) {
    return;
  }
  var uname = $( "#uname" ).val();
  $( "#uname" ).val("");
  var ctext = $( "#ctext" ).val();
  $( "#ctext" ).val("");

  post('/comments/', {author: uname, content: ctext});
}

function displayComments() {
  var comments = getCookie("comments");
  if ( !comments ) {
    comments = "Friso Buurman|Test comment|Fri, 01 Dec 2017 11:57:03 GMTz"
  }

  $( ".commentSection ol li" ).remove();

  var commentsArray = comments.split('z');
  for(var i = 0; i < commentsArray.length - 1; i++) {
    commentArray = commentsArray[i].split('|');
    $( ".commentSection ol" ).append("<li><article class=\"comment\"><div class=\"entry-content\">" + commentArray[1] + "</div><footer class=\"post-info\"><abbr class=\"published\" title=\"" + commentArray[2] + "\">" + commentArray[2] + "</abbr><address class=\"vcard author\">Door: " + commentArray[0] + "</address></footer></article></li>");
  }

  $( ".commentSection ol li:odd" ).css( "background-color", "#e9e9e9" );
  $( ".commentSection ol li:even" ).css( "background-color", "#f6f6f6" );
}

function validateForms() {
  if ( !$( "#uname" ).val() || !$( "#ctext" ).val() ) {
    alert("Zowel het 'Naam' als het 'Reactie' veld moeten ingevuld zijn!");
    return false;
  }else {
    return true;
  }
}

function setDisableComments(disable) {
  $('.commentSectionContent button').prop('disabled', disable);
  $('.commentSectionContent input').prop('disabled', disable);
  $('.commentSectionContent textarea').prop('disabled', disable);

  if (disable) {
    $('.commentSectionContent button').css('cursor', 'not-allowed');
    $('.commentSectionContent button').prop('title', 'Accept cookie-usage to enable comments');
    $('.commentSectionContent input').prop('title', 'Accept cookie-usage to enable comments');
    $('.commentSectionContent textarea').prop('title', 'Accept cookie-usage to enable comments');
  }else {
    $('.commentSectionContent button').css('cursor', 'default');
    $('.commentSectionContent button').prop('title', '');
    $('.commentSectionContent input').prop('title', '');
    $('.commentSectionContent textarea').prop('title', '');
  }
}

//manage cookies
setDisableComments(true);
var cname = "useCookies";
if ( getCookie(cname) ) {
  removeCookieBar();

  if (getCookie(cname) == "true") {
    setDisableComments(false);
  }
}else {
  showCookieBar();
}

function removeCookieBar() {
  $( "#cookiebar" ).remove();
}

function showCookieBar() {
  $( "#cookiebar" ).css('visibility', "visible");
}

function cookieYes() {
  setCookie(cname, "true", 31);
  setDisableComments(false);
  removeCookieBar();
}

function cookieNo() {
  removeCookieBar();
}

//general cookie functions
function setCookie(cname, cvalue) {
    setCookie(cname, cvalue, 31);
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
