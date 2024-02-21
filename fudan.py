"""
Title: Fudan Bot
Author: Chirag Giri
Date: February 19, 2024
Purpose: This code demonstrates how to create a simple moderation Discord bot using Python.
Usage: Moderation bot with security features like rate limiting, logging and permissions management.
License: None
Version History:
- 1.0 (February 19, 2024): Initial version
"""

import discord
from discord.ext import commands
from datetime import datetime
from discord.ext.commands import has_permissions

# Initialize Discord intents to specify the bot's behavior
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")

# Variables and constants
BOTTOKEN = "YOUR BOT TOKEN HERE" #enter your bot token before running
banned_words = []

# Helper function for loading banned words when the bot starts
def load_banned_words():
    global banned_words
    try:
        with open("banned_words.txt") as file:
            for line in file:
                banned_words.append(line.rstrip())
        print ("Banned words loaded successfully.")
    except FileNotFoundError:
        print("Error: banned_words.txt not found. Banned words list will be empty.")

# Event handler for when the bot is ready and connected to Discord
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Oregon Trials'))
    print("The bot is online.")
    print("-----------------------------")

#Load banned words on start.
load_banned_words()
print("-----------------------------")
    
# Simple command to verify bot functionality
@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the fudan bot.")

# MODERATION COMMANDS

# Command to add a word to the list of banned words
@client.command()
async def banword(ctx, word):
    if word.lower() not in banned_words:
        #update the current instance of banned_words
        banned_words.append(word.lower())
        try:
            with open("banned_words.txt", "a") as file:
                file.write("\n" + word)
                await ctx.send("Word banned.")
        except FileNotFoundError:
            print("Error: banned_words.txt not found. Banned words list will be empty.")
    else:
        await ctx.send(f"'{word}' is already in the list of banned words.")

# Command to kick a member from the server
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')

# Command to ban a member from the server
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been **banned**')

# Command to unban a member from the server
@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, member: discord.User, *, reason=None):
    if reason == None:
        reason = f"No Reason Provided"
    await ctx.guild.unban(member, reason = reason)
    await ctx.send(f"{member.mention} has been **unbanned**", delete_after=15)

# Command to purge a specified number of messages from the channel
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user) # Set a rate limit of 5 seconds per user
@has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit = amount + 1) # add one because it counts the command

# Command to mute a member in the voice channel
@client.command()
@has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    await member.edit(mute=True)
    await ctx.send(f"{member.mention} has been **muted**")

# Command to unmute a member in the voice channel
@client.command()
@has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    await member.edit(mute=False)
    await ctx.send(f"{member.mention} has been **unmuted**")

# Command to display bot information and usage instructions
@client.command()
async def help(ctx):
    help_embed = discord.Embed(
        title="Fudan Bot Help",
        description=(
            "This bot provides various moderation commands and logging features.\n"
            "To use moderation commands, ensure you have the necessary permissions.\n\n"
            "**Available Commands:**\n"
            "`!hello`: Test command to check if the bot is working.\n"
            "`!banword <word>`: Ban a word from being used in messages.\n"
            "`!kick <member> [reason]`: Kick a member from the server.\n"
            "`!ban <member> [reason]`: Ban a member from the server.\n"
            "`!unban <user> [reason]`: Unban a user from the server.\n"
            "`!purge [amount]`: Delete a specified number of messages from the channel.\n"
            "`!mute <member>`: Mute a member in the voice channel.\n"
            "`!unmute <member>`: Unmute a member in the voice channel.\n"
        ),
        color=discord.Color.blue()
    )
    help_embed.set_footer(text="For more details, contact the bot owner.")
    await ctx.send(embed=help_embed)

# EVENT HANDLERS
    
# Event handler to process messages and handle banned words
@client.event
async def on_message(message):
    await client.process_commands(message) #Process commands

    #Handle banned words
    if any(word in message.content.lower() for word in banned_words):
        await message.delete()
        await message.channel.send(f"Illegal action. {message.author} has been warned.")

# Event handler to create a log when a message is deleted.
@client.event
async def on_message_delete(message):
    z =client.get_channel(1208778075005784114)
    embed = discord.Embed(title = f"{message.author}'s Message was Deleted", description = f"Deleted Message: {message.content}\nAuthor: {message.author.mention}\nLocation: {message.channel.mention}", timestamp=datetime.now(), color = discord.Colour.red())
    embed.set_author(name = message.author.name, icon_url = message.author.display_avatar)
    await z.send(embed=embed)

# Event handler to create a log when a message is edited.
@client.event
async def on_message_edit(before, after):
    z =client.get_channel(1208778075005784114)
    embed = discord.Embed(title = f"{before.author} edited their message", description = f"Before: {before.content}\nAfter: {after.content}\nAuthor: {before.author.mention}\nLocation: {before.channel.mention}", timestamp=datetime.now(), color = discord.Colour.blue())
    embed.set_author(name = before.author.name, icon_url = before.author.display_avatar)
    await z.send(embed=embed)

# Event handler to create a log when a member's role and nickname is updated.
@client.event
async def on_member_update(before, after):
    z =client.get_channel(1208778075005784114)
    if len(before.roles) > len(after.roles):
        role = next(role for role in before.roles if role not in after.roles)
        embed = discord.Embed(title = f"{before}'s Role has been Removed", description=f"{role.name} was removed from {before.mention}", timestamp=datetime.now(), color = discord.Colour.blue())

    elif len(after.roles) > len(before.roles):
        role = next(role for role in after.roles if role not in before.roles)
        embed = discord.Embed(title = f"{before} got a new role", description=f"{role.name} was added to {before.mention}", timestamp=datetime.now(), color = discord.Colour.green())

    elif before.nick != after.nick:
        embed = discord.Embed(title = f"{before}'s Nickname Changed.", description=f"Before: {before.nick}\nAfter: {after.nick}", timestamp=datetime.now(), color = discord.Colour.blue())

    else:
        return
    
    embed.set_author(name = before.name, icon_url=after.display_avatar)
    await z.send(embed = embed)

# Event handler to create a log when a channel has been created.
@client.event
async def on_guild_channel_create(channel):
    z =client.get_channel(1208778075005784114)
    embed = discord.Embed(title = f"{channel.name} was Created", description= channel.mention, timestamp= datetime.now(), color = discord.Colour.green())
    await z.send(embed = embed)

# Event handler to create a log when a channel has been deleted.
@client.event
async def on_guild_channel_delete(channel):
    z =client.get_channel(1208778075005784114)
    embed = discord.Embed(title = f"{channel.name} was Deleted", timestamp= datetime.now(), color = discord.Colour.red())
    await z.send(embed = embed)

# ERROR HANDLERS
    
# Event handler for handling errors raised by commands
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): #checks if on cooldown
        msg = '**Still on cooldown**, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)

# Error handler for the ban command
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban people!")

# Error handler for the kick command
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to kick people!")

client.run(BOTTOKEN)