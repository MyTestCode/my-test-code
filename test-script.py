#Python 2.7.10
#!/usr/bin/python
import requests
import simplejson as json
import re

#-----------------------------------------
#Function to get url request.
#Input header should be correct.
#-----------------------------------------
def send_request(page):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'}
    url = "http://api.viki.io/v4/videos.json?app=100250a&per_page=10&page=%s" %(page)
    response = requests.get(url, headers=headers)
    status = response.status_code
	
	#Check for request status. If status is successful then return json objects. If
	#status is 403 then check the request header is set correctly then exit.
    if status == 200:
	  return response.json()
    elif status == 403:
	  print "Getting http status 403 for the request. You may want to check if the request header is correct."
	  exit(1)
    else:
	  print "There is a problem with retrieving json objects."
	  exit(1)

	  
#-----------------------------------------
#Function to parse json objects in the response then count number of hd keys flag set to true or false.
#This function only test up to 10 pages.
#-----------------------------------------
def parse_json_objects():
    page_number = 0      #Give initial page number
    count_flag_true = 0  #counter for hd key set to true
    count_flag_false = 0 #counter for hd key set to false
	
	#Loop through only 10 pages 
    while (page_number < 10):
	   page_number += 1
	   json_objects = send_request(page_number)
	   more_status = json_objects['more']    #Check more status flag for data
	   
	   #If more status flag is true then proceed to parse json objects
	   if more_status == 1:
              for each_obj in json_objects['response']:
                  hd_flag = each_obj['flags']['hd']
                  if hd_flag == 1:   #Check hd flag set to true=1
                    count_flag_true += 1
                  elif hd_flag == 0: #Check hd flag set to false=0
                    count_flag_false += 1
           else:
               print "There is no data"
	  
    print "Total number of hd keys true for all 10 pages = ", count_flag_true
    print "Total number of hd keys false for all 10 pages = ", count_flag_false
	
#-----------------------------------------
# main
#-----------------------------------------
parse_json_objects()
