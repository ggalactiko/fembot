import discord
message_content = ''
last_message = ''
last_message_content = ''
spam_counter = 0

__version__ = "1.0.0"

async def AntiScam(message: discord.Message, bot, whitelist, muted_role, logs_channel):
    global message_content, last_message, last_message_content, spam_counter
    message_content = f'{message.author.id}: {message.content}'
    message_content = message_content.replace("'", "`")
    mentions = message.raw_mentions
    # AntiScam-System
    if message.author.bot and message.author.public_flags == 65536:
        return

    if message_content == last_message_content and message.content != '' and message.author.id not in whitelist:
        spam_counter += 1
        await message.delete()

    else:
        last_message = message
        last_message_content = message_content
        spam_counter = 0

    if len(mentions) > 10 and message.author.id not in whitelist:
        await message.delete()
        spam_counter = 2

    if spam_counter > 1 and message.author.id not in whitelist:
        spam_counter = 0
        muted = discord.utils.get(message.author.guild.roles, name=muted_role)
        await last_message.delete()
        await message.author.add_roles(muted)
        channel = bot.get_channel(logs_channel)
        await channel.send(f'USUARIO MUTEADO: {message_content}')
    await bot.process_commands(message)