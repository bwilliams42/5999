'''
Created on Dec 3, 2013

@author: bwilliams
'''

import requests
import json

def clean(text):
    return text.encode('utf-8')

params = {'client_id': 'bb2707a8fd0145e6a3c06d455321c697'}
USERS_OVER_3000 = 0

def get_crossfit_user_from_media():
    global USERS_OVER_3000
    page = 1
    page_request_url = 'https://api.instagram.com/v1/tags/crossfit/media/recent'
    while True:
        resp = requests.get(page_request_url, params=params)
        if resp.status_code != requests.codes.OK:
            return None
        
        body = json.loads(resp.text)
        
        for media in body['data']:
            resp = requests.get('https://api.instagram.com/v1/users/{}'.
                                    format(media['user']['id']), params=params)
            
            if resp.status_code != requests.codes.ok:
                print 'something went wrong with request'
                print resp.text
                break
            user = json.loads(resp.text)['data']
            if user['counts']['followed_by'] >= 1000 and \
                bio_has_crossfit(user['bio']):
                USERS_OVER_3000 += 1
                follower_user(user)

        if 'pagination' in body and 'next_url' in body['pagination']:
            page_request_url = body['pagination']['next_url']
            page += 1
            print '--------page {}--------------'.format(page)
        else:
            break

def follower_user(user):
    print 'FOLLOWING..\nuser: {}\nbio: {}\nfollowers: {}'.format(user['username'],
                                                    clean(user['bio']),
                                                    user['counts']['followed_by'])
    

def bio_has_crossfit(bio):
    bio = bio.lower()
    if bio.find('crossfit') != -1:
        return True
    return False
    
if __name__ == '__main__':
    get_crossfit_user_from_media()
    print USERS_OVER_3000