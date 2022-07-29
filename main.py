import discord
from discord.ext import commands
import os
import asyncio
import youtube_dl
import pafy
from discord.utils import get
from discord import PCMVolumeTransformer

intents = discord.Intents.default()
intents.members = True

# prefix our commands with '!'
bot = commands.Bot(command_prefix='!')



@bot.event
async def on_ready():
    print("Bot is ready")

@bot.event
async def on_member_join(member):
    await bot.process_commands(member)
    channel = bot.get_channel(985195225096007741)
    tmpmsg = await channel.send(f"<@{member.id}> 早安午安晚安 (ΦωΦ)")

@bot.event
#有訊息時,觸發事件
async def on_message(message):
    await bot.process_commands(message)
    channel = bot.get_channel(985195225096007741)
    keyword   = ["hi","嗨","哈摟"]
    keyword_1 = ["哈利","蜘蛛","綠仙","山怪"]
    keyword_2 = ["演奏會"]
    keyword_3 = ["桌遊","uno","狼人殺"]
    if message.content in keyword :
        tmpmsg = await channel.send(f"Hi <@{message.author.id}>")
    if message.content in keyword_1:
        tmpmsg = await channel.send('@everyone 打哈利瞜 (ΦωΦ)')
    if message.content in keyword_2:
        tmpmsg = await channel.send('@everyone 鋼琴演奏會 快開始搂 (ΦωΦ) 地點:艾蘭多收藏室')
    if message.content in keyword_3:
        tmpmsg = await channel.send('@everyone 桌遊開打瞜 (ΦωΦ)')
    #如果以「說」開頭
    if message.content.startswith('說'):
      #分割訊息成兩份
      tmp = message.content.split(" ",2)
      #如果分割後串列長度只有1
      if len(tmp) == 1:
        await channel.send("<@{ctx.author.id}> 你要我說什麼啦 ε٩(๑> ₃ <)۶з")
      else:
        await channel.send(tmp[1])
    if message.content == '弗麗嘉':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await channel.send('看到弗麗嘉 天天都開心 ε٩(๑> ₃ <)۶з"')
    if message.content == '怪女孩':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await channel.send('怪女孩 你今天好像很美? ε٩(๑> ₃ <)۶з"')
    if message.content == '番茄' :
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await channel.send('番茄 屁眼站出來o(≧口≦)o')
    if message.content == "ray" or message.content == 'Ray':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await channel.send('ray 聽說你的鳥很大(๑•̀ㅂ•́)و✧')
    if message.content  == "diffin" or message.content == 'Diffin':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await channel.send('diffin 想你 （づ￣3￣）づ╭❤～')
    if message.content == 'Eru'or message.content == 'eru':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await channel.send('Eru 破關機器 ก็ʕ•͡ᴥ•ʔ ก้')
    if message.content == "帥" or message.content == '我好帥':
        tmpmsg = await channel.send(f'<@{message.author.id}> 唉呦，你要確定ㄟ (ー`′ー)')
    if message.content == '阿秀':
        tmpmsg = await channel.send('阿秀  早安午安晚安 ≡ω≡')
    if message.content == '暉智':
        tmpmsg = await channel.send('暉智 要回來找我呦~ ✧(≖ ◡ ≖✿)')
    if message.content == '甄甄':
        tmpmsg = await channel.send('甄甄 歡迎加入~ ✧(≖ ◡ ≖✿)')
    if message.content == '屁眼':
        tmpmsg = await channel.send(f' 屁眼派對萬歲 ✧(≖ ◡ ≖✿) ')


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # 2d array containing [song, channel]
        self.song_queue = {}
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0:
            return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel, please connect to the channel you want the bot to join.")

        else:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Connected to voice channel: '{channel}'")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, *,song = None):
        if song is None:
            return await ctx.send("You must include a song to play.")

        if ctx.voice_client is None:
            return await ctx.send("I must be in a voice channel to play a song.")

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I could not find the given song, try using my search command.")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"Song added to the queue at position {queue_len+1}")

            else:
                return await ctx.send("Maximum queue limit has been reached, please wait for the current song to end to add more songs to the queue")

        await self.play_song(ctx,song)
        await ctx.send(f"Now playing: {song}")


    @commands.command()
    async def vol(self, ctx = commands.Context, *,percentage: float):
        """Changes the player's volume"""

        volume = max(0.0, min(1.0, percentage / 100))

        source = ctx.guild.voice_client.source

        if not isinstance(source, discord.PCMVolumeTransformer):
            return await ctx.send("This source doesn't support adjusting volume or "
                                  "the interface to do so is not exposed.")
        source.volume = volume

        await ctx.send(f'**`{ctx.author}`**: Set the volume to **{volume * 100:.2f}%**')

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You forgot to include a song to search for.")

        await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(3, song)

        embed = discord.Embed(title="Song Queue",
                      description="",
                      colour=discord.Colour.dark_gold())

        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)
    @commands.command()
    async def checkqueue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("Queue is empty")
        else:
            embed = discord.Embed(title="Song Queue", description="", colour=discord.colour.blue())
            i = 1
            for url in self.song_queue[ctx.guild.id]:
                embed.description += f"{i}) {url}\n"
                i += 1
            await ctx.send(embed=embed)
            await ctx.send("Loading....")

    @commands.command()
    async def queue(self, ctx, *, song=None): # display the current guilds queue
        if song is None:
            return await ctx.send("You must include a song to queue.")

        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for a song, this may take a few seconds...")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I couldn't find the song you asked for. Try using my search command to find the song you want.")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"Song added to the queue at position {queue_len+1}")
            else:
                return await ctx.send("Maximum queue limit has been reached, please wait for the current song to end to add more songs to the queue")

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        #try to play next in the queue if it exists
        await self.play_music(ctx)


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")

        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.")


async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))

bot.loop.create_task(setup())
bot.run("TOKEN")
