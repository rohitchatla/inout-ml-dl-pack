
# second method

import pytesseract
#from PIL import Image
import datetime
import cv2
import sys
import os
import os.path
import re
import numpy as np
#import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use("Agg")
#import matplotlib.pyplot as plt
import datefinder
import base64

#class to extract text from an image where the image file is passed as an argument
class Text_Extractor():
    #Constructor
    def __init__(self,image_file,file):
        self.image_file=image_file
        self.file=file
        if self is None:
            return 0
        
#Function to extract the text from image as string 
    def extract_text(self): 

        #img=Image.open(self.image_file)

        #print(self.image_file)
        #print(self.file)

        #img = cv2.imread(self.image_file)

        im_bytes = base64.b64decode(self.file)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)# im_arr is one-dim Numpy array
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        

        # plt.imshow(img)
        # img = Image.fromarray(img, 'RGB')
        # img.save('my.png')
        # img.show()

        #resize the image
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        #convert the image to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        

        #the following command uses the tesseract directory path to get the trained data in the config option
        pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
        text=pytesseract.image_to_string(img) #,config='--tessdata-dir "/usr/local/Cellar/tesseract/4.0.0_1/share/tessdata"'
        return text
    
#class to validate if  an image is a adhar card where the text is passed as an argument
class Aadhar_Card_Validator():
    #Constructor
    def __init__(self,text):
        self.text=text
#Function to validate if an image contains text showing its an aadhar card
    def is_aadhar_card(self):
               res=self.text.split()
               dates={}
               details={}           
               if 'GOVERNMENT OF INDIA'  in self.text:
                   print ("Aadhar card is valid and the details are below:")
                   #print(res)
                   index=res.index('INDIA')
                   name=''
                   if res[index+3].isalpha():
                      name= res[index+3] + " " + res[index+4] + " " + res[index+5]
                      details['name']=name
                   else :
                      name= res[index+4] + " " + res[index+5] + " " + res[index+6]
                      details['name']=name
               else:
                    name=res[0] + " " + res[1]
               if len(name)>1:
                   print("Name:  " + name)
               else:
                    print("Name not read")
               p = re.compile('d+/d+/d+')
               date=[]
               matches = datefinder.find_dates(self.text)
               for match in matches:
                    date.append(str(match))
               print("Date of birth: "+date[0])
               details['date1']=date[0]
               #date_time = matches.strftime("%m/%d/%Y, %H:%M:%S")
               #date_time = matches.isoformat(' ', 'seconds')
               #print("date and time:",date_time)

               if (p.findall(self.text)):
                    dates=p.findall(self.text)
               if len(dates)>0 and len(dates[0])>1:
                   print("Date of birth: "+ str(dates[0]))
                   details['date2']=dates[0]
               aadhar_number=''
               for word in res:
                  if 'yob' in word.lower():
                       yob=re.findall('d+', word)
                       if yob:
                           print ('Year of Birth: ' + yob[0])
                  if len(word) == 4 and word.isdigit():
                      aadhar_number=aadhar_number  + word + ' '
               if len(aadhar_number)>=14:
                   print("Aadhar number is :"+ aadhar_number)
                   details['aadhar_no']=aadhar_number
               else:
                    print("Aadhar number not read")
                    print("Try again or try  another file")
               return details

def cleaning(text):
       bad_chars = ['>', '=', '-','——']
      
       # initializing test string 
       test_string = text
      
       # printing original string 
       #print ("Original String : " + test_string)
      
       # using replace() to 
       # remove bad_chars 
       for i in bad_chars :
           test_string = test_string.replace(i, '')
       return test_string

def main(filename,file):
    
      #  if len(sys.argv) != 2:
      #       print ("Wrong number of arguments")
      #       sys.exit(1)
       image_file_name = filename #"aadhar.jpg"#sys.argv[1]
         # Check for right infilename extension.
       file_ext = os.path.splitext(image_file_name)[1]
       if file_ext.upper() not in ('.JPG', '.PNG' ):
             print( "Input filename extension should be .JPG or .PNG")
             sys.exit(1)
       te=Text_Extractor(image_file_name,file)
       text=te.extract_text()
       # print(text)
       # initializing bad_chars_list
       test_string=cleaning(text)
       #print(test_string)
       acv=Aadhar_Card_Validator(test_string)
       details=acv.is_aadhar_card()
       return details
#main()