#!/usr/bin/python3
"""
cards server
"""
import logging
import sys
print(sys.version)
from config import Config

class ContextFilter(logging.Filter):
    def filter(self, record):
        if 'GET /socket.io/?EIO' in str(record) or 'POST /socket.io/?EIO' in str(record): return False
        else: return True


if __name__ == "__main__":
    from app import app
    from app.logconfig import handler
    logmehere = logging.getLogger('werkzeug')
    logmehere.addFilter(ContextFilter())
    logmehere.addHandler(handler)
    
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    app.logger.error('bollocks')
    app.debug = True
    extra = ['templates']
    import os
    for f in os.listdir('.'):
        extra += [f] 
    app.run(host='0.0.0.0', port=Config.PORT, threaded=True, extra_files=extra, use_reloader=False)
