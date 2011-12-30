/**
 * Global JS file
 */

// async load scripts
Modernizr.load([{
		
	// if touch device run fixes
	test: Modernizr.touch,
	yep: {
		'mbphelper': '/assets/vendor/mbphelper.js'		
	},
	callback: {
		'mbphelper': function() {
			MBP.scaleFix();
			MBP.hideUrlBar();
		}
	},
	
	// common loads
	load: {
		'socketio' : '/socket.io/socket.io.js',
		'jquery' : 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js'
	},	
	callback: {
		'jquery' : function () {
			
			// on dom ready
			(function($) {		
				
				// assign vars
				var socket = io.connect(window.location.href), // connect socket;
					$connections = $('#connections'), // dom stuff
					$playlist = $('#playlist'),
					$chat = $('#chat'),
					$chatForm = $chat.find('form'),
					$chatMessages = $('#chat').find('ul');
					
				// --- socket events (on = socket.io event)----
		
				// socket event: listen out for connections changes
				socket.on('connections', function (data) {
					$connections.text(data);
				});
							
				// socket event: listen out for playlist changes
				socket.on('playlist', function (data) {

					var $item = $playlist.find('.track').eq(data),
						$previous = $item.prev();

					// move up one
					$item.detach();
					$previous.before($item);
					
				});
				
				// socket event: listen out for incoming chat messages
				socket.on('chat', function (data) {

					// build new chat message and append to dom
					var $li = $('<li/>')
						.text(data.message)
						.prependTo($chatMessages);
				});
				
				// --- client events (on = jquery 1.7 bind event) ---
							
				// client event: delegate votes within playlist 
				$playlist.on('click.halite', 'a.vote', function() {
					
					// assign vars
					var $this = $(this),
						$item = $this.closest('.track');
						
					// if not at top then send index
					if ($item.index() > 0 ) {
						socket.emit('playlist', $item.index());	
					}								
					// socket.emit('playlist', { id: $item.data('id'), direction: $this.data('vote') }); // example of json data
				});
				
				// client event: submit chat
				$chatForm.on('submit.halite', function(e) {
					
					// assign vars
					var $this = $(this);
						$input = $this.find('input'); 
					
					// kill submit
					e.preventDefault();
					
					// send message
					socket.emit('chat', { 
						message: $input.val() 
					});
					
					// reset input
					$input.val('');
				});
			})(jQuery);		
		}
	}
}]); 