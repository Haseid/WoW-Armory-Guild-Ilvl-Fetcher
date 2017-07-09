# _*_ coding: utf-8 _*_
from urllib.request import urlopen
import re
import sys
#http://eu.battle.net/wow/en/guild/ravencrest/Stand_In_Fire_DPS_Higher
guild_URL = str(sys.argv[1])
guild_roster_html_str = ""
guild_chars_html_str = ""
guild_char_ilvl = []

print("Fetching guild pages")
for i in range(1,11):
	guild_roster_html_str += urlopen(sys.argv[1]+"/roster?page="+str(i)).read().decode('utf-8')
	sys.stdout.write("Download progress: %d%%   \r" %(i/10*100))
	sys.stdout.flush()

# Making character URLs from the guild pages
guild_char_URLs = ["http://eu.battle.net" + char_URL for char_URL in re.findall(r"\"(/wow/en/character/.*?)\"[\s\S]*?" , guild_roster_html_str)]
print("\n\nFound "+str(len(guild_char_URLs))+" characters\n")


print("Fetching guild members ilvl")
for i, char_URL in enumerate(guild_char_URLs):
	try:
		guild_chars_html_str = urlopen(char_URL).read().decode('utf-8')
		guild_char_ilvl += re.findall(r"CharacterHeader-name\"[\s\S]*?>(\S*)</a[\s\S]*?(\d+)\ ilvl" , guild_chars_html_str)
		# Pulling out character name and ilvl from html string
		sys.stdout.write("Download progress: %d%%   \r" %(i/len(guild_char_URLs)*100))
		sys.stdout.flush()
	except Exception as e:
		print("\n\n\n")
		print(e)
		print(char_URL)
		print("\n\n\n")

file = open("data.txt", "w", encoding="utf8")
for data in guild_char_ilvl:
	file.write(data[0]+" "+data[1]+"\n")
file.close()