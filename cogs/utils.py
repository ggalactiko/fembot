import asyncio
from datetime import datetime
from typing import Optional
from discord import app_commands
import discord
import requests
import aiohttp

class utils(app_commands.Group):
    def __init__(self):  
        super().__init__()

    @app_commands.command(name="lock", description="Bloquea un canal")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]):
        channel = channel or interaction.channel
        if channel.permissions_for(interaction.guild.default_role).send_messages is False:
            return await interaction.response.send_message("El canal ya está bloqueado", ephemeral=True)
        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        embed = discord.Embed(title="Canal bloqueado", description="El canal ha sido bloqueado", color=0x00ff00)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unlock", description="Bloquea un canal")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]):
        channel = channel or interaction.channel
        if channel.permissions_for(interaction.guild.default_role).send_messages is True:
            return await interaction.response.send_message("El canal ya está desbloqueado", ephemeral=True)
        await channel.set_permissions(interaction.guild.default_role, send_messages=True)
        embed = discord.Embed(title="Canal bloqueado", description="El canal ha sido bloqueado", color=0x00ff00)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='purge', description='Elimina cierta cantidad de mensajes')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int , channel: Optional[discord.TextChannel] = None):
        if amount > 100:
            amount = 100
        channel =  channel or interaction.channel
        deleted_messages = await channel.purge(limit=amount)
        await interaction.response.send_message(f"{len(deleted_messages)} Mensajes eliminados \n\n Nota:Los mensajes anteriores a 2 semanas no se eliminarán", ephemeral=True) # Subtracting 1 as it's the message of the command
                  
    @app_commands.command(name="reminder", description="Crea un recordatorio")
    async def remind(self, interaction: discord.Interaction, time: str, reminder: str):
        try:
            user = interaction.user.mention
            seconds = 0
            log = discord.Embed(color=0xe9a9a9, timestamp=datetime.utcnow())
            embed = discord.Embed(color=0xe9a9a9)
            if time.lower().endswith("d"):
                seconds += int(time[:-1]) * 60 * 60 * 24
                counter = f"{seconds // 60 // 60 // 24} días"
            if time.lower().endswith("h"):
                seconds += int(time[:-1]) * 60 * 60
                counter = f"{seconds // 60 // 60} horas"
            if time.lower().endswith("m"):
                seconds += int(time[:-1]) * 60
                counter = f"{seconds // 60} minutos"
            if time.lower().endswith("s"):
                seconds += int(time[:-1])
                counter = f"{seconds} segundos"
            if seconds == 0 or seconds > 7776000:
                await interaction.response.send_message("Especifique una hora válida.")
            else:
                log.set_author(name=f"{interaction.user.display_name}- Remind", icon_url=interaction.user.avatar.url)
                log.set_footer(text=f"{counter} | {reminder}")
                embed.add_field(
                name="**Reminder**",
                value=f"{user}, me pediste que te recordara `{reminder}` hace `{counter}` en [#{interaction.channel.name}]({interaction.channel.jump_url})."
                )
                await interaction.response.send_message(f"Te recordaré `{reminder}` en `{counter}`.")
                await asyncio.sleep(seconds)
                await interaction.user.send(embed=embed)
                await interaction.channel.send(user,embed=log)
                return
        except ValueError:
            await interaction.response.send_message("Unexpected error") 

    @app_commands.command(name="shorten", description="Shorten a link")
    async def shorturl(self, interaction: discord.Interaction, url:str ):
        async with aiohttp.ClientSession() as session:
            request = await session.post('https://galactiko.net/api/v1/redirects', json={'url': url})
            dogjson = await request.json()
            status = dogjson['status']
            if status == "success":
                dogurl = dogjson['key']
                embed = discord.Embed(title="Dog", description=f"{url} has been shortened to {dogurl}", color=discord.Color.purple())
                await interaction.response.send_message(embed=embed)
            await interaction.response.send_message(embed=embed) 

    @app_commands.command(name="nuke")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def nuke(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        nuke_channel = channel or interaction.channel
        embed1=discord.Embed(title="Nuked the Channel sucessfully!")
        embed1.set_thumbnail(url="https://images2.minutemediacdn.com/image/upload/c_crop,h_1126,w_2000,x_0,y_83/f_auto,q_auto,w_1100/v1555949079/shape/mentalfloss/581049-mesut_zengin-istock-1138195821.jpg")
        embed1.set_author(name=f"{interaction.user}", icon_url=f"{interaction.user.avatar.url}")
        embed1.timestamp = datetime.datetime.now()
        embed3=discord.Embed(title="THIS CHANNEL HAS BEEN NUKED! BY THE MOTHER FUCKER URSS FOR THE THIRD WORLD WAR")
        embed3.set_thumbnail(url="https://media0.giphy.com/media/oe33xf3B50fsc/giphy.gif")
        embed3.set_footer(text=f"Nuked by {interaction.user}", icon_url=f"{interaction.user.avatar.url}")
        embed3.timestamp = datetime.datetime.now()
        if interaction.guild.rules_channel  == nuke_channel:
            await interaction.response.send_message("no puedes nuke el canal de reglas")
            return
        if interaction.guild.public_updates_channel  == nuke_channel:
            await interaction.response.send_message("no puedes nuke el canal de publicaciones")
            return
        else:
            channel_position = nuke_channel.position
            new_channel = await nuke_channel.clone(reason="Has been Nuked!")
            await nuke_channel.delete()
            await new_channel.send(embed=embed3)
            await new_channel.edit(position=channel_position, sync_permissions=True)
            await interaction.response.send_message(embed=embed1, ephemeral=True)

    @app_commands.command(name="say")
    @app_commands.describe(text="Mensaje que se enviará")
    async def say(self, interaction:discord.Interaction, text: str):
        if "@here" in text:
            await interaction.response.send_message("No puedes usar @here", ephemeral=True)
            return
        if "@everyone" in text:
            await interaction.response.send_message("No puedes usar @everyone", ephemeral=True)
            return
        else:
            await interaction.response.send_message(f"{text} \n\n-{interaction.user}")
            return

async def setup(bot):
    bot.tree.add_command(utils())