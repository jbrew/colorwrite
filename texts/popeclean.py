import re

with open('theyoungpope.txt', 'r') as f:
	text = f.read()

text = re.sub(r'\<.*?\>', '', text)
text = re.sub(r'\[.*?\]', '', text)
text = re.sub(r'\&lt;i\&gt;', '', text)
text = re.sub(r'\&lt;\/i\&gt;', '', text)
text = re.sub(r'\&quot;', '', text)

text = ''.join([i if ord(i) < 128 else '' for i in text])




with open('youngpopeclean', 'w') as f:
	f.write(text)