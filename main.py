import asyncio
import youtube_dl
import pafy
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix='!')  # prefix our commands with '!'

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.event
async def on_member_join(member):
    await bot.process_commands(member)
    channel = bot.get_channel(999653093929123935)
    tmpmsg = await channel.send(f"<@{member.id}> 早安午安晚安 (ΦωΦ)")

@bot.event
#有訊息時,觸發事件
async def on_message(message):
    await bot.process_commands(message)
    channel = bot.get_channel(999653093929123935)
    keyword   = ["hi","嗨","哈摟"]
    keyword_1 = ["哈利","蜘蛛"]
    keyword_2 = ["桌遊","uno"]
    if message.content in keyword :
        tmpmsg = await channel.send(f"Hi <@{message.author.id}>")
    if message.content in keyword_1:
        tmpmsg = await channel.send('@everyone 打哈利瞜 (ΦωΦ)')
    if message.content in keyword_2:
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
        tmpmsg = await channel.send('ray 能當你男友嗎(๑•̀ㅂ•́)و✧')
    if message.content  == "diffin" or message.content == 'Diffin':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await channel.send('diffin 想你 （づ￣3￣）づ╭❤～')
    if message.content == 'Eru'or message.content == 'eru':
        #發送訊息，並將本次訊息資料存入tmpmsg，方便之後刪除
        tmpmsg = await channel.send('Eru 破關機器 ก็ʕ•͡ᴥ•ʔ ก้')
    if message.content == "帥":
        tmpmsg = await channel.send(f'<@{message.author.id}> 唉呦，你要確定ㄟ (ー`′ー)')
    if message.content == '阿秀':
        tmpmsg = await channel.send('阿秀  早安午安晚安 ≡ω≡')
    if message.content == '暉智':
        tmpmsg = await channel.send('暉智 要回來找我呦~ ✧(≖ ◡ ≖✿)')
    if message.content == '甄甄':
        tmpmsg = await channel.send('甄甄 歡迎加入~ ✧(≖ ◡ ≖✿)')

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel, please connect to the channel you want the bot to join.")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, *, song=None):
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
                return await ctx.send(f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}.")

            else:
                return await ctx.send("Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("You forgot to include a song to search for.")

        await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(3, song)

        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", colour=discord.Colour.red())

        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command()
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
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
