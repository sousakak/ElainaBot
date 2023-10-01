from config import *

### report コマンド ###
async def report(interaction, message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )

    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(logChannel)

    embed = discord.Embed(title='報告されたメッセージ', url=message.jump_url)
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name + '#' + message.author.discriminator, icon_url=message.author.display_avatar.url)
    embed.set_footer(text='ID: ' + str(message.author.id))
    embed.timestamp = message.created_at

    await log_channel.send(embed=embed)