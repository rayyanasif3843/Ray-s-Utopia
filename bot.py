import discord
from discord.ext import commands
from discord.utils import get
from datetime import timedelta
import yt_dlp

TOKEN = "YOUR_BOT_TOKEN"

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=",", intents=intents)

# ---------------- EVENTS ----------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ---------------- MODERATION ----------------

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member} was kicked.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} was banned.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):
    await member.timeout(timedelta(minutes=minutes), reason=reason)
    await ctx.send(f"⏰ {member.mention} timed out for {minutes} minutes.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    await member.timeout(None)
    await ctx.send(f"✅ Removed timeout from {member.mention}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Deleted {amount} messages.", delete_after=3)

# ---------------- WARN SYSTEM ----------------

warnings = {}

@bot.command()
@commands.has_permissions(moderate_members=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    if member.id not in warnings:
        warnings[member.id] = []

    warnings[member.id].append(reason)

    await ctx.send(
        f"⚠️ {member.mention} warned.\nReason: {reason}\nTotal Warnings: {len(warnings[member.id])}"
    )

@bot.command()
async def warnings(ctx, member: discord.Member):
    if member.id not in warnings:
        return await ctx.send("No warnings found.")

    text = "\n".join(warnings[member.id])
    await ctx.send(f"Warnings for {member.mention}:\n{text}")

# ---------------- MUTE ----------------

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    mute_role = get(ctx.guild.roles, name="Muted")

    if mute_role is None:
        mute_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(
                mute_role,
                send_messages=False,
                speak=False
            )

    await member.add_roles(mute_role)
    await ctx.send(f"🔇 {member.mention} muted.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role = get(ctx.guild.roles, name="Muted")

    if mute_role:
        await member.remove_roles(mute_role)

    await ctx.send(f"🔊 {member.mention} unmuted.")

# ---------------- MUSIC ----------------

@bot.command()
async def play(ctx, url):
    if not ctx.author.voice:
        return await ctx.send("Join a voice channel first.")

    channel = ctx.author.voice.channel

    if not ctx.voice_client:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client

    ydl_opts = {
        'format': 'bestaudio/best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    vc.stop()

    vc.play(
        discord.FFmpegPCMAudio(audio_url),
        after=lambda e: print("Finished")
    )

    await ctx.send(f"🎵 Playing: {info['title']}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Music stopped.")

# ---------------- RUN ----------------

bot.run(TOKEN)
