import discord
from discord import Intents
import asyncio
import cv2
from PIL import Image
import random

TOKEN = ''
USER_ID =   # Замените на ID нужного пользователя

intents = Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

def video_to_ascii_frames(video_path, output_width=40):
    cap = cv2.VideoCapture(video_path)
    frames = []
    ascii_chars = ".,-~:=$#@"
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray_frame.shape
        aspect_ratio = height / width
        new_width = output_width
        new_height = int(aspect_ratio * new_width * 0.55)
        resized_gray = cv2.resize(gray_frame, (new_width, new_height))
        ascii_frame = ""
        for y in range(new_height):
            for x in range(new_width):
                gray_value = resized_gray[y, x]
                ascii_frame += ascii_chars[gray_value * len(ascii_chars) // 256]
            ascii_frame += "\n"
        frames.append(ascii_frame)
    cap.release()
    return frames

async def send_animation(channel, frames, delay=0.7):
    msg = await channel.send('Starting animation...') 
    for frame in frames:
        try:
            await msg.edit(content=f'```\n{frame}\n```')
        except discord.errors.HTTPException:
            await asyncio.sleep(delay) 
            await msg.edit(content=f'```\n{frame}\n```') 
        await asyncio.sleep(delay)  

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    print(f"Received message from {message.author}: {message.content}")  
    if message.author.id != USER_ID:  
        return
    print(f"Message from target user: {message.content}")  
    if message.content == 'фокус': # Заменить на слово тригер!
        await message.delete()  
        video_path = '12.mp4'
        frames = video_to_ascii_frames(video_path)
        asyncio.create_task(send_animation(message.channel, frames))
        return
    if message.content.startswith('!start_animation'):
        video_path = '12.mp4'
        frames = video_to_ascii_frames(video_path)
        asyncio.create_task(send_animation(message.channel, frames))

client.run(TOKEN)
