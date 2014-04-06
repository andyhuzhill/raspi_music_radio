#!/usr/bin/env python
# *-* encoding: utf-8 *-* #
# =============================================
#      Author   : Andy Scout
#    Homepage   : http://andyhuzhill.github.com
#    E-mail     : andyhuzhill@gmail.com
#
#  Description  : This program play the online 
#                 music on douban.com
#  Revision     : 1.0
#
# =============================================

import urllib2
import urllib
import json
import sys
import os
import ConfigParser
from cookielib import CookieJar
import subprocess

child = subprocess.Popen

def saveToFile(fileName, content):
    file = open(fileName, 'wb')
    file.write(content)
    file.close()

def getPlayList(channel='0', opener=None):
    url = 'http://douban.fm/j/mine/playlist?type=n&channel=' + channel
    if opener == None:
        playlist = json.loads(urllib2.urlopen(url).read())
        return playlist
    else:
        playlist = json.loads(opener.open(urllib2.Request(url)).read())
        return playlist

def signIn(username, password):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar()))
    while True:
        print ('Geting verify code...')
        captcha_id = opener.open(urllib2.Request(
            'http://douban.fm/j/new_captcha')).read().strip('"')
        saveToFile('verify_code.jpg',
             opener.open(urllib2.Request('http://douban.fm/misc/captcha?size=m&id=' + captcha_id)).read())
        captcha = raw_input('Verify Code:')
        print 'Loging ... '
        response = json.loads(opener.open(
            urllib2.Request('http://douban.fm/j/login'),
            urllib.urlencode({
                'source': 'radio',
                'alias' : username,
                'form_password': password,
                'captcha_solution': captcha,
                'captcha_id' : captcha_id,
                'task':'sync_channel_list'})).read())
        if 'err_msg' in response.keys():
            print(response['err_msg'])
        else:
            print('Login success!')
            return opener

def getVerifyCode():
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar()))
    captcha_id = opener.open(urllib2.Request(
        'http://douban.fm/j/new_captcha')).read().strip('"')
    saveToFile('static/verify_code.jpg',
             opener.open(urllib2.Request('http://douban.fm/misc/captcha?size=m&id=' + captcha_id)).read())
    return captcha_id

def SignIn(username, passwd, verifycode_id, verifycode):
    print verifycode_id
    print verifycode
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(CookieJar()))
    response = json.loads(opener.open(
        urllib2.Request('http://douban.fm/j/login'),
        urllib.urlencode({
            'source': 'radio',
            'alias' : username,
            'form_password': passwd,
            'captcha_solution': verifycode,
            'captcha_id' : verifycode_id,
            'task':'sync_channel_list'})).read())
    if 'err_msg' in response.keys():
        print(response['err_msg'])
        return False, None
    else:
        print('Login success!')
        return True, opener


def getListLength(playlist):
    cnt = 0
    for item in playlist:
        cnt += 1
    return cnt

def getNItemOfList(playlist, num):
    cnt = 0
    for item in playlist:
        cnt += 1
        if cnt == num:
            return item

def playSongOfList(playlist, num=0):
    global child
    if num > getListLength(playlist['song']):
        return False, None, None
    else:
        song = getNItemOfList(playlist['song'], num) 
        print song
        try:
            child.kill()
            child = subprocess.Popen(['mpg123', song['url']])
        except Exception, e:
            child = subprocess.Popen(['mpg123', song['url']])
        return True, song, child

def play(channel='0', opener=None):
    while True:
        if opener == None:
            playlist = getPlayList(channel)
        else:
            playlist = getPlayList(channel, opener)

        if playlist['song'] == []:
            break

        for song in playlist['song']:
            picture = 'picture/' + song['picture'].split('/')[-1]

            saveToFile( picture,
                    urllib2.urlopen(song['picture']).read())

            print("Now is playing <%s> from [%s]"%(song['title'],song['artist']))

            cmd = 'mpg123 -q ' + song['url']

            os.system(cmd)



def main(argv):
    channel = '1'
    user = 'andyhuzhill@gmail.com'
    password = 'huZHIll!2#4'

    try:
        channel = argv[1]
    except Exception, e:
        channel = '0'

    print channel
    opener = signIn(user, password)
    opener = None
    play(channel)


if __name__ == '__main__':
    main(sys.argv)
