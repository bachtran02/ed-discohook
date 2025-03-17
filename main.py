import os
import asyncio
import requests
import logging as log

from dotenv import load_dotenv
from datetime import datetime, timezone
from edpy import edpy

from static import *

# webhook url that can be loaded from .env with same name (see .env.example)
COURSE_IDS = {
    12345: 'CS_XYZ_WEBHOOK',  
    12346: 'DATA_XYZ_WEBHOOK',    
    12347: 'INFO_XYZ_WEBHOOK',
}

class EventHandler:

    def __init__(self, client: edpy.EdClient, webhooks: dict) -> None:
        self.client = client
        self.webhooks = webhooks
        self.courses = None
    
    async def update_courses(self):
        # update user courses cache every hour
        while True:
            self.courses = await self.client.get_courses()
            await asyncio.sleep(3600)
 
    @edpy.listener(edpy.ThreadNewEvent)
    async def on_new_thread(self, event: edpy.ThreadNewEvent):

        thread: edpy.Thread = event.thread

        if thread.is_private == True:
            return
        
        if not self.courses:
            await self.update_courses()
        course = next(filter(lambda x: x.id == thread.course_id, self.courses), None)

        # send payload to Discord
        requests.post(
            url=self.webhooks.get(course.id),
            json={
                'username': 'Ed',
                'avatar_url': ED_ICON,
                'embeds': self.build_embed(thread, course)
            })

    @staticmethod
    def build_embed(thread: edpy.Thread, course: edpy.Course):

        return [{
            'title': '#{} **{}**'.format(thread.number, thread.title),
            'description': thread.document,
            'url': BASE_URL + '/courses/{}/discussion/{}'.format(thread.course_id, thread.id),
            'color': EMBED_COLORS.get(thread.type, UKNOWN_COLOR),
            'author': {
                'name': '{} • {}'.format(course.code, thread.category),
                'url': BASE_URL + '/courses/{}/discussion'.format(thread.course_id)},
            'footer': {
                'text': 'Anonymous User' if thread.is_anonymous else '{} ({})'.format(
                    thread.user.name, thread.user.course_role.capitalize()),
                'icon_url': AVATAR_URL + thread.user.avatar if not thread.is_anonymous and
                    thread.user.avatar else USER_ICON
            },
            'timestamp': f'{datetime.now(timezone.utc).isoformat()[:-9]}Z'
        }]

async def main():
    load_dotenv()

    webhook_urls = {course_id: os.getenv(webhook) for 
        course_id, webhook in COURSE_IDS.items()}

    client = edpy.EdClient()
    handler = EventHandler(client=client, webhooks=webhook_urls)
    client.add_event_hooks(handler)
    
    await asyncio.gather(
        handler.update_courses(),
        client.subscribe(list(webhook_urls.keys())))

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    asyncio.run(main())