from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
import uvicorn
import json
from datetime import time, datetime, timedelta, date


DEFAULT_MAC = None


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
    global DEFAULT_MAC

    with open('timeframes.json', 'r') as timeframes_file:
        timeframes = json.load(timeframes_file)
    for frame in timeframes:
        if 'default-mac' in frame:
            DEFAULT_MAC = frame['default-mac']
            continue

        day_of_month_field = frame['cron-start'].split(' ')[2]
        if day_of_month_field == '*':
            frame['days'] = list(range(1, 31+1))
        else:
            frame['days'] = list(map(int, day_of_month_field.split(',')))
        day_of_week_field = frame['cron-start'].split(' ')[4]
        
        if day_of_week_field == '*':
            frame['weekdays'] = list(range(0, 6+1))
        else:
            weekday_encoding = {
                                'MON': 0,
                                'TUE': 1,
                                'WED': 2,
                                'THU': 3,
                                'FRI': 4,
                                'SAT': 5,
                                'SUN': 6
                                }
            frame['weekdays'] = list(map(lambda weekday_name: weekday_encoding[weekday_name] , day_of_week_field.split(',')))
        
        frame['duration'] = timedelta(minutes=int(frame['duration']))


def is_in_frame(time, frame, day_offset=0):
    # CAVEAT: Says it uses cron strings, but actually ignores month. <>
    start = datetime.combine(date=date.today() - timedelta(days=day_offset), time=starttime_from_cronstring(frame['cron-start']))
    # CAVEAT: Combination of day of month and day of week is a bit tricky and may not work as usual cron implementations do. <>
    if start.weekday() not in frame['weekdays']:
        return False
    if start.day not in frame['days']:
        return False
    end = start + frame['duration']
    # print(end)
    return time >= start and time <= end


def is_in_frame_of_yesterday(time, frame):
    return is_in_frame(time, frame, day_offset=1)


def has_correct_mac(frame, client_mac):
    client_mac = client_mac.replace('-', ':')
    return frame['client_mac'] == client_mac


def is_in_any_frame(time, **kwargs):
    client_mac = kwargs.pop('client_mac')

    for frame in timeframes:
        if not has_correct_mac(frame, client_mac):
            continue

        if is_in_frame(time, frame):
            # print(f'(Current) time {time} s in frame {frame}')
            return True
        if is_in_frame_of_yesterday(time, frame):
            # print(f'(Current) time {time} s in frame of yesterday {frame}')
            return True
    return False


def is_in_any_frame_now(**kwargs):
    return is_in_any_frame(datetime.now(), **kwargs)


app = Starlette(on_startup=[load_timeframes])


def get_shutdowntimestatus(client_mac=None):
    client_mac = client_mac if client_mac else DEFAULT_MAC

    return PlainTextResponse(f'{is_in_any_frame_now(client_mac)}')


@app.route('/client_mac/{client_mac:str}')
def request_shutdowntimestatus(request):
    return get_shutdowntimestatus(request.path_params.get('client_mac'))


@app.route('/')
def request_shutdowntimestatus_old_wo_mac(request):
    return get_shutdowntimestatus()


if __name__ == '__main__':
    uvicorn.run('powercontrol_server:app', host='0.0.0.0', port=8000, reload=True)
