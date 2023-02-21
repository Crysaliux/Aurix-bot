#Here is a part of the main Aurix code.
#You may use it in your own projects.

import discord
from discord.ext import commands
import json
import requests
import sqlite3
import random
import peewee
from peewee import *
from random import choice

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)

e_db = SqliteDatabase('economy_databank.db')

class Money(Model):
    guild_id = IntegerField()
    user_id = IntegerField()
    amount = IntegerField()

    class Meta:
        database = e_db

class Bank(Model):
    guild_id = IntegerField()
    user_id = IntegerField()
    amount = IntegerField()

    class Meta:
        database = e_db

e_db.connect()
e_db.create_tables([Money, Bank])

u_db = SqliteDatabase('utilities_databank.db')

class Warns(Model):
    guild_id = IntegerField()
    user_id = IntegerField()
    warn = CharField(max_length=200)
    index = IntegerField()

    class Meta:
        database = u_db

class Language(Model):
    guild_id = IntegerField()
    lang = CharField(max_length=20)

    class Meta:
        database = u_db

u_db.connect()
u_db.create_tables([Warns, Language])

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandNotFound):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    em = discord.Embed(title="Несуществующая команда",
                                       description='Данной команды не существует.',
                                       color=0xFFFF00)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="Non-existing command",
                                       description='Command does not exist.',
                                       color=0xFFFF00)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Non-existing command",
                               description='Command does not exist.',
                               color=0xFFFF00)
            await ctx.send(embed=em)

    elif isinstance(error, commands.MissingPermissions):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    em = discord.Embed(title="Недостаточно прав",
                                       description='У вас недостаточно прав на выполнение этой команды.',
                                       color=0xFFFF00)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="Not enough permissions",
                                       description='You dont have enough permissions to execute this command.',
                                       color=0xFFFF00)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Not enough permissions",
                               description='You dont have enough permissions to execute this command.',
                               color=0xFFFF00)
            await ctx.send(embed=em)

    elif isinstance(error, commands.CommandOnCooldown):
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    em = discord.Embed(title="Данная команда на задержке",
                                       description=f"Попробуйте снова через {error.retry_after:.2f}s.",
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="Command is on cooldown",
                                       description=f"Try again in {error.retry_after:.2f}s.",
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Command is on cooldown",
                               description=f"Try again in {error.retry_after:.2f}s.",
                               color=0x39d0d6)
            await ctx.send(embed=em)
    else:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    em = discord.Embed(title="Возникла непредвиденная ошибка",
                                       description=f'```{error}```',
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="Unexpected error occured",
                                       description=f'```{error}```',
                                       color=0x39d0d6)
                    await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Unexpected error occured",
                               description=f'```{error}```',
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

