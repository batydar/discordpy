import discord
from discord.ext import commands, tasks
from utils import *
from functions import *
import os

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(command_prefix="k!", intents=intents)
game = Game()


@Bot.event
async def on_ready():
    batydar2.start()
    await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Sizi"))
    print('Ben hazırım')
    Channel = Bot.get_channel(998394790251081859)
    await Channel.purge(limit=5)
    Text = "Kayıt olmak için tıklayınız"
    Moji = await Channel.send(Text)
    await Moji.add_reaction('🎉')


@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="hos-geldiniz")
    await channel.send(f"{member.mention} aramıza katıldı, Hoş geldi!")


@Bot.event
async def on_reaction_add(reaction, member):
    Channel = Bot.get_channel(998394790251081859)
    if reaction.message.channel.id != Channel.id:
        return
    if reaction.emoji == "🎉":
        Role = discord.utils.get(member.guild.roles, name="üye")
        await member.add_roles(Role)


@tasks.loop(hours=24)
async def batydar2():
    for c in Bot.get_all_channels():
        if c.id == 951837316295557190:
            await c.send("s aktifleşin lan")


@Bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="gorusuruz")
    await channel.send(f"{member.mention} aramızdan ayrıldı, Görüşürüz :cry:")
    print(f"{member} aramızdan ayrıldı, Görüşürüz :sad:")


@Bot.command()
async def batydar(ctx):
    await ctx.send('Ustam')


@Bot.command(aliases=["game", "zar", "oyun"])
async def dice(ctx, *args):
    if "roll" in args:
        await ctx.send(game.roll_dice())
    else:
        await ctx.send("'roll' yazmadığın sürece zar atmam")


@Bot.command()
@commands.has_role("mod")
async def clear(ctx, amount):
    await ctx.channel.purge(limit=int(amount))


@Bot.command()
@commands.has_role("mod")
async def kick(ctx, member: discord.Member, *args, reason="Yok"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} atıldı :x:")


@Bot.command(aliases=["copy"])
@commands.has_role("admin")
async def clone_channel(ctx, amount=1):
    for i in range(amount):
        await ctx.channel.clone()
    await ctx.send("Başarıyla kopyalandı")


@Bot.command()
@commands.has_role("admin")
async def ban(ctx, member: discord.Member, *args, reason="Yok"):
    await member.ban(reason=reason)


@Bot.command()
@commands.has_role("admin")
async def idunban(ctx, *, members):
    banned_users = await ctx.guild.bans()
    user_id = members

    for bans in banned_users:
        user = bans.user

        print(user)
        print(user.id)
        print(user_id)

        if (str(user.id) == str(user_id)):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned user {user.mention}")
            return


@Bot.command()
@commands.has_role("admin")
async def unban(ctx, *, members):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = members.split('#')

    for bans in banned_users:
        user = bans.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned user {user.mention}")
            return


@Bot.command()
async def load(ctx, extension):
    yourID = 267002229179940866
    if ctx.message.author.id == yourID:
        Bot.load_extension(f"cogs.{extension}")
    else:
        await ctx.send('Botun sahibi ve yetkilendirdikleri dışındakiler bu komutu kullanamaz')


@Bot.command()
async def reload(ctx, extension):
    yourID = 267002229179940866
    if ctx.message.author.id == yourID:
        Bot.unload_extension(f"cogs.{extension}")
        Bot.load_extension(f"cogs.{extension}")
    else:
        await ctx.send('Botun sahibi ve yetkilendirdikleri dışındakiler bu komutu kullanamaz')


@Bot.command()
async def question(ctx):
    await ctx.message.add_reaction("🇦")
    await ctx.message.add_reaction("🇧")
    await ctx.message.add_reaction("🇨")
    await ctx.message.add_reaction("🇩")


@Bot.command()
async def unload(ctx, extension):
    yourID = 267002229179940866
    if ctx.message.author.id == yourID:
        Bot.unload_extension(f"cogs.{extension}")
    else:
        await ctx.send('Botun sahibi ve yetkilendirdikleri dışındakiler bu komutu kullanamaz')


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        Bot.load_extension(f"cogs.{filename[:-3]}")

Bot.run(TOKEN)
