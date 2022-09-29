import discord
from discord.ext import commands
import json
import requests
import sqlite3
import random
import peewee
from peewee import *


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

conn = sqlite3.connect('data.db')
cur = conn.cursor()

bot = commands.Bot(command_prefix='+', intents=intents)
bot.remove_command('help')

db = SqliteDatabase('data.db')

class Server(Model):
    id = IntegerField()
    content = CharField(max_length=20)

    class Meta:
        database = db

db.connect()
db.create_tables([Server])

cur.execute("SELECT * FROM Server;")
result = cur.fetchall()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    guildid = message.guild.id
    cont = message.content
    guild = Server.create(id=guildid, content=cont)
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command does not exist.")

game = discord.Game("+helpcom")
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.group(invoke_without_command=True)
async def helpcom(ctx):
    await ctx.send('''
📃**information**
+helpcom, +creator, +userinfo, +avatar

💻**moderation**
+ban, +kick, +role_add, +clear

⚒**utility**
+print, +create_channel, +doc_java, +doc_js, +doc_python, 
+discord_dev, +github, +wikifur

🎮**fun**
+fox, +numbers, +roll

💾**other**
+ping

Write **+commands_help** for commands description
''')


@bot.group(invoke_without_command=True)
async def creator(ctx):
    await ctx.send('Orix bot was created by **Mechasdl#1401**')


@bot.group(invoke_without_command=True)
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Random Fox')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


@bot.group(invoke_without_command=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'User <@{member.id}> was banned')
    await member.ban(reason=reason)


@bot.group(invoke_without_command=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'User <@{member.id}> was kicked')
    await member.kick(reason=reason)


@bot.group(invoke_without_command=True)
async def numbers(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.message.channel

    number = random.randint(1, 100)
    await ctx.send('I have a number in mind between 1 and 100, guess')

    for i in range(0, 5):
        guess = await bot.wait_for('message', check=check)

        if guess.content < str(number):
            await ctx.send('Higher!')

        elif guess.content > str(number):
            await ctx.send('Lower!')

        elif guess.content == str(number):
            await ctx.send('you won!')

        else:
            return  # Or something else

    else:
        await ctx.send("You lost, type +numbers to play again.")


@bot.group(invoke_without_command=True)
async def doc_java(ctx):
    await ctx.send('https://docs.oracle.com/en/java/')

@bot.group(invoke_without_command=True)
async def doc_js(ctx):
    await ctx.send('https://devdocs.io/javascript/')

@bot.group(invoke_without_command=True)
async def doc_python(ctx):
    await ctx.send('https://docs.python.org/3/')
    
@bot.group(invoke_without_command=True)
async def discord_dev(ctx):
    await ctx.send('https://discord.com/developers/docs/intro')

@bot.group(invoke_without_command=True)
async def github(ctx):
    await ctx.send('https://github.com/Crysaliux')

@bot.group(invoke_without_command=True)
async def userinfo(ctx,member:discord.Member = None, guild: discord.Guild = None):
    await ctx.message.delete()
    if member == None:
        emb = discord.Embed(title="User information", color=ctx.message.author.color)
        emb.add_field(name="Name :", value=ctx.message.author.display_name,inline=False)
        emb.add_field(name="User ID :", value=ctx.message.author.id,inline=False)
        t = ctx.message.author.status

        emb.add_field(name="Status :", value=ctx.message.author.activity,inline=False)
        emb.add_field(name="Server role :", value=f"{ctx.message.author.top_role.mention}",inline=False)
        emb.add_field(name="Account was created :", value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        emb.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title="User information", color=member.color)
        emb.add_field(name="Name :", value=member.display_name,inline=False)
        emb.add_field(name="User ID :", value=member.id,inline=False)
        t = member.status

        emb.add_field(name="Status :", value=member.activity,inline=False)
        emb.add_field(name="Server role :", value=f"{member.top_role.mention}",inline=False)
        emb.add_field(name="Account was created :", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
        await ctx.send(embed = emb)

@bot.group(invoke_without_command=True)
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))
    await ctx.channel.send('```Messages were successfully deleted```')

@bot.group(invoke_without_command=True)
async def print(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg

	await ctx.channel.send(response)
@bot.group(invoke_without_command=True)
@commands.has_permissions(manage_roles = True)
async def role_add(ctx, user : discord.Member, role:discord.Role):
    await user.add_roles(role)
    await ctx.send(f" Added role {role} to {user.mention}")

@bot.group(invoke_without_command=True)
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar
    await ctx.send(userAvatarUrl)

@bot.group(invoke_without_command=True)
async def commands_help(ctx):
    await ctx.send('''
📃**information**
+helpcom - information about commands,
+creator - information about creator, 
+userinfo [user] - shows user information, 
+avatar [user] - shows user avatar,
+commands_help - commands description

💻**moderation**
+ban [user] [why?] - bans mentioned user, 
+kick [user] [why?] - kicks mentioned user,
+role_add [role] [user] - adds mentioned role to a mentioned user,
+clear [amount] - deletes previous messages

⚒**utility**
+print [message] - prints your message,
+create_channel [name] - creates new server channel,
+doc_java - java documentation, 
+doc_js - JavaScript documentation, 
+doc_python - python documentation,
+discord_dev - discord developer portal, 
+github - our github page,
+wikifur - Wikifur community

🎮**fun**
+fox - random picture of a cute fox🦊
+numbers - guess a number!
+roll [rolls amount] [sides amount] - rolls a dice

💾**other**
+ping - replies with pong
''')

@bot.group(invoke_without_command=True)
async def create_channel(ctx, *, name):
    await ctx.guild.create_text_channel(name)

@bot.group(invoke_without_command=True)
async def wikifur(ctx):
    await ctx.send("https://ru.wikifur.com/wiki/")

@bot.group(invoke_without_command=True)
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.group(invoke_without_command=True)
async def scc(ctx):
    await ctx.send('''
    
+inspiration
+host
+audit_data''')

@bot.group(invoke_without_command=True)
async def inspiration(ctx):
    await ctx.send('https://steamcommunity.com/id/goldrenard/')

@bot.group(invoke_without_command=True)
async def host(ctx):
    await ctx.send('https://dashboard.heroku.com/apps/orix-bot-15/resources')

@bot.group(invoke_without_command=True)
async def audit_data(ctx):
    await ctx.send(result)


bot.run('')