$(document).ready(function() {
	var body = $('#body');
	body.append('Echo: <input id="echo-text" type="text"> <input id="echo-button" type="submit"><br>');
	body.append('Reverse: <input id="reverse-text" type="text"> <input id="reverse-button" type="submit"><br>');
	body.append('Hello: <select id="hello-language"><option value="en">English</option><option value="de">German</option></select> <input id="hello-name" type="text"> <input id="hello-button" type="submit"><br>');
	body.append('<div id="response"></div>')

	$('#echo-button').click(function() {
		$('#response').html('Wait...');
		echo.echo($('#echo-text').val(), function(resp) {
			$('#response').html(resp)
		})
	});
	$('#reverse-button').click(function() {
		$('#response').html('Wait...');
		echo.reverse($('#reverse-text').val(), function(resp) {
			$('#response').html(resp)
		})
	});
	$('#hello-button').click(function() {
		$('#response').html('Wait...');
		echo.hello($('#hello-language').val(), $('#hello-name').val(), function(resp) {
			$('#response').html(resp)
		})
	});
})