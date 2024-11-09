import discord
from discord.ext import commands
import json
import requests
import sqlite3
import random
import peewee
from peewee import *
from random import choice

#Intents are not provided, cause safety reasons

bot = commands.Bot(command_prefix='A.', intents=intents)
bot.remove_command('help')
#loading extensions, economy, moderation, utilities, information, fun
bot.load_extension("Au_econ")
bot.load_extension("Au_mod")
bot.load_extension("Au_util")
bot.load_extension("Au_info")
bot.load_extension("Au_fun")
#MySQL is used as a database
e_db = MySQLDatabase('-', user='-', password='-',
                         host='-', port=0)

class Money(Model):
    guild_id = BigIntegerField()
    user_id = BigIntegerField()
    amount = BigIntegerField()

    class Meta:
        database = e_db

class Bank(Model):
    guild_id = BigIntegerField()
    user_id = BigIntegerField()
    amount = BigIntegerField()

    class Meta:
        database = e_db

class Shop(Model):
    guild_id = BigIntegerField()
    item = CharField(max_length=20)
    cost = BigIntegerField()
    extra_roles = BigIntegerField()

    class Meta:
        database = e_db

e_db.connect()
e_db.create_tables([Money, Bank, Shop])

u_db = MySQLDatabase('-', user='-', password='-',
                         host='-', port=0)

class Warns(Model):
    guild_id = BigIntegerField()
    user_id = BigIntegerField()
    warn = CharField(max_length=200)
    index = BigIntegerField()

    class Meta:
        database = u_db

class Language(Model):
    guild_id = BigIntegerField()
    lang = CharField(max_length=20)

    class Meta:
        database = u_db

class Join(Model):
    guild_id = BigIntegerField()
    role_id = BigIntegerField()
    settings = CharField(max_length=20)

    class Meta:
        database = u_db

class Mute(Model):
    guild_id = BigIntegerField()
    role_id = BigIntegerField()
    settings = CharField(max_length=20)

    class Meta:
        database = u_db

class Ticket(Model):
    guild_id = BigIntegerField()
    index = BigIntegerField()

    class Meta:
        database = u_db

class TicketRole(Model):
    guild_id = BigIntegerField()
    role_id = BigIntegerField()

    class Meta:
        database = u_db

class Logs(Model):
    guild_id = BigIntegerField()
    channel_id = BigIntegerField()
    settings = CharField(max_length=20)

    class Meta:
        database = u_db

u_db.connect()
u_db.create_tables([Warns, Language, Join, Mute, Ticket, TicketRole, Logs])

