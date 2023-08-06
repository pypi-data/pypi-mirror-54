#!/usr/bin/env python
# coding: utf-8

# In[51]:


from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
import re
from io import StringIO
import nltk 


# In[89]:


class PDFParser007:
    def __init__(self):
        self.packageRequired = ['pdfminer.six','nltk']
        self.methods = ['convert_pdf_to_txt','Headings','Paragraphs','Sentences']
    def convert_pdf_to_txt(self,path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text



    def Headings(self,path):
     text=self.convert_pdf_to_txt(path)
     if len(text)>0:
       text=text.replace('\xa0',' ').replace('\x0c',' ').replace('\r',' ').replace('\t',' ')
       text = text.encode('ascii', 'ignore').decode("utf-8")
       text11=[text]
       if '\n' in text:
            text11=text.split('\n')


       text12=[]
       for i in text11: 
            if len("".join(re.findall("[a-zA-Z0-9]+", i)))>0 :
                   text12.append(i.strip())
            else:
               text12.append('#')
       text13=text12
       heading=[]


       for i in text12[:]:
          if len(i)>0 and i!=text12[0] and i!=text12[-1] and i[0].isupper() and text12[text12.index(i)-1]=='#' and text12[text12.index(i)+1]=='#' and len(i.split(' '))>1 and len(i.split(' '))<8 :
               heading.append(i)

          elif len(i)>0 and (i==text12[0] or i==text12[-1]) and len(i.split(' '))>1 and len(i.split(' '))<8 :
               heading.append(i)

          elif len(i)>0 and len(i.split(' '))>1 and len(i.split(' '))<8 :
               heading.append(i)


       heading1=[]
       for j in heading:
           p="! @ # $ % ^ *  { } [ ] ' ' + ? / \  | =  : ;  < > "
           p1=p.split()
           if len("".join(re.findall("[a-zA-Z]+", j)))>20 and j[0].isupper() and all(x not in j for x in p1) and len("".join(re.findall("[0-9]+", j)))==0:
               heading1.append(j)

       return heading1
     else:
            return []

        
    def Paragraphs(self,path):
     text=self.convert_pdf_to_txt(path)
     if len(text)>0:
           
       text=text.replace('\xa0',' ').replace('\x0c',' ').replace('\r',' ').replace('\t',' ')
       text = text.encode('ascii', 'ignore').decode("utf-8")
       text11=[text]
       if '\n' in text:
            text11=text.split('\n')
       
       
       text12=[]
       for i in text11: 
            if len("".join(re.findall("[a-zA-Z0-9]+", i)))>0 :
                   text12.append(i.strip())
            else:
               text12.append('#')
       text13=text12
       
    
       for i in text12[:]:
          if len(i)>0 and i!=text12[0] and i!=text12[-1] and i[0].isupper() and text12[text12.index(i)-1]=='#' and text12[text12.index(i)+1]=='#' and len(i.split(' '))>1 and len(i.split(' '))<8 :
               
               text13.remove(i)
          elif len(i)>0 and (i==text12[0] or i==text12[-1]) and len(i.split(' '))>1 and len(i.split(' '))<8 :
               
               text13.remove(i)
          elif len(i)>0 and len(i.split(' '))>1 and len(i.split(' '))<8 :
               
               text13.remove(i)
       s2=[]
       s=''
       for i in text13:
           i1=i.strip()
           if i1!='#' :
               s=s +' ' + i1
           elif s!='':
               s2.append(s.strip())
               s=''
       
       s2.append(s.strip())
    
       s3=[]
       s=''
       for i in s2:
           i1=i.strip()
           if len(i1)>0:
            if  len(s2[s2.index(i)-1])>0 and (i1[0].isupper() or s2[s2.index(i)-1][-1]=='.' ) and len(i)>0:
               s3.append(s)  
               s=i1   
           else:
               s=s +' ' + i1
       s3.append(s)  
       
       para=[]
       for i in s3:
        if len("".join(re.findall("[a-zA-Z]+", i)))>0 and i.strip()[-1]=='.' and i[0].isupper() and len("".join(re.findall("[0-9]+", i)))/len("".join(re.findall("[a-zA-Z]+", i)))<.3:
            para.append(i)
       
       return para
    
     else:
            return []
     
     
    def Sentences(self,path):
       para=self.Paragraphs(path)     
       sentences=[]
       for p1 in para:
          s1=p1.split()
          s1.append('The')
          s=''
          for i in s1[:-1]:
           
           if i[-1]=='.' and s1[s1.index(i)+1][0].isupper() and (nltk.pos_tag([s1[s1.index(i)+1]])[0][1] in ['PRP','DT','PRP$'] or nltk.pos_tag([s1[s1.index(i)+1]])[0][1].startswith('NN') or s1[s1.index(i)+1] in ['The','We','I','Our']) :
              s=s+ ' ' +i
              
              if len(s.split())>5:
                 sentences.append(s.strip())
              s=''
           else:
               s=s+ ' ' +i
       return sentences 


# In[ ]:




