import sys
import re
import fileinput
from itertools import ifilter
import subprocess
import os
import eyeD3

from os import listdir
from os.path import isfile, join
from os import walk
from collections import defaultdict
import os.path
from subprocess import check_output
from time import time
import difflib 

#music directory
mypath = "/home/rocky/Desktop/music/"

#formats to be supported
video_formats = [".mp4",".MP4",".flv",".FLV",".avi",".AVI"]
audio_formats = [".mp3",".MP3",".m4a"]

#searching the main directory
def get_filepaths(directory):

    file_paths = []  

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths 
full_file_paths = get_filepaths(mypath)


#to check for audio files
def check_audio(link):
	for x in range(0,len(audio_formats)):
		if audio_formats[x] in link:
			return 1
	
	return 0


#check for a file in the path
def checkinpath(link,search):
	link_list = link.split("/")
	
	for x in range(0,len(link_list)):
		a = str(link_list[x])
		if search in a:
			return 1

	return 0


#song dictionary
allsongs = []
path = os.path.join(os.path.dirname(__file__), '')

songfiles1234 = defaultdict(dict)
song_titles123 = []


#list of songs in directory
cnt123 = 0
for line in full_file_paths:
	supported_flag = 0
	for cnt in range(0,len(video_formats)+len(audio_formats)):
		if cnt < len(video_formats) and video_formats[cnt] in line:
			supported_flag = 1
		if cnt >= len(video_formats) and audio_formats[cnt-len(video_formats)] in line:
			supported_flag = 1

	if supported_flag == 1 :
		allsongs.append(line)
		line123 = line.replace(mypath,"")
		song_titles123.append(line123)
		songfiles1234[line123] = line
	
	
list1 = []
query_songs = []
xsong = []


for x in range(2,len(sys.argv)):
	if sys.argv[x] != '$' :
		xsong.append(sys.argv[x])

	else:
		query_songs.append(xsong)
		xsong = []

	if x == len(sys.argv) - 1:
		query_songs.append(xsong)



#search
query = sys.argv[1]
titles_list = []
features = ["song","artist","album","genre","audio"]


###search function
def PlaySearch(songs_list,query123):
	for line in song_titles123:
		audio_file_constant = 0
		audio_file_constant1 = check_audio(line) 
		full_path = ''

		if audio_file_constant1 == 1:
			tag = eyeD3.Tag()
			if tag.link(songfiles1234[line]) :
				audio_file_constant = 1
				small_title = tag.getTitle()
				small_artist = tag.getArtist()
				small_album = tag.getAlbum()
				small_genre = tag.getGenre()
	
		for x in range(0,len(songs_list)):		
			c = 1	
			d = 1
			e = 1

			####search in path file
			for z in range(0,len(songs_list[x])):
				small_search = songs_list[x][z].lower()
				small_line = line.lower()
				xyz = checkinpath(small_line,small_search)
				if  xyz == 1 :
					c = 0
				else:
					c = 1
					break;

			if c == 0 :

				if audio_file_constant == 1 :
					strtitle = small_title.lower() + " " + small_artist.lower() + " " + small_album.lower()
					if strtitle not in titles_list:
						titles_list.append(strtitle)
						list1.append(songfiles1234[line])

				else:		
					list1.append(songfiles1234[line])
				
				break;	


			##search in song title	
			elif (query123 == 'song' or query123 == 'list') and audio_file_constant == 1:
				for y in range(2,len(sys.argv)):
					small_search1 = sys.argv[y].lower()
					if small_search1 in small_title.lower():
						d = 0
					else:
						d = 1
						break;
				
				if d == 0 :
					strtitle = small_title.lower() + " " + small_artist.lower() + " " + small_album.lower()
					if strtitle not in titles_list:
						titles_list.append(strtitle)
						list1.append(songfiles1234[line])
					break;



			#search in song artist		
			elif (query123 == 'artist' or query123 == "list") and audio_file_constant == 1:
				for y in range(2,len(sys.argv)):
					small_search1 = sys.argv[y].lower()
					if small_search1 in small_artist.lower():
						d = 0
					else:
						d = 1
						break;
				if d == 0 :
					strtitle = small_title.lower() + " " + small_artist.lower() + " " + small_album.lower()
					if strtitle not in titles_list:
						titles_list.append(strtitle)
						list1.append(songfiles1234[line])
					break;


			##seach in song album		
			elif (query123 == 'album' or query123 == "list") and audio_file_constant == 1:
				for y in range(2,len(sys.argv)):
					small_search1 = sys.argv[y].lower()
					if small_search1 in small_album.lower():
						d = 0
					else:
						d = 1
						break;
				if d == 0 :
					strtitle = small_title.lower() + " " + small_artist.lower() + " " + small_album.lower()
					if strtitle not in titles_list:
						titles_list.append(strtitle)
						list1.append(songfiles1234[line])
					break;


			##search in song genre		
			elif (query123 == 'genre' or query123 == "list") and audio_file_constant == 1:
				for y in range(2,len(sys.argv)):
					small_search1 = sys.argv[y].lower()
					if small_genre :
						if small_search1 in str(small_genre).lower():
							d = 0
						else:
							d = 1
							break;

				if d == 0 :
					strtitle = small_title.lower() + " " + small_artist.lower() + " " + small_album.lower()
					if strtitle not in titles_list:
						titles_list.append(strtitle)
						list1.append(songfiles1234[line])
					break;


	return list1


