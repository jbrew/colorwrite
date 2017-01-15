import os

for filename in os.listdir('data/tfidf'):
	path = 'data/tfidf/%s' % filename
	with open(path, 'r') as input:
		text = input.read()
		
	savename = 'data/tfidf/%s_compiled' % filename.split('_')[0]
	
	if os.path.exists(savename):
		with open(savename, 'a') as output:
			output.write(text)
	else:
		with open(savename, 'w') as output:
			output.write(text)