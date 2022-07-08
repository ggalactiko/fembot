import io
import json
import random
from typing import Optional
import requests
import aiohttp
import discord
from discord.ext import commands
import asyncio
import os
from discord.app_commands import Choice
from colorama import Fore
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
default_prefix = os.getenv("default_prefix") or "!"

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await uwu.load_extension(f"cogs.{filename[:-3]}")
                print(f"{Fore.LIGHTBLUE_EX}Loaded {filename}")
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}Failed to load {filename}")
                print(f"{Fore.LIGHTRED_EX}{e}")

def when_mentioned_or_function(func):
    def inner(bot, message):
        r = func(bot, message)
        prefixes = commands.when_mentioned(bot, message)
        prefixes.append(r)
        return prefixes
    return inner

def get_prefix(client, message):
    if not message.guild:
        return default_prefix
    else:
        try:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
            return prefixes.get(str(message.guild.id))
        except KeyError:
            return default_prefix

#configs
whitelist = []
intents = discord.Intents.default()
intents.members = True
intents.presences = False
intents.message_content = True
uwu = commands.Bot(command_prefix=when_mentioned_or_function(get_prefix), intents = intents)
tree = uwu.tree
uwu.remove_command("help")

@uwu.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingPermissions):  
        embed = discord.Embed(description=f":x: You need `{', '.join(error.missing_permissions)}` permission(s) to run this command", color = 0xff0000)
        await ctx.send(embed=embed)
        return 

    elif isinstance(error, commands.BadArgument): 
        await ctx.send("Ingresa una entrada valida")
        return
    raise error

@tree.error
async def error_handler(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message(str(error), ephemeral=True)
    if isinstance(error, discord.app_commands.BotMissingPermissions):
        await interaction.response.send_message(str(error), ephemeral=True)

#bot events

async def presence():
    names = [f"{len(uwu.guilds)} servers", "/help", "galactiko.net"]
    counter = 0
    while True:
        for index, item in enumerate(names):
            if counter == len(names):
                counter = 0
            
            if index == counter:
                await uwu.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=item))
                counter += 1
                await asyncio.sleep(30)

@uwu.event
async def on_ready():
    await tree.sync()
    print(f"{Fore.LIGHTBLUE_EX}{uwu.user.name} is ready to go!, watching {len(uwu.guilds)} servers, tree synced")
    await presence()

@uwu.event
async def on_guild_join(guild: discord.Guild):
    prefix = default_prefix
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f) 

    prefixes[str(guild.id)] = prefix

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4) 

    channel = random.choice(guild.text_channels) 
    embed = discord.Embed(title=f"Gracias por agregar {uwu.user.name} a su servidor", description=f"Mi prefijo predeterminado es {prefix}, puedes cambiarlo usando `{prefix}setprefix <nuevo prefijo>`", color=0x00ff00)
    await channel.send(embed=embed)

@uwu.event
async def on_guild_remove(guild): 
    with open('prefixes.json', 'r') as f: 
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) 

    with open('prefixes.json', 'w') as f: 
        json.dump(prefixes, f, indent=4)


#Message listeners
@uwu.event
async def on_message(message: discord.Message):
    if f"<@{uwu.user.id}>" == message.content:
        with open("prefixes.json", "r") as f:
         prefixes = json.load(f)
        prefix = prefixes.get(str(message.guild.id))
        prefix = prefix or default_prefix
        await message.channel.send(f"Mi prefix en este servidor es `{prefix}` \n Escribe `{prefix}help` para ver los comandos")
    await uwu.process_commands(message)

uwu.sniped_messages = {}
@uwu.event
async def on_message_delete(message: discord.Message):
    if message.author.bot:
        return
    else:
        if message.attachments:
            uwu.sniped_messages[message.channel.id] = (message.attachments[0].url, message.author, message.channel.name, message.created_at)
        else:
            uwu.sniped_messages[message.channel.id] = (message.content, message.author, message.channel.name, message.created_at)

uwu.esniped_messages = {}
@uwu.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.bot:
        return
    else:
        if before.attachments:
            if after.attachments:
                e = after.attachments[0].url
            else:
                e = after.content
            uwu.esniped_messages[before.channel.id] = (before.attachments[0].url, before.author, before.channel.name, before.created_at, e, after.jump_url)
        else:
            if after.attachments:
                e = after.attachments[0].url
            else:
                e = after.content
            uwu.esniped_messages[before.channel.id] = (before.content, before.author, before.channel.name, before.created_at, e, after.jump_url)

