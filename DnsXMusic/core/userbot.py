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
from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.clients = []
        # Config se saari session strings ek list mein daal rahe hain
        self.sessions = [
            config.STRING1, 
            config.STRING2, 
            config.STRING3, 
            config.STRING4, 
            config.STRING5
        ]

    async def start(self):
        LOGGER(__name__).info("Starting Assistant Clients...")
        
        for i, session in enumerate(self.sessions, start=1):
            if not session:
                continue

            client = Client(
                name=f"DnsAssistant{i}",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                in_memory=True,
                session_string=str(session),
            )
            
            try:
                await client.start()
                
                # Ek hi baar join kafi hai
                try:
                    await client.join_chat("DNS_NETWORK")
                except:
                    pass

                # Identity fetch karna
                get_me = await client.get_me()
                client.username = get_me.username
                client.id = get_me.id
                client.mention = get_me.mention
                client.name = f"{get_me.first_name} {get_me.last_name or ''}".strip()
                
                # Lists update karna
                assistants.append(i)
                assistantids.append(get_me.id)
                
                # Assistant ko class attribute mein save karna (self.one, self.two...)
                setattr(self, ["one", "two", "three", "four", "five"][i-1], client)
                self.clients.append(client)

                # Log Group mein message bhejna
                try:
                    await client.send_message(config.LOG_GROUP_ID, f"Assistant {i} Started")
                except Exception:
                    LOGGER(__name__).error(
                        f"Assistant {i} failed to access Log Group. Promote as admin!"
                    )

                LOGGER(__name__).info(f"Assistant {i} Started as {client.name}")

            except Exception as e:
                LOGGER(__name__).error(f"Assistant {i} failed to start: {str(e)}")
                # Agar aap chahte hain ki koi ek string fail hone pe bot ruk jaye toh niche wali line uncomment karein
                # sys.exit()

    async def stop(self):
        for client in self.clients:
            try:
                await client.stop()
            except:
                pass
        LOGGER(__name__).info("All Assistants Stopped.")
