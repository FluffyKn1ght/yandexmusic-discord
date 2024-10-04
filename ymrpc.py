import discordrp
import time
import asyncio

client_id = "YOUR-CLIENT-ID" # https://discord.com/developers / SEE README.md
interval = 10 # Как часто обновлять статус / How often to update the presence

from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def get_media_info():
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:
        if current_session.source_app_user_model_id == "ru.yandex.desktop.music":
            info = await current_session.try_get_media_properties_async()

            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

            info_dict['genres'] = list(info_dict['genres'])

            return info_dict


async def main():
    start_time = int(time.time())
    
    with discordrp.Presence(client_id) as presence:
        while True:
            current_media_info = await get_media_info()
            print(current_media_info)
            
            if current_media_info:
                presence.set(
                    {
                        "name": "name", # 1
                        "details": current_media_info["title"], # 2
                        "state": current_media_info["artist"], # 3
                        "timestamps": {"start": start_time}, # 4
                        "type": 2,
                        
                    }
                )
            else:
                presence.clear()
            
            time.sleep(interval)
            
asyncio.run(main())