##creating the xspf file
def playinvlc(list123):
	playlistfiles = get_filepaths(path)

	p = subprocess.Popen("ps -A | grep vlc", shell = True, stdout=subprocess.PIPE)
	out, err = p.communicate()

	if len(out) != 0 :
		t1 = time()
		t2 = int(t1)
		playlist_file = path + "playlist" + str(t2) + ".xspf" 

	else : 
		for line in playlistfiles:
			if "playlist" in line:
				os.remove(line)
	
		playlist_file = path + "playlist.xspf"

	new123 = open(playlist_file,'w')

	if len(list123) > 0 :
		new123.write("<?xml version='1.0' encoding='UTF-8'?><playlist xmlns='http://xspf.org/ns/0/' xmlns:vlc='http://www.videolan.org/vlc/playlist/ns/0/' version='1'>	<title>Playlist</title> <trackList>")

		for x in range(0,len(list123)) :
			new123.write("\n")
			new123.write("<track><location>file://")
			cat = list123[x].replace(" & "," %26 ").replace("&","%26").replace(" ","%20")
			new123.write(cat)
			new123.write("</location><extension application='http://www.videolan.org/vlc/playlist/0'><vlc:id>")
			strx = str(x)
			new123.write(strx)
			new123.write("</vlc:id></extension></track>")

		new123.write("\n")
		new123.write("</trackList><extension application='http://www.videolan.org/vlc/playlist/0'><vlc:item tid='0'/>")

		for x in range(0,len(list123)):
			new123.write("\n")
			new123.write("<vlc:item tid='")
			strx = str(x)
			new123.write(strx)
			new123.write("'/>")

		new123.write("</extension></playlist>")
		new123.close()

		filetoplay = "vlc " +  playlist_file + " && exit" 

		result = subprocess.Popen(filetoplay,shell = True)

	else :
		print sys.argv[1] + " not found"

		songsearch = ''
		for x in range(0,len(songs_list[0])):
			songsearch = songsearch + str(songs_list[0][x]) + " "

		print songsearch
		#print difflib.get_close_matches(songsearch + ".mp3", song_titles123)
		print difflib.get_close_matches('appel', ['ape', 'apple', 'peach', 'puppy'])


	return


	
if query in features:
	print query_songs
	list1 = PlaySearch(query_songs,query)
	play123 = playinvlc(list1)

elif query == 'list':
	printlist = PlaySearch(query_songs,query)
	for x in range(0,len(printlist)) :
		audio_file_constant1 = check_audio(printlist[x]) 
		if audio_file_constant1 == 1:
			tag = eyeD3.Tag()
			if tag.link(printlist[x]) :
				small_title = tag.getTitle()
				small_album = tag.getAlbum()
				print str(x+1) + ") " + small_title +  " ********* FROM THE ALBUM ********* " + small_album +"\n"

			else:
				file123 = printlist[x].split("/")
				xyz = len(file123)
				filetoprint = file123[xyz-1]
				print str(x+1) + ") " + filetoprint + "\n"
	
		else:
			file123 = printlist[x].split("/")
			xyz = len(file123)
			filetoprint = file123[xyz-1]
			print str(x+1) + ") " + filetoprint + "\n"
	

	print "Enter the numbers songs numbers to be played / quit to exit"
	ttt = raw_input()
	if ttt.lower() != "quit":
		tttlist = ttt.split(',')
		listtoplay = []
		for xyz in range(0,len(tttlist)):
			rr = tttlist[xyz].replace(" ","")
			intrr = int(rr)
			print intrr
			print printlist[xyz-1]
			listtoplay.append(printlist[xyz-1]) 

		play123 = playinvlc(listtoplay)


else:
	print "Wrong format......Enter 'song/album/artist/genre name' "

	

