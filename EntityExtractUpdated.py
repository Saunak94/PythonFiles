
import nltk
import json
import string
from flask import Flask 	 				#flask Import
from flask import jsonify	 				#
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import RegexpParser				#
from nltk.corpus import treebank_chunk 		#
from nltk.corpus import stopwords 	
# import en_core_web_sm
import spacy						#NER
nlp = spacy.load("en_core_web_sm")
#nlp = en_core_web_sm.load()					#NER
app = Flask(__name__)						#Flask


#Entity Detect
def ner(text1):
	X1=""
	ner1=""
	doc = nlp(text1)
	for X1 in doc.ents:
		print("X1:",X1)
		print("X1 label:",X1.label_)
		ner1=(X1.label_)
	if ner1=="ORG":
		ner1="Organization"
	else:
		ner1=''
	print("ner Return",ner1)
	return ner1



#Main Code
@app.route('/<string:text>')	
def autolearn(text):
#title- Makes 1st letter of a word capital
#Defining    
	named_entities = []
	stop_words = ['Of','Me','Details','In','On','The','Hello','Energy Consumption','Chiller']
	entity_type=['Building', 'Facility','Floor','Wing','Room']
	entry2=[]

	text=text.title()
	x = word_tokenize(text)

	#for x1 in x:
	#	if not x1 in stop_words:
	#		if x1 !='':
#				entry2.append(x1)
#	print(entry2)
#	x=(' '.join(map(str, entry2))) 
#	print("x: ",x)
#	x=word_tokenize(x)
#	entry2=[]


	pos=nltk.pos_tag(x) 
	print(pos)


	#Chunking with Regular Expression
	grammar =r"""
			CHUNK: {<NN|NNS\$><NN|NNP|NNPS|NNS>*}   
					{<VBG>+<CD>}
					{<CD>?<NNP>*<CD>?<NNP>*}
						{<VBG>+[A-Z]}
			"""
	cp = nltk.RegexpParser(grammar)
	Chunking=cp.parse(pos)
	print(Chunking)



	##Extracting Chunks and Converting to String 
	for t in Chunking.subtrees():
		if t.label() == 'CHUNK':
			named_entities.append(' '.join([w for w, t in t.leaves()]))
	print("The Entities Are:-")           
	print(named_entities)
	filtered_sentence = [w for w in named_entities if not w in stop_words]
	print("The filtered_sentence Are:-")           
	print(filtered_sentence) 	

	


	for w in filtered_sentence:
		print("w: ",w)
		a='Null'
		b=''
		words = w.split()
		for w1 in words:
			print("w1: ",w1)
			if w1 in entity_type:
				b=w1	#+'Name'
				a='got a value'
		print ("w:",w)
		if w=='Johnson Controls':
			b='Organization'
			a='got a value'
		if a=='Null':
			b=ner(w)
		#print("b: ",b)
		if b=='':
			#print("B is now General")
			b="General"

		e={'entity_name':w, 'entity_type':b, "SublistID": "Null"}
		entry2.append(e)
	
	s=json.dumps(entry2)
	print(s)
	return s

if __name__ == '__main__':
    app.debug = True
    app.run()
    