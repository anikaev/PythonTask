#!/usr/bin/env python3
import re
from urllib.request import urlopen
import urllib.parse
from urllib import error
import sys
from collections import deque

F = 'Философия'


def get_content(name):
    names = 'https://ru.wikipedia.org/wiki/' + urllib.parse.quote(name)
    try:
        with urlopen(names, data=None, timeout=10) as page:
            content = page.read()
            return content
    except urllib.error.URLError:
        return None


def extract_content(page):
    if len(page) == 0:
        return (0, 0)

    start = page.find('div id="mw-content-text"')
    end = page.find('class="mw-hidden')
    if end == -1 or start == -1:
        return (-1, -1)
    return (start, end)


def extract_links(page, begin, end):
    if begin > end:
        return None
    string = page[begin:end]
    regex = r'(?<=[hH]ref=["\']\/wiki\/)([^:#]*?)(?=["\'])'
    set_links = list(re.findall(regex, string))
    for i in range(len(set_links)):
        set_links[i] = urllib.parse.unquote(set_links[i])
    temp = []

    for x in set_links:
        if x not in temp:
            temp.append(x)

    return temp


def find_chain(start, finish):
    if start == finish:
        return [start]

    queue = deque([start])
    used_url = set([start])
    parent = {}

    while queue:
        current = queue.popleft()
        page = get_content(current)
        if page is None:
            continue
        page = page.decode('utf-8')
        begin, end = extract_content(page)
        links = extract_links(page, begin, end)

        if links is not None:
            for link in links:
                if link == finish:
                    parent[link] = current
                    path = [finish]
                    while path[-1] != start:
                        path.append(parent[path[-1]])
                    return path[::-1]
                if link not in used_url:
                    used_url.add(link)
                    parent[link] = current
                    queue.append(link)
    return None


def main():
    name = sys.argv[1]
    var = find_chain(name, F)
    print(var)


if __name__ == "__main__":
    main()
