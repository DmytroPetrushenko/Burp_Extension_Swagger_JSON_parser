import re


def get_host_from_url(json_url):
    regex = r".*://([\w\.-]+)/.*"
    matches = re.findall(regex, json_url, re.MULTILINE)
    return matches[0]