import os
import datetime
import youtube_dl
import discord
from discord.utils import get

mainGuild = 745725474465906732 # hjelp eg sitter fast i doen
hahaYes = 627151632534339595 # haha yes
mog = 745729242423099585 # Mog emote
hjelp = 746301264148562001 # Hjelp emote
TheFlip = 758463821831471174
last_channel = None

# Markus, BruhBot 2000 and Free Smiley Dealer 2.0 (no particular order)
TheFlipReacts = [748496866827829261, 475418097990500362, 595813672811626516]

# music queue
queues = {}

class MogBot(discord.Client):
	async def on_ready(self):
		global mainGuild
		print('Logged on as {0}!'.format(self.user))
		for guild in self.guilds:
			if guild.id == mainGuild:
				mainGuild = guild
				break

	async def run_command(self, command, channel, message):
		global mainGuild
		if not isinstance(command, str) or not isinstance(channel, discord.TextChannel):
			return
		argv = command.split()
		print(argv)
		if argv[0] == "say":
			response = ""
			for x in range(1,len(argv)):
				response += argv[x]+" "
			await channel.send(response)
			await message.delete()
		elif argv[0] == "delete":
			print("deleting "+command[7:])
			if len(argv) < 2:
				return
			async for m in channel.history():
				if m.content == command[7:]:
					print("Found one!")
					await m.delete()
		elif argv[0] == "join":
			global voice
			channel = message.author.voice.channel
			voice = get(client.voice_clients, guild=message.channel.guild)

			if voice and voice.is_connected():
				await voice.move_to(channel)
			else:
				voice = await channel.connect()
			await message.channel.send("Joined pog!")
		elif argv[0] == "leave":
			channel = message.author.voice.channel
			voice = get(client.voice_clients, guild=message.channel.guild)

			if voice and voice.is_connected():
				await voice.disconnect()
				await message.channel.send("Left pog!")
		elif argv[0] == "play":
			if len(argv) < 2:
				return
			voice = get(client.voice_clients, guild=message.channel.guild)
			def check_queue():
				Queue_infile = os.path.isdir("./Queue")
				if Queue_infile is True:
					DIR = os.path.abspath(os.path.realpath("Queue"))
					length = len(os.listdir(DIR))
					still_q = length - 1
					try:
						first_file = os.listdir(DIR)[0]
					except:
						print("Queue empty")
						queues.clear()
						return
					main_location = os.path.dirname(os.path.realpath(__file__))
					song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
					if length != 0:
						print("Song done, next one coming up")
						print("Songs still in q: {still_q}")
						song_there = os.path.isfile("song.mp3")
						if song_there:
							os.remove("song.mp3")
						shutil.move(song_path, main_location)
						for file in os.listdir("./"):
							if file.endswith(".mp3"):
								os.rename(file, 'song.mp3')

						voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
						voice.source = discord.PCMVolumeTransformer(voice.source)
						voice.source.volume = 0.07
					else: # length == 0
						queues.clear()
						return
				else: # Queue_infile is not True
					queues.clear()
					print("Queue ended")

			song_there = os.path.isfile("song.mp3")
			try:
				if song_there:
					os.remove("song.mp3")
					queues.clear()
					print("Deleted old mp3")
			except PermissionError:
				print("Could not delete old mp3 file, probably currently playing")
				await message.channel.send("ERROR: YOU FUCKED MY ASSHOLE OWOWOWOW IT HUUUURTS!! ;;")
				return
			Queue_infile = os.path.isdir("./Queue")
			try:
				Queue_folder = "./Queue"
				if Queue_infile is True:
					shutil.rmtree(Queue_folder)
					print("Removed old Queue folder")
			except:
				print("Could not remove old Queue folder")

			await message.channel.send("Getting shit ready my nibbas")

			ydl_opts = {
				'format': 'bestaudio/best',
				'quiet': True,
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '192',
				}],
			}

			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				print("Downloading audio POG")
				ydl.download([argv[1]])

			for file in os.listdir("./"):
				if file.endswith(".mp3"):
					name = file
					os.rename(file, "song.mp3")
					print("Renamed POG")

			voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
			voice.source = discord.PCMVolumeTransformer(voice.source)
			voice.source.volume = 0.07

			nname = name.rsplit("-", 2)
			await message.channel.send("Playing POG ({nname[0]})")
			print("Playing POG")
		elif argv[0] == "pause":
			voice = get(client.voice_clients, guild=message.channel.guild)
			if voice and voice.is_playing():
				voice.pause()
				await message.channel.send("Paused POG")
			else:
				await message.channel.send("Bruh, not even playing")
		elif argv[0] == "resume":
			voice = get(client.voice_clients, guild=message.channel.guild)
			if voice and voice.is_playing():
				voice.resume()
				await message.channel.send("Resumed POG")
			else:
				await message.channel.send("We're already playing mister")
		elif argv[0] == "skip":
			voice = get(client.voice_clients, guild=message.channel.guild)
			queues.clear()
			if voice and voice.is_playing():
				voice.stop()
				await message.channel.send("Skipped POG")
			else:
				await message.channel.send("Bruh the queue is empty")
		elif argv[0] == "queue":
			Queue_infile = os.path.isdir("./Queue")
			if Queue_infile is False:
				os.mkdir("Queue")
			DIR = os.path.abspath(os.path.realpath("Queue"))
			q_num = len(os.listdir(DIR))
			q_num += 1
			add_queue = True
			while add_queue:
				if q_num in queues:
					q_num += 1
				else:
					add_queue = False
					queues[q_num] = q_num

			queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

			ydl_opts = {
				'format': 'bestaudio/best',
				'quiet': True,
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '192',
				}],
			}

			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([argv[1]])
			
			await message.channel.send("Added song to queue POG")

	async def on_message(self, message):
		global last_channel
		last_channel = message.channel
		if mainGuild == None:
			return
		if message.content == "@forsen":
			file = discord.File("forsenE.jpg", filename="image.jpg")
			embed = discord.Embed()
			embed.color = 0xFF00FF
			embed.title = "@{0.name}".format(message.author)
			embed.description = "Spechimen"
			embed.timestamp = datetime.datetime.today()
			embed.set_image(url="attachment://image.jpg")
			embed.set_footer(text="Hallais", icon_url="https://www.google.com/favicon.ico")
			embed.set_thumbnail(url="https://www.google.com/favicon.ico")
			embed.set_author(name="Tapsen", url="https://pepega.no", icon_url="https://www.google.com/favicon.ico")
			embed.add_field(name="Peppersen", value="Yes.", inline=True)
			embed.add_field(name="Peppersen", value="Yes.", inline=True)
			await message.channel.send(file=file, embed=embed)
			return
		print('Message from {0.author}: {0.content}'.format(message))
		if message.author.id in TheFlipReacts:
			await message.add_reaction(await mainGuild.fetch_emoji(mog))
		if message.author.id == 179024507657256960:
			await message.add_reaction(await mainGuild.fetch_emoji(TheFlip))
		if message.content == ":TheFlip:":
			await message.delete()
			await message.channel.send(await mainGuild.fetch_emoji(TheFlip))
		elif "TheFlip" in message.content or "flip" in message.content.lower() or "monki" in message.content.lower():
			await message.add_reaction(await mainGuild.fetch_emoji(TheFlip))
		elif message.content.lower().startswith('hei') or "mog" in message.content.lower() or "pog" in message.content.lower():
			await message.add_reaction(await mainGuild.fetch_emoji(mog))
		if "hjelp" in message.content.lower():
			em = await mainGuild.fetch_emoji(hjelp)
			await message.add_reaction(em)
		elif "moment" in message.content.lower() and message.author.id not in (748488018058543116,595813672811626516):
			words = message.content.split()
			for i in range(0, len(words)):
				if words[i].lower() == "moment" and words[i-1].lower() != "bruh":
					await message.channel.send(words[i-1] + " moment indeed @" + message.author.name)
					break
		elif message.content == "Pain.":
			await message.channel.send("chill bro")
		elif message.content == "gn" or ("god" in message.content and "natt" in message.content):
			await message.channel.send("natta bro") # Add time limit
		if message.content.startswith('!'):
			await self.run_command(message.content[1:], message.channel, message)

client = MogBot()
with open ("token.txt", "r") as token_file:
	token = token_file.readlines()

client.run(token[0])
