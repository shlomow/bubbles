import bubbles
import bubbles.utils as utils
import datetime as dt

def upload_thought(address, user_id, thought):
    conn = utils.Connection.connect(address[0], address[1])
    thought = bubbles.Thought(user_id, dt.datetime.now(), thought)
    conn.send(thought.serialize())
