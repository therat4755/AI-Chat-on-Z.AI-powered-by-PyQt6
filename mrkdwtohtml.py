import re

with open('file.md', 'r', encoding='UTF-8') as f:
    text = f.read()

bold_toggle = False
def replace_bold(match):
    global bold_toggle
    bold_toggle = not bold_toggle
    return '<b>' if bold_toggle else '</b>'

result = re.sub(r'\*\*|__', replace_bold, text)
result = re.sub(r'~', '<s>', result)

with open('result.html', 'w', encoding='UTF-8') as f2:
    f2.write(result)
