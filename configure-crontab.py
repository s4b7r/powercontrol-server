import json
from pathlib import Path

from powercontrol_timeframes import is_config_dict


with open('timeframes.json', 'r') as timeframes_file:
    timeframes = json.load(timeframes_file)
pwd = str(Path('.').resolve())
with open('powercontrol-server-crontab', mode='w') as cronfile:
    for frame in filter(lambda x: not is_config_dict(x), timeframes):
        cronfile.write(f'{frame["cron-start"]} root {pwd}/wake.sh {frame["client-mac"]}\n')
