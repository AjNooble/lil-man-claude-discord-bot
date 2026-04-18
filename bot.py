import discord
import anthropic
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        user_message = message.content.replace(f"<@{client.user.id}>", "").strip()
        async with message.channel.typing():
            response = anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": user_message}]
            )
            await message.channel.send(response.content[0].text)

client.run(os.environ["DISCORD_TOKEN"])
