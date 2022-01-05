from requests.api import request

from .views import result
from .finalOCR import do_ocr  
from .final_parser import resume_parsed  

file = result(request)

ocr  = do_ocr(file)

def final_info():
    info = resume_parsed(ocr)
    return info 
