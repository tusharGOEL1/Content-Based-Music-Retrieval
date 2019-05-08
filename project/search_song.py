import pickle
import librosa
import numpy as np
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize
import os
import math

try:
	from .noise_red import noisered
	from .helper import pattern_relation, entropy, extract_features, read_songs, match
except:
	from noise_red import noisered
	from helper import pattern_relation, entropy, extract_features, read_songs, match


SAX_VOCAB_LENGTH = 6
NO_OF_FEATURES = 51
K = 3
NO_OF_SONGS = 100 #no of songs in the databse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

song_directory = os.path.join(BASE_DIR, "songs")
tree_directory = os.path.join(BASE_DIR, "attribute_trees")
processed_song_directory = os.path.join(BASE_DIR, "processed_songs")
search_song_dir = os.path.join(BASE_DIR, "search_song_dir")


def search_in_attribute_tree(sax_id, sax_rep, sax_len): # searches for given representation by loading the tree from disk and returns score for each song in the database
	tree_on_disk = open(os.path.join(tree_directory,'attribute_tree'+str(sax_id)), 'rb')
	# pickle.dump(t, tree_on_disk, protocol=2)
	t = pickle.load(tree_on_disk)
	tree_on_disk.close()
	pr = pattern_relation(sax_rep, sax_len)
	r = 0
	c = 0
	score_attribute = []

	for i in range(0, NO_OF_SONGS):
		score_attribute.append(0)

	for i in range(0, len(pr)):
		id = pr[i][0]
		r = int(id/SAX_VOCAB_LENGTH)
		c = id%SAX_VOCAB_LENGTH
		t_pr = t[r][c]

		for j in range(0, len(t_pr)):
			score_attribute[t_pr[j][0]] = score_attribute[t_pr[j][0]] + match(t_pr[j][1], pr[i][1])

	entro = entropy(sax_rep)
	score_attribute = [x*entro for x in score_attribute]
	return	score_attribute	



def search_song(song_location,flag):
	#noise reduction called

	# new_location = noisered(song_location,0)
	# if new_location is None:
	# 	return [None, None, None]
	new_location = song_location

	# print("loc : " + new_location)
	sax_rep = extract_features(new_location)
	if sax_rep is None:
		return [None, None, None]
	final_score = [0]*NO_OF_SONGS

	for i in range(0,NO_OF_FEATURES):
		partial_score = search_in_attribute_tree(i, sax_rep[i], SAX_VOCAB_LENGTH)
		final_score = [x+y for x,y in zip(final_score, partial_score)]

	song_ids = list(range(0,NO_OF_SONGS))
	final_score, song_ids = zip(*sorted(zip(final_score, song_ids)))

	
	p = os.path.join(BASE_DIR,"song_names")
	dict = open(p, 'rb')

	song_dictionary = pickle.load(dict)
	dict.close()


	#for i in reversed(range(0, NO_OF_SONGS)):
		#print("Proceesing song " + i+1 +"\n")
		#print(song_dictionary[song_ids[i]], final_score[i])

	return song_dictionary, final_score, song_ids

def accuracy_calculator():
	song_dictionary, song_path = read_songs(search_song_dir)
	acc=0
	for song in song_path: 
		#print(song)
		f = os.path.basename(song)
		print("Searching for Song: "+f)
		d, s, ids = search_song(song,0)
		if d is None:
			print("Song not found")
			return None, None
		l=[]
		scores = []
		for i in range(-1,-4,-1):
			l.append(d[ids[i]])
			scores.append(s[ids[i]])
		scores.sort()
		scores.reverse()
		print(l)
		print(scores)

		if f in l:
			acc=acc+1
	# print(d, s, ids)
	acc=(acc/len(song_path))*100
	print(acc)
	print("Accuracy :" + str(acc) +"%")
	return l, scores

if __name__ == '__main__':
	accuracy_calculator()