class MyViewENG(discord.ui.View):
    @discord.ui.select(
        placeholder = "Choose a category",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="📃information",
                description="All commands from category 📃information"
            ),
            discord.SelectOption(
                label="💻server-managment",
                description="All commands from category 💻server-managment"
            ),
            discord.SelectOption(
                label="⚒additional-utility",
                description="All commands from category ⚒additional-utility"
            ),
            discord.SelectOption(
                label="🎮fun",
                description="All commands from category 🎮fun"
            ),
            discord.SelectOption(
                label="💵economy",
                description="All commands from category 💵economy"
            ),
            discord.SelectOption(
                label="💾other",
                description="All commands from category 💾other"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == "📃information":
            help_emb = discord.Embed(title='Command list', colour=0x39d0d6)
            help_emb.add_field(name='📃information',
                               value='/help - information about commands,\n/userinfo [user] - shows user information,\n/avatar [user] - shows user avatar,\n/serverinfo - shows current server information,\n/statistics - shows current bot statistics',
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "💻server-managment":
            help_emb = discord.Embed(title='Command list', colour=0x39d0d6)
            help_emb.add_field(name='💻server-managment',
                               value='/ban [user] {reason} - bans mentioned user, \n/unban [user] - unbans mentioned user, \n/kick [user] {reason} - kicks mentioned user,\n/role_add [role] [user] - adds mentioned role to a mentioned user,\n/clear [amount] - deletes previous messages, \n/set_lang [ru] - изменить язык бота на русский, \n/warn [user] [warn] [index] - warns mentioned user,\n/warn_list [user] - shows all warns for specified user,\n/pardon [user] [index] - clears all warns for specified user',
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "⚒additional-utility":
            help_emb = discord.Embed(title='Command list', colour=0x39d0d6)
            help_emb.add_field(name='⚒additional-utility',
                               value="/print [message] - prints your message,\n/create_channel [name] - creates new server channel,\n/github - link to our github page,\n/wikifur - link to Wikifur community",
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "🎮fun":
            help_emb = discord.Embed(title='Command list', colour=0x39d0d6)
            help_emb.add_field(name='🎮fun',
                               value="/fox - random picture of a cute fox🦊\n/numbers - guess a number!\n/roll [rolls amount] [sides amount] - rolls a dice,\n/hug [user] - hugs mentioned user,\n/sum [number] [number] - sums two mentioned numbers,\n/choice - Orix will answer 'yes' or 'no',\n/play_with [user] {game} - ask user to play some game with you,\n/lick [user] - lick somebody :з",
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "💵economy":
            help_emb = discord.Embed(title='Command list', colour=0x39d0d6)
            help_emb.add_field(name='💵economy',
                               value="/give_money [user] [amount] - give some amount of your money to mentioned user,\n/balance {user} - shows your current balance,\n/set_money [user] [amount] - sets mentioned amount of money to mentioned user,\n/work [crime/business/casual] - earn some money right now!,\n/deposit [amount] - deposit some money to your bank account,\n/deduct [amount] - deposit some money from your bank account",
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "💾other":
            help_emb = discord.Embed(title='Command list', colour=0x39d0d6)
            help_emb.add_field(name='💾other', value='/ping - replies with pong', inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        await interaction.response.send_message(embed=help_emb)

class MyViewRU(discord.ui.View):
    @discord.ui.select(
        placeholder = "Выбери категорию",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="📃информация",
                description="Все команды категории 📃information"
            ),
            discord.SelectOption(
                label="💻управление-сервером",
                description="Все команды категории 💻управление-сервером"
            ),
            discord.SelectOption(
                label="⚒дополнительные-утилиты",
                description="Все команды категории ⚒дополнительные-утилиты"
            ),
            discord.SelectOption(
                label="🎮развлечения",
                description="Все команды категории 🎮развлечения"
            ),
            discord.SelectOption(
                label="💵экономика",
                description="Все команды категории 💵экономика"
            ),
            discord.SelectOption(
                label="💾другое",
                description="Все команды категории 💾другое"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == "📃информация":
            help_emb = discord.Embed(title='Список команд', colour=0x39d0d6)
            help_emb.add_field(name='📃информация',
                               value='/help - список всех команд,\n/userinfo [пользователь] - показывает информацию об указанном пользователе,\n/avatar [пользователь] - показывает аватар указанного пользователя,\n/serverinfo - показывает информацию о сервере',
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "💻управление-сервером":
            help_emb = discord.Embed(title='Список команд', colour=0x39d0d6)
            help_emb.add_field(name='💻управление-сервером',
                               value='/ban [пользователь] {причина} - банит указанного пользователя,\n/unban [пользователь] - разбанивает указанного пользователя, \n/kick [пользователь] {причина} - кикает указанного пользователя,\n/role_add [роль] [пользователь] - добавляет указанную роль, указанному пользователю,\n/clear [количество] - удаляет указанное количество сообщений,\n/set_lang [eng] - set bot language to english,\n/warn [пользователь] [предупреждение] [индекс] - предупреждает указанного пользователя,\n/warn_list [пользователь] - показывает все предупреждения у указанного пользователя,\n/pardon [пользователь] [индекс] - удаляет все предупреждения у указанного пользователя',
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "⚒дополнительные-утилиты":
            help_emb = discord.Embed(title='Список команд', colour=0x39d0d6)
            help_emb.add_field(name='⚒дополнительные-утилиты',
                               value="/print [сообщение] - выводит указанное сообщение,\n/create_channel [название] - создает новый канал с указанным названием,\n/github - репозиторий проекта в гитхабе,\n/wikifur - Викифур",
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "🎮развлечения":
            help_emb = discord.Embed(title='Список команд', colour=0x39d0d6)
            help_emb.add_field(name='🎮развлечения',
                               value="/fox - рандомная картинка милой лисички🦊\n/numbers - угадай число!\n/roll [количество бросков] [количество сторон] - бросает кубик,\n/hug [user] - обнимает указанного пользователя,\n/sum [число] [число] - складывает два указанных числа,\n/choice - Orix ответит 'да' или 'нет',\n/play_with [пользователь] {игра} - попроси пользователя сыграть с тобой в игру",
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "💵экономика":
            help_emb = discord.Embed(title='Список команд', colour=0x39d0d6)
            help_emb.add_field(name='💵экономика',
                               value="/give_money [пользователь] [количество] - вы отдаете указанную сумму 💷 другому пользователю,\n/balance {пользователь} - показывает ваш баланс,\n/set_money [пользователь] [количество] - устанавливает указанное количество 💷, указанному пользователю,\n/work [crime/business/casual] - вы можете заработать немного 💷, но ваша зарплата не постоянна,\n/deposit [количество] - пополните свой банковский счет,\n/deduct [количество] - снимите деньги со своего банковского счета",
                               inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        elif select.values[0] == "💾другое":
            help_emb = discord.Embed(title='Список команд', colour=0x39d0d6)
            help_emb.add_field(name='💾другое', value='/ping - понг', inline=False)
            help_emb.set_footer(text=community_rights,
                                icon_url=creator_url)

        await interaction.response.send_message(embed=help_emb)

@bot.slash_command(name = "help", description = "information about commands")
async def help(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                help_emb = discord.Embed(title='''
                    \nВыбери категорию ниже.
                    \nОбязательные аргументы - ```[]```
                    \nНеобязательные аргументы - ```{}```''', colour=0x39d0d6)
                await ctx.respond(embed=help_emb, view=MyViewRU())
            else:
                help_emb = discord.Embed(title='''
                    \nChoose a category below.
                    \nRequired arguments - ```[]```
                    \nOptional arguments - ```{}```''', colour=0x39d0d6)
                await ctx.respond(embed=help_emb, view=MyViewENG())
    else:
        help_emb = discord.Embed(title='''
            \nChoose a category below.
            \nRequired arguments - ```[]```
            \nOptional arguments - ```{}```''', colour=0x39d0d6)
        await ctx.respond(embed=help_emb, view=MyViewENG())

@bot.slash_command(name = "userinfo", description = "shows user information")
@commands.has_permissions(administrator=True)
async def userinfo(ctx, member:discord.Member):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                emb = discord.Embed(title="Информация", color=member.color)
                emb.add_field(name="Имя :", value=member.display_name, inline=False)
                emb.add_field(name="Айди :", value=member.id, inline=False)
                t = member.status

                emb.add_field(name="Статус :", value=member.activity, inline=False)
                emb.add_field(name="Роль на сервере :", value=f"{member.top_role.mention}", inline=False)
                emb.add_field(name="Аккаунт был создан :",
                              value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                              inline=False)
                emb.set_thumbnail(url=member.avatar)
                emb.set_footer(text=community_rights,
                               icon_url=creator_url)
                await ctx.respond(embed=emb)
            else:
                emb = discord.Embed(title="User information", color=member.color)
                emb.add_field(name="Name :", value=member.display_name, inline=False)
                emb.add_field(name="User ID :", value=member.id, inline=False)
                t = member.status

                emb.add_field(name="Status :", value=member.activity, inline=False)
                emb.add_field(name="Server role :", value=f"{member.top_role.mention}", inline=False)
                emb.add_field(name="Account was created :",
                              value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                              inline=False)
                emb.set_thumbnail(url=member.avatar)
                emb.set_footer(text=community_rights,
                               icon_url=creator_url)
                await ctx.respond(embed=emb)
    else:
        emb = discord.Embed(title="User information", color=member.color)
        emb.add_field(name="Name :", value=member.display_name, inline=False)
        emb.add_field(name="User ID :", value=member.id, inline=False)
        t = member.status

        emb.add_field(name="Status :", value=member.activity, inline=False)
        emb.add_field(name="Server role :", value=f"{member.top_role.mention}", inline=False)
        emb.add_field(name="Account was created :",
                      value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                      inline=False)
        emb.set_thumbnail(url=member.avatar)
        emb.set_footer(text=community_rights,
                       icon_url=creator_url)
        await ctx.respond(embed=emb)

@bot.slash_command(name = "avatar", description = "shows user avatar")
@commands.has_permissions(administrator=True)
async def avatar(ctx, *,  user : discord.Member=None):
    if user is None:
        userAvatarUrl = ctx.author.avatar
        await ctx.respond(userAvatarUrl)
    else:
        userAvatarUrl = user.avatar
        await ctx.respond(userAvatarUrl)

@bot.slash_command(name = "serverinfo", description = "shows information about current server")
@commands.has_permissions(administrator=True)
async def serverinfo(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                info_emb = discord.Embed(title=f'Информация о сервере', colour=0x39d0d6)
                info_emb.set_thumbnail(url=ctx.guild.icon)
                info_emb.add_field(name='Название:', value=ctx.guild, inline=False)
                info_emb.add_field(name='Айди:', value=ctx.guild.id, inline=False)
                info_emb.add_field(name='Количество участников:', value=len(ctx.guild.members), inline=False)
                info_emb.add_field(name='Количество ролей:', value=len(ctx.guild.roles), inline=False)
                info_emb.add_field(name='Владелец:', value=ctx.guild.owner, inline=False)
                info_emb.set_footer(text=community_rights,
                                    icon_url=creator_url)
                await ctx.respond(embed=info_emb)
            else:
                info_emb = discord.Embed(title=f'Server information', colour=0x39d0d6)
                info_emb.set_thumbnail(url=ctx.guild.icon)
                info_emb.add_field(name='Server name:', value=ctx.guild, inline=False)
                info_emb.add_field(name='Server id:', value=ctx.guild.id, inline=False)
                info_emb.add_field(name='Number of members:', value=len(ctx.guild.members), inline=False)
                info_emb.add_field(name='Number of roles:', value=len(ctx.guild.roles), inline=False)
                info_emb.add_field(name='Server owner:', value=ctx.guild.owner, inline=False)
                info_emb.set_footer(text=community_rights,
                                    icon_url=creator_url)
                await ctx.respond(embed=info_emb)
    else:
        info_emb = discord.Embed(title=f'Server information', colour=0x39d0d6)
        info_emb.set_thumbnail(url=ctx.guild.icon)
        info_emb.add_field(name='Server name:', value=ctx.guild, inline=False)
        info_emb.add_field(name='Server id:', value=ctx.guild.id, inline=False)
        info_emb.add_field(name='Number of members:', value=len(ctx.guild.members), inline=False)
        info_emb.add_field(name='Number of roles:', value=len(ctx.guild.roles), inline=False)
        info_emb.add_field(name='Server owner:', value=ctx.guild.owner, inline=False)
        info_emb.set_footer(text=community_rights,
                            icon_url=creator_url)
        await ctx.respond(embed=info_emb)

@bot.slash_command(name = "statistics", description = "Shows bot's statistics")
async def statistics(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                guilds = len(list(bot.guilds))
                users = len(list(bot.users))
                stats = discord.Embed(title='Statistics', colour=0x39d0d6)
                stats.set_thumbnail(
                    url='https://cdn.discordapp.com/avatars/1012029552635162674/c5c88afdd98386c8df956658f4f3057d.png?size=1024')
                stats.add_field(name='Количество серверов:', value=f'{guilds}', inline=False)
                stats.add_field(name='Количество пользователей:', value=f'{users}', inline=False)
                await ctx.respond(embed=stats)
            else:
                guilds = len(list(bot.guilds))
                users = len(list(bot.users))
                stats = discord.Embed(title='Statistics', colour=0x39d0d6)
                stats.set_thumbnail(
                    url='https://cdn.discordapp.com/avatars/1012029552635162674/c5c88afdd98386c8df956658f4f3057d.png?size=1024')
                stats.add_field(name='Total amount of servers:', value=f'{guilds}', inline=False)
                stats.add_field(name='Total amount of users:', value=f'{users}', inline=False)
                await ctx.respond(embed=stats)
    else:
        guilds = len(list(bot.guilds))
        users = len(list(bot.users))
        stats = discord.Embed(title='Statistics', colour=0x39d0d6)
        stats.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/1012029552635162674/c5c88afdd98386c8df956658f4f3057d.png?size=1024')
        stats.add_field(name='Total amount of servers:', value=f'{guilds}', inline=False)
        stats.add_field(name='Total amount of users:', value=f'{users}', inline=False)
        await ctx.respond(embed=stats)

@bot.slash_command(name = "ban", description = "bans mentioned user")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                ban_emb = discord.Embed(title=f'Пользователь <@{member.id}> был забанен',
                                   description=f'Причина: {reason}',
                                   color=0x39d0d6)
                await ctx.respond(embed=ban_emb)
            else:
                ban_emb = discord.Embed(title=f'User <@{member.id}> was banned',
                                        description=f'Reason: {reason}',
                                        color=0x39d0d6)
                await ctx.respond(embed=ban_emb)
    else:
        ban_emb = discord.Embed(title=f'User <@{member.id}> was banned',
                                description=f'Reason: {reason}',
                                color=0x39d0d6)
        await ctx.respond(embed=ban_emb)

@bot.slash_command(name = "unban", description = "unbans mentioned user")
@commands.has_permissions(administrator = True)
async def unban(ctx, user: discord.User):
  await ctx.guild.unban(user=user)
  getlang = Language.get_or_none(guild_id=ctx.guild.id)
  if getlang is not None:
      for language in Language.select().where(Language.guild_id == ctx.guild.id):
          if language.lang == "ru":
              unban_emb = discord.Embed(title=f'Пользователь <@{user}> был разбанен', color=0x39d0d6)
              await ctx.respond(embed=unban_emb)
          else:
              unban_emb = discord.Embed(title=f'User <@{user}> was unbanned', color=0x39d0d6)
              await ctx.respond(embed=unban_emb)
  else:
      unban_emb = discord.Embed(title=f'User <@{user}> was unbanned', color=0x39d0d6)
      await ctx.respond(embed=unban_emb)

@bot.slash_command(name = "kick", description = "kicks mentioned user")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                kick_emb = discord.Embed(title=f'Пользователь <@{member.id}> был кикнут',
                                        description=f'Причина: {reason}',
                                        color=0x39d0d6)
                await ctx.respond(embed=kick_emb)
            else:
                kick_emb = discord.Embed(title=f'User <@{member.id}> was kicked',
                                        description=f'Reason: {reason}',
                                        color=0x39d0d6)
                await ctx.respond(embed=kick_emb)
    else:
        kick_emb = discord.Embed(title=f'User <@{member.id}> was kicked',
                                 description=f'Reason: {reason}',
                                 color=0x39d0d6)
        await ctx.respond(embed=kick_emb)

@bot.slash_command(name = "role_add", description = "adds mentioned role to a mentioned user")
@commands.has_permissions(manage_roles = True)
async def role_add(ctx, user: discord.Member, role:discord.Role):
    await user.add_roles(role)
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                role_emb = discord.Embed(title=f"Вы добавили роль {role} пользователю {user.mention}", color=0x39d0d6)
                await ctx.respond(embed=role_emb)
            else:
                role_emb = discord.Embed(title=f"Added role {role} to {user.mention}", color=0x39d0d6)
                await ctx.respond(embed=role_emb)
    else:
        role_emb = discord.Embed(title=f"Added role {role} to {user.mention}", color=0x39d0d6)
        await ctx.respond(embed=role_emb)

@bot.slash_command(name = "clear", description = "deletes previous messages")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, *, amount: int=None):
    if amount > 250:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    msg_emb = discord.Embed(title=f'Вы можете удалить не более 250 сообщений за один раз', color=0x39d0d6)
                    await ctx.respond(embed=msg_emb)
                else:
                    msg_emb = discord.Embed(title=f'You cant delete more than 250 messages at once', color=0x39d0d6)
                    await ctx.respond(embed=msg_emb)
        else:
            msg_emb = discord.Embed(title=f'You cant delete more than 250 messages at once', color=0x39d0d6)
            await ctx.respond(embed=msg_emb)
    else:
        await ctx.channel.purge(limit=amount)
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    msg_emb = discord.Embed(title=f'```{amount} сообщений было успешно удалено```', color=0x39d0d6)
                    await ctx.respond(embed=msg_emb)
                else:
                    msg_emb = discord.Embed(title=f'```{amount} messages were deleted```', color=0x39d0d6)
                    await ctx.respond(embed=msg_emb)
        else:
            msg_emb = discord.Embed(title=f'```{amount} messages were deleted```', color=0x39d0d6)
            await ctx.respond(embed=msg_emb)

@bot.slash_command(name = "set_lang", description = "change your bot language ru/eng")
@commands.has_permissions(administrator=True)
async def set_lang(ctx, *, lang: discord.Option(str, choices=[discord.OptionChoice(name="ru", value="ru", name_localizations=None), discord.OptionChoice(name="en", value="en", name_localizations=None)])):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        delete = Language.get(Language.guild_id == ctx.guild.id)
        delete.delete_instance()
        langset = Language.create(guild_id=ctx.guild.id, lang=lang)
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.respond("Вы изменили язык бота на русский")
            else:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "en":
                        await ctx.respond("Your bot language is english")
    else:
        langset = Language.create(guild_id=ctx.guild.id, lang=lang)
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.respond("Вы изменили язык бота на русский")
            else:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "en":
                        await ctx.respond("Your bot language is english")

@bot.slash_command(name = "warn", description = "warns mentioned user")
@commands.has_permissions(administrator=True)
async def warn(ctx, user: discord.Member, *, warn: str, index: int=None):
    if user.id == ctx.author.id:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    msg_emb = discord.Embed(title=f'Вы не можете выдать предупреждение себе же!', color=0x39d0d6)
                    await ctx.respond(embed=msg_emb)
                else:
                    msg_emb = discord.Embed(title=f'You cant give a warn to yourself!', color=0x39d0d6)
                    await ctx.respond(embed=msg_emb)
        else:
            msg_emb = discord.Embed(title=f'You cant give a warn to yourself!', color=0x39d0d6)
            await ctx.respond(embed=msg_emb)
    else:
        if user == bot.user:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        msg_emb = discord.Embed(title=f'Вы не можете выдать предупреждение боту!', color=0x39d0d6)
                        await ctx.respond(embed=msg_emb)
                    else:
                        msg_emb = discord.Embed(title=f'You cant give a warn to a bot!', color=0x39d0d6)
                        await ctx.respond(embed=msg_emb)
            else:
                msg_emb = discord.Embed(title=f'You cant give a warn to a bot!', color=0x39d0d6)
                await ctx.respond(embed=msg_emb)
        else:
            new_warn = Warns.create(guild_id=ctx.guild.id, user_id=user.id, warn=warn, index=index)
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        warns_emb = discord.Embed(title=f"Пользователь {user}, получил предупреждение: {warn}",
                                                  color=0x39d0d6)
                        await ctx.respond(embed=warns_emb)
                        channel = await user.create_dm()
                        warn_emb = discord.Embed(title=f"Вы были предупреждены: {warn}, сервер: {ctx.guild}",
                                                 color=0x39d0d6)
                        await channel.send(embed=warn_emb)
                    else:
                        warns_emb = discord.Embed(title=f"User {user}, was warned: {warn}", color=0x39d0d6)
                        await ctx.respond(embed=warns_emb)
                        channel = await user.create_dm()
                        warn_emb = discord.Embed(title=f"You were warned: {warn}, server: {ctx.guild}", color=0x39d0d6)
                        await channel.send(embed=warn_emb)
            else:
                warns_emb = discord.Embed(title=f"User {user}, was warned: {warn}", color=0x39d0d6)
                await ctx.respond(embed=warns_emb)
                channel = await user.create_dm()
                warn_emb = discord.Embed(title=f"You were warned: {warn}, server: {ctx.guild}", color=0x39d0d6)
                await channel.send(embed=warn_emb)

@bot.slash_command(name = "warn_list", description = "shows all warns for specified user")
@commands.has_permissions(administrator=True)
async def warn_list(ctx, user: discord.Member):
    warns_get = Warns.get_or_none(guild_id=ctx.guild.id, user_id=user.id)
    if warns_get is not None:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    warns_emb = discord.Embed(title=f'Предупреждения пользователя {user}',
                                              colour=0x39d0d6)
                    for warns in Warns.select().where(Warns.guild_id == ctx.guild.id, Warns.user_id == user.id):
                        warns_emb.add_field(name=f'[Предупреждение]:', value=f'{warns.warn}, **индекс**[{warns.index}]',
                                            inline=False)
                        await ctx.respond(embed=warns_emb)
                else:
                    warns_emb = discord.Embed(title=f'Warns for user {user}',
                                              colour=0x39d0d6)
                    for warns in Warns.select().where(Warns.guild_id == ctx.guild.id, Warns.user_id == user.id):
                        warns_emb.add_field(name=f'[Warn]:', value=f'{warns.warn}, **index**[{warns.index}]',
                                            inline=False)
                        await ctx.respond(embed=warns_emb)
        else:
            warns_emb = discord.Embed(title=f'Warns for user {user}',
                                      colour=0x39d0d6)
            for warns in Warns.select().where(Warns.guild_id == ctx.guild.id, Warns.user_id == user.id):
                warns_emb.add_field(name=f'[Warn]:', value=f'{warns.warn}, **index**[{warns.index}]',
                                    inline=False)
                await ctx.respond(embed=warns_emb)
    else:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    warns_emb = discord.Embed(title=f"У пользователя {user} нету предупреждений", color=0x39d0d6)
                    await ctx.respond(embed=warns_emb)
                else:
                    warns_emb = discord.Embed(title=f"User {user} has no warns", color=0x39d0d6)
                    await ctx.respond(embed=warns_emb)
        else:
            warns_emb = discord.Embed(title=f"User {user} has no warns", color=0x39d0d6)
            await ctx.respond(embed=warns_emb)

@bot.slash_command(name = "pardon", description = "clears all warns for specified user")
@commands.has_permissions(administrator=True)
async def pardon(ctx, user: discord.Member, index: int=None):
    warns_get = Warns.get_or_none(guild_id=ctx.guild.id, user_id=user.id)
    if warns_get is not None:
        if index is None:
            for warns in Warns.select().where(Warns.guild_id == ctx.guild.id, Warns.user_id == user.id):
                delete = Warns.get(Warns.guild_id == ctx.guild.id, Warns.user_id == user.id)
                delete.delete_instance()
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        warns_emb = discord.Embed(title=f"Все предупреждения пользователя {user} были успешно удалены",
                                                  color=0x39d0d6)
                        await ctx.respond(embed=warns_emb)
                    else:
                        warns_emb = discord.Embed(title=f"Successfully deleted all warns for user {user}",
                                                  color=0x39d0d6)
                        await ctx.respond(embed=warns_emb)
            else:
                warns_emb = discord.Embed(title=f"Successfully deleted all warns for user {user}",
                                          color=0x39d0d6)
                await ctx.respond(embed=warns_emb)
        else:
            for warns in Warns.select().where(Warns.guild_id == ctx.guild.id, Warns.user_id == user.id, Warns.index == index):
                delete = Warns.get(Warns.guild_id == ctx.guild.id, Warns.user_id == user.id, Warns.index == index)
                delete.delete_instance()
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        warns_emb = discord.Embed(title=f"Все предупреждения с индексом {index} пользователя {user} были успешно удалены",
                                                  color=0x39d0d6)
                        await ctx.respond(embed=warns_emb)
                    else:
                        warns_emb = discord.Embed(
                            title=f"Successfully deleted all warns with index {index} for user {user}",
                            color=0x39d0d6)
                        await ctx.respond(embed=warns_emb)
            else:
                warns_emb = discord.Embed(
                    title=f"Successfully deleted all warns with index {index} for user {user}",
                    color=0x39d0d6)
                await ctx.respond(embed=warns_emb)
    else:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    warns_emb = discord.Embed(
                        title=f"У пользователя {user} нету предупреждений",
                        color=0x39d0d6)
                    await ctx.respond(embed=warns_emb)
                else:
                    warns_emb = discord.Embed(
                        title=f"User {user} has no warns",
                        color=0x39d0d6)
                    await ctx.respond(embed=warns_emb)
        else:
            warns_emb = discord.Embed(
                title=f"User {user} has no warns",
                color=0x39d0d6)
            await ctx.respond(embed=warns_emb)

@bot.slash_command(name = "print", description = "prints your message")
@commands.has_permissions(manage_messages=True)
async def print(ctx, *, text: str):
    print_emb = discord.Embed(
        title=text,
        color=0x39d0d6)
    await ctx.respond(embed=print_emb)

@bot.slash_command(name = "create_channel", description = "creates new server channel")
@commands.has_permissions(administrator=True)
async def create_channel(ctx, *, name):
    await ctx.guild.create_text_channel(name)
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                channel_emb = discord.Embed(
                    title=f"Канал {name} был успешно создан",
                    color=0x39d0d6)
                await ctx.respond(embed=channel_emb)
            else:
                channel_emb = discord.Embed(
                    title=f"Channel {name} was successfuly created",
                    color=0x39d0d6)
                await ctx.respond(embed=channel_emb)
    else:
        channel_emb = discord.Embed(
            title=f"Channel {name} was successfuly created",
            color=0x39d0d6)
        await ctx.respond(embed=channel_emb)

@bot.slash_command(name = "fox", description = "random picture of a cute fox🦊")
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox')
    json_data = json.loads(response.text)
    embed = discord.Embed(color=0xff9900, title='Random Fox')
    embed.set_image(url=json_data['link'])
    await ctx.respond(embed=embed)

@bot.slash_command(name = "numbers", description = "guess a number!")
async def numbers(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                await ctx.respond("❌Эта функция в данный момент недоступна")
            else:
                await ctx.respond("❌This function is currently unavailable")
    else:
        await ctx.respond("❌This function is currently unavailable")

@bot.slash_command(name = "roll", description = "rolls a dice")
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    dice_emb = discord.Embed(
        title=', '.join(dice),
        color=0x39d0d6)
    await ctx.respond(embed=dice_emb)

@bot.slash_command(name = "hug", description = "hugs mentioned user")
async def hug(ctx, user : discord.Member):
    if user == bot.user:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    hug_emb = discord.Embed(
                        title=f"Укажите пользователя не являющегося ботом!",
                        color=0x39d0d6)
                    await ctx.respond(embed=hug_emb)
                else:
                    hug_emb = discord.Embed(
                        title=f"Specify a non-bot user!",
                        color=0x39d0d6)
                    await ctx.respond(embed=hug_emb)
        else:
            hug_emb = discord.Embed(
                title=f"Specify a non-bot user!",
                color=0x39d0d6)
            await ctx.respond(embed=hug_emb)
    else:
        getlang = Language.get_or_none(guild_id=ctx.guild.id)
        if getlang is not None:
            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                if language.lang == "ru":
                    hug_emb = discord.Embed(
                        title=f"{ctx.author.name} обнял {user.name}!",
                        color=0x39d0d6)
                    await ctx.respond(embed=hug_emb)
                else:
                    hug_emb = discord.Embed(
                        title=f"{ctx.author.name} hugged {user.name}!",
                        color=0x39d0d6)
                    await ctx.respond(embed=hug_emb)
        else:
            hug_emb = discord.Embed(
                title=f"{ctx.author.name} hugged {user.name}!",
                color=0x39d0d6)
            await ctx.respond(embed=hug_emb)

@bot.slash_command(name = "sum", description = "sums two mentioned numbers")
async def sum(ctx, a: int, b: int):
    sum = a + b
    sum_emb = discord.Embed(
        title=sum,
        color=0x39d0d6)
    await ctx.respond(embed=sum_emb)

@bot.slash_command(name = "choice", description = "Orix will answer 'yes' or 'no'")
async def choice(ctx):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                from random import choice
                answer = choice(['да', 'нет'])
                choice_emb = discord.Embed(
                    title=answer,
                    color=0x39d0d6)
                await ctx.respond(embed=choice_emb)
            else:
                from random import choice
                answer = choice(['yes', 'no'])
                choice_emb = discord.Embed(
                    title=answer,
                    color=0x39d0d6)
                await ctx.respond(embed=choice_emb)
    else:
        from random import choice
        answer = choice(['yes', 'no'])
        choice_emb = discord.Embed(
            title=answer,
            color=0x39d0d6)
        await ctx.respond(embed=choice_emb)

@bot.slash_command(name = "play_with", description = "ask user to play with you")
async def play_with(ctx, user: discord.Member, *, game=None):
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                channel = await user.create_dm()
                play_emb = discord.Embed(
                    title=f"Пользователь {ctx.author} хочет сыграть с вами в игру {game}",
                    color=0x39d0d6)
                await channel.send(embed=play_emb)
            else:
                channel = await user.create_dm()
                play_emb = discord.Embed(
                    title=f"User {ctx.author} wants to play a game called {game} with you",
                    color=0x39d0d6)
                await channel.send(embed=play_emb)
    else:
        channel = await user.create_dm()
        play_emb = discord.Embed(
            title=f"User {ctx.author} wants to play a game called {game} with you",
            color=0x39d0d6)
        await channel.send(embed=play_emb)
    getlang = Language.get_or_none(guild_id=ctx.guild.id)
    if getlang is not None:
        for language in Language.select().where(Language.guild_id == ctx.guild.id):
            if language.lang == "ru":
                play_emb = discord.Embed(
                    title="Пользователь успешно получил сообщение",
                    color=0x39d0d6)
                await ctx.respond(embed=play_emb)
            else:
                play_emb = discord.Embed(
                    title="User successfully got message",
                    color=0x39d0d6)
                await ctx.respond(embed=play_emb)
    else:
        play_emb = discord.Embed(
            title="User successfully got message",
            color=0x39d0d6)
        await ctx.respond(embed=play_emb)