#View class
class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Diversión"),
            discord.SelectOption(label="Moderación"),
            discord.SelectOption(label="Interacción"),
            discord.SelectOption(label="Configuración"),
            discord.SelectOption(label="Experimental"),
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        diversion = discord.Embed(title="Diversión", description="**Cat** \nEnvía una foto aleatoria de un gato \n**Dog** \nEnvía una foto aleatoria de un perro \n**Fox** \nEnvía una foto aleatoria de un zorro \n**Panda** \nEnvía una foto aleatoria de un panda \n**Horny** \nHorny license just for u \n**Simp** \nSimp license just for u \n**meme** \nEnvia un meme al azar \n**Impersonate** \nEnvía un mensaje como otro usuario \n**Gay** \n**Jail** \n**simpometer** ")
        diversion.set_thumbnail(url="https://cdn.discordapp.com/avatars/947294593764978719/f3df73cffa759708395056036da2bf0e.webp?size=1024")
        diversion.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
        interaccion = discord.Embed(title="Interacción", description="***Interacción*** \n**Hug** \n**Pat** \n**Wink** \n**petpet**⚠️")
        interaccion.set_thumbnail(url="https://cdn.discordapp.com/avatars/947294593764978719/f3df73cffa759708395056036da2bf0e.webp?size=1024")
        interaccion.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
        configuracion = discord.Embed(title="Configuración", description="**setprefix** \nCambia el prefix del bot")
        configuracion.set_thumbnail(url="https://cdn.discordapp.com/avatars/947294593764978719/f3df73cffa759708395056036da2bf0e.webp?size=1024")
        configuracion.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
        moderacion = discord.Embed(title="Moderación", description="**Ban** \nBanea al usuario mencionado \n**Kick** \nExpulsa al usuario mencionado \n**Mute** \nSilencia al usuario mencionado \n**Nuke** \nBorra todos los mensajes de un canal y lo clona \n**Purge** \nBorra un cierto número de mensajes de un canal")
        moderacion.set_thumbnail(url="https://cdn.discordapp.com/avatars/947294593764978719/f3df73cffa759708395056036da2bf0e.webp?size=1024")
        moderacion.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)

        if self.values[0] == "Diversión":
            await interaction.response.edit_message(embed=diversion)
        elif self.values[0] == "Moderación":
            await interaction.response.edit_message(embed=moderacion)
        elif self.values[0] == "Interacción":
            await interaction.response.edit_message(embed=interaccion)
        elif self.values[0] == "Configuración":
            await interaction.response.edit_message(embed=configuracion)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

