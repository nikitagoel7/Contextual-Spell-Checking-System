# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:12:18 2019

@author: Nikita
"""

        
# Natural Language Toolkit: code_cfg1
import nltk
from nltk import CFG
from nltk import data
from nltk import RecursiveDescentParser
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import Nonterminal, nonterminals, Production, CFG
from nltk.tree import Tree
from textblob import TextBlob
import language_check
import string
import json

def main(k):
    #opening the processed text file
    #change the path according to the system 
    f1 = open(r'path containing edited text files\\"+str(k)+".txt", 'rb')
    txt = f1.read().decode('utf-8')
#    txt = txt.decode('utf-8')
#    txt = txt.decode('utf-8')
    f1.close()
    
    #loading the training set
    simple_cfg = data.load('file:spell.cfg', 'cfg')

#    txt = """The girafee is angri. He angri to walk.
#    After that he slept. While sleping he snored loudly. Dont no what to do.""" 
#    
    tokened = txt.split('\n')
    #stop_words = set(stopwords.words('english'))
    
    #checking grammatical errors using language-check library
    tool = language_check.LanguageTool('en-US')
    
    matches = tool.check(txt)
    
    #used for creating the error dictionary which stores the errors wrt to their indicies
    errors = {}
    
    #used to store the index and the respective sentence in which error is present. Useful at the time of parsing
    err_sen = {}
    #err_sens = {}
    
    #formation of errors and err_sen dictionaries
    for i in range(len(matches)):
        fromx = matches[i].fromx   #extracts the beginning index of incorrect word with respect to a paragraph
        fromy = matches[i].fromy   #extracts the index with respect to each paragraph
        tox = matches[i].tox       #extracts the end index of incorrect word with respect to a paragraph
        t = tokened[fromy]
        u = t[fromx:tox].strip()
        if u == '' or u in string.punctuation or u == '”':
            continue
        else:
            errors[str((fromx, fromy))] = u.lower()
        sent = sent_tokenize(t)
        for j in range (0, len(sent)):
            if u in sent[j]:
                if t.index(sent[j][0]) <= fromx :
                    x = sent[j]
                    
            else:
                continue
    #        err_sen[(fromx, fromy)] = []
            err_sen[str((fromx, fromy))] = x.lower()
            
   
            
    m = 0  
    print (len(matches))
    
    #parsing each item in the errors dictionary and updating the errors wherever required
    for key, val in errors.items():
#        
        m = m+1
        print(m)
        
        #textblob is being used to suggest the suggestions and their confidence score. 
        #The highest confidence is considered in this case for each incorrect word and 
        #is being compared wrt to the orignal word(orignal word can be useful if it is 
        #a medical term and also textblob helps in rechecking the word)
        tb = TextBlob(val)
        top_suggested_word = tb.words[0].spellcheck()[0][0]
#        print(tb.words[0].spellcheck())
        
        #If both, orignal and suggested word is same then it can be concluded that there
        #is a contextual error raised by language-check and user needs to check its grammartical error
        if (top_suggested_word == val):
            errors[key] = val + " :Contexual Error"
        else:
#            print (top_suggested_word, val, False)
            
            ##PROCESSING AND PARSING WITH ORIGINAL WORD 
            #preprocessing the tokenized values in order to avoid errors
            tokenized = sent_tokenize(err_sen[key])
            
            tokenized = tokenized[0].translate(str.maketrans('', '', string.punctuation))
            
            tokenized = tokenized.replace("’", "")
            tokenized = tokenized.replace("”", "")
            tokenized = tokenized.replace("“", "")
            wordsList = nltk.word_tokenize(tokenized)
            
            
            #pos tagging while keeping the orignal word in the sentence
            tagged = nltk.pos_tag(wordsList) 
      
#            print("Original: ", tagged)
    
            lhs = []
            rhs = []
            
            #preparing a lexicon to be inserted in the self learning training model
            for i in range(len(tagged)):
    
                lhs.append(nltk.grammar.Nonterminal(tagged[i][1]))
        
                rhs.append(nltk.grammar.Nonterminal(tagged[i][0]))
                
            new_production_original = []
            
            for i in range(len(rhs)):
                
                #if the training set already contains the production, then no need to
                #add another production
                if(len(simple_cfg.productions(rhs=str(rhs[i])))):
                    
