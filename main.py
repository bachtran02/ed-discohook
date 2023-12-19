import os
import asyncio
import requests

from dotenv import load_dotenv
from datetime import datetime
from edspy import edspy

from static import *

BASE_URL = 'https://edstem.org/us'

course_ids = dict()

class EventHandler:
 
    @edspy.listener(edspy.ThreadNewEvent)
    async def on_thread_create(self, event: edspy.ThreadNewEvent):

        thread, course = event.thread, event.course

        user = 'Anonymous User' if thread.is_anonymous else '{} ({})'.format(
            thread.user['name'], thread.user['course_role'].capitalize())
        
        embeds = [{
            'title': '#{} **{}**'.format(thread.number, thread.title),
            'description': thread.document,
            'url': BASE_URL + '/courses/{}/discussion/{}'.format(thread.course_id, thread.id),
            'color': EMBED_COLORS.get(thread.type, UKNOWN_EMBED_COLOR),
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
            url=course_ids[course.id],
            json={'username': 'Ed', 'avatar_url': ED_ICON,'embeds': embeds})

async def main():
    load_dotenv()

    for course_id in COURSE_IDS:
        course_ids[course_id] = os.getenv(COURSE_IDS[course_id])

    client = edspy.EdClient()
    client.add_event_hooks(EventHandler())
    await client.subscribe(list(course_ids.keys()))

if __name__ == '__main__':
    edspy.enable_logger()
    asyncio.run(main())