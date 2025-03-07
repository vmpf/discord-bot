import discord
from discord.ext import commands, tasks
import asyncio
import random
import datetime
import time
import pytz
import requests
import os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=',', intents=intents, help_command=None)
load_dotenv() 
token = os.getenv('DISCORD_TOKEN')
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f"{round(bot.latency * 1000)}ms", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.green())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title="User Kicked", description=f"{member.mention} has been kicked. Reason: {reason}", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(title="User Banned", description=f"{member.mention} has been banned. Reason: {reason}", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(title="Messages Purged", description=f"{amount} messages have been deleted.", color=discord.Color.orange())
    await ctx.send(embed=embed, delete_after=5)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(title="Messages Cleared", description=f"{amount} messages have been deleted.", color=discord.Color.orange())
    await ctx.send(embed=embed, delete_after=5)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    embed = discord.Embed(title="User Muted", description=f"{member.mention} has been muted.", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role in member.roles:
        await member.remove_roles(role)
        embed = discord.Embed(title="User Unmuted", description=f"{member.mention} has been unmuted.", color=discord.Color.green())
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title="Channel Locked", description="This channel has been locked.", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title="Channel Unlocked", description="This channel has been unlocked.", color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command()
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    embed = discord.Embed(title="Coin Flip", description=f"Result: {result}", color=discord.Color.purple())
    await ctx.send(embed=embed)

@bot.command()
async def roll(ctx, sides: int = 6):
    result = random.randint(1, sides)
    embed = discord.Embed(title="Dice Roll", description=f"You rolled a {result} on a {sides}-sided die.", color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.gold())
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Owner", value=guild.owner.mention)
    embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def uptime(ctx):
    delta = datetime.datetime.utcnow() - bot.start_time
    embed = discord.Embed(title="Uptime", description=str(delta).split('.')[0], color=discord.Color.green())
    await ctx.send(embed=embed)
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of all available commands:", color=discord.Color.blue())
    embed.add_field(name=",ping", value="Shows the bot's latency.", inline=False)
    embed.add_field(name=",avatar [member]", value="Displays the avatar of the specified member (or yourself).", inline=False)
    embed.add_field(name=",kick [member] [reason]", value="Kicks a member from the server.", inline=False)
    embed.add_field(name=",ban [member] [reason]", value="Bans a member from the server.", inline=False)
    embed.add_field(name=",purge [amount]", value="Deletes a specified number of messages.", inline=False)
    embed.add_field(name=",clear [amount]", value="Clears a specified number of messages.", inline=False)
    embed.add_field(name=",mute [member]", value="Mutes the specified member.", inline=False)
    embed.add_field(name=",unmute [member]", value="Unmutes the specified member.", inline=False)
    embed.add_field(name=",lock", value="Locks the current channel.", inline=False)
    embed.add_field(name=",unlock", value="Unlocks the current channel.", inline=False)
    embed.add_field(name=",coinflip", value="Flips a coin (Heads or Tails).", inline=False)
    embed.add_field(name=",roll [sides]", value="Rolls a dice with the specified number of sides.", inline=False)
    embed.add_field(name=",serverinfo", value="Displays information about the current server.", inline=False)
    embed.add_field(name=",uptime", value="Shows how long the bot has been online.", inline=False)
    
    embed.set_footer(text="Use ,<command> for detailed information.")
    await ctx.send(embed=embed)


bot.start_time = datetime.datetime.utcnow()
bot.run(token)
