from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.dispatcher import Dispatcher
from utils.config import API_TOKEN




# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a file handler for the logger
handler = logging.FileHandler('bot.log')
handler.setLevel(logging.DEBUG)

# Add the file handler to the logger
logger.addHandler(handler)





storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot,
                storage=storage)



