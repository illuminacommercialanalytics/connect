# API
from typing import List
from typing import Optional
from fastapi import FastAPI

# General
import configparser
import pandas as pd
import time

# EXPORT TO GOOGLE SHEETS
import pygsheets
import gspread
from gspread_dataframe import get_as_dataframe

# Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# tabcmd
import os
import sys
import subprocess

### My Functions ###
# tableau login function
def tab_login(tabcmd_location, tabcmd_url, username, passwd): 
    try:
        p=subprocess.run('{0} login -s {1} -u {2} -p {3} -no-certcheck'\
        .format(os.path.join(os.path.normpath(tabcmd_location)), tabcmd_url, username, passwd ),shell=True)
        r=p.returncode
        return r
    except subprocess.SubprocessError as e:
        print(e)
        sys.exit(1)

# tableau logout function
def tab_logout(tabcmd_location):
    try:    
        p=subprocess.run('{0} logout'.format(os.path.join(os.path.normpath(tabcmd_location))),shell=True)         
    except subprocess.SubprocessError as e:
        print(e)
        sys.exit(1)
      
def getTabServData(tabcmd_location, whichdash, saveto, tab_serv_fname, username, passwd):
    command = '{0} get -t Commercial "{1}" -f "{2}" -u {3} -p {4} -no-certcheck'\
    .format(os.path.join(os.path.normpath(tabcmd_location)),\
    whichdash, saveto + tab_serv_fname + '.pdf', username, passwd)
    time.sleep(1) #delay number of seconds
    try:    
        p=subprocess.run(command, shell=True)
    except subprocess.SubprocessError as e:
        print(e)
        sys.exit(1)
    time.sleep(1) #delay number of seconds 



app = FastAPI(
    title="VTP - Send Email",
    description="A FastAPITableau app to send an email with attachment from the VTP dashboard.",
    version="0.1.0"
)


@app.get("/")
async def sendemail():
    #####
    ##### create rsconnect folder in prod
    #####
    command = 'whoami'  ###############################***********************
    p=subprocess.run(command, shell=True)
    