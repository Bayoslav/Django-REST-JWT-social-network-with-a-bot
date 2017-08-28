import json
from config import number_of_users,max_posts_per_user,max_likes_per_user,register
import requests
import sys
import random
content = []
#from BeautifulSoup import bs4 as bs
#import lorem
print(number_of_users)
print(max_posts_per_user)

for i in range(0,number_of_users,1):
    username = 'TestUser0' + str(i)
    email = 'gaming4ever93@gmail.com'
    data = {
        'username' : username,
        'email' : email,
        'password' : 'password',
    } #POSTDATA
    if(register):
        r = requests.post('http://127.0.0.1:8000/api/register/', data=data)
        print("Registering")
    print("Logging in")
    r = requests.post('http://127.0.0.1:8000/api/login/', data=data)
    token = (r.text[10:-2])
    print("Getting the token")
    token = 'JWT ' + token
    print(token)
    headers = {'Authorization': token}
    rand = random.randint(1,max_posts_per_user)
    for j in range(0,rand,1):
        userdict = {
        'username' : username,
        'postnum' : rand,
        }
        title = "Post_0" + str(i) + str(j)
        postdata = {
        'title' : title,
        'text' : 'LoremIpsum',
        }
        print("Making a post")
        r=requests.post('http://127.0.0.1:8000/api/posts/', data=postdata, headers=headers)
    content.append(userdict)
newlist = sorted(content,key=lambda k: k['postnum'], reverse=True)
print(newlist)

def like(username):
    email = 'gaming4ever93@gmail.com'
    data = {
        'username' : username,
        'email' : email,
        'password' : 'password',
    }
    r = requests.post('http://127.0.0.1:8000/api/login/', data=data)
    token = (r.text[10:-2])
    token = 'JWT ' + token
    #print(token)
    headers = {'Authorization': token}
    b=requests.get('http://127.0.0.1:8000/api/posts/', headers=headers)
    dzejson = b.json()
    #print(dzejson) #for testing
    userurl = 'http://127.0.0.1:8000/api/users/?username=' + username
    user = requests.get(userurl)
    userjson = user.json()
    m=0
    counter=0
    for iterate in dzejson: #Iterating over JSON post list
        counter=counter+1
        if(m<max_likes_per_user): #m defines the current number of  users likes
            if(iterate['likers']==[]):
                post_id = str(iterate['id'])
                #sending likes through GET
                if(iterate['creator']==userjson['id']): #prevents the bot from liking his own post
                    continue
                else:
                    r=requests.get('http://127.0.0.1:8000/api/like/?postid='+ post_id + '&like=true', headers=headers)
                    m=m+1
            else:
                if(counter==len(dzejson)):
                   sys.exit()

#adding likes
for dic in newlist: #gets the dictionary in the list of dictionaries newlist
    username = dic['username'] #extracts the username from the dictionary
    like(username) #calls like method/function
