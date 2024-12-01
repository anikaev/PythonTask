#!/usr/bin/env python3

import sys
import unittest
import re
from datetime import datetime, timezone, timedelta


def merge(*iterables, key=None):
    merged = []
    for iterable in iterables:
        merged.extend(iterable)
    return iter(sorted(merged, key=key))


def log_key(line):
    pattern = r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) ([+-]\d{4})\]'
    match = re.search(pattern, line)
    if not match:
        raise ValueError(f"Ошибка: {line}")

    timestamp_str, tz_str = match.groups()
    dt = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S')

    tz_hours = int(tz_str[:3])
    tz_minutes = int(tz_str[0] + tz_str[3:])
    tz_delta = timedelta(hours=tz_hours, minutes=tz_minutes)
    tz_info = timezone(tz_delta)

    dt = dt.replace(tzinfo=tz_info)
    return dt

class TestMergeCollections(unittest.TestCase):

    def test_bsc_merge(self):
        a = [1, 2, 3]
        b = [4, 5, 6]
        c = [7, 9, 10]
        expected = [1, 2, 3, 4, 5, 6, 7, 9, 10]
        result = list(merge(a, b, c))
        self.assertEqual(result, expected)

    def test_key_func(self):
        iterable = [('A', 1), ('B', 3), ('C', 2)]
        test = merge(iterable, key=lambda x: x[1])
        self.assertEqual(list(test), [('A', 1), ('C', 2), ('B', 3)])

    def test_one_sequence(self):
        iterable = (1, 6, 2, 8)
        test = merge(iterable)
        self.assertEqual(list(test), [1, 2, 6, 8])

    def test_two_sequences_eq_size(self):
        iterables = [(1, 2, 8), (4, 3, 5)]
        test = merge(*iterables)
        self.assertEqual(list(test), [1, 2, 3, 4, 5, 8])

    def test_merge_w_key(self):
        fruits1 = ['a', 'b', 'c']
        fruits2 = ['ad', 'bd', 'cd']
        expected = ['a', 'ad', 'b', 'bd', 'c', 'cd']
        result = list(merge(fruits1, fruits2, key=lambda x: x))
        self.assertEqual(result, expected)

    def test_is_iterables(self):
        f = 1
        expected = []

    def test_merge_with_em(self):
        empty = []
        numbers1 = [1, 3, 5]
        numbers2 = [2, 4, 6]
        expected = [1, 2, 3, 4, 5, 6]
        result = list(merge(empty, numbers1, numbers2))
        self.assertEqual(result, expected)

    def test_merge_logs(self):
        logs1 = [
            "192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "
            "\"GET /tv/useUser "
            "HTTP/1.1\" 200 432 \"http://callider/graph/personal\""
            " \"Mozilla/4.0 ...\" 2878948",
            "192.168.12.108 - - [17/Feb/2013:06:37:21 +0600] "
            "\"GET /tv/useUser HTTP/1.1\" "
            "200 432 \"http://callider/index.php\" "
            "\"Mozilla/4.0 ...\" 2881091",
            "192.168.74.151 - - [17/Feb/2013:06:37:21 +0600] "
            "\"GET /tv/useUser HTTP/1.1\""
            " 200 432 \"http://callider.kontur/pause/index\" "
            "\"Mozilla/5.0 ...\" 2913330"
        ]
        logs2 = [
            "192.168.12.61 - - [17/Feb/2013:06:37:21 +0600] "
            "\"GET /pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1\" "
            "200 986 \"http://callider/pause/index\" "
            "\"Mozilla/4.0 ...\" 3334081",
            "192.168.65.56 - - [17/Feb/2013:06:37:21 +0600] "
            "\"GET /pause/ajaxPause?pauseConfigId=all&admin=1 HTTP/1.1\""
            " 200 1047 \"http://192.168.65.101/pause/index\" "
            "\"Mozilla/5.0 ...\" 3376692"
        ]
        expected = [
            "192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "
            "\"GET /tv/useUser HTTP/1.1\" "
            "200 432 \"http://callider/graph/personal\" "
            "\"Mozilla/4.0 ...\" 2878948",
            "192.168.12.108 - - [17/Feb/2013:06:37:21 +0600]"
            " \"GET /tv/useUser HTTP/1.1\" "
            "200 432 \"http://callider/index.php\""
            " \"Mozilla/4.0 ...\" 2881091",
            "192.168.74.151 - - [17/Feb/2013:06:37:21 +0600] "
            "\"GET /tv/useUser HTTP/1.1\" "
            "200 432 \"http://callider.kontur/pause/index\" "
            "\"Mozilla/5.0 ...\" 2913330",
            "192.168.12.61 - - [17/Feb/2013:06:37:21 +0600] "
            "\"GET /pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1\""
            " 200 986 \"http://callider/pause/index\""
            " \"Mozilla/4.0 ...\" 3334081",
            "192.168.65.56 - - [17/Feb/2013:06:37:21 +0600]"
            " \"GET /pause/ajaxPause?pauseConfigId=all&admin=1 HTTP/1.1\" "
            "200 1047 \"http://192.168.65.101/pause/index\" "
            "\"Mozilla/5.0 ...\" 3376692"
        ]
        result = list(merge(logs1, logs2, key=log_key))
        self.assertEqual(result, expected)

    def test_merge_s_keys(self):
        a = [1, 3, 5]
        b = [1, 3, 5]
        expected = [1, 1, 3, 3, 5, 5]
        result = list(merge(a, b))
        self.assertEqual(result, expected)


