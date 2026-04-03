import re
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        
        self.text.append(d)

    def get_data(self):
        return ''.join(self.text)


def remove_html_tags(text):
    """
    Remove HTML tags from a string, handling nested tags and preserving text content.
    
    Args:
    text (str): The input string containing HTML tags
    
    Returns:
    str: The input string with HTML tags removed
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    # First, use regex to remove script and style elements and their contents
    text = re.sub(r'(?is)<(script|style).*?>.*?</\1>', '', text)
    
    # Then use HTMLParser to handle the remaining HTML
    stripper = MLStripper()
    stripper.feed(text)
    return stripper.get_data()


def fix_url(url):
    return f'https://boards.greenhouse.io{url}'