#                    print('test')
    
                    continue
                
                #appending new production
                else:
    
                    #converting tokens to the language specific non-terminals
                    if(str(lhs[i]) == 'JJ'): 
    
                        lhs[i] = nltk.grammar.Nonterminal('Adj')
    
                    elif(str(lhs[i]) == 'NN' or str(lhs[i]) == 'NNS' or str(lhs[i]) == 'NN$' or str(lhs[i]) == 'NNS$' or str(lhs[i]) == 'NC'):
    
                        lhs[i] = nltk.grammar.Nonterminal('N')
    
                    elif(str(lhs[i]) == 'NP' or str(lhs[i]) == 'NNP' or str(lhs[i]) == 'NNPS' or str(lhs[i]) == 'NPS' or str(lhs[i]) == 'NP$' or str(lhs[i]) == 'NPS$'):
    
                        lhs[i] = nltk.grammar.Nonterminal('PropN')
    
                    elif(str(lhs[i]) == 'VB' or str(lhs[i]) == 'VBD' or str(lhs[i]) == 'VBG' or str(lhs[i]) == 'VBN' or str(lhs[i]) == 'VBP' or str(lhs[i]) == 'VBZ'):
    
                        lhs[i] = nltk.grammar.Nonterminal('V')
                        
                    elif(str(lhs[i]) == 'IN' or str(lhs[i]) == 'TO'):
    
                        lhs[i] = nltk.grammar.Nonterminal('P')
                        
                    elif(str(lhs[i]) == 'PN' or str(lhs[i]) == 'PN$' or str(lhs[i]) == 'PP$' or str(lhs[i]) == 'PP$$' or str(lhs[i]) == 'PPL' or str(lhs[i]) == 'PPLS' or str(lhs[i]) == 'PPO' or str(lhs[i]) == 'PPS' or str(lhs[i]) == 'PPSS' or str(lhs[i]) == 'PRP' or str(lhs[i]) == 'PRP$'):
    
                        lhs[i] = nltk.grammar.Nonterminal('PP')
                    else:
                        lhs[i] = nltk.grammar.Nonterminal('N')
                        
                    new_production = nltk.grammar.Production(nltk.grammar.Nonterminal(lhs[i]), [str(rhs[i])])
                    
                    #appending new production
                    new_production_original.append(nltk.grammar.Production(nltk.grammar.Nonterminal(lhs[i]), [str(rhs[i])]))
    
                    simple_cfg._productions.append(new_production)
    
    #        print(simple_cfg)
            
            #forming a new cfg in order to update the changes and start running 
            simple_cfg_1 =  nltk.grammar.CFG.fromstring(str(simple_cfg).split('\n')[1:])
    
            simple_cfg_1._start = simple_cfg.start()
    
    ##        print(simple_cfg_1)
            
            #forming a parse tree with the known grammar and testing the grammatical 
            #correctness of the sentence when parsed with the orignal word 
            rd = RecursiveDescentParser(simple_cfg_1)
    
            parse_tree_original = []
    
            for t in rd.parse(tokenized.split()):
    
                parse_tree_original = t
    
#                print(parse_tree_original)
    
            ##PROCESSING AND PARSING WITH NEW SUGGESTED WORD 
            #replacing the orignal word with top suggested word by the textblob
            text = err_sen[key].replace(val, top_suggested_word, 1)
    
            tokenized = sent_tokenize(text)
            
            #preprocessing the tokenized values in order to avoid errors
            tokenized = tokenized[0].translate(str.maketrans('', '', string.punctuation))
    
            tokenized = tokenized.replace("’", "")
            tokenized = tokenized.replace("”", "")
            tokenized = tokenized.replace("“", "")
            wordsList = nltk.word_tokenize(tokenized)
            
            #pos tagging while keeping the suggested and replaced word in the sentence
            tagged = nltk.pos_tag(wordsList) 
      
#            print("Replaced: ", tagged)
    
            lhs = []
            rhs = []
            
            #preparing a lexicon to be inserted in the self learning training model
            for i in range(len(tagged)):
    
                lhs.append(nltk.grammar.Nonterminal(tagged[i][1]))
        
                rhs.append(nltk.grammar.Nonterminal(tagged[i][0]))
            
            new_production_suggested = []
    
            for i in range(len(rhs)):
                
                #if the training set already contains the production, then no need to
                #add another production
                if(len(simple_cfg.productions(rhs=str(rhs[i])))):
                    
