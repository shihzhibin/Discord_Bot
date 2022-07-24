#packages
import discord
from discord.ext import commands
import os




bot = commands.Bot(command_prefix='!')  # prefix our commands with '/'


@bot.command()
async def play(ctx, url : str):
     voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='哈利池')
     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
     await voiceChannel.connect()



@bot.event
async def on_member_join(member):
    channel = bot.get_channel(999653093929123935)
    tmpmsg = await channel.send(f"<@{member.id}> 早安午安晚安 (ΦωΦ)")
#start the bot with our token
bot.run("OTk3ODMxNzkyNjgzOTE3MzQy.GLZDdw.4wZYNfWawIn4-jqfokNeUQz-ZP0fl5seQQfqEo")





@bot.event
#當有訊息時
async def on_message(message):
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
