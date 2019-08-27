import os


def record_execution():
    fields = {'runtime': (datetime.datetime.now() - start_time).total_seconds()}
    write_measurement('runtime', fields)

def end_profile():
    pr.disable()
    filename = os.path.join(tempfile.gettempdir(), "{ppid}_{pid}_{cmd}.dmp".format(ppid=ppid,pid=pid,cmd=os.path.basename(sys.argv[0])))

    fields = {'profile': filename}
    write_measurement('profile', fields)
    pr.dump_stats(filename)

def write_measurement(measurement, fields):
    import influxdb
    client = influxdb.InfluxDBClient()
    client.switch_database('ProfAll')
    tags = {'args': (' '.join(sys.argv)), 'interpretter': sys.executable,
            'version': '.'.join(str(x) for x in sys.version_info), 'pid': pid, 'ppid': ppid}
    if not client.write_points(
            [{'measurement': measurement, 'tags': tags,
              'fields': fields}]):
        sys.stderr.write('Write to influxdb failed.')
    client.close()

mode = os.environ.get('PROFALL', '')
if mode != 'OFF':
    import atexit
    import datetime
    import sys

    pid = os.getpid()
    ppid = os.getppid()
    start_time = datetime.datetime.now()
    atexit.register(record_execution)

if mode == 'PROFILE':
    import cProfile
    import tempfile

    pr = cProfile.Profile()
    pr.enable()

    atexit.register(end_profile)

if __name__ == '__main__':
    record_execution()
