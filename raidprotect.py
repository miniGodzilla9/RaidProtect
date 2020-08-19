import discord
from discord.ext.commands import *
from discord.ext import commands
from discord import Permissions
from discord import Webhook, AsyncWebhookAdapter

import random
import colorama
from colorama import Fore, Style
import aiohttp
import asyncio


token = ""


client = commands.Bot(command_prefix = "$")
client.remove_command(name = "help")


@client.event
async def on_ready():
    print("Bot is ready.")
    game = discord.Game(
        f"$help || {len(client.users)} users and {len(client.guilds)} servers")
    await client.change_presence(activity=game, status=discord.Status.dnd)







@client.command()
@has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
  try:
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Purged {amount} messages in {ctx.message.channel} successfully.")
  except:
    await ctx.send(f"Couldn't purge {amount} messages in {ctx.channel}. You're either missing permissions or my role isn't high enough.")

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, user, reason = None):
  try:
    await user.send(f"You were kicked from **{ctx.guild.name}** for **{reason}**")
    await user.kick()
    await ctx.send(f"{user.name} was kicked for **{reason}**")
  except:
    await ctx.send(f"{user.name} wasn't kicked. You're either missing permissions or my role isn't high enough.")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, user, reason = None):
  try:
    await user.send(f"You were banned from **{ctx.guild.name}** for **{reason}**")
    await user.ban()
    await ctx.send(f"{user.name} was banned for **{reason}**")
  except:
    await ctx.send(f"{user.name} wasn't banned. You're either missing permissions or my role isn't high enough.")

@client.command()
@has_permissions(kick_members=True)
async def warn(ctx, user, reason = None):
  try:
    await user.send(f"You were warned in **{ctx.guild.name}** for **{reason}**")
    await ctx.send(f"{user.name} was warned for **{reason}**")
  except:
    await ctx.send(f"{user.name} wasn't warned. You're either missing permissions or my role isn't high enough.")

@client.command()
@has_permissions(manage_channels=True)
async def slowmode(ctx, delay):
  await ctx.channel.edit(slowmode_delay = delay)
  await ctx.send(f"Slowmode delay set to {delay} seconds.")

@client.command()
@has_permissions(ban_members = True)
async def hackban(ctx, member_id, *, reason=None):
  member = discord.Object(id=member_id)
  await ctx.guild.ban(member, reason = reason)
  member = client.fetch_member(member_id)
  await ctx.channel.send(f"Hackbanned **{member}** for **{reason}**.")

@client.command()
async def help(ctx):
 embed = discord.Embed(color=discord.Colour.darker_grey(), timestamp=ctx.message.created_at)

 embed.set_author(name="Help", icon_url=ctx.author.avatar_url)
 embed.add_field(name="**``slowmode <delay>``**", value="Sets a slowmode delay in the channel. The maximum delay is 21600.", inline=False)
 embed.add_field(name="**``warn <user> <reason>``**", value="Warns the user.", inline=False)
 embed.add_field(name="**``kick <user> <reason>``**", value="Kicks the user.", inline=False)
 embed.add_field(name="**``ban <user> <reason>``**", value="Bans the user.", inline=False)
 embed.add_field(name="**``hackban <user id>``**", value="Bans a user outside of a guild.", inline=False)
 embed.add_field(name="**``purge <amount>``**", value="Purges messages.", inline=False)
 embed.add_field(name="**``logs setup``**", value="Sets up logging.", inline=False)
 embed.add_field(name="**``logs bind <channel>``**", value="Binds logging to another channel.", inline=False)


 embed.add_field(name="⠀", value="⠀", inline=False)
 embed.add_field(name="The bot will automatically kick users who are blacklisted in our system.", value="Note: You must have the required permissions to use the moderation commands.", inline=False)

 await ctx.send(embed=embed)




@client.event
async def on_guild_channel_delete(channel):
    await asyncio.sleep(1)

    async for entry in channel.guild.audit_logs(limit=1):
        embed = discord.Embed(
            title='Channel Deleted',
            description=
            f"Channel **{channel.name}** was deleted by {entry.user.mention}.")
        webhooks = await channel.guild.webhooks()
        for webhook in webhooks:
            if webhook.name == "Raid Protect Logs":
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        webhook.url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(embed=embed)


