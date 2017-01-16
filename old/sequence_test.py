sentence = 'some example phrase'

def sequence_list(sentence, reach, max_size):
	tokens = sentence.split()
	if reach == 1:
		return [tokens[i:] for i in range(len(tokens))]
	else:
		return [tokens[i:reach*-1+1] for i in range(len(tokens)-1)]

print sequence_list(sentence, 1, 2)
print sequence_list(sentence, 2, 2)