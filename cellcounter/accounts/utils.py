import re


def read_signup_email(email):
    url_match = re.search(r"https?://[^/]*(/.*reset/\S*)", email.body)
    if url_match is None:
        return None, None
    return url_match.group(), url_match.groups()[0]