@client.event
async def on_guild_role_create(role):
    await asyncio.sleep(1)

    async for entry in role.guild.audit_logs(limit=1):
        embed = discord.Embed(
            title='Role Created',
            description=f"{role.mention} was created by {entry.user.mention}.")
        webhooks = await role.guild.webhooks()
        for webhook in webhooks:
            if webhook.name == "Raid Protect Logs":
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        webhook.url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(embed=embed)


@client.event
async def on_guild_role_delete(role):
    await asyncio.sleep(1)

    async for entry in role.guild.audit_logs(limit=1):
        embed = discord.Embed(
            title='Role Deleted',
            description=f"**{role.name}** was deleted by {entry.user.mention}."
        )
        webhooks = await role.guild.webhooks()
        for webhook in webhooks:
            if webhook.name == "Raid Protect Logs":
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        webhook.url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(embed=embed)


@client.event
async def on_member_ban(guild, member):

    await asyncio.sleep(1)
    async for entry in guild.audit_logs(limit=1):
        embed = discord.Embed(
            title='Member Banned',
            description=
            f"**{member}** was banned by {entry.user.mention} for **{entry.reason}**."
        )
        embed.set_footer(text=f"Member ID - {member.id}")
        webhooks = await guild.webhooks()
        for webhook in webhooks:
            if webhook.name == "Raid Protect Logs":
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        webhook.url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(embed=embed)


@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    await asyncio.sleep(1)

    async for entry in channel.guild.audit_logs(limit=1):
        embed = discord.Embed(
            title='Message Pinned',
            description=
            f"A message was pinned by {entry.user.mention} in {channel.mention}."
        )
        webhooks = await channel.guild.webhooks()
        for webhook in webhooks:
            if webhook.name == "Raid Protect Logs":
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        webhook.url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(embed=embed)


@client.event
async def on_message_delete(message):
    await asyncio.sleep(1)

    async for entry in message.guild.audit_logs(limit=1):
        channel = message.channel
        embed = discord.Embed(
            title='Message Deleted',
            description=
            f"A message was deleted from {message.author.mention} in {channel.mention}."
        )
        embed.add_field(
            name='Message Content', value=f"```{message.content}```")
        webhooks = await message.guild.webhooks()
        for webhook in webhooks:
            if webhook.name == "Raid Protect Logs":
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        webhook.url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(embed=embed)


@client.event
async def on_message_edit(before, after):
    await asyncio.sleep(1)
    if before.author.bot == True:
        return
    else:
        channel = before.channel
        embed = discord.Embed(
            title='Message Edited',
            description=
            f"A message was edited from {before.author.mention} in {channel.mention}.\n[Jump to Message]({before.jump_url})"
        )
        embed.add_field(name='Current Content', value=f"```{after.content}```")
        embed.add_field(
            name='Previous Content', value=f"```{before.content}```")
        webhooks = await before.channel.guild.webhooks()
        for webhook in webhooks:
            if webhook.name == "Raid Protect Logs":
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(
                        webhook.url, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(embed=embed)

with open("logspfp.jpg", 'rb') as f:
    logspfp = f.read()

@client.command()
async def logs(ctx, choice, *, channel: discord.TextChannel = None):
    guild = ctx.guild
    if choice == 'setup':
        message = await ctx.channel.send("Setting up logs...")
        channel = await guild.create_text_channel("logging")
        await channel.set_permissions(guild.default_role, send_messages=False)
        await channel.create_webhook(name="Raid Protect Logs", avatar=logspfp)
        await message.edit(content=f"Logging is now set up.\n{channel.mention}"
                           )
    if choice == 'bind':
        message = await ctx.channel.send(
            f"Binding logs to {channel.mention}...")
        webhooks = await ctx.guild.webhooks()
        for webhook in webhooks:
            if webhook.name == 'Raid Protect Logs':
                await webhook.delete()
            channel = channel
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                if webhook.name == "Raid Protect Logs":
                    await webhook.delete()
            await channel.create_webhook(name="Raid Protect Logs", avatar=logspfp)
            await message.edit(content=f"Logs are bound to {channel.mention}.")


client.run(token)
