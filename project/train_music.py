import pickle
import librosa
import numpy as np
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize
import os
import math
from helper import pattern_relation, song_sax_representation, read_songs
from noise_red import noisered

SAX_VOCAB_LENGTH = 6
NO_OF_FEATURES = 51
K = 3
NO_OF_SONGS = 100 #no of songs in the databse

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

song_directory = os.path.join(BASE_DIR, "songs")
tree_directory = os.path.join(BASE_DIR, "attribute_trees")
processed_song_directory = os.path.join(BASE_DIR, "processed_songs")
search_song_dir = os.path.join(BASE_DIR, "search_song_dir")



def add_song_to_attribute_tree(afpi_tree, song_id, pattern, pattern_len): # adds the pattern relation for a songs to the afpi tree for an attribute

	for i in range(0, pattern_len):
		pr = pattern[i]
		pr_id = pr[0]
		row = int(pr_id/SAX_VOCAB_LENGTH)
		col = pr_id%SAX_VOCAB_LENGTH

		(afpi_tree[row][col]).append([song_id,pr[1]])

	return afpi_tree

def create_attribute_tree(song_ids, sax_reps, sax_len): # creates afpi tree for an attribute given list of song ids, sax representations and length of the representations

	afpi = []

	for i in range(0, SAX_VOCAB_LENGTH):
		afpi.append([])

	for i in range(0, SAX_VOCAB_LENGTH):
		for j in range(0, SAX_VOCAB_LENGTH):
			afpi[i].append([])

	for i in range(0, len(sax_reps)):
		pr = pattern_relation(sax_reps[i], sax_len)
		afpi = add_song_to_attribute_tree(afpi, song_ids[i], pr, len(pr))

	return afpi


def create_data_structure(): # creates 51 afpi trees

	song_dictionary1, song_path1 = read_songs(song_directory)

	# for s in song_path1:
	# 	f = noisered(s,1)

	song_dictionary, song_path = read_songs(song_directory)
	dic = open(os.path.join(BASE_DIR, "song_names"), 'wb')
	pickle.dump(song_dictionary, dic)
	dic.close()
	song_sax_rep = song_sax_representation(song_path)

	song_sax_rep = [list(x) for x in zip(*song_sax_rep)]
	song_ids = list(range(0,NO_OF_SONGS))

	for i in range(0, NO_OF_FEATURES):
		afpi = create_attribute_tree(song_ids, song_sax_rep[i], SAX_VOCAB_LENGTH)
		store_tree = open(os.path.join(tree_directory,"attribute_tree"+str(i)), 'wb')
		pickle.dump(afpi, store_tree)
		store_tree.close()
		print("Attribute Tree "+str(i)+" created!!")

	print("All Attribute Trees created!!")



def KLT(a):
    """
    Returns Karhunen Loeve Transform of the input and the transformation matrix and eigenval

    Ex:
    import numpy as np
    a  = np.array([[1,2,4],[2,3,10]])

    kk,m = KLT(a)
    print kk
    print m

    # to check, the following should return the original a
    print np.dot(kk.T,m).T

    """
    val,vec = np.linalg.eig(np.cov(a))
    klt = np.dot(vec,a)
    return klt,vec,val

if __name__=='__main__':
	create_data_structure()