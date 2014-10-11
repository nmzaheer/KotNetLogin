import argparse
import base64
from bs4 import BeautifulSoup, Comment
import getpass
import os
import requests
import urllib
import urllib2

URL1 = "https://netlogin.kuleuven.be/cgi-bin/wayf2.pl"
URL2 = "https://netlogin.kuleuven.be/cgi-bin/netlogin.pl"
PATH = '/etc/kotnet.conf'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", help="Setup the account or change login credentials", action="store_true")
    args = parser.parse_args()
    if args.setup:
        set_account()
    else:
        auto_login()

def auto_login():
    payload = {'inst':'kuleuven', 'lang':'en', 'submit':'Ga verder / Continue'}
    s = requests.Session()
    r = s.get(URL1, params=payload)
    soup= BeautifulSoup(r.content)
    name = soup.find('input',{'type':'password'})['name']
    [userid, pwd] = get_details()
    encoded_data = urllib.urlencode({'inst':'kuleuven','lang':'en','uid':userid,name:pwd,'submit':'Login'})
    req = urllib2.Request(URL2, encoded_data)
    res = urllib2.urlopen(req)
    soup = BeautifulSoup(res.read())
    comment = soup.findAll(text=lambda text:isinstance(text, Comment) and "password verification successful" in text)
    if comment:
        print "Successfully logged into your Kotnet account"
    else:
        print "Unable to login. Try doing it manually"

def set_account():
    username = raw_input("Enter your username :")
    pwd = getpass.getpass()
    encoded_pwd = base64.b64encode(pwd)
    with open(PATH,'w') as doc:
        doc.write(username+":"+encoded_pwd)
        print "Login credentials saved successfully"

def get_details():
    with open(PATH,'r') as doc:
        [uid,pwd] = doc.read().split(':')
        pwd = base64.b64decode(pwd)
        return [uid,pwd]
        
if __name__ == '__main__':
    main()
