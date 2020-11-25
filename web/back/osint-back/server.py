from gevent.pywsgi import WSGIServer
from api import app  # if yourapplication imports from views,
                                 # the sort would happen once; here.
app.debug = True
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()