#!/usr/bin/python

import BeautifulSoup
import urllib
import hashlib
import os
import sys

IMGPATH = 'imgs'
maxDepth = 10

findPages = set()
visitedPages = set()
visitedPagesHash = set()

imgList = set()
imgHashList = set()
imglist = {}
imghashlist = {}
output = None

def addImage(img):
    if img in imgList :
        return
    imgList.add(img)
    try:
        d = urllib.urlopen(img)
    except:
        return
    imgdata = d.read()
    imgmd5 = hashlib.md5(imgdata).hexdigest()
    if imgmd5 in imgHashList :
        return
    imgHashList.add(imgmd5)

    if len(imgdata) < 10000:
        return

    output.write('<a href=%s>%s</a><br>\n'%(img,img))
    filename = img.split('/')[-1]

    if( len(filename) > 255 ):
        filename = filename[-100:]

    if not os.path.exists(IMGPATH) :
        os.makedirs(IMGPATH)

    new_path = '%s/%s_%s'%(IMGPATH,imgmd5,filename)
    f = open(new_path , 'w')
    f.write(imgdata)
    f.close()

def start( uri ):
    global findPages
    visitUri(uri)
    find_new = 1
    depth = 1
    while find_new == 1 and depth < maxDepth:
        find_new = 0
        toVisitPages = findPages 
        findPages = set()
        for page in toVisitPages :
            try:
                visitUri(page)
            except:
                pass
            find_new = 1
        depth += 1


def getBaseUri(uri):
    idx = uri.rfind('/')
    if idx == -1 :
        return uri
    return uri[:idx]

def getTopUri(uri):
    pidx = uri.find('://')
    uri2 = uri[pidx+3:]
    idx = uri2.find('/')
    if idx == -1 :
        return uri
    return '%s%s'%(uri[:pidx+3],uri2[:idx])

def visitUri ( uri ):
    if uri in visitedPages :
        return
    visitedPages.add(uri)

    try:
        d = urllib.urlopen(uri)
    except:
        return

    html = d.read()
    hash = hashlib.md5(html).hexdigest()
    if hash in visitedPagesHash :
        return
    visitedPagesHash.add(hash)

    print 'visit %s'%uri
    
    soup = None
    try:
        soup = BeautifulSoup.BeautifulSoup(html)
    except:
        return

    base_uri = getBaseUri(uri)
    top_uri = getTopUri(uri)
    links = soup.findAll('a')
    for link in links :
        if not link.has_key('href') :
            continue
        sub_uri = link['href']

        if sub_uri.lower().find('javascript') != -1 :
            continue
        if sub_uri.startswith('http://') :
            pass
        elif sub_uri.startswith('/'):
            sub_uri = '%s%s'%(top_uri,sub_uri)
        else:
            sub_uri = '%s/%s'%(base_uri, sub_uri)
        sub_top = getTopUri(sub_uri)
        if sub_top == top_uri : # check for external link
            if not sub_uri in visitedPages and not sub_uri in findPages:
                findPages.add(sub_uri)

    frames = soup.findAll('frame')
    for frame in frames:
        if not frame.has_key('src'):
            continue
        sub_uri = frame['src']

        if sub_uri.find('javascript') != -1 :
            continue
        if sub_uri.startswith('http://') :
            pass
        elif sub_uri.startswith('/'):
            sub_uri = '%s%s'%(top_uri,sub_uri)
        else:
            sub_uri = '%s/%s'%(base_uri, sub_uri)
        sub_top = getTopUri(sub_uri)
        if sub_top == top_uri : # check for external link
            if not sub_uri in visitedPages and not sub_uri in findPages:
                findPages.add(sub_uri)
                #print sub_uri
        
    imgs = soup.findAll('img')
    for img in imgs:
        if not img.has_key('src'):
            continue
        imglink = img['src']
        if imglink.startswith('http://'):
            pass
        elif imglink.startswith('/'):
            imglink = '%s%s'%(top_uri, imglink)
        else:
            imglink = '%s/%s'%(base_uri, imglink)
        addImage(imglink)

if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        print 'usage : %s url [outputdir] [logfile]'%sys.argv[0]
        sys.exit(0)
    url = sys.argv[1]
    logfile = 'img.html'
    if len(sys.argv) > 2 :
        IMGPATH = sys.argv[2] 
    if len(sys.argv) > 3 :
        logfile = sys.argv[3]
    
    output = open('img.html', 'w+')
    start(url)
    output.close()

