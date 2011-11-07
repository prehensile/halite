##
# halitewrappers.py
#
# wrappers for various commandline utilities
#
import subprocess
import time

ALSA_DEVICE = "hw=0,0"

class MPlayerWrapper():
	
	def exec_mplayer( self, in_args, stdin=None ):
		args = [ "mplayer", "-vo", "null", "-ao", "pulse" ]
		args.extend( in_args )
		# subprocess.call( [ "mplayer", "-vo", "null", "-ao",("alsa:device=%s" % ALSA_DEVICE), "-cache", "8192", "-" ], stdin=pipe );
		# subprocess.Popen( args, stdin=stdin, stdout=subprocess.PIPE )
		subprocess.call( args, stdin=stdin )
		time.sleep( 1 )
		
	def play_pipe( self, pipe ):
		self.exec_mplayer( [ "-cache", "8192", "-" ], pipe )
		
	def play_file( self, file ):
		self.exec_mplayer( [ file ] );
	
