#
# Copyright (C) 2024 by MISH0009@Github, < https://github.com/MISH0009 >.
#
# This file is part of < https://github.com/MISH0009/DNS > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/MISH0009/DNS/blob/master/LICENSE >
#
# All rights reserved.
#

import sys
import uvloop
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
)

# uvloop installation (Windows compatibility check)
try:
    uvloop.install()
except Exception:
    pass

import config
from ..logging import LOGGER


class DnsBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            "DnsXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
        )

    async def start(self):
        await super().start()
        
        # Identity Information
        self.username = self.me.username
        self.id = self.me.id
        self.name = f"{self.me.first_name} {self.me.last_name or ''}".strip()
        self.mention = self.me.mention

        # Log Group Notification
        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                text=f"<u><b>{self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except Exception as e:
            LOGGER(__name__).error(
                "Bot has failed to access the log Group. Make sure that you have added your bot to your log channel and promoted as admin!"
            )
            # sys.exit() # Optional: keeps bot running even if log fails

        # Set Bot Commands
        if config.SET_CMDS:
            try:
                # Private Chats Commands
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
                        BotCommand("help", "ɢᴇᴛ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇɴᴜ"),
                        BotCommand("ping", "ᴄʜᴇᴄᴋ ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                # Group Chats Commands
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "sᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ʀᴇǫᴜᴇᴛᴇᴅ sᴏɴɢ"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                # Admin Commands
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "sᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ʀᴇǫᴜᴇᴛᴇᴅ sᴏɴɢ"),
                        BotCommand("skip", "ᴍᴏᴠᴇ ᴛᴏ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ"),
                        BotCommand("pause", "ᴘʟᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ sᴏɴɢ"),
                        BotCommand("resume", "ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴘᴀᴜsᴇᴅ sᴏɴɢ"),
                        BotCommand("end", "ᴄʟᴇᴀʀ ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ʟᴇᴀᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛ"),
                        BotCommand("shuffle", "Rᴀɴᴅᴏᴍʟʏ sʜᴜғғʟᴇs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴘʟᴀʏʟɪsᴛ."),
                        BotCommand("playmode", "Aʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ ᴅᴇғᴀᴜʟᴛ ᴘʟᴀʏᴍᴏᴅᴇ"),
                        BotCommand("settings", "Oᴘᴇɴ ᴛʜᴇ sᴇᴛᴛɪɴɢs ᴏғ ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ."),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except Exception as e:
                LOGGER(__name__).warning(f"Could not set commands: {e}")

        # Check Admin Permissions in Log Group
        try:
            member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote Bot as Admin in Logger Group")
                sys.exit()
        except Exception:
            pass

        LOGGER(__name__).info(f"MusicBot Started as {self.name}")

    async def stop(self):
        await super().stop()
        LOGGER(__name__).info("Bot Stopped.")
