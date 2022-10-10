import discord
from discord.ext import commands
import json
import requests
import sqlite3
import random
import peewee
from peewee import *
from random import choice
import console
from console import sys_start


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

db = SqliteDatabase('utility.db')

class Money(Model):
    username = CharField(max_length=20)
    amount = IntegerField()

    class Meta:
        database = db

class Language(Model):
    guild_id = IntegerField()
    lang = CharField(max_length=20)

    class Meta:
        database = db

db.connect()
db.create_tables([Money, Language])

sys_start()

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    await ctx.send("Данной команды не существует.")

                else:
                    await ctx.send("Command does not exist.")

        else:
            await ctx.send("Command does not exist.")

game = discord.Game("$helpcom")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=game)
    for guild in bot.guilds:
        for member in guild.members:
            user = Money.get_or_none(username=member)
            if user is not None:
                pass

            else:
                account = Money.create(username=member, amount='0')

@bot.event
async def on_member_join(member):
    user = Money.get_or_none(username=member)
    if user is not None:
        pass

    else:
        account = Money.create(username=member, amount='0')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.group(invoke_without_command=True)
async def helpcom(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                help_emb = discord.Embed(title=f'Вызвано {ctx.author.name}', colour=0x39d0d6)
                help_emb.add_field(name='📃информация', value='$helpcom, $creator, $userinfo, $avatar', inline=False)
                help_emb.add_field(name='💻модерация', value='$ban, $kick, $role_add, $clear, $set_lang', inline=False)
                help_emb.add_field(name='⚒утилиты',
                                   value='$print, $create_channel, $contact, $doc_java, $doc_js, $doc_python, $discord_dev, $github, $wikifur',
                                   inline=False)
                help_emb.add_field(name='🎮развлечения', value='$fox, $numbers, $roll, $hug, $sum, $choice', inline=False)
                help_emb.add_field(name='💵экономика',
                                   value='$user_create_account, $give_money, $balance, $user_balance, $set_money, $work',
                                   inline=False)
                help_emb.add_field(name='💾другое', value='''$ping

                    Для полного описания команд пропишите **$commands_help**''', inline=False)
                await ctx.channel.send(embed=help_emb)
                await ctx.message.delete()

            else:
                help_emb = discord.Embed(title=f'Called by {ctx.author.name}', colour=0x39d0d6)
                help_emb.add_field(name='📃information', value='$helpcom, $creator, $userinfo, $avatar', inline=False)
                help_emb.add_field(name='💻moderation', value='$ban, $kick, $role_add, $clear, $set_lang', inline=False)
                help_emb.add_field(name='⚒utility',
                                   value='$print, $create_channel, $contact, $doc_java, $doc_js, $doc_python, $discord_dev, $github, $wikifur',
                                   inline=False)
                help_emb.add_field(name='🎮fun', value='$fox, $numbers, $roll, $hug, $sum, $choice', inline=False)
                help_emb.add_field(name='💵economy',
                                   value='$user_create_account, $give_money, $balance, $user_balance, $set_money, $work',
                                   inline=False)
                help_emb.add_field(name='💾other', value='''$ping

                    For commands description write **$commands_help**''', inline=False)
                await ctx.channel.send(embed=help_emb)
                await ctx.message.delete()

    else:
        help_emb = discord.Embed(title=f'Called by {ctx.author.name}', colour=0x39d0d6)
        help_emb.add_field(name='📃information', value='$helpcom, $creator, $userinfo, $avatar', inline=False)
        help_emb.add_field(name='💻moderation', value='$ban, $kick, $role_add, $clear, $set_lang', inline=False)
        help_emb.add_field(name='⚒utility',
                           value='$print, $create_channel, $contact, $doc_java, $doc_js, $doc_python, $discord_dev, $github, $wikifur',
                           inline=False)
        help_emb.add_field(name='🎮fun', value='$fox, $numbers, $roll, $hug, $sum, $choice', inline=False)
        help_emb.add_field(name='💵economy',
                           value='$user_create_account, $give_money, $balance, $user_balance, $set_money, $work',
                           inline=False)
        help_emb.add_field(name='💾other', value='''$ping

            For commands description write **$commands_help**''', inline=False)
        await ctx.channel.send(embed=help_emb)
        await ctx.message.delete()


@bot.group(invoke_without_command=True)
async def creator(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send('Orix bot был создан **Mechasdl#1401**')

            else:
                await ctx.send('Orix bot was created by **Mechasdl#1401**')

    else:
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
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send(f'Пользователь <@{member.id}> был забанен')
                await member.ban(reason=reason)

            else:
                await ctx.send(f'User <@{member.id}> was banned')
                await member.ban(reason=reason)

    else:
        await ctx.send(f'User <@{member.id}> was banned')
        await member.ban(reason=reason)

@bot.group(invoke_without_command=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send(f'Пользователь <@{member.id}> был кикнут')
                await member.kick(reason=reason)

            else:
                await ctx.send(f'User <@{member.id}> was kicked')
                await member.kick(reason=reason)

    else:
        await ctx.send(f'User <@{member.id}> was kicked')
        await member.kick(reason=reason)

@bot.group(invoke_without_command=True)
async def numbers(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.message.channel

                number = random.randint(1, 100)
                await ctx.send('Я загадал число от 1 до 100, отгадай это число')

                for i in range(0, 5):
                    guess = await bot.wait_for('message', check=check)

                    if guess.content < str(number):
                        await ctx.send('Больше!')

                    elif guess.content > str(number):
                        await ctx.send('Меньше!')

                    elif guess.content == str(number):
                        await ctx.send('ты победил!')

                    else:
                        return  # Or something else

                else:
                    await ctx.send("You lost, type $numbers to play again.")

            else:
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
                    await ctx.send("You lost, type $numbers to play again.")

    else:
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
            await ctx.send("You lost, type $numbers to play again.")

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
@commands.has_permissions(administrator=True)
async def userinfo(ctx,member:discord.Member = None, guild: discord.Guild = None):
    await ctx.message.delete()
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                if member == None:
                    emb = discord.Embed(title="Информация", color=ctx.message.author.color)
                    emb.add_field(name="Имя :", value=ctx.message.author.display_name, inline=False)
                    emb.add_field(name="Айди :", value=ctx.message.author.id, inline=False)
                    t = ctx.message.author.status

                    emb.add_field(name="Статус :", value=ctx.message.author.activity, inline=False)
                    emb.add_field(name="Роль на сервере :", value=f"{ctx.message.author.top_role.mention}", inline=False)
                    emb.add_field(name="Аккаунт был создан :",
                                  value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                  inline=False)
                    emb.set_thumbnail(url=ctx.message.author.avatar_url)
                    await ctx.send(embed=emb)
                else:
                    emb = discord.Embed(title="Информация", color=member.color)
                    emb.add_field(name="Имя :", value=member.display_name, inline=False)
                    emb.add_field(name="Айди :", value=member.id, inline=False)
                    t = member.status

                    emb.add_field(name="Статус :", value=member.activity, inline=False)
                    emb.add_field(name="Роль на сервере :", value=f"{member.top_role.mention}", inline=False)
                    emb.add_field(name="Аккаунт был создан :",
                                  value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
                    await ctx.send(embed=emb)

            else:
                if member == None:
                    emb = discord.Embed(title="User information", color=ctx.message.author.color)
                    emb.add_field(name="Name :", value=ctx.message.author.display_name, inline=False)
                    emb.add_field(name="User ID :", value=ctx.message.author.id, inline=False)
                    t = ctx.message.author.status

                    emb.add_field(name="Status :", value=ctx.message.author.activity, inline=False)
                    emb.add_field(name="Server role :", value=f"{ctx.message.author.top_role.mention}", inline=False)
                    emb.add_field(name="Account was created :",
                                  value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                  inline=False)
                    emb.set_thumbnail(url=ctx.message.author.avatar_url)
                    await ctx.send(embed=emb)
                else:
                    emb = discord.Embed(title="User information", color=member.color)
                    emb.add_field(name="Name :", value=member.display_name, inline=False)
                    emb.add_field(name="User ID :", value=member.id, inline=False)
                    t = member.status

                    emb.add_field(name="Status :", value=member.activity, inline=False)
                    emb.add_field(name="Server role :", value=f"{member.top_role.mention}", inline=False)
                    emb.add_field(name="Account was created :",
                                  value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
                    await ctx.send(embed=emb)

    else:
        if member == None:
            emb = discord.Embed(title="User information", color=ctx.message.author.color)
            emb.add_field(name="Name :", value=ctx.message.author.display_name, inline=False)
            emb.add_field(name="User ID :", value=ctx.message.author.id, inline=False)
            t = ctx.message.author.status

            emb.add_field(name="Status :", value=ctx.message.author.activity, inline=False)
            emb.add_field(name="Server role :", value=f"{ctx.message.author.top_role.mention}", inline=False)
            emb.add_field(name="Account was created :",
                          value=ctx.message.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
            emb.set_thumbnail(url=ctx.message.author.avatar_url)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title="User information", color=member.color)
            emb.add_field(name="Name :", value=member.display_name, inline=False)
            emb.add_field(name="User ID :", value=member.id, inline=False)
            t = member.status

            emb.add_field(name="Status :", value=member.activity, inline=False)
            emb.add_field(name="Server role :", value=f"{member.top_role.mention}", inline=False)
            emb.add_field(name="Account was created :", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                          inline=False)
            await ctx.send(embed=emb)

@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send('```Сообщения были успешно удалены```')

            else:
                await ctx.send('```Messages were successfully deleted```')

    else:
        await ctx.send('```Messages were successfully deleted```')

@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def print(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg

	await ctx.channel.send(response)
@bot.group(invoke_without_command=True)
@commands.has_permissions(manage_roles = True)
async def role_add(ctx, user : discord.Member, role:discord.Role):
    await user.add_roles(role)
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send(f" Вы добавили роль {role} пользователю {user.mention}")

            else:
                await ctx.send(f" Added role {role} to {user.mention}")

    else:
        await ctx.send(f" Added role {role} to {user.mention}")

@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar
    await ctx.send(userAvatarUrl)

@bot.group(invoke_without_command=True)
async def commands_help(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                help_emb = discord.Embed(title=f'Вызвано {ctx.author.name}', colour=0x39d0d6)
                help_emb.add_field(name='📃информация',
                                   value='$helpcom - список всех команд,\n$creator - информация о создателе,\n$userinfo [пользователь] - показывает информацию об указанном пользователе,\n$avatar [пользователь] - показывает аватар указанного пользователя,\n$commands_help - описание всех команд',
                                   inline=False)
                help_emb.add_field(name='💻модерация',
                                   value='$ban [пользователь] [причина] - банит указанного пользователя,\n$kick [пользователь] [причина] - кикает указанного пользователя,\n$role_add [роль] [пользователь] - добавляет указанную роль, указанному пользователю,\n$clear [количество] - удаляет указанное количество сообщений, \n$setlang [eng] - set bot language to english',
                                   inline=False)
                help_emb.add_field(name='⚒утилиты',
                                   value="$print [сообщение] - выводит указанное сообщение,\n$create_channel [название] - создает новый канал с указанным названием,\n$contact - сообщите о проблеме,\n$doc_java - документация джава,\n$doc_js - документация джаваскрипт,\n$doc_python - документация питона,\n$discord_dev - портал разработчиков дискорд,\n$github - репозиторий проекта в гитхабе,\n$wikifur - Викифур",
                                   inline=False)
                help_emb.add_field(name='🎮развлечения',
                                   value="$fox - рандомная картинка милой лисички🦊\n$numbers - угадай число!\n$roll [количество бросков] [количество сторон] - бросает кубик\n$hug [user] - обнимает указанного пользователя\n$sum [число] [число] - складывает два указанных числа\n$choice - Orix ответит 'да' или 'нет'",
                                   inline=False)
                help_emb.add_field(name='💵экономика',
                                   value="$user_create_account [пользователь] - создает аккаунт для указанного пользователя,\n$give_money [пользователь] [количество] - вы отдаете указанную сумму денег другому пользователю,\n$balance - показывает ваш баланс,\n$user_balance [пользователь] - показывает баланс указанного пользователя,\n$set_money [пользователь] [количество] - устанавливает указанное количество денег, указанному пользователю,\n$work - вы можете заработать немного денег, но ваша зарплата не постоянна",
                                   inline=False)
                help_emb.add_field(name='💾другое', value='$ping - replies with pong', inline=False)
                await ctx.channel.send(embed=help_emb)
                await ctx.message.delete()

            else:
                help_emb = discord.Embed(title=f'Called by {ctx.author.name}', colour=0x39d0d6)
                help_emb.add_field(name='📃information',
                                   value='$helpcom - information about commands,\n$creator - information about creator,\n$userinfo [user] - shows user information,\n$avatar [user] - shows user avatar,\n$commands_help - commands description',
                                   inline=False)
                help_emb.add_field(name='💻moderation',
                                   value='$ban [user] [why?] - bans mentioned user,\n$kick [user] [why?] - kicks mentioned user,\n$role_add [role] [user] - adds mentioned role to a mentioned user,\n$clear [amount] - deletes previous messages, \n$setlang [ru] - изменить язык бота на русский',
                                   inline=False)
                help_emb.add_field(name='⚒utility',
                                   value="$print [message] - prints your message,\n$create_channel [name] - creates new server channel,\n$contact - contact bot creator,\n$doc_java - java documentation,\n$doc_js - JavaScript documentation,\n$doc_python - python documentation,\n$discord_dev - discord developer portal,\n$github - our github page,\n$wikifur - Wikifur community",
                                   inline=False)
                help_emb.add_field(name='🎮fun',
                                   value="$fox - random picture of a cute fox🦊\n$numbers - guess a number!\n$roll [rolls amount] [sides amount] - rolls a dice\n$hug [user] - hugs mentioned user\n$sum [number] [number] - sums two mentioned numbers\n$choice - Orix will answer 'yes' or 'no'",
                                   inline=False)
                help_emb.add_field(name='💵economy',
                                   value="$user_create_account [user] - creates account for mentioned user,\n$give_money [user] [amount] - give some amount of your money to mentioned user,\n$balance - shows your current balance,\n$user_balance [user] - shows mentioned user balance,\n$set_money [user] [amount] - sets mentioned amount of money to mentioned user,\n$work - you can earn some money, but your salary is not stable",
                                   inline=False)
                help_emb.add_field(name='💾other', value='$ping - replies with pong', inline=False)
                await ctx.channel.send(embed=help_emb)
                await ctx.message.delete()

    else:
        help_emb = discord.Embed(title=f'Called by {ctx.author.name}', colour=0x39d0d6)
        help_emb.add_field(name='📃information',
                           value='$helpcom - information about commands,\n$creator - information about creator,\n$userinfo [user] - shows user information,\n$avatar [user] - shows user avatar,\n$commands_help - commands description',
                           inline=False)
        help_emb.add_field(name='💻moderation',
                           value='$ban [user] [why?] - bans mentioned user,\n$kick [user] [why?] - kicks mentioned user,\n$role_add [role] [user] - adds mentioned role to a mentioned user,\n$clear [amount] - deletes previous messages, \n$setlang [ru] - изменить язык бота на русский',
                           inline=False)
        help_emb.add_field(name='⚒utility',
                           value="$print [message] - prints your message,\n$create_channel [name] - creates new server channel,\n$contact - contact bot creator,\n$doc_java - java documentation,\n$doc_js - JavaScript documentation,\n$doc_python - python documentation,\n$discord_dev - discord developer portal,\n$github - our github page,\n$wikifur - Wikifur community",
                           inline=False)
        help_emb.add_field(name='🎮fun',
                           value="$fox - random picture of a cute fox🦊\n$numbers - guess a number!\n$roll [rolls amount] [sides amount] - rolls a dice\n$hug [user] - hugs mentioned user\n$sum [number] [number] - sums two mentioned numbers\n$choice - Orix will answer 'yes' or 'no'",
                           inline=False)
        help_emb.add_field(name='💵economy',
                           value="$user_create_account [user] - creates account for mentioned user,\n$give_money [user] [amount] - give some amount of your money to mentioned user,\n$balance - shows your current balance,\n$user_balance [user] - shows mentioned user balance,\n$set_money [user] [amount] - sets mentioned amount of money to mentioned user,\n$work - you can earn some money, but your salary is not stable",
                           inline=False)
        help_emb.add_field(name='💾other', value='$ping - replies with pong', inline=False)
        await ctx.channel.send(embed=help_emb)
        await ctx.message.delete()

@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
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
async def inspiration(ctx):
    await ctx.send('https://steamcommunity.com/id/goldrenard/')

@bot.group(invoke_without_command=True)
async def host(ctx):
    await ctx.send('https://dashboard.heroku.com/apps/orix-bot-15/resources')

@bot.group(invoke_without_command=True)
async def hug(ctx, user : discord.Member):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send(f"Обнял {user.mention}!")

            else:
                await ctx.send(f"Hugged {user.mention}!")

    else:
        await ctx.send(f"Hugged {user.mention}!")

@bot.group(invoke_without_command=True)
async def contact(ctx):
    await ctx.send('https://linktr.ee/crysaliux')

@bot.group(invoke_without_command=True)
async def sum(ctx, a: int, b: int):
    sum = a + b
    await ctx.send(sum)

@bot.group(invoke_without_command=True)
async def choice(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                from random import choice
                answer = choice(['да', 'нет'])
                await ctx.send(answer)

            else:
                from random import choice
                answer = choice(['yes', 'no'])
                await ctx.send(answer)

    else:
        from random import choice
        answer = choice(['yes', 'no'])
        await ctx.send(answer)

@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def user_create_account(ctx, user : discord.Member):
    user_get = Money.get_or_none(username=user)
    if user_get is not None:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    await ctx.send("У этого пользователя уже есть аккаунт!")

                else:
                    await ctx.send("This user has already got an account!")

        else:
            await ctx.send("This user has already got an account!")

    else:
        account = Money.create(username=user, amount='0')
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    await ctx.send(f"Вы успешно создали аккаунт для пользователя: {user}")

                else:
                    await ctx.send(f"You have successfully created your account for user: {user}")

        else:
            await ctx.send(f"You have successfully created your account for user: {user}")

@bot.group(invoke_without_command=True)
async def give_money(ctx, user : discord.Member, *, much: int):
    for money in Money.select().where(Money.username == ctx.author):
        if money.amount < much:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        await ctx.send("У вас недостаточно денег!")

                    else:
                        await ctx.send("You dont have enough money!")

            else:
                await ctx.send("You dont have enough money!")

        else:
            for money in Money.select().where(Money.username == ctx.author):
                delete = Money.get(Money.username == ctx.author)
                delete.delete_instance()
                account = Money.create(username=ctx.author, amount=money.amount - clamp(much, 0, 10000))
                for money in Money.select().where(Money.username == user):
                    delete = Money.get(Money.username == user)
                    delete.delete_instance()
                    account = Money.create(username=user, amount=money.amount + clamp(much, 0, 10000))
                    getlang = Language.get_or_none(guild_id=ctx.guild.id)
                    if getlang is not None:
                        for language in Language.select().where(Language.guild_id == ctx.guild.id):
                            if language.lang == "ru":
                                await ctx.send(f"Вы дали {much} золота пользователю: {user}")

                            else:
                                await ctx.send(f"You gave {much} gold to user: {user}")

                    else:
                        await ctx.send(f"You gave {much} gold to user: {user}")

@bot.group(invoke_without_command=True)
async def balance(ctx):
    for money in Money.select().where(Money.username == ctx.author):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    await ctx.send(f"У вас {money.amount} золота")

                else:
                    await ctx.send(f"You have {money.amount} gold")

        else:
            await ctx.send(f"You have {money.amount} gold")

@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def user_balance(ctx, user : discord.Member):
    for money in Money.select().where(Money.username == user):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    await ctx.send(
                        f"Пользователь {user} имеет {money.amount} золота")

                else:
                    await ctx.send(f"User {user} has {money.amount} gold")

        else:
            await ctx.send(f"User {user} has {money.amount} gold")

@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def set_money(ctx, user : discord.Member, *, much: int):
    delete = Money.get(Money.username == user)
    delete.delete_instance()
    account = Money.create(username=user, amount=much)
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send(
                    f"Вы установили {much} золота для пользователя: {user}")

            else:
                await ctx.send(f"You have set {much} gold for user: {user}")

    else:
        await ctx.send(f"You have set {much} gold for user: {user}")

@bot.group(invoke_without_command=True)
@commands.cooldown(1, 10000.0, commands.BucketType.user)
async def work(ctx):
    salary = random.randint(1, 150)
    for money in Money.select().where(Money.username == ctx.author):
        delete = Money.get(Money.username == ctx.author)
        delete.delete_instance()
        account = Money.create(username=ctx.author, amount=money.amount + salary)
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    await ctx.send(f"Вы очень усердно работали эту неделю и вы заработали немного денег, этого должно хватить...")

                else:
                    await ctx.send(
                        f"You have been working hard this week and you earned some money, lets hope that will be enough...")

        else:
            await ctx.send(
                f"You have been working hard this week and you earned some money, lets hope that will be enough...")

@bot.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def set_lang(ctx, *, lang: str):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        delete = Language.get(Language.guild_id == ctx.guild.id)
        delete.delete_instance()
        langset = Language.create(guild_id=ctx.guild.id, lang=lang)
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send("Вы изменили язык бота на русский")

            else:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "eng":
                        await ctx.send("Your bot language is english")

    else:
        langset = Language.create(guild_id=ctx.guild.id, lang=lang)
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.send("Вы изменили язык бота на русский")

            else:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "eng":
                        await ctx.send("Your bot language is english")
