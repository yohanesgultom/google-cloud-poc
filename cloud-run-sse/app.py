import flask
import queue
import time
import threading

class MessageAnnouncer:
    """
    Hold messages in queue to improve reliability
    In flask-sse (other module), this task is delegated to Redis
    """

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def format_sse(self, data: dict, event: str = None) -> str:        
        msg = f'data: {data}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
        return msg

    def announce(self, data: dict, event: str = None):
        """
        The event parameter is optional, it allows defining topics to which clients can subscribe to. 
        This avoids having to define one message queue for each topic.
        """
        msg = self.format_sse(data, event=event)
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

def long_backend_process(announcer: MessageAnnouncer, t: int = 60):
    """
    Long process emulator
    """
    delay = t/100
    for i in range(100):
        announcer.announce({'progress': i+1})
        time.sleep(delay)

app = flask.Flask(__name__)
announcer = MessageAnnouncer()

@app.route('/')
def index():
    return flask.render_template('client.html')

@app.route('/ping')
def ping():
    """
    Manually trigger a message push
    """
    announcer.announce({'message': 'pong'})
    return {}, 200

@app.route('/start')
def start():
    """
    Start long backend process
    """
    threading.Thread(target=long_backend_process, args=(announcer, 60,)).start()
    return {}, 200

@app.route('/listen', methods=['GET'])
def listen():
    """
    Blocking api that listens to the message push
    will be used inside the SSE client like EventSource (in javascript)
    """
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg
    return flask.Response(stream(), mimetype='text/event-stream')
