import os
import asyncio
import requests

from dotenv import load_dotenv
from datetime import datetime
from edspy import edspy

load_dotenv()

EMBED_COLOR = 0x2e115b
BASE_URL = 'https://edstem.org/us'
USER_ICON = 'https://raw.githubusercontent.com/bachtran02/ed-discohook/main/assets/user.png'
ED_ICON = 'https://raw.githubusercontent.com/bachtran02/ed-discohook/main/assets/ed.png'

COURSE_IDS = {
    42930: os.getenv('CS61A_WEBHOOK'),
    43134: os.getenv('CS70_WEBHOOK'),
    44018: os.getenv('DATA8_WEBHOOK'), 
    22867: os.getenv('OTHERS_WEBHOOK'), 
    23247: os.getenv('OTHERS_WEBHOOK'), 
}

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
                'icon_url': USER_ICON,
            },
            'timestamp': f'{datetime.utcnow().isoformat()[:-3]}Z'
        }]

        res = requests.post(
            url=COURSE_IDS[course.id],
            json={'username': 'Ed', 'avatar_url': ED_ICON,'embeds': embeds})

async def main():
    
    client = edspy.EdClient()
    client.add_event_hooks(EventHandler())
    await client.subscribe(list(COURSE_IDS.keys()))

if __name__ == '__main__':
    asyncio.run(main())