community_rights = '-'
creator_url = '-'
game = discord.Game("-")

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandNotFound):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    em = discord.Embed(title="⚠Несуществующая команда⚠",
                                       description='Данной команды не существует.',
                                       color=0xFFFF00)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="⚠Non-existing command⚠",
                                       description='Command does not exist.',
                                       color=0xFFFF00)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(title="⚠Non-existing command⚠",
                               description='Command does not exist.',
                               color=0xFFFF00)
            await ctx.send(embed=em)

    elif isinstance(error, commands.MissingPermissions):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    em = discord.Embed(title="⚠Недостаточно прав⚠",
                                       description='У вас недостаточно прав на выполнение этой команды.',
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="⚠Not enough permissions⚠",
                                       description='You dont have enough permissions to execute this command.',
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(title="⚠Not enough permissions⚠",
                               description='You dont have enough permissions to execute this command.',
                               color=0x39d0d6)
            await ctx.send(embed=em)

    elif isinstance(error, commands.CommandOnCooldown):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    em = discord.Embed(title="⚠Данная команда на задержке⚠",
                                       description=f"Попробуйте снова через {error.retry_after:.2f}s.",
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="⚠Command is on cooldown⚠",
                                       description=f"Try again in {error.retry_after:.2f}s.",
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(title="⚠Command is on cooldown⚠",
                               description=f"Try again in {error.retry_after:.2f}s.",
                               color=0x39d0d6)
            await ctx.send(embed=em)

    else:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    em = discord.Embed(title="⚠Недостаточно прав⚠",
                                       description='У бота недостаточно прав на выполнение этой команды.',
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="⚠Not enough permissions⚠",
                                       description='Bot doesnt have enough permissions to execute this command.',
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(title="⚠Not enough permissions⚠",
                               description='Bot doesnt have enough permissions to execute this command.',
                               color=0x39d0d6)
            await ctx.send(embed=em)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=game)
    for guild in bot.guilds:
        get_guild = Money.get_or_none(guild_id=guild.id)
        if get_guild is not None:
            pass
        else:
            for member in guild.members:
                account = Money.create(user_id=member.id, amount='0', guild_id=guild.id)

@bot.event
async def on_member_join(member):
    user = Money.get_or_none(user_id=member.id, guild_id=member.guild.id)
    if user is not None:
        pass

    else:
        account = Money.create(user_id=member.id, amount='0', guild_id=member.guild.id)
    getjoin = Join.get_or_none(guild_id=member.guild.id)
    if getjoin is None:
        pass
    else:
        for join in Join.select().where(Join.guild_id == member.guild.id):
            if join.settings == 'off':
                pass
            else:
                role = member.guild.get_role(join.role_id)
                await member.add_roles(role)
    getlogs = Logs.get_or_none(guild_id=member.guild.id)
    if getlogs is None:
        pass
    else:
        for logs in Logs.select().where(Logs.guild_id == member.guild.id):
            if logs.settings == 'on':
                channel = bot.get_channel(logs.channel_id)
                getlang = Language.get_or_none(guild_id=member.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == member.guild.id):
                        if language.lang == "ru":
                            join_emb = discord.Embed(title='📋Новый пользователь присоединился', colour=0x39d0d6)
                            join_emb.add_field(name='📁Имя:', value=member.name, inline=False)
                            join_emb.add_field(name='📁Айди:', value=member.id, inline=False)
                            join_emb.add_field(name='📁Аккаунт был создан:',
                                               value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                               inline=False)
                            await channel.send(embed=join_emb)
                        else:
                            join_emb = discord.Embed(title='📋New user joined', colour=0x39d0d6)
                            join_emb.add_field(name='📁Username:', value=member.name, inline=False)
                            join_emb.add_field(name='📁User ID:', value=member.id, inline=False)
                            join_emb.add_field(name='📁Account created:',
                                               value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                               inline=False)
                            await channel.send(embed=join_emb)
                else:
                    join_emb = discord.Embed(title='📋New user joined', colour=0x39d0d6)
                    join_emb.add_field(name='📁Username:', value=member.name, inline=False)
                    join_emb.add_field(name='📁User ID:', value=member.id, inline=False)
                    join_emb.add_field(name='📁Account created:',
                                       value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
                    await channel.send(embed=join_emb)
            else:
                pass

@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(1034869012074606632)
    await channel.send(f'Bot was added to a new server, called ```{guild}```({guild.id})', file=discord.File("on_guild_join.gif"))
    for member in guild.members:
        user = Money.get_or_none(user_id=member.id, guild_id=guild.id)
        if user is not None:
            pass

        else:
            account = Money.create(user_id=member.id, amount='0', guild_id=guild.id)

@bot.event
async def on_member_remove(member):
    user = Money.get_or_none(user_id=member.id, guild_id=member.guild.id)
    if user is not None:
        delete = Money.get(Money.user_id == member.id, Money.guild_id == member.guild.id)
        delete.delete_instance()
    else:
        pass
    getlogs = Logs.get_or_none(guild_id=member.guild.id)
    if getlogs is None:
        pass
    else:
        for logs in Logs.select().where(Logs.guild_id == member.guild.id):
            if logs.settings == 'on':
                channel = bot.get_channel(logs.channel_id)
                getlang = Language.get_or_none(guild_id=member.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == member.guild.id):
                        if language.lang == "ru":
                            join_emb = discord.Embed(title='📋Пользователь покинул сервер', colour=0x39d0d6)
                            join_emb.add_field(name='📁Имя:', value=member.name, inline=False)
                            join_emb.add_field(name='📁Айди:', value=member.id, inline=False)
                            join_emb.add_field(name='📁Аккаунт был создан:',
                                               value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                               inline=False)
                            await channel.send(embed=join_emb)
                        else:
                            join_emb = discord.Embed(title='📋User leaved server', colour=0x39d0d6)
                            join_emb.add_field(name='📁Username:', value=member.name, inline=False)
                            join_emb.add_field(name='📁User ID:', value=member.id, inline=False)
                            join_emb.add_field(name='📁Account created:',
                                               value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                               inline=False)
                            await channel.send(embed=join_emb)
                else:
                    join_emb = discord.Embed(title='📋User leaved server', colour=0x39d0d6)
                    join_emb.add_field(name='📁Username:', value=member.name, inline=False)
                    join_emb.add_field(name='📁User ID:', value=member.id, inline=False)
                    join_emb.add_field(name='📁Account created:',
                                       value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
                    await channel.send(embed=join_emb)
            else:
                pass

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        getlogs = Logs.get_or_none(guild_id=after.guild.id)
        if getlogs is None:
            pass
        else:
            for logs in Logs.select().where(Logs.guild_id == after.guild.id):
                if logs.settings == 'on':
                    channel = bot.get_channel(logs.channel_id)
                    getlang = Language.get_or_none(guild_id=after.guild.id)
                    if getlang is not None:
                        for language in Language.select().where(Language.guild_id == after.guild.id):
                            if language.lang == "ru":
                                role_emb = discord.Embed(title='📋Пользователь изменил роли', colour=0x39d0d6)
                                role_emb.add_field(name='📁Имя:', value=after.name, inline=False)
                                role_emb.add_field(name='📁Айди:', value=after.id, inline=False)
                                role_emb.add_field(name='📁Аккаунт был создан:',
                                                   value=after.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                                   inline=False)
                                role_emb.add_field(name='Новые роли:', value=", ".join([r.mention for r in after.roles]),
                                                   inline=False)
                                await channel.send(embed=role_emb)
                            else:
                                role_emb = discord.Embed(title='📋User changed roles', colour=0x39d0d6)
                                role_emb.add_field(name='📁Username:', value=after.name, inline=False)
                                role_emb.add_field(name='📁User ID:', value=after.id, inline=False)
                                role_emb.add_field(name='📁Account created:',
                                                   value=after.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                                                   inline=False)
                                role_emb.add_field(name='New roles:', value=", ".join([r.mention for r in after.roles]),
                                                   inline=False)
                                await channel.send(embed=role_emb)
                    else:
                        role_emb = discord.Embed(title='📋User changed roles', colour=0x39d0d6)
                        role_emb.add_field(name='📁Username:', value=after.name, inline=False)
                        role_emb.add_field(name='📁User ID:', value=after.id, inline=False)
                        role_emb.add_field(name='📁Account created:',
                                           value=after.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
                        role_emb.add_field(name='New roles:', value=", ".join([r.mention for r in after.roles]),
                                           inline=False)
                        await channel.send(embed=role_emb)
                else:
                    pass

@bot.event
async def on_guild_remove(guild):
    leave = Money.get_or_none(guild_id=guild.id)
    if leave is not None:
        delete = Money.get(Money.guild_id == guild.id)
        delete.delete_instance()
    else:
        pass

@bot.slash_command(name = "ping", description = "Replies with pong!")
async def ping(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                money_emb = discord.Embed(
                    title=f'✔Понг! {bot.latency}',
                    color=0x39d0d6)
                await ctx.respond(embed=money_emb)
            else:
                money_emb = discord.Embed(
                    title=f'✔Pong! {bot.latency}',
                    color=0x39d0d6)
                await ctx.respond(embed=money_emb)
    else:
        money_emb = discord.Embed(
            title=f'✔Pong! {bot.latency}',
            color=0x39d0d6)
        await ctx.respond(embed=money_emb)

bot.run('-')
