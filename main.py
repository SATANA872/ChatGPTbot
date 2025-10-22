import asyncio
import aiohttp
import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

# Токен для твоего бота
API_TOKEN = '8013345611:AAFLtY-kRoE5xkMiXZ9uzvoUJukSE96voXg'

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
        'Cookie': '_ga=GA1.1.998087329.1761150330; _ga_8F4G6QNTRF=GS2.1.s1761150330$o1$g1$t1761150333$j57$l0$h0; XSRF-TOKEN=eyJpdiI6IjhRS1VWSnBRY09QdHRxb2tKbE4rcFE9PSIsInZhbHVlIjoiL0t6bWtlUXZUeG5Fd1RlQlJMcHhtcFhZclZYMkxIWWxqeHp6dzJ5TDA2YmtOWFNUbWMveHFtQ01MdzBqSGFyMXJlVmRtZWtHWW5OYU4yVHc0MmVaWVFNYVdDZks3b1E4TmdYOUZwK3R6cE5ldnZFM2gvZi9VUS9OMzdReU1tV2IiLCJtYWMiOiJlNzU0ZGY4MzY2YjVmMTgxZmU2YmMxMWI1NmExM2Y4OTdiYjI5YWYzYWZlMmI3ODFjMDYwYzBhODYxNjkxZTk0In0%3D; chatgpt5org_session=eyJpdiI6InpyNExtTjJzSGVNVXlHUkpHRjh5TGc9PSIsInZhbHVlIjoiZlN5eVgxVDYvdHZxN2NqamNJeVcrV2xlRkJjNXg1Z05uYjE0TzVNTVAyNE04cHBnZVkxUUFvY3JOTW94UFhVREhwSmFRUXVobEVLSlpZVk5KZlI3S2NmVi9mcFBQNWxYNUFnalV1NGwrQ2RlSmkrK2EwNW9LTDIwSGdBanZMRUQiLCJtYWMiOiJmYzYzN2ViMjk1YmY5NGEyYTY2YzIxMjIzZmQ0NzE0ZmQyNDkzNWY3YWFlYzFlYjU0ZDAyYWVlMTVjY2NmZThhIn0%3D',
        'Origin': 'https://chatgpt5.org',
        'Referer': 'https://chatgpt5.org/chat',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "YaBrowser";v="24.10", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    payload = {
        "message": message,
        "recaptcha_token": "0.iJ6396y_Wxyg6RDdEV5i9ckGyXY-DgkHqc7xHMpWE2elJ9Rmg49KMIUEqFR4GjeVK18Ng39nPOTgU9XqVtJO9_Ovi8_Qf4T0q2EBkw-gXz7tKDFL-m2p-QL3Y-g3BQZnvgomQnqv-C8-jmqglPg-HNbLkYkt7z0eKX-DKTyuB8vJw3lIe9k6Dxs5Inrm27gA7OsOpjQaqodnK6T4vEXurYTVeGqo7qQuVI22fTCXOCJ-ba7sd_kYGYJe48hRMo138ZuWKCRPdOU3SG5YYP8T_HMnDsBmkuoc0JZ3HiaoB_dKC_xHGNvyNAbbBOZNTLE8E34mbBl--M88S3FZ79fIn5X-lERzCVgg7ME0micidSkD9oN0MedXmlasS8svCuvRTf4k4mQNbLcslPNyt55JUJPfR5Z49bUuN1mjBFbLWagsnZaxpb2pafHneL8JCx6RUBgpBJXv2Op0pyNn1oyIdVxe7iP7IhlrZoG_PwavMa6yzAIsyBp00S20s7K5ASZPdIc4oFN90G3SJqLt42dboSPeerBBgHedr5Os5I52lNQy989erHpZas64JLx8qbAM3b2lCWCLBQd3ADifbwVTSlK-w3DWvC9UKxzJVYklEAehX7gp7z1bDKAHdkU1K4COCzgmEz5Ot1zcYaMAK0IOLfDrEHBExuiSklk-Juu04mcEXzYDehqEv32awVkjk6b6quQAnLKkI_GLnzGmeoUiU45KfB6F-XTszAYPodktZikEWzucwbsBHnOFGNujn_2FM8e3R62ONm7tNMAma1OCzt0LphJAUf36JXWUTP8BiJML-UVyoHxC0jYbT845A4sgGJ_i2MnqJi_4PLTlMIO9SxVk_8iW99hiTsygI-O5AdjhT2aGBDGnf-j01Bh5p03FHAGCUQArtSsQbwm1ioNimOjkZa3HgAB59QO0AsU-T4ch9xd3ndAPkqy_xFus3Iaa.D5KIxrVahpaZuJJiOY90ww.4c0bdabce087f8493253bd0d4e8aa023d6a413bbd4f7e23078193a5c032c4487",
        "temperature": 0.7,
        "presence_penalty": 0,
        "top_p": 1,
        "frequency_penalty": 0
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()
            return data


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Напиши любое сообщение, и я отправлю запрос к GPT.")


# Обработчик всех текстовых сообщений (кроме команд)
@dp.message(F.text)
async def get_gpt_response(message: Message):
    # Игнорируем команды
    if message.text.startswith('/'):
        return
    
    try:
        # Отправляем уведомление о том, что бот работает
        await bot.send_chat_action(message.chat.id, "typing")
        
        response = await fetch_data(message.text)
        
        # Форматируем ответ и отправляем пользователю
        result = json.dumps(response, indent=4, ensure_ascii=False)
        
        # Telegram имеет лимит на длину сообщения (4096 символов)
        if len(result) > 4000:
            # Разбиваем на части
            for i in range(0, len(result), 4000):
                await message.answer(f"```\n{result[i:i+4000]}\n```", parse_mode='Markdown')
        else:
            await message.answer(f"```\n{result}\n```", parse_mode='Markdown')
            
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


async def main():
    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
