# OMR
## overview

      OMR is an application to grade students. The system typically used in universities to grade students and mark exam papers is complex , expensive and not flexible at all . Universities buy expensive hardware machines and specific paper type and that made the deployment of the electronic grading hard and not very likely to be used. 
       Our system solves this problem by letting the doctors design their own exam paper and grade students, it also benefits the students themselves by providing a complete website for complaints saving money , time and effort of such a long process. Using artificial intelligence (AI) and image processing techniques we’ve been able to provide the most efficient and simple app for a complete student grading system, helping the education in Egypt to be an easy sufficient experience and that’s our main goal.

### Technologies
Python :(Basic Language). 
openCV: 
Threshold
Detect corners
Masking( count number of non zero pixels)
Read/write images	
NumPy 
Immutils
Find contours 											
Json
Description file for the image
MySQL
Store the student’s information after evaluation
Pyqt5
Creating user interface
Excel 	
Provide the reports for the doctor


### Implementation
Doctor registration 
Store Subject information 
Handle JSON File
Read model answer image  
Extract answers and store them into answer KEY list 
Read students answer images 
Extract answers and store them into  student answer list
Comparing student answer with answer KEY and return student’s mark 
Store students marks, archive their sheets , show results , export results in excel sheet   
Analyze results

