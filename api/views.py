from django.http import response
from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView 
import datetime  
from rest_framework.generics import CreateAPIView

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .models import my_input
from .serializers import MyInputSerializer

from pyresparser import ResumeParser
import pprint
import json

import pdf2image
import easyocr as e
import numpy as np
import PIL
from PIL import ImageDraw
import spacy 


import random
import spacy.cli

class ResumeAPI(CreateAPIView):
  serializer_class = MyInputSerializer
  def post(self, request, *args, **kwargs):
    fileobj = request.FILES['upload_file']
    my_input.objects.create(upload_file=fileobj)
    user_input = my_input.objects.all().last()
    req_file = user_input.upload_file.path

    data2 = ResumeParser(req_file).get_extracted_data()
    y = json.dumps(data2)

    
    bounds= []
    Name = []
    Work = []
    Skills = []
    Education = []
    Projects = []
    Certificates = []
    Achievements = []
    Projects = []
    Other = []
    links = []
    DOB=[]
    
    reader = e.Reader(['en'])
    images = (pdf2image.convert_from_path(req_file, 
      poppler_path=r'poppler-0.68.0\bin'))
      
    for i in range(0,len(images)):
        bounds.append(reader.readtext(np.array(images[i]), min_size=0,
          slope_ths=0.2,ycenter_ths=0.7,height_ths=0.6,width_ths=0.8,
          decoder='beamsearch', beamWidth=10))
    text=''
    for j in range(len(bounds)):
          for i in range(len(bounds[j])):
              text = text + bounds[j][i][1] + '\n'
       

    nlp2 = spacy.load(r'en_core_web_sm')
    
   
    data = text 
    
    doc2 = nlp2(data)
    for ent in doc2.ents:
      if ent.label_ == 'Name':
        Name.append(ent.text_with_ws)
      #print("NAME: ",Name )        

    for ent in doc2.ents:
      if ent.label_ == 'Work Exp':
        Work.append(ent.text_with_ws)
        
      #print("WORK EXPERIENCE: ",Work)        

    for ent in doc2.ents:
      if ent.label_ == 'Education':
        Education.append(ent.text_with_ws)
      #print("EDUCATION: ",Education)        

    for ent in doc2.ents:
      if ent.label_ == 'Projects':
        Projects.append(ent.text_with_ws)
      #print("PROJECTS: ",Projects)        

    for ent in doc2.ents:
      if ent.label_ == 'Skills':
        Skills.append(ent.text_with_ws)
      #print("SKILLS: ",Skills)        

    for ent in doc2.ents:
      if ent.label_ == 'Certificates':
        Certificates.append(ent.text_with_ws)
      #print("CERTIFICATES: ",Certificates)        

    for ent in doc2.ents:
      if ent.label_ == 'Achievements':
        Achievements.append(ent.text_with_ws)
      #print("ACHIEVEMENTS: ",Achievements)        

    for ent in doc2.ents:
      if ent.label_ == 'Other Deatils':
        Other.append(ent.text_with_ws)
      #print("OTHER DETAILS: ",Other)        


          
    import re
    phone_pattern = re.compile(r'[0-9]{10}')
    phone_matches = phone_pattern.findall(data)
      #print("CONTACT: ",phone_matches)

    email_pattern = re.compile(r'[a-zA-Z0-9-\.]+@[a-zA-z-0-9-\.]*\.[a-z]*')
    email_matches = email_pattern.findall(data)
      #print("EMAIL: ",email_matches)

    status = re.compile(r'\bSingle\b | \bMarried\b | \bUnmarried\b | \bDivorced\b ', flags=re.I | re.X)
    status =  status.findall(data)
      #print("MARITAL STATUS: ",status)

    nationality = re.compile(r'\bIndia\b | \bIndian\b | \bNRI\b | \bNon-Indian\b ', flags=re.I | re.X)
    nationality = nationality.findall(data)
      #print("NATIONALITY: ",nationality)

    sex = re.compile(r'\bMale\b | \bFemale\b | \bLGBT\b | \bLGBTQ\b | \bTransGender | \bTrans Gender\b | \bTrans-Gender\b | \bGay\b | \bLesbian\b', flags=re.I | re.X)
    sex = sex.findall(data)
      #print("GENDER: ",sex)

    languages = re.compile(r'\bHindi\b | \bEnglish\b | \bTamil\b | \bGujrati\b | \bTelugu\b | \bMalayalam\b | \bKannad\b | \bBengali\b | \bMarathi\b | \bPunjabi\b | \bKashmiri\b | \bBihari\b | \bUrdu\b | \bArabic\b | \bAssami\b | \bManipuri\b | \bGoan\b | \bNepali\b', flags=re.I | re.X)
    languages= languages.findall(data)
      #print("LANGUAGES KNOWN: ",languages)

    # if Work == [] and data['experience'] != None:
    #   Work.append(data['experience'].text)
    # if Education == [] and data['degree'] != None:
    #   Education.append(data['degree'])
    # if Name == [] and data['name'] != None:
    #   Work.append(data['name'])
    # if Skills == [] and data['skills'] != None:
    #   Work.append(data['skills'])
    https_links = ''.join(re.findall(r'(https?://\S+)', data))
    linkedin = ''.join(re.findall(r'(linkedin.com?\S+)', data))
    github = ''.join(re.findall(r'(github.com?\S+)', data))
    medium = ''.join(re.findall(r'(medium.com?\S+)', data))
    blogspot = ''.join(re.findall(r'(blogspot.com?\S+)', data))
    personal = ''.join(re.findall(r'(www.?\S+)', data))


    if personal =='':
      pass

    else:
      links.append(personal)

    if linkedin =='':
      pass
    else:
      links.append(linkedin)

    if medium =='':
      pass
    else:
      links.append(medium)

    if blogspot =='':
      pass
    else:
      links.append(blogspot)

    if github =='':
      pass
    else:
      links.append(github)

    dob = re.compile(r'\d{2}-\d{2}-\d{4} | \d{4}-\d{2}-\d{2} | \d{2}-\d{2}-\d{2} | \d{2}\\d{2}\\d{4} | \d{4}\\d{2}\\d{4} | \d{2}\\d{2}\\d{2} | \d{2}.\d{2}.\d{4} | \d{4}.\d{2}.\d{2} | \d{2}.\d{2}.\d{2} | \d{2}th-Jan-\d{4} | \d{2}th-January-\d{4} | \d{2}th-Feb-\d{4} | \d{2}th-February-\d{4} | \d{2}th-Mar-\d{4} | \d{2}th-March-\d{4} | \d{2}th-April-\d{4} | \d{2}th-May-\d{4} | \d{2}th-Apr-\d{4} | \d{2}th-Jun-\d{4} | \d{2}th-June-\d{4} | \d{2}th-July-\d{4} | \d{2}th-Jul-\d{4} | \d{2}th-August-\d{4} | \d{2}th-Aug-\d{4} | \d{2}th-September-\d{4} | \d{2}th-Sept-\d{4} | \d{2}th-Oct-\d{4} | \d{2}th-October-\d{4} | \d{2}th-November-\d{4} | \d{2}th-Nov-\d{4} | \d{2}th-Dec-\d{4} | \d{2}th-December-\d{4}', flags=re.I | re.X)
    dob = ''.join(dob.findall(data))
    DOB.append(dob)

    Final_result = {
          "NAME: ":data2['name'],
          "CONTACT: ":[phone_matches,data2['mobile_number']],
          "EMAIL: ": data2['email'],
          "WORK EXPERIENCE: ":{
                "DESIGNATION: ": data2['designation'],        
                "COMPANY NAME: ": data2['company_names'], 
                "WORK: ": data2['experience']
                               },
          
          "EDUCATION: ":[Education, data2['degree'],data2['college_name']],
          "PROJECTS: ":Projects,
          "SKILLS: ":data2['skills'],
          "LINKS: ":links,
          "CERTIFICATES: ":Certificates,
          "ACHIEVEMENTS: ":Achievements,
          "LANGUAGES KNOWN: ":languages,
          "DATE OF BIRTH: ":DOB,
          "MARITAL STATUS: ":status,
          "NATIONALITY: ":nationality,
          "GENDER: ":sex,
          "LANGUAGES KNOWN: ":languages,
          "OTHER DETAILS: ":Other
      }  
    print(Final_result) 
    return Response(data = Final_result)
    
  


