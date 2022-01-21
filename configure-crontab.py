import json
from pathlib import Path


with open('timeframes.json', 'r') as timeframes_file:
    timeframes = json.load(timeframes_file)
pwd = str(Path('.').resolve())
with open('powercontrol-server-crontab', mode='w') as cronfile:
    for frame in timeframes:
        if 'default-mac' in frame:
            DEFAULT_MAC = frame['default-mac']
            continue

        cronfile.write(f'{frame["cron-start"]} root {pwd}/wake.sh {frame["client-mac"]}\n')
