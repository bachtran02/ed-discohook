import os
import asyncio
import requests

from dotenv import load_dotenv
from datetime import datetime
from edspy import edspy

load_dotenv()

EMBED_COLOR = 0x2e115b
BASE_URL = 'https://edstem.org/us'
ICON_URL = 'https://raw.githubusercontent.com/bachtran02/ed-discohook/main/assets/icon.jpg'

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
            'color': EMBED_COLOR,
            'author': {
                'name': '{} • {}'.format(course.code, thread.category),
                'url': BASE_URL + '/courses/{}/discussion'.format(thread.course_id)},
            'footer': {
                'text': user,
                'icon_url': ICON_URL,
            },
            'timestamp': f'{datetime.utcnow().isoformat()[:-3]}Z'
        }]

        res = requests.post(
            url=os.getenv('WEBHOOK_URL'),
            json={'username': 'Ed', 'embeds': embeds})

async def main():
    
    course_ids = [42930, 43134, 44018, 22867, 23247]
    
    client = edspy.EdClient()
    client.add_event_hooks(EventHandler())
    await client.subscribe(course_ids)

if __name__ == '__main__':
    asyncio.run(main())