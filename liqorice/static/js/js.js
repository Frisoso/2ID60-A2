$( "html").hide().fadeIn(1000);
$( ".socialNetworkNav" ).hide().fadeIn(2000);

setTimeout(function(){
  $('#alertBar').fadeOut(1000, function() { $(this).remove(); });
}, 5000);
