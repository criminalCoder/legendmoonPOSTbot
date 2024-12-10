import asyncio
from pyrogram import filters, Client, enums
from config import *
from lazydeveloperr.database import db 
from asyncio.exceptions import TimeoutError
from lazydeveloperr.txt import lazydeveloper
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from random import shuffle
from pyrogram.errors import FloodWait
from plugins.Data import Data
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError,
    MessageIdInvalidError
)
# user_forward_data = {}
St_Session = {}
handler = {}

def manager(id, value):
    global handler
    handler[id] = value
    return handler

def get_manager():
    global handler
    return handler


PHONE_NUMBER_TEXT = (
    "📞__ Now send your Phone number to Continue"
    " include Country code.__\n**Eg:** `+13124562345`\n\n"
    "Press /cancel to Cancel."
)

def set_session_in_config(id, session_string):
    from config import Lazy_session  # Import St_Session to modify it
    Lazy_session[id] = session_string

def set_api_id_in_config(id, lazy_api_id):
    from config import Lazy_api_id  # Import api id to modify it
    Lazy_api_id[id] = lazy_api_id

def set_api_hash_in_config(id, lazy_api_hash):
    from config import Lazy_api_hash  # Import api hash to modify it
    Lazy_api_hash[id] = lazy_api_hash

# lazydeveloperrsession = {}

@Client.on_message(filters.private & filters.command("connect"))
async def connect_session(bot, msg):
    user_id = msg.from_user.id
    
    if not await verify_user(user_id):
        return await msg.reply("⛔ You are not authorized to use this bot.")
    
    init = await msg.reply(
        "Starting session connection process..."
    )
    # get users session string
    session_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `TELETHON SESSION STRING`", filters=filters.text
    )
    if await cancelled(session_msg):
        return
    lazydeveloper_string_session = session_msg.text
    
    #get user api id 
    api_id_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_ID`", filters=filters.text
        )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ API_ID (ᴡʜɪᴄʜ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ). ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    
    # get user api hash
    api_hash_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_HASH`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text

    # 
    success = await bot.send_message(
        chat_id=msg.chat.id,
        text="Trying to login...\n\nPlease wait 🍟"
    )
    await asyncio.sleep(1)
    try:
        lazydeveloperrsession = TelegramClient(StringSession(lazydeveloper_string_session), api_id, api_hash)
        await lazydeveloperrsession.start()

        # for any query msg me on telegram - @LazyDeveloperr 👍
        if lazydeveloperrsession.is_connected():
            await db.set_session(user_id, lazydeveloper_string_session)
            await db.set_api(user_id, api_id)
            await db.set_hash(user_id, api_hash)
            await bot.send_message(
                chat_id=msg.chat.id,
                text="Session started successfully! ✅ Use /rename to proceed and enjoy renaming journey 👍."
            )
            print(f"Session started successfully for user {user_id} ✅")
        else:
            raise RuntimeError("Session could not be started. Please re-check your provided credentials. 👍")
    except Exception as e:
        print(f"Error starting session for user {user_id}: {e}")
        await msg.reply("Failed to start session. Please re-check your provided credentials. 👍")
    finally:
        await success.delete()
        await lazydeveloperrsession.disconnect()
        if not lazydeveloperrsession.is_connected():
            print("Session is disconnected successfully!")
        else:
            print("Session is still connected.")
        await init.edit_text("with ❤ @---", parse_mode=enums.ParseMode.HTML)
        return

@Client.on_message(filters.private & filters.command("get_session"))
async def getsession(client , message):
    user_id = message.from_user.id
    session = await db.get_session(user_id)
    if not session:
        await client.send_message(chat_id=user_id, text=f"😕NO session found !\n\nHere are some tools that you can use...\n\n|=> /generate - to gen session\n|=> /connect - to connect session\n|=> /rename - to start process", parse_mode=enums.ParseMode.HTML)
        return
    await client.send_message(chat_id=user_id, text=f"Here is your session string...\n\n<spoiler><code>{session}</code></spoiler>\n\n⚠ Please dont share this string to anyone, You may loOSE your account.", parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("login"))