#                    print('test1')
    
                    continue
               #appending new production
                else:
    
                    #converting tokens to the language specific non-terminals
                    if(str(lhs[i]) == 'JJ'):
    
                        lhs[i] = nltk.grammar.Nonterminal('Adj')
    
                    elif(str(lhs[i]) == 'NN' or str(lhs[i]) == 'NNS' or str(lhs[i]) == 'NN$' or str(lhs[i]) == 'NNS$' or str(lhs[i]) == 'NC'):
    
                        lhs[i] = nltk.grammar.Nonterminal('N')
    
                    elif(str(lhs[i]) == 'NP' or str(lhs[i]) == 'NNP' or str(lhs[i]) == 'NNPS' or str(lhs[i]) == 'NPS' or str(lhs[i]) == 'NP$' or str(lhs[i]) == 'NPS$'):
    
                        lhs[i] = nltk.grammar.Nonterminal('PropN')
    
                    elif(str(lhs[i]) == 'VB' or str(lhs[i]) == 'VBD' or str(lhs[i]) == 'VBG' or str(lhs[i]) == 'VBN' or str(lhs[i]) == 'VBP' or str(lhs[i]) == 'VBZ'):
    
                        lhs[i] = nltk.grammar.Nonterminal('V')
                        
                    elif(str(lhs[i]) == 'IN' or str(lhs[i]) == 'TO'):
    
                        lhs[i] = nltk.grammar.Nonterminal('P')
                        
                    elif(str(lhs[i]) == 'PN' or str(lhs[i]) == 'PN$' or str(lhs[i]) == 'PP$' or str(lhs[i]) == 'PP$$' or str(lhs[i]) == 'PPL' or str(lhs[i]) == 'PPLS' or str(lhs[i]) == 'PPO' or str(lhs[i]) == 'PPS' or str(lhs[i]) == 'PPSS' or str(lhs[i]) == 'PRP' or str(lhs[i]) == 'PRP$'):
    
                        lhs[i] = nltk.grammar.Nonterminal('PP')
                    
                    else:
                        
                        lhs[i] = nltk.grammar.Nonterminal('N')
                        
                new_production = nltk.grammar.Production(nltk.grammar.Nonterminal(lhs[i]), [str(rhs[i])])
                
                #appending new production
                new_production_suggested.append(nltk.grammar.Production(nltk.grammar.Nonterminal(lhs[i]), [str(rhs[i])]))
    
                simple_cfg._productions.append(new_production)

            #forming a new cfg in order to update the changes and start running     
            simple_cfg_1 =  nltk.grammar.CFG.fromstring(str(simple_cfg).split('\n')[1:])
    
            simple_cfg_1._start = simple_cfg.start()
            
            #forming a parse tree with the known grammar and testing the grammatical 
            #correctness of the sentence when parsed with the suggested word
            rd = RecursiveDescentParser(simple_cfg_1)
    
            parse_tree_suggested = []
    
            for t in rd.parse(tokenized.split()):
    
                parse_tree_suggested = t
    
#                print(parse_tree_suggested)
    
            
            ##COMPARISON BETWEEN THE RESULTS OBTAINED AFTER PARSING THE ORIGINAL
            ##VS THE SUGGESTED WORD
            #if suggested word gives correct grammatical results and original 
            #results in wrong grammatical results -> SUGGESTED WORD WINS AND IS 
            #UPDATED IN THE ERRORS DICTIONARY
            if((len(parse_tree_original) == 0) and (len(parse_tree_suggested))):
                errors[key] = val + ": "+ top_suggested_word
                
#                print("Suggested Wins")
            
            #if suggested word gives incorrect grammatical results and original 
            #results in right grammatical results -> SUGGESTED WORD LOSES AND IS 
            #NOT UPDATED IN THE ERRORS DICTIONARY, it remains as it is
            elif((len(parse_tree_suggested) == 0) and (len(parse_tree_original))):
                pass
#                print("Original Wins")
    
            #if suggested word as well as original word gives incorrect 
            #grammatical results and original results -> THE ORIGINAL WORD IS WRONG 
            #BOTH CONTEXTUALLY AND GRAMMATICALLY, HENCE CONTEXTUAL ERROR IS RAISED
            # AND WORD IS SUGGESTED
            elif((len(parse_tree_original) == 0) and (len(parse_tree_suggested) == 0)):    
                errors[key] = val + ": Contextual Error but suggested change can be ->"+ top_suggested_word
#                print("Original Wins given both have lost")
    
            #if suggested word as well as original word gives correct 
            #grammatical results and original results ->  SUGGESTED WORD LOSES AND IS 
            #NOT UPDATED IN THE ERRORS DICTIONARY, it remains as it is
            elif((len(parse_tree_original)) and (len(parse_tree_suggested))):
                pass
    
#                print("Original Wins given both have won")
            
            #The changes are again written in the training set, hence enabling it 
            #to become self learning
            f = open("spell.cfg", "wb")
    
            for i in range(len(simple_cfg_1.productions())):
                cf = "\n"+str(simple_cfg_1.productions()[i])
                f.write(cf.encode('utf-8'))
    
            f.close()
                  
    #The updated errors dictionary is dumped in the json file
    with open("F:\Projects\Contextual Spell Checker\Edited Files\\"+str(k)+".json", 'w') as fp:
        json.dump(errors, fp)
    
    