class TestLogKeyFunction(unittest.TestCase):

    def test_correct_log_entry(self):
        log = ("192.168.12.10 - - [17/Feb/2013:06:37:21 +0600] "
               "\"GET /tv/useUser HTTP/1.1\" "
               "200 432 \"http://callider/graph/personal\""
               "\"Mozilla/4.0 ...\" 2878948")
        expected = datetime.strptime("17/Feb/2013:06:37:21",
                                     '%d/%b/%Y:%H:%M:%S').replace(
            tzinfo=timezone(timedelta(hours=6)))
        result = log_key(log)
        self.assertEqual(result, expected)

    def test_inv_log(self):
        b_log = "РќРµ РїСЂР°РІРёР»СЊРЅС‹Р№ Р»РѕРі"
        with self.assertRaises(ValueError):
            log_key(b_log)

    def test_different_timestamps(self):
        log1 = ("192.168.12.10 - - [16/Feb/2013:23:59:59 +0600]"
                " \"GET /home HTTP/1.1\" 200 123 \"-\" "
                "\"Mozilla/5.0 ...\" 123456")
        log2 = ("192.168.12.10 - - [17/Feb/2013:00:00:00 +0600]"
                " \"GET /home HTTP/1.1\" 200 123 \"-\""
                " \"Mozilla/5.0 ...\" 123457")
        expected1 = datetime.strptime("16/Feb/2013:23:59:59",
                                      '%d/%b/%Y:%H:%M:%S').replace(
            tzinfo=timezone(timedelta(hours=6)))
        expected2 = datetime.strptime("17/Feb/2013:00:00:00",
                                      '%d/%b/%Y:%H:%M:%S').replace(
            tzinfo=timezone(timedelta(hours=6)))
        self.assertEqual(log_key(log1), expected1)
        self.assertEqual(log_key(log2), expected2)

    def test_merge_custom_key(self):
        log1 = "[13/May/2012:06:33:17 +0600] Log entry 1"
        log2 = "[13/May/2012:06:33:18 +0600] Log entry 2"
        log3 = "[13/May/2012:06:33:16 +0600] Log entry 3"

        result = list(merge([log1, log2, log3], key=log_key))
        expected_order = [log3, log1, log2]
        self.assertEqual(result, expected_order)


def read_log(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        print(f"РќРµС‚Сѓ: {filepath}")
    except IOError as e:
        print(f"РћС€РёР±РєР° ({e.errno}): {e.strerror}")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        files = sys.argv[1:]
        sources = [read_log(file) for file in files]
        merged_logs = merge(*sources, key=log_key)

        for entry in merged_logs:
            print(entry)
    else:
        unittest.main()