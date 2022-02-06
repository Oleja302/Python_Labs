import re

text = "Petr93, Johnny70, adwawddawdaw Service2002"
template = re.compile(r"[A-Z]\w*\d{2}|[A-Z]\w*\d{4}")
result = re.findall(template, text)
print(result)