#Bot commands(apps)
@tree.context_menu(name="Horny")
async def horny(interaction: discord.Interaction, user: discord.Member):
    member = user
    async with aiohttp.ClientSession() as session:
            async with session.get(
            f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.url.format("png")}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    em = discord.Embed(
                    title="bonk",
                    color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://horny.png")
                    await interaction.response.send_message(embed=em, file=file)
                else:
                    await interaction.response.send_message('No horny :(')
            await session.close()

def cooldown_for_everyone_but_me(interaction: discord.Interaction) -> Optional[discord.app_commands.Cooldown]:
    if interaction.user.id == 915329928390639648:
        return None
    return discord.app_commands.Cooldown(per=30, rate=5)

@tree.command(name="ping", description="Get the bot's ping")
async def ping(interaction: discord.Interaction):
    x = requests.get("https://galactiko.net/api/v1/ping")
    q = x.json()["ping"]
    embed = discord.Embed(title="🏓 Pong!")
    embed.add_field(name="Discord API", value=f"{interaction.client.latency * 1000}ms")
    embed.add_field(name="Galactiko.net API", value=f"{q} seconds")
    await interaction.response.send_message(embed=embed)

@tree.command()
@discord.app_commands.describe(member='member to impersonate')
@discord.app_commands.describe(message='message to send')
@discord.app_commands.checks.dynamic_cooldown(cooldown_for_everyone_but_me)
async def impersonate(interaction: discord.Interaction, member: discord.Member, message: str):
    if member == uwu.user:
        await interaction.response.send_message('You can\'t impersonate me', ephemeral=True)
        return
    if member.bot:
        await interaction.response.send_message('You can\'t impersonate bots', ephemeral=True)
        return
    if member == interaction.user:
        await interaction.response.send_message('You can\'t impersonate yourself', ephemeral=True)
        return
    else:
        if "@everyone" in message:
            await interaction.response.send_message('Hey!, you cannot do these', ephemeral=True)
            return
        if "@here" in message:
            await interaction.response.send_message('Hey!, you cannot do these', ephemeral=True)
            return
        if "http" in message:
            await interaction.response.send_message('Hey!, you cannot do these', ephemeral=True)
            return
        else:
            webhook = await interaction.channel.create_webhook(name=member.display_name, reason=f"impersonate by {interaction.user}")
            await webhook.send(str(message), username=member.display_name, avatar_url=member.display_avatar.url)
            webhooks = await interaction.channel.webhooks()
            for webhook in webhooks:
                if member.display_name in webhook.name:
                    await webhook.delete()
            await interaction.response.send_message(f'{member.mention} has been impersonated', ephemeral=True)

@tree.command()
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Ayuda", description="Selecciiona una categoría para ver los comandos <:pan:970052408350769232>")
    await interaction.response.send_message(embed=embed, view=SelectView(), ephemeral=True)

@tree.command(name="add", description=f"Add me to your server")
async def add(interaction: discord.Interaction):
    embed = discord.Embed(title="Invitame a tu servidor!", color=discord.Color.purple()) 
    embed.set_image(url='https://affectionate-hawking-8dcfae.netlify.app/937411863388512276.gif') 
    view = discord.ui.View()
    style = discord.ButtonStyle.green  
    item = discord.ui.Button(style=style, label="Invite", url="https://galactiko.net/invite")  
    view.add_item(item=item)  
    await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

@tree.command(name = 'snipe')
@discord.app_commands.checks.has_permissions(manage_messages=True)
@discord.app_commands.choices(edited=[
    Choice(name='True', value=1),
    Choice(name='False', value=2),
])
async def snipe(interaction: discord.Interaction, edited: Optional[Choice[int]] = None):
    await interaction.response.defer(thinking=True)
    await asyncio.sleep(0.5)
    value = edited.value or 2
    if value == 2:

        try:
            contents, author, channel_name, time = uwu.sniped_messages[interaction.channel.id]
        except:
                await interaction.followup.send("No hay mensajes borrados recientemente")
                return
        embed = discord.Embed(description=contents,
                                color=interaction.user.color,
                                timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar.url)
        embed.set_footer(text=f"Eliminado en #{channel_name}")
        
        await interaction.followup.send(embed=embed)

    if value == 1:
        try:
            contents, author, channel_name, time, e, url = uwu.esniped_messages[interaction.channel.id]
        except:
                await interaction.followup.send("No hay mensajes editados recientemente")
                return
        embed = discord.Embed(description=f"[Redirección al mensaje]({url})",
                                color=interaction.user.color,
                                timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar.url)
        embed.set_footer(text=f"Editado en #{channel_name}")
        embed.add_field(name="Antes", value=contents, inline=False)
        embed.add_field(name="Después", value=e, inline=False)
        await interaction.followup.send(embed=embed)

@tree.context_menu(name="Simp")
async def simp(interaction: discord.Interaction, user: discord.Member ):
        member = user
        async with aiohttp.ClientSession() as session:
                async with session.get(
                f'https://some-random-api.ml/canvas/simpcard?avatar={member.avatar.url.format("png")}'
                ) as af:
                    if 300 > af.status >= 200:
                        fp = io.BytesIO(await af.read())
                        file = discord.File(fp, "simpcard.png")
                        em = discord.Embed(
                            title="Simp!",
                            color=0xf1f1f1,
                        )
                        em.set_image(url="attachment://simpcard.png")
                        await interaction.response.send_message(embed=em, file=file)
                    else:
                        await interaction.response.send_message('Simp')
                await session.close()

@tree.context_menu(name="Jail")
async def jail(interaction: discord.Interaction, user: discord.Member):
    member = user
    async with aiohttp.ClientSession() as session:
            async with session.get(
            f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.url.format("png")}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "jail.png")
                    em = discord.Embed(
                        title="lo agarraron los municipales :c",
                        color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://jail.png")
                    await interaction.response.send_message(embed=em, file=file)
                else:
                    await interaction.response.send_message('Something went wrong')      
            await session.close()

@tree.context_menu(name="Gay")
async def gay(interaction: discord.Interaction, user: discord.Member):
    member = user
    async with aiohttp.ClientSession() as session:
            async with session.get(
            f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.url.format("png")}'
        ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gay.png")
                    em = discord.Embed(
                    title="gei",
                    color=0xf1f1f1,
                    )
                    em.set_image(url="attachment://gay.png")
                    await interaction.response.send_message(embed=em, file=file)
                else:
                    await interaction.response.send_message('gei')
            await session.close()

async def main():
    async with uwu:
        await load_extensions()
        await uwu.start(TOKEN)
asyncio.run(main())

