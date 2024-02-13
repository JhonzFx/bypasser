import os
import re
import time
import urllib
import random
import string
import base64
import discord
import asyncio
import requests
from io import BytesIO
from discord.ext import commands
from urllib.parse import urlparse, parse_qs
from collections import defaultdict
from captcha.image import ImageCaptcha
from captcha.audio import AudioCaptcha
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

fluxus_api = "ok"

class Bot(commands.Bot):
  def __init__(self, intents: discord.Intents, **kwargs):
    super().__init__(command_prefix="!", intents=intents, case_insensitive=True)

async def on_ready(self):
  print(f"Logged in as {self.user}")
  await self.tree.sync()

intents = discord.Intents.all()
bot = Bot(intents=intents)

@bot.hybrid_command(name="fluxus", description="Bypass Fluxus Key rinx")
async def fluxus(ctx, url: str):
    try:
        maintenance_keywords = ["keyrblx", "panda", "gateway", "codex", "hohohubv"]
        if any(keyword in url for keyword in maintenance_keywords):
            embed = discord.Embed(title="Invalid URL", description="Invalid URL. Please provide a Fluxus URL", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # hey rinx, this part extracts HWID from URL.
        parsed_url = urlparse(url)
        hwid = parse_qs(parsed_url.query).get('HWID')
        if not hwid:
            await ctx.send("Invalid URL. Please provide a URL containing the HWID parameter.")
            return

        api_url = fluxus_api + hwid[0]
        response = requests.get(api_url)

        if response.status_code == 200:
            embed = discord.Embed(title="Bypass Fluxus Key rinx", description=response.text, color=discord.Color.green())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Failed to Bypass URL", description="The URL could not be bypassed. Please try again later.", color=discord.Color.red())
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Example: https://keysystem.fluxteam.net/android/checkpoint/start.php?HWID=xxxx")

@fluxus.error
async def on_fluxus_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(str(error))

bot.run("ok")