'''def index(request):
  return render(request,'index.html') ''' 

# def result(request):
#   fileobj = request.FILES['test']
#   my_input.objects.create(upload_file=fileobj)
#   user_input = my_input.objects.all().last()
#   req_file = user_input.upload_file.path
  
#   bounds= []
#   Name = []
#   Work = []
#   Skills = []
#   Education = []
#   Projects = []
#   Certificates = []
#   Achievements = []
#   Projects = []
#   Other = []
  
#   reader = e.Reader(['en'])
#   images = (pdf2image.convert_from_path(req_file, 
#     poppler_path=r'C:\Program Files\poppler-0.68.0\bin'))
    
#   for i in range(0,len(images)):
#       bounds.append(reader.readtext(np.array(images[i]), min_size=0,
#         slope_ths=0.2,ycenter_ths=0.7,height_ths=0.6,width_ths=0.8,
#         decoder='beamsearch', beamWidth=10))
#   text=''
#   for j in range(len(bounds)):
#         for i in range(len(bounds[j])):
#             text = text + bounds[j][i][1] + ' '

#   nlp2 = spacy.load(r"C:\Users\Asus\OneDrive\Desktop\Practice Selenium\OCR and NER")
#   data = text
  
#   doc2 = nlp2(data)
#   for ent in doc2.ents:
#     if ent.label_ == 'Name':
#       Name.append(ent.text_with_ws)
#     #print("NAME: ",Name )        

