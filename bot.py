from pyrogram import Client 
from config import API_ID, API_HASH, BOT_TOKEN, FORCE_SUB, PORT
from aiohttp import web
from route import web_server
import pyromod.listen
import os

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="postforwarder",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
            max_concurrent_transmissions=100,
        )
    # the one and only - LazyDeveloperr ❤
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username 
        self.force_channel = FORCE_SUB
        if FORCE_SUB:
            try:
                link = await self.export_chat_invite_link(FORCE_SUB)                  
                self.invitelink = link
            except Exception as e:
                print(e)
                print("Make Sure Bot admin in force sub channel")             
                self.force_channel = None
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"       
        await web.TCPSite(app, bind_address, PORT).start()     
        print(f"| ❤ |==> ʟᴀᴢʏᴅᴇᴠᴇʟᴏᴘᴇʀʀ ɪɴɪᴛɪᴀᴛᴇᴅ {me.first_name} <==| 🍿 |")
      

    async def stop(self, *args):
        await super().stop()      
        print("Bot Stopped")
       

bot=Bot()
bot.run()
