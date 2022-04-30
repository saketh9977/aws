import datetime

def get_cur_timestamp_str():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

def print_(data):
    timestamp = get_cur_timestamp_str()
    print(f"{timestamp}: {data}")