import motor.motor_asyncio
from config import DB_URL, DB_NAME

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user
        self.settings_col = self.db.settings  # New collection for settings like skip_msg_id
        self.forwarded_col = self.db.forwarded_messages  # New collection for forwarded IDs

    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
    
    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)
        
    async def set_forward(self, id, forward):
        print(forward)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'forward_id': forward}})
        print(z)

    async def get_forward(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('forward_id', None)
    

    # session
    async def set_session(self, id, session_string):
        print(session_string)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_session_string': session_string}})
        print(z)

    async def get_session(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_session_string', None)
    
    # api hash
    async def set_hash(self, id, api_hash):
        print(api_hash)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_api_hash': api_hash}})
        print(z)

    async def get_hash(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_api_hash', None)

    
    # api id
    async def set_api(self, id, api_id):
        print(api_id)
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_api_id': api_id}})
        print(z)

    async def get_api(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_api_id', None)
    

    async def get_lazy_target_chat_id(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('lazy_target_chat_id', None)
    
    async def set_lazy_target_chat_id(self, id, target_chat_id):
        z = await self.col.update_one({'_id': int(id)}, {'$set': {'lazy_target_chat_id': target_chat_id}})
        print(z)
    # setting sikp messages for the bot
    async def set_skip_msg_id(self, message_id):
        """
        Save the skip_msg_id in the settings collection.
        If it already exists, update it; otherwise, insert a new entry, codes by lazydeveloperr
        """
        await self.settings_col.update_one(
            {"type": "skip_msg"},
            {"$set": {"type": "skip_msg", "message_id": message_id}},
            upsert=True
        )

    async def get_skip_msg_id(self):
        """
        Retrieve the skip_msg_id from the settings collection.
        Returns 0 if no entry exists. codes by lazydeveloperr
        """
        record = await self.settings_col.find_one({"type": "skip_msg"})
        return record.get("message_id", 0) if record else 0

    # Forwarded IDs management
    # async def get_forwarded_ids(self, user_id: int) -> set:
    #     """
    #     Get the set of forwarded message IDs for a specific user.
    #     """
    #     user_data = await self.forwarded_col.find_one({"user_id": user_id})
    #     if user_data and "forwarded_ids" in user_data:
    #         return set(user_data["forwarded_ids"])
    #     return set()

    # async def add_forwarded_id(self, user_id: int, msg_id: int):
    #     """
    #     Add a forwarded message ID to the database for a specific user.
    #     """
    #     await self.forwarded_col.update_one(
    #         {"user_id": user_id},
    #         {"$addToSet": {"forwarded_ids": msg_id}},  # Use $addToSet to avoid duplicates
    #         upsert=True  # Create the document if it doesn't exist
    #     )
    async def get_forwarded_ids(self, user_id, channel_id):
        """
        Get the list of forwarded IDs for a specific user and channel.
        """
        user = await self.col.find_one({'_id': user_id})
        if not user:
            return set()  # No forwarded messages found

        forwarded = user.get('forwarded_ids', {})
        return set(forwarded.get(str(channel_id), []))  # Return forwarded IDs for the channel

    async def add_forwarded_id(self, user_id, channel_id, msg_id):
        """
        Add a message ID to the list of forwarded IDs for a specific user and channel.
        """
        await self.col.update_one(
            {'_id': user_id},
            {'$addToSet': {f'forwarded_ids.{channel_id}': msg_id}}
        )

    async def clean_forwarded_ids(self, user_id, channel_id=None):
        """
        Remove forwarded IDs for a specific channel or all channels for a user.
        If `channel_id` is None, all forwarded IDs are cleared for the user.
        """
        if channel_id:
            await self.col.update_one(
                {'_id': user_id},
                {'$unset': {f'forwarded_ids.{channel_id}': ""}}
            )
        else:
            await self.col.update_one(
                {'_id': user_id},
                {'$unset': {'forwarded_ids': ""}}
            )


    async def get_channel_ids(self, user_id):
        user = await self.col.find_one({"_id": user_id})
        return user.get("channel_ids", []) if user else []
    
    async def remove_channel_id(self, user_id, channel_id):
        await self.col.update_one(
            {"_id": user_id},
            {"$pull": {"channel_ids": channel_id}}
        )

    async def add_channel_id(self, user_id, channel_id):
        await self.col.update_one(
            {"_id": user_id},
            {"$addToSet": {"channel_ids": channel_id}},
            upsert=True
        )

db = Database(DB_URL, DB_NAME)
