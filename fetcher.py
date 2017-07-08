# _*_ coding: utf-8 _*_
from urllib.request import urlopen
import re
import sys

guild_URL = str(sys.argv[1])
guild_roster_html_str = ""
guild_chars_html_str = ""

print("Fetching guild pages")
for i in range(1,11):
	guild_roster_html_str += str(urlopen(sys.argv[1]+"/roster?page="+str(i)).read())
	sys.stdout.write("Download progress: %d%%   \r" %(i/10*100))
	sys.stdout.flush()

# Making character URLs from the guild pages
guild_char_URLs = ["http://eu.battle.net" + char_URL for char_URL in re.findall(r"\"(/wow/en/character/.*?)\"[\s\S]*?" , guild_roster_html_str)]
print("\n\nFound "+str(len(guild_char_URLs))+" characters\n")

print("Fetching guild members ilvl")
for i, char_URL in enumerate(guild_char_URLs):
	guild_chars_html_str += str(urlopen(char_URL).read())
	sys.stdout.write("Download progress: %d%%   \r" %(i/len(guild_char_URLs)*100))
	sys.stdout.flush()

# Pulling out character name and ilvl from html string
guild_char_ilvl = re.findall(r"CharacterHeader-name\"[\s\S]*?>(\S*)</a[\s\S]*?(\d+)\ ilvl" , guild_chars_html_str)

file = open("data.txt", "w")
file.write(guild_char_ilvl)
file.close()