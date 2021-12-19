import json


with open('timeframes.json', 'r') as timeframes_file:
    timeframes = json.load(timeframes_file)
with open('/etc/cron.d/pwrctrl-srv', mode='w') as cronfile:
    for frame in timeframes:
        cronfile.write(f'{frame["cron-start"]} etherwake {frame["client-mac"]}\n')
