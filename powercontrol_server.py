from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
import uvicorn
import json
from datetime import time, datetime


def load_timeframes():
    global timeframes
    with open('timeframes.json', 'r') as timeframes_file:
        timeframes = json.load(timeframes_file)
    for frame in timeframes:
        frame['start'] = time.fromisoformat(frame['start'])
        frame['end'] = time.fromisoformat(frame['end'])


def is_in_frame(time, frame):
    time = time.time()
    return time >= frame['start'] and time <= frame['end']


def is_in_any_frame(time):
    for frame in timeframes:
        if is_in_frame(time, frame):
            return True
    return False


def in_any_frame_now():
    return is_in_any_frame(datetime.now())


app = Starlette(on_startup=[load_timeframes])


@app.route('/')
def get_shutdowntimestatus(request):
    return PlainTextResponse(f'{in_any_frame_now()}')


if __name__ == '__main__':
    uvicorn.run('powercontrol_server:app', host='0.0.0.0', port=8000, reload=True)