#   for ent in doc2.ents:
#     if ent.label_ == 'Work Exp':
#       Work.append(ent.text_with_ws)
#     #print("WORK EXPERIENCE: ",Work)        

#   for ent in doc2.ents:
#     if ent.label_ == 'Education':
#       Education.append(ent.text_with_ws)
#     #print("EDUCATION: ",Education)        

#   for ent in doc2.ents:
#     if ent.label_ == 'Projects':
#       Projects.append(ent.text_with_ws)
#     #print("PROJECTS: ",Projects)        

#   for ent in doc2.ents:
#     if ent.label_ == 'Skills':
#       Skills.append(ent.text_with_ws)
#     #print("SKILLS: ",Skills)        

#   for ent in doc2.ents:
#     if ent.label_ == 'Certificates':
#       Certificates.append(ent.text_with_ws)
#     #print("CERTIFICATES: ",Certificates)        

#   for ent in doc2.ents:
#     if ent.label_ == 'Achievements':
#       Achievements.append(ent.text_with_ws)
#     #print("ACHIEVEMENTS: ",Achievements)        

#   for ent in doc2.ents:
#     if ent.label_ == 'Other Deatils':
#       Other.append(ent.text_with_ws)
#     #print("OTHER DETAILS: ",Other)        


        
#   import re
#   phone_pattern = re.compile(r'[0-9]{10}')
#   phone_matches = phone_pattern.findall(data)
#     #print("CONTACT: ",phone_matches)

#   email_pattern = re.compile(r'[a-zA-Z0-9-\.]+@[a-zA-z-0-9-\.]*\.[a-z]*')
#   email_matches = email_pattern.findall(data)
#     #print("EMAIL: ",email_matches)

#   status = re.compile(r'\bSingle\b | \bMarried\b | \bUnmarried\b | \bDivorced\b ', flags=re.I | re.X)
#   status =  status.findall(data)
#     #print("MARITAL STATUS: ",status)

#   nationality = re.compile(r'\bIndia\b | \bIndian\b | \bNRI\b | \bNon-Indian\b ', flags=re.I | re.X)
#   nationality = nationality.findall(data)
#     #print("NATIONALITY: ",nationality)

#   sex = re.compile(r'\bMale\b | \bFemale\b | \bLGBT\b | \bLGBTQ\b | \bTransGender | \bTrans Gender\b | \bTrans-Gender\b | \bGay\b | \bLesbian\b', flags=re.I | re.X)
#   sex = sex.findall(data)
#     #print("GENDER: ",sex)

#   languages = re.compile(r'\bHindi\b | \bEnglish\b | \bTamil\b | \bGujrati\b | \bTelugu\b | \bMalayalam\b | \bKannad\b | \bBengali\b | \bMarathi\b | \bPunjabi\b | \bKashmiri\b | \bBihari\b | \bUrdu\b | \bArabic\b | \bAssami\b | \bManipuri\b | \bGoan\b | \bNepali\b', flags=re.I | re.X)
#   languages= languages.findall(data)
#     #print("LANGUAGES KNOWN: ",languages)


#   Final_result = {
#         "NAME: ":Name,
#         "CONTACT: ":phone_matches,
#         "EMAIL: ":email_matches,
#         "WORK EXPERIENCE: ":Work,
#         "EDUCATION: ":Education,
#         "PROJECTS: ":Projects,
#         "SKILLS: ":Skills,
#         "CERTIFICATES: ":Certificates,
#         "ACHIEVEMENTS: ":Achievements,
#         "LANGUAGES KNOWN: ":languages,
#         "MARITAL STATUS: ":status,
#         "NATIONALITY: ":nationality,
#         "GENDER: ":sex,
#         "LANGUAGES KNOWN: ":languages,
#         "OTHER DETAILS: ":Other
#     }  
#   print(Final_result) 
#   return render(request, 'index.html',Final_result)
  
  

'''def give_file():

  user_input = my_input.objects.all().last()
  req_file = user_input.upload_file
  return req_file'''

