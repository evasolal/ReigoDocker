import sys, os
from flask import Flask, render_template,request,json, url_for, flash, request, session, redirect, Blueprint
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import Crawler
import process_db
import selenium


sys.dont_write_bytecode = True
ATTRIBUTES = ["ADDRESS","BEDROOMS", "BATHROOMS","SIZE","SOLD_ON","ZESTIMATE","WALK_SCORE","TRANSIT_SCORE", "GREAT_SCHOOLS"]

#Create our application
app = Flask(__name__)
app.config["DEBUG"] = True

#Def our home page
@app.route('/')
def home():
    return render_template('home.html')


#Get an address and return properties about this address, if the address is in Zillow database, else return "No information available"
@app.route('/', methods=['POST'])
def get_address_post():
    a = request.form.get('address')
    try :
        infos = Crawler.get_info(a)
        
        #Add the address to our database
        process_db.add_entrie([a]+infos)

        #Create Python Dict with the properties of the address
        properties = {"ADDRESS":a}
        for i in range(1, len(ATTRIBUTES)):
            properties[ATTRIBUTES[i]]=infos[i-1]
        return to_HTML(properties)
    except(selenium.common.exceptions.NoSuchElementException) :
        return "No information available"



#Return a html page with informations about the address
def to_HTML(dic):
    page = '<style> table, th, td {border : 1px solid black;}</style> <h2 style="color:red;"> Address Properties </h2>'
    page+= '<table style = "width:100%"><tr>'
    
    for k in dic.keys():
        page+='<th>' + k + '</th>'
    page+='</tr><tr>'
    for v in dic.values():
        page+='<td rowspan = "2">'+ str(v) +'</td>'
    page+='</tr></table>'
    return page
    
    
if __name__ == "__main__":
    app.run(host = "0.0.0.0")
