from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
import uvicorn
import json
from datetime import time, datetime, timedelta, date


def starttime_from_cronstring(cronstring):
    tokens = cronstring.split(' ')
    minutes = list(map(int, tokens[0].split(',')))
    hours = list(map(int, tokens[1].split(',')))
    # CAVEAT: Says it uses cron strings, but actually uses only one hour and minute from cron string. <>
    hour = hours[0]
    minute = minutes[0]
    starttime = f'{hour:02d}:{minute:02d}:00'
    return time.fromisoformat(starttime)


def load_timeframes():
    global timeframes
    with open('timeframes.json', 'r') as timeframes_file:
        timeframes = json.load(timeframes_file)
    for frame in timeframes:
        # CAVEAT: Says it uses cron strings, but can't go with wildcard for day of month. <>
        frame['days'] = list(map(int, frame['cron-start'].split(' ')[2].split(',')))
        frame['duration'] = timedelta(minutes=int(frame['duration']))


def is_in_frame(time, frame, day_offset=0):
    # CAVEAT: Says it uses cron strings, but actually ignores month and day of week. <>
    start = datetime.combine(date=date.today() - timedelta(days=day_offset), time=starttime_from_cronstring(frame['cron-start']))
    if start.day not in frame['days']:
        return False
    end = start + frame['duration']
    print(end)
    return time >= start and time <= end


def is_in_frame_of_yesterday(time, frame):
    return is_in_frame(time, frame, day_offset=1)


def is_in_any_frame(time):
    for frame in timeframes:
        if is_in_frame(time, frame):
            print(f'(Current) time {time} s in frame {frame}')
            return True
        if is_in_frame_of_yesterday(time, frame):
            print(f'(Current) time {time} s in frame of yesterday {frame}')
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
