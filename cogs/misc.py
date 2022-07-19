import asyncio
import io
import json
import requests
import discord
import aiohttp
from discord.ext import commands
from datetime import datetime
import random
import os 


class msc(commands.Cog):  # All cogs must inherit from commands.Cog
    """A simple, basic cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def load_extensions(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await self.bot.load_extension(f"cogs.{filename[:-3]}")
                except:
                    print(f"Failed to load extension{filename[:-3]}")

    async def reload_extensions(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await self.bot.reload_extension(f"cogs.{filename[:-3]}")
                except:
                    print(f"Failed to reload extension{filename[:-3]}")

    async def unload_extensions(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                try:
                    await self.bot.unload_extension(f"cogs.{filename[:-3]}")
                except:
                    print(f"Failed to unload extension{filename[:-3]}")

    view = discord.ui.View()
    style = discord.ButtonStyle.green  
    item = discord.ui.Button(style=style, label="Add Fembot", url="https://galactiko.net/invite")  
    view.add_item(item=item)  
    embed = discord.Embed(title="", description="As of August 30, prefix commands will no longer work; use slash commands instead, type '/' to see a list of available commands, if you can't see any try re-inviting me", color=discord.Color.red())

    @commands.command(name="shorten", aliases=["shorturl"])
    async def shorten(self, ctx, url= None):
        """Shorten a URL."""
        if url is None:
            await ctx.send("Please provide a URL to shorten.")
            return
        x = requests.post("https://galactiko.net/api/redirects", json = {'url': url})
        catjson = await x.json() 
        shurl = catjson['key']
        embed = discord.Embed(title="URL shortened", description=f"{url} has been shortened to {shurl}", color=discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.command(name='say', help='Envía un mensaje a través del bot')
    async def say(self, ctx: commands.Context, message=None):
        autor=ctx.message.author
        if message is None:
            await ctx.send("Please provide a message to send.")
            return
        if "http" in message:
            await ctx.send("Please do not include a URL in your message.")
            return
        if "@everyone" in message:
            await ctx.send("Please do not include @everyone in your message.")
            return
        if "@here" in message:
            await ctx.send("Please do not include @here in your message.")
            return
        if "discord.gg" in message:
            await ctx.send("Please do not include a discord.gg link in your message.")
            return
        if "discordapp.com/invite" in message:
            await ctx.send("Please do not include a discordapp.com/invite link in your message.")
            return
        else:
            await ctx.send(f"{message} \n\n Enviado por:{autor}")
            await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: commands.Context, prefix = None):
        if prefix is None:
            await ctx.send("Ingrese un prefix")
        elif prefix is not None:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
            prefixes[str(ctx.guild.id)] = prefix
            with open("prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=4)
            await ctx.send(f"Prefix changed to: {prefix}")

    @commands.command(name='dog', help='Envía una imagen random de un perro')
    async def dog(self, ctx: commands.Context):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog') 
      dogjson = await request.json()
     embed = discord.Embed(title="Doggo!", color=discord.Color.purple()) 
     embed.set_image(url=dogjson['link']) 
     await ctx.send(embed=embed) 
     await ctx.send(embed=self.embed, view=self.view)


    @commands.command(name="botconfig")
    @commands.is_owner()
    async def botconfigs(self, ctx, cg= None, changes= None):
        if cg is None:
            await ctx.send("Ingrese una configuracion")
        elif cg is not None:
            config = cg.lower()
            if config == "load":
                async with ctx.typing():
                    if changes == "all":
                        await self.load_extensions()
                        await ctx.send("Done!")
                    else:
                        await self.bot.load_extension(f"cogs.{changes}")
                        await asyncio.sleep(5)
                        await ctx.send("Done!")
            if config == "reload":
                async with ctx.typing():
                    if changes == "all":
                        await self.reload_extensions()
                        await ctx.send("Done!")
                    else:
                        await self.bot.reload_extension(f"cogs.{changes}")
                        await asyncio.sleep(5)
                        await ctx.send("Done!")
            if config == "unload":
                async with ctx.typing():
                    if changes == "all":
                        await self.unload_extensions()
                        await ctx.send("Done!")
                    else:
                        await self.bot.unload_extension(f"cogs.{changes}")
                        await asyncio.sleep(5)
                        await ctx.send("Done!")

    @commands.command(name='cat', help='Envía una imagen random de un gato')
    async def cat(self, ctx: commands.Context):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      catjson = await request.json() 
     embed = discord.Embed(title="kitty!", color=discord.Color.purple()) 
     embed.set_image(url=catjson['link']) 
     await ctx.send(embed=embed) 
     await ctx.send(embed=self.embed, view=self.view)

    @commands.command(name='fox', help='Envía una imagen random de un zorro')
    async def fox(self, ctx: commands.Context):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/fox')
      foxjson = await request.json() 
     embed = discord.Embed(title="Fox!", color=discord.Color.orange()) 
     embed.set_image(url=foxjson['link']) 
     await ctx.send(embed=embed) 
     await ctx.send(embed=self.embed, view=self.view)

    @commands.command(name='panda', help='Envía una imagen random de un panda')
    async def panda(self, ctx: commands.Context):
     async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/panda')
      pandajson = await request.json() 
     embed = discord.Embed(title="Panda!", color=discord.Color.green()) 
     embed.set_image(url=pandajson['link']) 
     await ctx.send(embed=embed) 
     await ctx.send(embed=self.embed, view=self.view)

    @commands.command()
    async def horny(self, ctx: commands.Context, member: discord.Member = None):
        '''Horny license just for u'''
        member = member or ctx.author
        async with ctx.typing():
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
                    await ctx.send(embed=em, file=file)
                 else:
                    await ctx.send('No horny :(')
                await session.close()
                await ctx.send(embed=self.embed, view=self.view)

    @commands.command()
    async def simp(self, ctx: commands.Context, member: discord.Member = None):
        '''simp license just for u'''
        member = member or ctx.author
        async with ctx.typing():

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
                    await ctx.send(embed=em, file=file)
                 else:
                    await ctx.send('Simp')
                await session.close()
                await ctx.send(embed=self.embed, view=self.view)

    @commands.command()
    async def jail(self, ctx: commands.Context, member: discord.Member = None):
        '''aaaa license just for u'''
        member = member or ctx.author
        async with ctx.typing():
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
                    await ctx.send(embed=em, file=file)
                 else:
                    await ctx.send('lo agarraron los municipales :c')
                await session.close()
                await ctx.send(embed=self.embed, view=self.view)

    @commands.command()
    async def gay(self, ctx: commands.Context, member: discord.Member = None):
        '''aaaa license just for u'''
        member = member or ctx.author
        async with ctx.typing():
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
                    await ctx.send(embed=em, file=file)
                 else:
                    await ctx.send('gei')
                await session.close()
                await ctx.send(embed=self.embed, view=self.view)

    class ViewWithButton(discord.ui.View):
        @discord.ui.button(style=discord.ButtonStyle.blurple, label='Another meme')
        async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            types = ["video", "img"]
            meme_type = random.choice(types)
            if meme_type == "img":

                    async with aiohttp.ClientSession() as session:
                        request = await session.get('https://gko.one/api/v2/memes?type=img')
                        catjson = await request.json() 
                    embed = discord.Embed(title="meme", color=discord.Color.purple()) 
                    embed.set_footer(text=f"source: {catjson['source']}")
                    embed.set_image(url=catjson['url']) 
                    await asyncio.sleep(0.4)
                    await interaction.response.send_message(embed=embed, view=self)
        
            if meme_type == "video":
                    async with aiohttp.ClientSession() as session:
                        request = await session.get('https://galactiko.net/api/v2/memes?type=video')
                        catjson = await request.json() 
                    async with aiohttp.ClientSession() as session:
                        async with session.get(catjson['url']) as af:
                            if 300 > af.status >= 200:
                                fp = io.BytesIO(await af.read())
                                file = discord.File(fp, "galactiko_com.mp4")
                                await interaction.response.send_message(file=file, view=self)
                            else:
                                await interaction.response.send_message.send('Err')
                        await session.close()
                
    @commands.command(pass_context=True)
    async def meme(self, ctx: commands.Context):
            types = ["video", "img"]
            meme_type = random.choice(types)
            if meme_type == "img":
                async with ctx.typing():
                    async with aiohttp.ClientSession() as session:
                        request = await session.get('https://gko.one/api/v2/memes?type=img')
                        catjson = await request.json() 
                    embed = discord.Embed(title="meme", color=discord.Color.purple()) 
                    embed.set_footer(text=f"source: {catjson['source']}")
                    embed.set_image(url=catjson['url']) 
                    await asyncio.sleep(0.4)
                    await ctx.send(embed=embed, view=self.ViewWithButton())
            if meme_type == "video":
                async with ctx.typing():
                    async with aiohttp.ClientSession() as session:
                        request = await session.get('https://galactiko.net/api/v2/memes?type=video')
                        catjson = await request.json() 
                    async with aiohttp.ClientSession() as session:
                        async with session.get(catjson['url']) as af:
                            if 300 > af.status >= 200:
                                fp = io.BytesIO(await af.read())
                                file = discord.File(fp, "galactiko_com.mp4")
                                await ctx.send(file=file, view=self.ViewWithButton())
                            else:
                                await ctx.send('Err')
                        await session.close()
            await ctx.send(embed=self.embed, view=self.view)

    @commands.command()
    async def simpometer(self, ctx: commands.Context):
        percentage = (random.randint(0, 100))
        embed = discord.Embed(title="Simp O Meter", description=f"Eres {percentage}% simp", color=discord.Color.purple()) 
        embed.set_image(url='https://assets.puzzlefactory.pl/puzzle/349/392/original.jpg')
        await ctx.send(embed=embed)
        await ctx.send(embed=self.embed, view=self.view)

    @commands.command()
    async def impersonate(self, ctx: commands.Context):
        view = discord.ui.View()
        style = discord.ButtonStyle.green  
        item = discord.ui.Button(style=style, label="Re Invite", url="https://galactiko.net/invite")  
        view.add_item(item=item)  
        await ctx.reply("¡Vaya!, este comando ahora está en desuso. Utilice /impersonate en su lugar. si no puede encontrar el comando, intente volver a invitarme.", view=view)

    @commands.command(case_insensitive=True, aliases=["reminder", "rm"])
    async def remind(self, ctx: commands.Context, time, *, reminder="something"):
        try:
            user = ctx.author.mention
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
                await ctx.send("Especifique una hora válida.")
            if reminder is None:
                await ctx.send("Por favor, dime qué recordarte.")
            else:
                log.set_author(name=f"{ctx.author.display_name}#{ctx.author.discriminator} - Remind", icon_url=ctx.author.avatar.url)
                log.set_footer(text=f"{counter} | {reminder}")
                embed.add_field(
                name="**Reminder**",
                value=f"{user}, me pediste que te recordara `{reminder}` hace `{counter}` ."
                )
                await ctx.send(f"Te recordaré `{reminder}` en `{counter}`.")
                await asyncio.sleep(seconds)
                await ctx.author.send(embed=embed)
                await ctx.send(embed=log)
                return
        except ValueError:
            await ctx.send("Unexpected error")
        await ctx.send(embed=self.embed, view=self.view)

async def setup(bot):
    await bot.add_cog(msc(bot))