async def generate_session(bot, msg):
    lazyid = msg.from_user.id

    if not await verify_user(lazyid):
        return await msg.reply("⛔ You are not authorized to use this bot.")
    

    init = await msg.reply(
        "sᴛᴀʀᴛɪɴG [ᴛᴇʟᴇᴛʜᴏɴ] sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛɪᴏɴ..."
    )
    user_id = msg.chat.id
    api_id_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_ID`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply(
            "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ API_ID (ᴡʜɪᴄʜ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ). ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    api_hash_msg = await bot.ask(
        user_id, "ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `API_HASH`", filters=filters.text
    )
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(
        user_id,
        "ɴᴏᴡ ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ `ᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ` ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ. \nᴇxᴀᴍᴘʟᴇ : `+19876543210`",
        filters=filters.text,
    )
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("sᴇɴᴅɪɴɢ ᴏᴛᴘ...")
    
    client = TelegramClient(StringSession(), api_id, api_hash)

    await client.connect()
    try:
        code = await client.send_code_request(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply(
            "`API_ID` ᴀɴᴅ `API_HASH` ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply(
            "`PHONE_NUMBER` ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    try:
        phone_code_msg = await bot.ask(
            user_id,
            "ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ꜰᴏʀ ᴀɴ ᴏᴛᴘ ɪɴ ᴏꜰꜰɪᴄɪᴀʟ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ. ɪꜰ ʏᴏᴜ ɢᴏᴛ ɪᴛ, sᴇɴᴅ ᴏᴛᴘ ʜᴇʀᴇ ᴀꜰᴛᴇʀ ʀᴇᴀᴅɪɴɢ ᴛʜᴇ ʙᴇʟᴏᴡ ꜰᴏʀᴍᴀᴛ. \nɪꜰ ᴏᴛᴘ ɪs `12345`, **ᴘʟᴇᴀsᴇ sᴇɴᴅ ɪᴛ ᴀs** `1 2 3 4 5`.",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply(
            "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 10 ᴍɪɴᴜᴛᴇs. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        await client.sign_in(phone_number, phone_code, password=None)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply(
            "ᴏᴛᴘ ɪs ɪɴᴠᴀʟɪᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply(
            "ᴏᴛᴘ ɪs ᴇxᴘɪʀᴇᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(
                user_id,
                "ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ʜᴀs ᴇɴᴀʙʟᴇᴅ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴘᴀssᴡᴏʀᴅ.",
                filters=filters.text,
                timeout=300,
            )
        except TimeoutError:
            await msg.reply(
                "ᴛɪᴍᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ ᴏꜰ 5 ᴍɪɴᴜᴛᴇs. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return
        try:
            password = two_step_msg.text
            
            await client.sign_in(password=password)
            
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply(
                "ɪɴᴠᴀʟɪᴅ ᴘᴀssᴡᴏʀᴅ ᴘʀᴏᴠɪᴅᴇᴅ. ᴘʟᴇᴀsᴇ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ sᴇssɪᴏɴ ᴀɢᴀɪɴ.",
                quote=True,
                reply_markup=InlineKeyboardMarkup(Data.generate_button),
            )
            return

    string_session = client.session.save()
    await db.set_session(lazyid, string_session)
    await db.set_api(lazyid, api_id)
    await db.set_hash(lazyid, api_hash)
    
    text = f"**ᴛᴇʟᴇᴛʜᴏɴ sᴛʀɪɴɢ sᴇssɪᴏɴ** \n\n||`{string_session}`||"

    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    success = await phone_code_msg.reply(
        "Session generated ! Trying to login 👍"
    )
    # Save session to the dictionary
    await asyncio.sleep(1)
    try:
        sessionstring = await db.get_session(lazyid)
        apiid = await db.get_api(lazyid)
        apihash = await db.get_hash(lazyid)

        lazydeveloperrsession = TelegramClient(StringSession(sessionstring), apiid, apihash)
        await lazydeveloperrsession.start()

        # for any query msg me on telegram - @LazyDeveloperr 👍
        if lazydeveloperrsession.is_connected():
            await bot.send_message(
                chat_id=msg.chat.id,
                text="Session started successfully! ✅ Use /rename to proceed and enjoy renaming journey 👍."
            )
            print(f"Session started successfully for user {user_id} ✅")
        else:
            raise RuntimeError("Session could not be started.")
    except Exception as e:
        print(f"Error starting session for user {user_id}: {e}")
        await msg.reply("Failed to start session. Please try again.")
    finally:
        await success.delete()
        await lazydeveloperrsession.disconnect()
        if not lazydeveloperrsession.is_connected():
            print("Session is disconnected successfully!")
        else:
            print("Session is still connected.")
        await init.edit_text("with ❤ @---", parse_mode=enums.ParseMode.HTML)
        return

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply(
            "ᴄᴀɴᴄᴇʟ ᴛʜᴇ ᴘʀᴏᴄᴇss!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    
    elif "/restart" in msg.text:
        await msg.reply(
            "ʙᴏᴛ ɪs ʀᴇsᴛᴀʀᴛᴇᴅ!",
            quote=True,
            reply_markup=InlineKeyboardMarkup(Data.generate_button),
        )
        return True
    
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("ᴄᴀɴᴄᴇʟʟᴇᴅ ᴛʜᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ ᴘʀᴏᴄᴇss!", quote=True)
        return True
    else:
        return False

lock = asyncio.Lock()

@Client.on_message(filters.private & filters.command("post"))
async def autoposter(client, message):
    user_id = message.from_user.id

    # Check if the user is allowed to use the bot
    if not await verify_user(user_id):
        return await message.reply("⛔ You are not authorized to use this bot.")
    

    # check running task
    if lock.locked():
        print('Wait until previous process complete.')
        return await message.reply("⚠️ Another process is running. Please wait until previous process complete. ⏳")
    
    # setting up target chat id to take post from - BASE-CHANNEL
    # chat_id = await client.ask(
    #     text="Send Target Channel Id, From Where You Want Posts To Be Forwarded: in `-100XXXX` Format ",
    #     chat_id=message.chat.id
    # )

    target_chat_id = await db.get_lazy_target_chat_id(user_id)
    # print(f'✅Set target chat => {target_chat_id}' )
    
    # try:
    #     chat_info = await client.get_chat(target_chat_id)
    # except Exception as e:
    #     await client.send_message(message.chat.id, f"Something went wrong while accessing chat : {chat_info}")
    #     print(f"Error accessing chat: {e}")

    # await db.set_lazy_target_chat_id(message.from_user.id, target_chat_id)

    # print(f"Starting to forward files from channel {target_chat_id} to All-Channels.")

    sessionstring = await db.get_session(user_id)
    apiid = await db.get_api(user_id)
    apihash = await db.get_hash(user_id)
    # Check if any value is missing
    if not sessionstring or not apiid or not apihash:
        missing_values = []
        if not sessionstring:
            missing_values.append("session string")
        if not apiid:
            missing_values.append("API ID")
        if not apihash:
            missing_values.append("API hash")
        
        missing_fields = ", ".join(missing_values)
        await client.send_message(
            chat_id=msg.chat.id,
            text=f"⛔ Missing required information:<b> {missing_fields}. </b>\n\nPlease ensure you have set up all the required details in the database.",
            parse_mode=enums.ParseMode.HTML
        )
        return  # Exit the function if values are missing
    
    lazy_userbot = TelegramClient(StringSession(sessionstring), apiid, apihash)
    await lazy_userbot.start()

    # Iterating through messages
    MAIN_POST_CHANNEL = target_chat_id  # Replace with your MAIN_POST_CHANNEL ID
    DELAY_BETWEEN_POSTS = 60  # 15 minutes in seconds

    # Fetch all messages from the main channel
    # forwarded_ids = set(await db.get_forwarded_ids(user_id))  # IDs already forwarded
    forwarded_ids = set(await db.get_forwarded_ids(user_id, MAIN_POST_CHANNEL))  # Fetch forwarded IDs for the main post channel
    messages = []

    async for msg in lazy_userbot.iter_messages(MAIN_POST_CHANNEL, reverse=True):
        if msg.id not in forwarded_ids:
            messages.append(msg)

    shuffle(messages)
    total_messages = len(messages)
    print(total_messages)
    in_queue = total_messages
    sent_count = 0

    if not messages:
        return await message.reply("✅ All messages from the main channel have already been forwarded.")
    
    # Initialize per-channel message queues
    channel_queues = {channel_id: messages.copy() for channel_id in CHANNELS}

    channel_progress = await client.send_message(
                user_id,
                lazydeveloper.CHANNEL_PROGRESS.format("⏳", "⏳", "⏳", "⏳")
            )

    post_progress = await client.send_message(
                user_id,
                lazydeveloper.POST_PROGRESS.format(sent_count, total_messages, in_queue, 0)
            )
    
    async with lock:
        try:
            while any(channel_queues.values()):  # Continue until all queues are empty
                in_queue -= 1
                for channel_id in CHANNELS:
                    
                    if not channel_queues[channel_id]:
                        continue  # Skip if the queue for this channel is empty

                    msg = channel_queues[channel_id].pop(0)  # Get the next message for this channel

                    try:
                        
                        # Validate message existence
                        message = await lazy_userbot.get_messages(MAIN_POST_CHANNEL, ids=msg.id)
                        if not message:
                            print(f"❌ Message ID {msg.id} does not exist in channel {MAIN_POST_CHANNEL}")
                            continue

                        # Forward the message to the current channel
                        main_post_link = f"https://t.me/c/{str(MAIN_POST_CHANNEL)[4:]}/{msg.id}"
                        fd = await lazy_userbot.forward_messages(channel_id, msg.id, MAIN_POST_CHANNEL)

                        print(f"✅ Forwarded message ID {msg.id} to channel {channel_id}")
                        fd_final_chat = str(channel_id)[4:]
                        forward_post_link = f"<a href='https://telegram.me/c/{fd_final_chat}/{fd.id}'>ʟɪɴᴋ</a>"
                        await channel_progress.edit_text(
                            lazydeveloper.CHANNEL_PROGRESS.format(channel_id, msg.id, forward_post_link, main_post_link),
                            parse_mode=enums.ParseMode.HTML
                        )

                        # Remove the message from all other channel queues
                        for other_channel in CHANNELS:
                            if other_channel != channel_id and msg in channel_queues[other_channel]:
                                channel_queues[other_channel].remove(msg)

                        # Mark the message as forwarded and update progress
                        forwarded_ids.add(msg.id)
                        await db.add_forwarded_id(user_id, MAIN_POST_CHANNEL, msg.id)
                        sent_count += 1
                        
                        progress_percentage = (sent_count / total_messages) * 100
                        percent = f"{progress_percentage:.2f}"
                        await post_progress.edit_text(
                            lazydeveloper.POST_PROGRESS.format(sent_count, total_messages, in_queue, percent),
                            parse_mode=enums.ParseMode.HTML
                        )

                        await asyncio.sleep(1)  # Short delay for smoother operation
                    except MessageIdInvalidError:
                        await message.reply(f"❌ Message ID {msg.id} is invalid or inaccessible in channel {MAIN_POST_CHANNEL}. Skipping...")
                        
                        # Remove the message from all other channel queues
                        for other_channel in CHANNELS:
                            if other_channel != channel_id and msg in channel_queues[other_channel]:
                                channel_queues[other_channel].remove(msg)
                        forwarded_ids.add(msg.id)
                        await db.add_forwarded_id(user_id, MAIN_POST_CHANNEL, msg.id)
                        sent_count += 1

                        progress_percentage = (sent_count / total_messages) * 100
                        percent = f"{progress_percentage:.2f}"
                        await post_progress.edit_text(
                            lazydeveloper.POST_PROGRESS.format(sent_count, total_messages, in_queue, percent),
                            parse_mode=enums.ParseMode.HTML
                        )

                        await asyncio.sleep(1)
                        continue 
                    except FloodWait as e:
                        print(f"⏳ FloodWait: Sleeping for {e.x} seconds.")
                        await asyncio.sleep(e.x)
                    except Exception as e:
                        print(f"❌ Failed to forward message ID {msg.id} to channel {channel_id}: {e}")
                        await asyncio.sleep(5)
                        continue
                if in_queue > 0:
                    print(f"⏳ Waiting {DELAY_BETWEEN_POSTS} seconds before processing the next batch.")
                    await asyncio.sleep(DELAY_BETWEEN_POSTS)

            await channel_progress.delete()
            await post_progress.delete()
            await message.reply("✅ Unique messages from the main channel have been forwarded to all subchannels.")


        # try:
        #     for msg in messages:
                
        #         try:
        #             in_queue -= 1
        #             # Forward message to all subchannels
        #             for channel_id in CHANNELS:
        #                 try:
        #                     # Custom caption with main channel link
        #                     main_post_link = f"https://t.me/c/{str(MAIN_POST_CHANNEL)[4:]}/{msg.id}"
        #                     # custom_caption = f"\n\n⚡Join: {CHANNEL_LINK1}\n⚡Join: {CHANNEL_LINK2}\n🔗 [Source Post]({main_post_link})"
                            
        #                     fd = await lazy_userbot.forward_messages(channel_id, msg.id, MAIN_POST_CHANNEL)

        #                     print(f"✅ Forwarded message ID {msg.id} to channel {channel_id}")
        #                     fd_final_chat = str(channel_id)[4:]
        #                     forward_post_link = f"<a href='https://telegram.me/c/{fd_final_chat}/{fd.id}'>ʟɪɴᴋ</a>"
        #                     await channel_progress.edit_text(lazydeveloper.CHANNEL_PROGRESS.format(channel_id, msg.id, forward_post_link, main_post_link), parse_mode=enums.ParseMode.HTML)
        #                     await asyncio.sleep(1)  # Short delay between subchannels
        #                 except FloodWait as e:
        #                     print(f"⏳ FloodWait: Sleeping for {e.x} seconds.")
        #                     await asyncio.sleep(e.x)
        #                 except Exception as e:
        #                     print(f"❌ Failed to forward message ID {msg.id} to channel {channel_id}: {e}")

        #             # Mark message as forwarded
        #             forwarded_ids.add(msg.id)
        #             await db.add_forwarded_id(user_id, msg.id)
        #             sent_count += 1
        #             progress_percentage = (sent_count/total_messages) * 100
        #             percent = f"{progress_percentage:.2f}"
        #             await post_progress.edit_text(lazydeveloper.POST_PROGRESS.format(sent_count, total_messages, in_queue, percent), parse_mode=enums.ParseMode.HTML)

        #             if in_queue > 0:
        #                 print(f"⏳ Waiting {DELAY_BETWEEN_POSTS} seconds before processing the next post.")
        #                 await asyncio.sleep(DELAY_BETWEEN_POSTS)

        #         except Exception as e:
        #             print(f"❌ Error forwarding message ID {msg.id}: {e}")

        #     await channel_progress.delete()
        #     await post_progress.delete()
        #     await message.reply("✅ Random messages from the main channel have been forwarded to all subchannels.")
        except Exception as e:
            print(e)

    await lazy_userbot.disconnect()

    if not lazy_userbot.is_connected():
        print("Session is disconnected successfully!")
    else:
        print("Session is still connected.")

    # try:
    #     # messages = []
    #     last_message_id = await db.get_skip_msg_id()  # Start fetching from the most recent message
    #     print(f"The last message id got => {last_message_id}")
    #     async with lock:
    #         # running first loop to show realtime update
    #         async for _ in lazy_userbot.iter_messages(MAIN_POST_CHANNEL, offset_id=last_message_id, reverse=True):
    #             total_messages += 1

    #         print(f"Total messages to forward: {total_messages}")
            
    #         if total_messages == 0:
    #             # If no messages to process, inform the user immediately
    #             await message.reply("✅ No new messages to forward.")
    #             return

    #         print(f"Total messages to forward: {total_messages}")
    #         sent_count = 0
    #         in_queue = total_messages

    #         channel_progress = await client.send_message(
    #             user_id,
    #             lazydeveloper.CHANNEL_PROGRESS.format("⏳", "⏳", "⏳", "⏳")
    #         )

    #         post_progress = await client.send_message(
    #             user_id,
    #             lazydeveloper.POST_PROGRESS.format(sent_count, total_messages, in_queue, 0)
    #         )

    #         # Fetch messages in reverse order
    #         async for msg in lazy_userbot.iter_messages(MAIN_POST_CHANNEL, offset_id=last_message_id, reverse=True):
    #             in_queue -= 1
    #             final_chat = str(MAIN_POST_CHANNEL)[4:]
    #             main_post_link = f"<a href='https://telegram.me/c/{final_chat}/{msg.id}'>ʟɪɴᴋ</a>"
    #             print(f"Current Queue => {in_queue}")
    #             channel_caption = f"\n\n⚡Join: {CHANNEL_LINK1}\n⚡Join: {CHANNEL_LINK2}"
    #             for channel_id in CHANNELS:
    #                 try:
    #                     fd = await lazy_userbot.forward_messages(channel_id, msg.id, MAIN_POST_CHANNEL)
    #                     # print('sethod 1 done')
    #                     # try:
    #                     #     if msg.text and not msg.media:
    #                     #         # Send text-only messages
    #                     #         await lazy_userbot.send_message(entity=channel_id, message=msg.text, parse_mode='html')
    #                     #         print('method 2 done')
                                
    #                     #     elif msg.media: 
    #                     #         # Send media with or without captions
    #                     #         await lazy_userbot.send_file(entity=channel_id, file=msg.media, caption=msg.text or "",  parse_mode='html')
    #                     #         print('method 3 done')
    #                     # except Exception as e:
    #                     #     print(f"error =>>>>>>>>> {e}")
    #                     #     pass

    #                     # await client.copy_message(chat_id=channel_id, from_chat_id=MAIN_POST_CHANNEL, message_id=msg.id, parse_mode=enums.ParseMode.HTML)
    #                     fd_final_chat = str(channel_id)[4:]
    #                     forward_post_link = f"<a href='https://telegram.me/c/{fd_final_chat}/{fd.id}'>ʟɪɴᴋ</a>"
    #                     print(f"✅ Forwarded message ID {msg.id} to channel {channel_id} |=> chatid =>{fd_final_chat} |=> fd link {forward_post_link}")

    #                     await channel_progress.edit_text(lazydeveloper.CHANNEL_PROGRESS.format(channel_id, msg.id, forward_post_link, main_post_link), parse_mode=enums.ParseMode.HTML)
    #                     await asyncio.sleep(1)  # Short delay between channels
    #                 except Exception as e:
    #                     print(f"❌ Failed to forward message ID {msg.id} to channel {channel_id}: {e}")

    #             # work after sending message :
    #             await db.set_skip_msg_id(msg.id)
    #             sent_count += 1
    #             progress_percentage = (sent_count/total_messages) * 100
    #             percent = f"{progress_percentage:.2f}"
    #             await post_progress.edit_text(lazydeveloper.POST_PROGRESS.format(sent_count, total_messages, in_queue, percent), parse_mode=enums.ParseMode.HTML)

    #             # Delay before processing the next message
    #             if in_queue > 0:
    #                 print(f"⏳ Waiting {DELAY_BETWEEN_POSTS} seconds before processing the next post.")
    #                 await asyncio.sleep(DELAY_BETWEEN_POSTS)

    #     await channel_progress.delete()
    #     await post_progress.delete()
    #     await message.reply(f"✅ ᴀʟʟ ᴍᴇssᴀɢᴇs ғʀᴏᴍ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ʜᴀᴠᴇ ʙᴇᴇɴ ғᴏʀᴡᴀʀᴅᴇᴅ ᴛᴏ ᴀʟʟ sᴜʙ-ᴄʜᴀɴɴᴇʟs.")

    # except Exception as e:
    #     print(f"❌ Error occurred: {e}")
    #     await message.reply("❌ Failed to process messages.")
    #     #finally disconnect the session to avoid broken pipe error 
    
    # await lazy_userbot.disconnect()

    # if not lazy_userbot.is_connected():
    #     print("Session is disconnected successfully!")
    # else:
    #     print("Session is still connected.")

@Client.on_message(filters.private & filters.command("index_db"))
async def indexdb(client, message):
    # setting up target chat id to take post from - BASE-CHANNEL
    user_id = message.from_user.id
    
    lazyid = message.from_user.id

    if not await verify_user(lazyid):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    chat_id_msg = await client.ask(
        text="Send Index Channel Id, From Where You Want Posts To Be Forwarded: in `-100XXXX` Format",
        chat_id=message.chat.id,
        filters=filters.text
    )

    try:
        target_chat_id = int(chat_id_msg.text)
        await db.set_lazy_target_chat_id(user_id, target_chat_id)
    except ValueError as e:
        await chat_id_msg.reply("Please send valid channel id")
        print(e)
        return

@Client.on_message(filters.private & filters.command("view_db"))
async def viewdb(client, message):
    user_id = message.from_user.id
    lazyid = message.from_user.id

    if not await verify_user(lazyid):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    try:
        id = await db.get_lazy_target_chat_id(user_id)
        await message.reply(f"Here is your current DB-CHANNEL-ID\n├🆔 {id}")
    except Exception as lazyerror:
        print(lazyerror)
        await message.reply("Something went wrong, PLease try again later...")
        return

@Client.on_message(filters.private & filters.command("index_channel"))
async def set_channel(client, message: Message):
    user_id = message.from_user.id
    
    lazyid = message.from_user.id

    if not await verify_user(lazyid):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    # Ask the user for the channel ID
    channel_msg = await client.ask(
        user_id, 
        "📱 Please send the `channel_id` you want to add to list:", 
        filters=filters.text
    )

    # Validate the channel ID
    try:
        channel_id = int(channel_msg.text)
    except ValueError:
        return await channel_msg.reply("❌ Invalid channel ID. Please send a valid Channel ID.")
    
    # Check if the channel ID is already in the user's list
    existing_channel_ids = await db.get_channel_ids(user_id)
    if channel_id in existing_channel_ids:
        return await channel_msg.reply(f"⚠️ Channel ID {channel_id} is already in your list. Please send another ID.")

    # Add the channel ID to the user's list using the existing database method

    await db.add_channel_id(user_id, channel_id)
    
    await channel_msg.reply(f"✅ Channel ID {channel_id} has been added successfully.")

@Client.on_message(filters.private & filters.command("remove_channel"))
async def remove_channel(client, message: Message):
    user_id = message.from_user.id
    lazyid = message.from_user.id

    if not await verify_user(lazyid):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    # Extract the channel_id from the message text
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("⚠️ Usage: `/remove_channel <channel_id>` to remove specific channel from list...\n\n❌ Please provide a `channel_id` to remove.")

    try:
        channel_id = int(parts[1])
    except ValueError:
        return await message.reply("❌ Invalid channel ID. Please provide a valid numeric ID.")

    # Remove the channel ID from the user's list using the existing database method
    await db.remove_channel_id(user_id, channel_id)
    
    await message.reply(f"✅ Channel ID {channel_id} has been removed successfully.")

@Client.on_message(filters.private & filters.command("view_channel_list"))
async def list_channels(client, message: Message):
    user_id = message.from_user.id
    lazyid = message.from_user.id

    if not await verify_user(lazyid):
        return await message.reply("⛔ You are not authorized to use this bot.")
    
    # Get the list of channel IDs from the database
    channel_ids = await db.get_channel_ids(user_id)

    if not channel_ids:
        return await message.reply("❌ You don't have any channel IDs saved yet.")

    # Format the list of channel IDs and send it to the user
    channel_list = "\n├🆔".join([str(channel_id) for channel_id in channel_ids])
    await message.reply(f"Your saved channel IDs:\n<code>{channel_list}</code>", parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("clean_forward_ids"))
async def clean_forward_ids(client, message):
    user_id = message.from_user.id
    # Verify user authorization
    if not await verify_user(user_id):
        return await message.reply("⛔ You are not authorized to use this bot.")

    args = message.text.split()
    if len(args) < 2:
        return await message.reply(
            "⚠️ Usage: `/clean_forward_ids <channel_id>` to clean specific channel, or `/clean_forward_ids all` to clean all channels.",
            parse_mode=enums.ParseMode.MARKDOWN
        )

    # Parse the channel_id or 'all'
    target = args[1]
    try:
        if target.lower() == 'all':
            await db.clean_forwarded_ids(user_id)
            return await message.reply("✅ All forwarded IDs for all channels have been cleared.")
        else:
            channel_id = int(target)
            await db.clean_forwarded_ids(user_id, channel_id)
            return await message.reply(f"✅ Forwarded IDs for channel `{channel_id}` have been cleared.")
    except Exception as e:
        print(f"❌ Error cleaning forwarded IDs: {e}")
        return await message.reply(f"❌ Failed to clean forwarded IDs: {e}")

async def verify_user(user_id: int):
    return user_id in ADMIN


