from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lazydeveloperr.utils import not_subscribed
from config import FORCE_SUB

@Client.on_message(filters.private & filters.create(not_subscribed))
async def is_not_subscribed(client, message):
    buttons = [[ InlineKeyboardButton(text="<b>📢ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ📢</b>", url=f"https://t.me/{FORCE_SUB}") ]]
    text = "<b>ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ</b>"
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
