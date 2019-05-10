from docx import Document 
import spell_checker

for k in range (1, 62):#loop till number of files that need to be checked
    print ('\n File No. being processed: '+str(k))
    
    #change the path according to the system 
    doc = Document(r"path containing unedited docx files\\"+str(k)+".docx") 
    txt = doc.paragraphs
    
    #change the path according to the system 
    f = open (r"path containing edited text files\\"+str(k)+".txt", 'ab')
    l = []

    #processing text extracted from docx
    for p in txt:
        if 'References' not in p.text :
            l.extend(p.text)
        else:
            break
     
    #writing the processed text to the text file    
    for j in l:
        f.write(j.encode('utf-8'))
    f.close()
    
    #finding errors
    spell_checker.main(k)
