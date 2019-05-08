import librosa
import numpy as np
from saxpy.znorm import znorm
from saxpy.paa import paa
from saxpy.sax import ts_to_string
from saxpy.alphabet import cuts_for_asize
import os
import math
from functools import reduce
from collections import Counter
SAX_VOCAB_LENGTH = 6
NO_OF_FEATURES = 51
K = 3
NO_OF_SONGS = 100 #no of songs in the databse

def or_binary(str1, str2): # performs binary or operation
	return ''.join([str(int(i) or int(j)) for i,j in zip(str1, str2)])

def char_to_int(ch): # finds the difference between characters in ascii
	return ord(ch)-ord('a')

def extract_features(song_name): # returns mfcc and chroma features in SAX represetation
	try:
		x, fs = librosa.load(song_name)
	except:
		return None
	mfccs = librosa.feature.mfcc(x, sr=fs,n_mfcc=39)
	chroma = librosa.feature.chroma_stft(x, sr=fs)
	feature_matrix = np.concatenate((mfccs,chroma))

	sax_rep = []

	sax_rep = [ts_to_string(paa(znorm(feat), SAX_VOCAB_LENGTH), cuts_for_asize(SAX_VOCAB_LENGTH)) for feat in feature_matrix]
	return sax_rep


def pattern_relation(sax_rep, sax_len): # generates pattern relation from sax representation
	pr = []
	for i in range(sax_len):
		p1 = []
		a = char_to_int(sax_rep[i])*SAX_VOCAB_LENGTH

		for j in range(i+1,i+K+1):
			if(j < sax_len):
				p1.append(a+char_to_int(sax_rep[j]))
			else: p1.append(-1)

		for j in range(len(p1)):
			if(p1[j] != -1):
				p2 = ""
				for k in range(len(p1)):
					if(p1[j] == p1[k]):
						p2 = p2+"1"
						if(j != k): p1[k] = -1
					else: p2 = p2+"0"

				pr.append([p1[j],p2])
				p1[j] = -1

	for i in range(0,len(pr)-K+1):
		for j in range(i+1,i+K):
			if(i<len(pr) and j<len(pr) and pr[i][0] == pr[j][0]):
				p_combine = or_binary(pr[i][1],pr[j][1])
				pr[i][1] = p_combine
				del pr[j]
	return pr

def entropy(string): # calculates entropy for a string given as input
	counts = Counter(string)
	l = len(string)
	prob = [float(v)/l for v in counts.values()]
	entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
	return entropy


def song_sax_representation(song_paths): # returns sax representations for each songs in a location
	sax_reps = []

	for i in range(0, len(song_paths)):
		feat = extract_features(song_paths[i])
		if feat is not None:
			sax_reps.append(feat)
			print("Song "+str(i)+" converted to sax representation")

	return sax_reps


def read_songs(path): # reads songs from given path and returns song names along with exact path for each song
	song_list = []
	song_path = []

	for song in os.listdir(path):
		song_list.append(song)
		song_path.append(os.path.join(path,song))
	return song_list, song_path


def match(str1, str2): # matches strings bit wise
	s = 0
	for i,j in zip(str1, str2):
		if i == j:
			s = s+1

	return s
