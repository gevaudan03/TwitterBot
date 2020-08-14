#Twitter Bot
#Author: Haojie Xu

import email
import imaplib
from bs4 import BeautifulSoup
import email.parser
import tweepy
import time

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

#login to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

#below is the API that talks to Twitter
api = tweepy.API(auth)

#Gmail credidential
username = ''
password = ''

#connect to gmail and login with login informations
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)

#print(mail.list())
mail.select("ConcreteandMortar")

#use the uni function, and pass in the string of the command as the first argument
#uid is unique identification for the item, each mail has its unique ID
#keyword "ALL" is used to get all results doncumented in RFC3501
result, data = mail.uid('search', None, "ALL")

#split() function splits string at a place, by default is any white space
#[-1] is the newest email in the list
inbox_item_list = data[0].split()
#print(inbox_item_list)
lastest_email_uid = inbox_item_list[-1]

#fetch the data for the latest email body
result2, data = mail.uid('fetch', lastest_email_uid, '(RFC822)')

#it's a mime format, can't use it directly as html yet
raw_email = data[0][1].decode("utf-8")

#the following lines check if the raw_email is mutlipart
b = email.message_from_string(raw_email)
if b.is_multipart():
    for part in b.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))

#not multipart, plain text, no attacments
else:
    body = b.get_payload(decode=True)

#create BeautifulSoup object and pass our email_message into the parameter to work with, don't worry aboiut 'lxml'
soup = BeautifulSoup(body, 'lxml')

#finds all h3 tags in the soup object and store them inside of the variable h3_list
h3_list = soup.find_all('h3')

def parse_to_title(article):
    article = article
    link = str(article.find('a')['href']).replace('&html=', '')
    str_0 = str(article).replace('style="font-size:17px;color:#1a0dab">', "")
    str_1 = str_0.replace('<h3 style="font-weight:normal;margin:0;font-size:17px;line-height:20px;"><a class="gse_alrt_title" href="', '')
    str_2 = str_1.replace('<b>', '')
    str_3 = str_2.replace('</b>', '')
    str_4 = str_3.replace('</a>', '')
    str_5 = str_4.replace('</h3>', '')
    str_6 = str_5.replace('&amp;html=" ', '')
    str_7 = str_6.replace('amp;', '')
    str_8 = str_7.replace(link, '')
    return str_8

def tweet_message(h3_list):
    h3_list = h3_list
    for x in range(len(h3_list)):
        url = h3_list[x].find('a')['href']
        title = parse_to_title(h3_list[x])
        api.update_status('New #durability #research on: "' + title + '" has been #published. For more information, please check out: ' + url)
        print(url)
        print(title)
        print("tweeted successfully")
        time.sleep(300)

tweet_message(h3_list)




