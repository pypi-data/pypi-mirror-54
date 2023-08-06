import pendulum
import yaml

def get_time():
    now = pendulum.now('Europe/Paris')
    print('Time now in paris is ' + now.to_datetime_string())

def read_config(file):
    with open(file) as f:
        data = yaml.full_load(f)
    return data
