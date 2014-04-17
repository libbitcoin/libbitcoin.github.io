function startplayer() {
    document.getElementById('player_area').style.opacity="0";
    setTimeout(function(){document.getElementById('player_area').style.display="none"}, 1000);
    setTimeout(function(){document.getElementById('player').style.display="block"}, 1000);
    if (document.body.clientWidth > 1025) { setTimeout(function(){jQuery("#youtube-player-container").tubeplayer("play")}, 3000); }
    $('html, body').animate({ scrollTop: 0 }, 'slow');
    setTimeout(function(){document.getElementById('player').style.opacity="1"}, 1000);
}

function showPaymentModal(amount) {
switch(amount) {
  case 5:
    $('#paymentModalLabel').text('Fund $5 and get');
    $('#tiggAmount').val(5);  
    $('#getThis').html('<p>2 codes to unlock all features of the app.</p>');
    break;

  case 10:
    $('#paymentModalLabel').text('Fund $10 and get');
    $('#tiggAmount').val(10);  
    $('#getThis').html('<p>5 unlock codes</p><p>Pre-register 1 user name</p>');
    break;

  case 25:
    $('#paymentModalLabel').text('Fund $25 and get');
    $('#tiggAmount').val(25);  
    $('#getThis').html('<p>10 unlock codes</p><p>Pre-register 3 user names</p>');
    break;

  case 50:
    $('#paymentModalLabel').text('Fund $50 and get');
    $('#tiggAmount').val(50);  
    $('#getThis').html('<p>Your name in "Funded by" in the app</p><p>10 unlock codes</p><p>Pre-register 3 user names</p>');
    break;

  case 500:
    $('#paymentModalLabel').text('Fund $500 and get');
    $('#tiggAmount').val(500);  
    $('#getThis').html('<p>Your name in "Funded by" the app</p><p>500 unlock codes! + pre-register 10 user-names</p>');
    break;
    
  case 1337:
  default:
    $('#tiggAmount').val(0);  
    $('#paymentModalLabel').text('Fund Heml.is');
    $('#getThis').html('<div class="input-prepend"><span class="add-on dollar_button">$</span><input name="amount" class="dollar text-center" id="prependInput" type="number" placeholder="enter amount"></div>');
    break;
  }

    $('#paymentModal').modal('show')
}

function querystring(key) {
    var re=new RegExp('(?:\\?|&)'+key+'=(.*?)(?=&|$)','gi');
    var r={}, m;

    while ((m=re.exec(document.location.search)) != null) {
        r.key = m[1];
    }

    return r.key || null;
}

$(function(){

    $('#fundlevelMenu a').click(function() {
        showPaymentModal($(this).data('fund'));
    });

	$('#paypp').click(function(){
		$('#tiggForm').attr('action', '/?go=paypal');
		$('#tiggForm').submit();
	});


$('#paybc').click(function(){
  $('#tiggForm').attr('action', '/?go=bitcoin');
  $('#tiggForm').submit();
});


$('#subMail').click(function(){
  $('#mejl').submit();
});

    $("#mejl").submit(function() {
        var foo = $.post('/addMail.php', { maillist: 1, email: $("#appendedInput").val()}, function() {
            $('#mailModal').modal('show');
        })
        .fail(function() {
           console.log('We really need better error handling...');
        });
        return false;
    });

    if ($('body').data('backer-modal') == 1) {
        $('#resultModal').modal('show');
    }

    if ($('body').data('show-modal') != 0) {
        $('#'+$('body').data('show-modal')+'Modal').modal('show');
    }
});


// var inline innan


var video_width = document.body.clientWidth;
if (video_width > 854) {
  video_width = 854;
  video_height = 480;
}
if (video_width < 854) {
  video_width = video_width - 40;
  video_height = (video_width/16)*9;
  document.getElementById('player').style.height=video_height+'px';
}
    
jQuery("#youtube-player-container").tubeplayer({
    width: video_width, 
    height: video_height,
    allowFullScreen: "true",
    initialVideo: "oPeujbY3feM",
    preferredQuality: "hd720",// preferred quality: default, small, medium, large, hd720
  showControls: 0, // whether the player should have the controls visible, 0 or 1
    showRelated: 0, // show the related videos when the player ends, 0 or 1 
    autoPlay: false, // whether the player should autoplay the video, 0 or 1
    showinfo: false, // if you want the player to include details about the video
    modestbranding: true, // specify to include/exclude the YouTube watermark
    theme: "light", // possible options: "dark" or "light"
    color: "white", // possible options: "red" or "white"
    onPlayerEnded: function(){
    document.getElementById('player').style.opacity="0";
    setTimeout(function(){document.getElementById('player_area').style.display="block"}, 1000);
    setTimeout(function(){document.getElementById('player').style.display="none"},1000);
    setTimeout(function(){document.getElementById('player_area').style.opacity="1"}, 1200);
    }, // when the player returns a state of ended
});
