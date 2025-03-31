from prettytable import PrettyTable
import subprocess
import json
from urllib import request
import re
import argparse


def traceroute(address, table):
    tracert = subprocess.Popen(["tracert", address], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    number = 0
    for line in iter(tracert.stdout.readline, ''):
        line = line.decode('cp866')
        ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
        if 'Трассировка маршрута' in line:
            print(line.split(' ')[-2], line.split(' ')[-1])
        elif 'Не удается' in line:
            print(line)
            return
        elif 'Превышен интервал ожидания запроса' in line:
            print('Превышен интервал ожидания запроса')
        elif 'Трассировка завершена' in line:
            print(table)
            return
        elif ip:
            number += 1
            info = json.loads(request.urlopen('https://ipinfo.io/' + ip[0] + '/json').read())
            if 'bogon' in info:
                table.add_row([number, info['ip'], '-', '-', '-'])
            else:
                try:
                    asn = info['org'].split()[0][2::]
                    provider = " ".join(info['org'].split()[1::])
                except KeyError:
                    asn, provider = '-', '-'
                table.add_row([number, info['ip'], asn, info['country'], provider])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("address")
    args = parser.parse_args()
    table = PrettyTable()
    table.field_names = ["№", "IP", "AS", "Country", "Provider"]
    traceroute(args.address, table)
