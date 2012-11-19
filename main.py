import re, socket, json, threading
from ConfigParser import RawConfigParser
from modules import lastfm, tf2lobby

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
commands = {}
parser = RawConfigParser()
np, lobbyparser = lastfm.NowPlaying(), tf2lobby.lobbyParser()

parser.read('botcfg.cfg')

botnick, password, streamname, lastfmuser, owner = parser.get('settings', 'botnick'), parser.get('settings', 'password'), parser.get('settings', 'streamname'), parser.get('settings', 'lastfmuser'), parser.get('settings', 'owner')

server, channel = "%s.jtvirc.com" % (streamname), "#%s" % (streamname)

LastFMMain = np.main(lastfmuser)

def connect(server, port):
	ircsock.connect((server, port))
	ircsock.send("Pass %s\n" % (password))
	ircsock.send("NICK %s\n" % (botnick))
	ircsock.send("JOIN %s\n" % (channel))

def doTF2Lobby(lobby):
	lobbyParser.main(lobby)
	sendmsg("Name: \"%s\" is on map \"%s\"" % (tf2lobby.lobbyname, tf2lobby.mapname))

def sendmsg(message):
	ircsock.send('PRIVMSG %s :%s\n' % (channel, message))

def dict():
	cmdfile = file('commands.json', 'r').read()
	#cmdfile = open("commands.txt")
	"""	print cmdfile
	for line in cmdfile:
		(key, val) = line.split('=')
		commands[(key)] = val
	print commands.keys()
	print commands.values()
	"""
	global commands
	commands = json.loads(cmdfile)

def cmds(nick, msg, sendmsg):
	for x in commands["commands"]:
		if re.search(x, msg, re.I):
			sendmsg(commands["commands"].get(x))

	for x in commands["execs"]:
		if re.search(x, msg, re.I):
			exec(commands["execs"].get(x))

	for x in commands["owner_commands"]:
		if nick in owner:
			if re.search(x, msg, re.I):
				exec(commands["owner_commands"].get(x))
			
def triggers(msg, sendmsg):
	for x in commands["triggers"]:
		if re.search(x, msg, re.I):
			sendmsg(commands["triggers"].get(x))

def main():
	dict()
	t = threading.Thread(target = LastFMMain)
	t.setDaemon(True)
	t.start()

	try:
		connect(server, 6667)
	except Exception as e:
		print e

	while True:
		ircmsg = ircsock.recv(1024)
		ircmsg = ircmsg.strip('\r\n')

		print ircmsg

		if ircmsg.find('PING ') != -1:
			ircsock.send('PING :Pong\n')

		if ircmsg.find(' PRIVMSG ') != -1:
			nick = ircmsg.split('!')[0][1:]
			msg = ircmsg.split(' PRIVMSG ')[-1].split(' :')[1]
			cmds(nick, msg, sendmsg)
			triggers(msg, sendmsg)

main()

