import asyncio
import aiohttp
import json
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

# Токен из переменной окружения
API_TOKEN = os.getenv('API_TOKEN', '8013345611:AAFLtY-kRoE5xkMiXZ9uzvoUJukSE96voXg')

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def fetch_data(message):
    url = 'https://chatgpt5.org/api/text'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://chatgpt5.org',
        'Referer': 'https://chatgpt5.org/chat',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    payload = {
        "message": message,
        "recaptcha_token": "0.iJ6396y_Wxyg6RDdEV5i9ckGyXY-DgkHqc7xHMpWE2elJ9Rmg49KMIUEqFR4GjeVK18Ng39nPOTgU9XqVtJO9_Ovi8_Qf4T0q2EBkw-gXz7tKDFL-m2p-QL3Y-g3BQZnvgomQnqv-C8-jmqglPg-HNbLkYkt7z0eKX-DKTyuB8vJw3lIe9k6Dxs5Inrm27gA7OsOpjQaqodnK6T4vEXurYTVeGqo7qQuVI22fTCXOCJ-ba7sd_kYGYJe48hRMo138ZuWKCRPdOU3SG5YYP8T_HMnDsBmkuoc0JZ3HiaoB_dKC_xHGNvyNAbbBOZNTLE8E34mbBl--M88S3FZ79fIn5X-lERzCVgg7ME0micidSkD9oN0MedXmlasS8svCuvRTf4k4mQNbLcslPNyt55JUJPfR5Z49bUuN1mjBFbLWagsnZaxpb2pafHneL8JCx6RUBgpBJXv2Op0pyNn1oyIdVxe7iP7IhlrZoG_PwavMa6yzAIsyBp00S20s7K5ASZPdIc4oFN90G3SJqLt42dboSPeerBBgHedr5Os5I52lNQy989erHpZas64JLx8qbAM3b2lCWCLBQd3ADifbwVTSlK-w3DWvC9UKxzJVYklEAehX7gp7z1bDKAHdkU1K4COCzgmEz5Ot1zcYaMAK0IOLfDrEHBExuiSklk-Juu04mcEXzYDehqEv32awVkjk6b6quQAnLKkI_GLnzGmeoUiU45KfB6F-XTszAYPodktZikEWzucwbsBHnOFGNujn_2FM8e3R62ONm7tNMAma1OCzt0LphJAUf36JXWUTP8BiJML-UVyoHxC0jYbT845A4sgGJ_i2MnqJi_4PLTlMIO9SxVk_8iW99hiTsygI-O5AdjhT2aGBDGnf-j01Bh5p03FHAGCUQArtSsQbwm1ioNimOjkZa3HgAB59QO0AsU-T4ch9xd3ndAPkqy_xFus3Iaa.D5KIxrVahpaZuJJiOY90ww.4c0bdabce087f8493253bd0d4e8aa023d6a413bbd4f7e23078193a5c032c4487",
        "temperature": 1,
        "presence_penalty": 0,
        "top_p": 1,
        "frequency_penalty": 0
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()
            return data


@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Напиши любое сообщение, и я отправлю запрос к GPT.")


@dp.message(F.text)
async def get_gpt_response(message: Message):
    if message.text.startswith('/'):
        return
    
    try:
        await bot.send_chat_action(message.chat.id, "typing")
        response = await fetch_data(message.text)
        result = json.dumps(response, indent=4, ensure_ascii=False)
        
        if len(result) > 4000:
            for i in range(0, len(result), 4000):
                await message.answer(f"```\n{result[i:i+4000]}\n```", parse_mode='Markdown')
        else:
            await message.answer(f"```\n{result}\n```", parse_mode='Markdown')
            
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
