"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, sys, time

from django.core.wsgi import get_wsgi_application
from .settings import DATABASES

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()




def typewriter(say, message_speed = 0.03, new_line_delay_time = 1):
    for character in say:
        sys.stdout.write(character)
        sys.stdout.flush()
        
        if character != "\n":
            time.sleep(message_speed)
        else:
            time.sleep(new_line_delay_time)


print("""
# ================================================
#     Created by Ridwan Renaldi, S.Kom. (rr867)
# ================================================
""")

db = DATABASES['default']
txt = '====================[DATABASE]====================\n'
txt += '• ENGINE \t: ' + str(db['ENGINE']) + '\n'
txt += '• NAME \t\t: ' + str(db['NAME']) + '\n'
txt += '• USER \t\t: ' + str(db['USER']) + '\n'
txt += '• PASSWORD \t: ' + str(db['PASSWORD']) + '\n'
txt += '• HOST \t\t: ' + str(db['HOST']) + '\n'
txt += '• PORT \t\t: ' + str(db['PORT']) + '\n'
txt += '• ENGINE \t: ' + str(db['ENGINE']) + '\n'
txt += '==================================================\n'

print(txt)
typewriter("Start Application...\n")







