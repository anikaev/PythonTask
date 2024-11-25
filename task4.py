import sys
import re

log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s- - \[(?P<datetime>[^\]]+)\]\s'
    r'"(?P<request>[^"]+)"\s(?P<status>\d{3})\s(?P<size>\d+)\s'
    r'"(?P<referrer>[^"]*)"\s"(?P<user_agent>[^"]*)"\s?'
    r'(?P<processing_time>\d+)?'
)


def get_params():
    files = []
    stats = []
    for param in sys.argv[1:]:
        if param.startswith("--"):
            stats.append(param[2:])
        else:
            files.append(param)
    return {'files': files, 'stats': stats}


def parse_logfile(filename):

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if log_pattern.match(line.strip()):
                request = log_pattern.match(line.strip()).group('request')
                parts = request.split()
                if len(parts) >= 2:
                    resource = parts[1]
                    yield {'ip': log_pattern.match(line.strip()).group('ip'), 'resource': resource}


def statistics(data, field):
    stats = {}
    for row in data:
        value = row.get(field)
        if value:
            if value in stats:
                stats[value] += 1
            else:
                stats[value] = 1
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    return sorted_stats


def main():
    params = get_params()
    files = params.get("files", [])
    stats = params.get("stats", [])

    av = {
        'popular_resource': 'resource',
        'active_client': 'ip'
    }

    for filename in files:
        print(f"============= {filename} =============")
        for stat in stats:
            field = av[stat]
            data = parse_logfile(filename)
            stat_result = statistics(data, field)
            if stat_result:
                top_item = stat_result[0]
                formatted_stat = stat.replace('_', ' ').capitalize()
                print(f"{formatted_stat}: {top_item[0]} ({top_item[1]} обращений)")
        print("")

if __name__ == "__main__":
    main()
