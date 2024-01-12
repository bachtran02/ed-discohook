from edspy.edspy import ThreadType

BASE_URL = 'https://edstem.org/us'

ED_ICON = 'https://raw.githubusercontent.com/bachtran02/ed-discohook/main/assets/ed.png'
USER_ICON = 'https://raw.githubusercontent.com/bachtran02/ed-discohook/main/assets/user.png'

POST_COLOR          = 0x66a2ff
QUESTION_COLOR      = 0xe06ce0
ANNOUNCEMENT_COLOR  = 0xfffb55
UKNOWN_COLOR        = 0x4dffa6

EMBED_COLORS = {
    ThreadType.POST         : POST_COLOR,
    ThreadType.QUESTION     : QUESTION_COLOR,
    ThreadType.ANNOUNCEMENT : ANNOUNCEMENT_COLOR,
}
