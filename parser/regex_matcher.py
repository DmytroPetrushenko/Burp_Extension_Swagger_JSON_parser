import re


# The method checks if the data corresponds to a certain format > http(s)://example.com/.
def get_host_from_url(json_url):
    try:
        regex = r".*://([\w\.-]+)/.*"
        matches = re.findall(regex, json_url, re.MULTILINE)
        return matches[0]
    except IndexError:
        return []
