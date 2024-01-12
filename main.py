import os
import asyncio
import requests
import logging

from dotenv import load_dotenv
from datetime import datetime
from edspy import edspy

from static import *

# webhook url that can be loaded from .env with same name (see .env.example)
COURSE_IDS = {
    12345: 'CS_XYZ_WEBHOOK',  
    12346: 'DATA_XYZ_WEBHOOK',    
    12347: 'INFO_XYZ_WEBHOOK',
}

class EventHandler:

    def __init__(self, client: edspy.EdClient, webhooks: dict) -> None:
        self.client = client
        self.webhooks = webhooks
 
    @edspy.listener(edspy.ThreadNewEvent)
    async def on_new_thread(self, event: edspy.ThreadNewEvent):

        thread: edspy.Thread = event.thread
        course: edspy.Course = await self.client.get_course(thread.course_id)

        user = 'Anonymous User' if thread.is_anonymous else '{} ({})'.format(
            thread.user['name'], thread.user['course_role'].capitalize())
        
        embeds = [{
            'title': '#{} **{}**'.format(thread.number, thread.title),
            'description': thread.document,
            'url': BASE_URL + '/courses/{}/discussion/{}'.format(thread.course_id, thread.id),
            'color': EMBED_COLORS.get(thread.type, UKNOWN_COLOR),
            'author': {
                'name': '{} • {}'.format(course.code, thread.category),
                'url': BASE_URL + '/courses/{}/discussion'.format(thread.course_id)},
            'footer': {
                'text': user,
                'icon_url': USER_ICON,
            },
            'timestamp': f'{datetime.utcnow().isoformat()[:-3]}Z'
        }]

        res = requests.post(
            url=self.webhooks.get(course.id),
            json={'username': 'Ed', 'avatar_url': ED_ICON,'embeds': embeds})

async def main():
    load_dotenv()

    webhook_urls = dict()
    for course_id in COURSE_IDS:
        webhook_urls[course_id] = os.getenv(COURSE_IDS[course_id])

    client = edspy.EdClient()
    client.add_event_hooks(EventHandler(client=client, webhooks=webhook_urls))
    await client.subscribe(list(webhook_urls.keys()))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())