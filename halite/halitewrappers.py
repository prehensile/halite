##
# halitewrappers.py
#
# wrappers for various commandline utilities
#
import subprocess

ALSA_DEVICE = "plug=dmixer"

class MPlayerWrapper():
	
	def play_pipe( self, pipe ):
		# subprocess.call( [ "mplayer", "-vo", "null", "-ao",("alsa:device=%s" % ALSA_DEVICE), "-cache", "8192", "-" ], stdin=pipe );
		subprocess.call( [ "mplayer", "-vo", "null", "-cache", "8192", "-" ], stdin=pipe )
	
	def play_file( self, file ):
		# subprocess.call( [ "mplayer", "-vo", "null", "-ao", ("alsa:device=%s" % ALSA_DEVICE), file ] );
		subprocess.call( [ "mplayer", "-vo", "null", file ] );
	
	
