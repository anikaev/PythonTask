#!/usr/bin/env python3
import sys
import re
import unittest
from unittest.mock import mock_open, patch


class LogAnalyzer:
    LOG_PATTERN = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s- - \[(?P<datetime>[^\]]+)\]\s'
        r'"(?P<request>[^"]+)"\s(?P<status>\d{3})\s(?P<size>\d+)\s'
        r'"(?P<referrer>[^"]*)"\s"(?P<user_agent>[^"]*)"\s?'
        r'(?P<processing_time>\d+)?'
    )

    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.parse_logfile()

    def parse_logfile(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file:
                match = self.LOG_PATTERN.match(line.strip())
                if match:
                    request = match.group('request')
                    parts = request.split()
                    if len(parts) >= 2:
                        resource = parts[1]
                        processing_time = match.group('processing_time')
                        processing_time = (int(processing_time)
                                           if processing_time else 0)
                        datetime = match.group('datetime')
                        user_agent = match.group('user_agent')
                        self.data.append({
                            'ip': match.group('ip'),
                            'resource': resource,
                            'processing_time': processing_time,
                            'datetime': datetime,
                            'user_agent': user_agent
                        })

    def get_popular_resource(self):
        stats = {}
        for row in self.data:
            resource = row['resource']
            stats[resource] = stats.get(resource, 0) + 1
        if not stats:
            return None, 0
        max_count = max(stats.values())
        popular_resources = [k for k, v in stats.items() if v == max_count]
        popular = min(popular_resources)
        return popular, max_count

    def get_active_client(self):
        stats = {}
        for row in self.data:
            ip = row['ip']
            stats[ip] = stats.get(ip, 0) + 1
        if not stats:
            return None, 0
        max_count = max(stats.values())
        active_clients = [k for k, v in stats.items() if v == max_count]
        active = min(active_clients)
        return active, max_count

    def get_popular_browser(self):
        stats = {}
        for row in self.data:
            browser = row['user_agent']
            stats[browser] = stats.get(browser, 0) + 1
        if not stats:
            return None, 0
        max_count = max(stats.values())
        popular_browsers = [k for k, v in stats.items() if v == max_count]
        popular = min(popular_browsers)
        return popular, max_count

    def get_slowest_page(self):
        max_time = -1
        slowest = None
        for row in self.data:
            if row['processing_time'] >= max_time:
                max_time = row['processing_time']
                slowest = row['resource']
        return slowest, max_time if max_time != -1 else None

    def get_fast_page(self):
        min_time = float('inf')
        fastest = None
        for row in self.data:
            if 0 < row['processing_time'] <= min_time:
                min_time = row['processing_time']
                fastest = row['resource']
        return fastest, min_time if min_time != float('inf') else None

    def get_slow_page(self):
        stats = {}
        counts = {}
        for row in self.data:
            resource = row['resource']
            stats[resource] = stats.get(resource, 0) + row['processing_time']
            counts[resource] = counts.get(resource, 0) + 1
        if not stats:
            return None, 0
        avg_stats = {}
        for k in stats:
            avg_stats[k] = stats[k] / counts[k]
        max_avg = max(avg_stats.values())
        slowest_avg_pages = [k for k, v in avg_stats.items() if v == max_avg]
        slowest_avg = slowest_avg_pages[0] if slowest_avg_pages else None
        return slowest_avg, max_avg

    def get_active_clientday(self):
        stats = {}
        for row in self.data:
            datetime = row['datetime']
            day = datetime.split(':')[0]
            ip = row['ip']
            if day not in stats:
                stats[day] = {}
            stats[day][ip] = stats[day].get(ip, 0) + 1
        active_by_day = {}
        for day, clients in stats.items():
            if not clients:
                active_by_day[day] = (None, 0)
                continue
            max_count = max(clients.values())
            active_clients = [k for k, v in clients.items() if v == max_count]
            active = min(active_clients)
            active_by_day[day] = (active, max_count)
        return active_by_day


def make_stat(filename):

    return LogAnalyzer(filename)


class LogStatTests(unittest.TestCase):
    def setUp(self):
        # Пример данных лог-файла
        self.sample_log = (
            '127.0.0.1 - - [10/Oct/2020:13:55:36 -0700] '
            '"GET /home HTTP/1.1" 200 1234 '
            '"http://example.com" "Mozilla/5.0" 150\n'
            '192.168.1.1 - - [10/Oct/2020:14:00:00 -0700]'
            ' "POST /submit HTTP/1.1"'
            ' 200 567 "http://example.com/home" "Chrome/90.0" 300\n'
            '127.0.0.1 - - [11/Oct/2020:10:00:00 -0700] '
            '"GET /contact HTTP/1.1" '
            '200 789 "http://example.com" "Mozilla/5.0" 100\n'
            '192.168.1.2 - - [11/Oct/2020:11:00:00 -0700]'
            ' "GET /home HTTP/1.1" '
            '200 1234 "http://example.com" "Safari/14.0" 200\n'
            '127.0.0.1 - - [12/Oct/2020:09:00:00 -0700] '
            '"GET /home HTTP/1.1" '
            '200 1234 "http://example.com" "Mozilla/5.0" 250\n'
        )
        self.mock_file = mock_open(read_data=self.sample_log)

    @patch('builtins.open')
    def test_popular_resource(self, mock_open_func):

        mock_open_func.side_effect = self.mock_file
        analyzer = make_stat('dummy.log')
        resource, count = analyzer.get_popular_resource()
        self.assertEqual(resource, '/home')
        self.assertEqual(count, 3)

    @patch('builtins.open')
    def test_active_client(self, mock_open_func):

        mock_open_func.side_effect = self.mock_file
        analyzer = make_stat('dummy.log')
        client, count = analyzer.get_active_client()
        self.assertEqual(client, '127.0.0.1')
        self.assertEqual(count, 3)

    @patch('builtins.open')
    def test_popular_browser(self, mock_open_func):

        mock_open_func.side_effect = self.mock_file
        analyzer = make_stat('dummy.log')
        browser, count = analyzer.get_popular_browser()
        self.assertEqual(browser, 'Mozilla/5.0')
        self.assertEqual(count, 3)

    @patch('builtins.open')
    def test_slowest_page(self, mock_open_func):

        mock_open_func.side_effect = self.mock_file
        analyzer = make_stat('dummy.log')
        page, time_ = analyzer.get_slowest_page()
        self.assertEqual(page, '/submit')
        self.assertEqual(time_, 300)

    @patch('builtins.open')
    def test_fastest_page(self, mock_open_func):

        mock_open_func.side_effect = self.mock_file
        analyzer = make_stat('dummy.log')
        page, time_ = analyzer.get_fast_page()
        self.assertEqual(page, '/contact')
        self.assertEqual(time_, 100)

    @patch('builtins.open')
    def test_average_slowest_page(self, mock_open_func):

        mock_open_func.side_effect = self.mock_file
        analyzer = make_stat('dummy.log')
        page, avg_time = analyzer.get_slow_page()
        self.assertEqual(page, '/submit')
        self.assertEqual(avg_time, 300.0)

    @patch('builtins.open')
    def test_active_clientday(self, mock_open_func):

        mock_open_func.side_effect = self.mock_file
        analyzer = make_stat('dummy.log')
        active_by_day = analyzer.get_active_clientday()
        expected = {
            '10/Oct/2020': ('127.0.0.1', 1),
            '11/Oct/2020': ('127.0.0.1', 1),
            '12/Oct/2020': ('127.0.0.1', 1),
        }
        self.assertEqual(active_by_day, expected)


def get_params():
    files = []
    stats = []
    for param in sys.argv[1:]:
        if param.startswith("--"):
            stats.append(param[2:])
        else:
            files.append(param)
    return {'files': files, 'stats': stats}


def main():
    params = get_params()
    files = params.get("files", [])
    stats = params.get("stats", [])

    av = {
        'popular_resource': 'popular_resource',
        'active_client': 'active_client',
        'popular_browser': 'popular_browser',
        'slowest_page': 'slowest_page',
        'fastest_page': 'fastest_page',
        'average_slowest_page': 'average_slowest_page',
        'active_client_by_day': 'active_client_by_day'
    }

    for filename in files:
        analyzer = make_stat(filename)
        print(f"============= {filename} =============")
        for stat in stats:
            if stat not in av:
                print(f"Unknown statistic: {stat}")
                continue
            if stat == 'popular_resource':
                result, count = analyzer.get_popular_resource()
                if result:
                    print(f"Popular resource: {result} ({count} обращений)")
            elif stat == 'active_client':
                result, count = analyzer.get_active_client()
                if result:
                    print(f"Active client: {result} ({count} обращений)")
            elif stat == 'popular_browser':
                result, count = analyzer.get_popular_browser()
                if result:
                    print(f"Popular browser: {result} ({count} обращений)")
            elif stat == 'slowest_page':
                result, time_ = analyzer.get_slowest_page()
                if result:
                    print(f"Slowest page: {result} ({time_} ms)")
            elif stat == 'fastest_page':
                result, time_ = analyzer.get_fast_page()
                if result:
                    print(f"Fastest page: {result} ({time_} ms)")
            elif stat == 'average_slowest_page':
                result, avg_time = analyzer.get_slow_page()
                if result:
                    print(f"Average slowest page: "
                          f"{result} ({avg_time:.2f} ms)")
            elif stat == 'active_client_by_day':
                results = analyzer.get_active_clientday()
                for day, (client, count) in sorted(results.items()):
                    print(f"Active client on {day}: "
                          f"{client} ({count} обращений)")
        print("")


if __name__ == "__main__":
    if 'test' in sys.argv:
        sys.argv.remove('test')
        unittest.main()
    else:
        main()
