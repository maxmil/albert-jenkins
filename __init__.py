# -*- coding: utf-8 -*-

"""Opens Jenkins job"""

from albertv0 import *
from urllib import request, parse
import json
import os
# import ConfigParser

__iid__ = "PythonInterface/v0.2"
__prettyname__ = "Jenkins"
__version__ = "1.0"
__trigger__ = "j "
__author__ = "maxmil"
__dependencies__ = []

packageName="jenkins"
iconPath = "%s/headshot.png" % os.path.dirname(__file__)
baseurl = 'https://jenkins.timgroup.com'
user_agent = "org.albert.extension.python.%s" % packageName

# def initialize():
#     configDir = os.path.join(configLocation(), packageName)
#     confFile = os.path.join(configDir, "%s.conf" % packageName)
#     parser = ConfigParser.RawConfigParser()
#     parser.read(confFile)
# 
#     baseurl = parser.get('DEFAULT', baseUrl)
    
def handleQuery(query):
    if query.isTriggered:
    
       stripped = query.string.strip()
    
       if stripped:
           results = []
           params = {'tree': 'jobs[name]'}
           get_url = "%s/api/json?%s" % (baseurl, parse.urlencode(params))
           
           req = request.Request(get_url, headers={'User-Agent': user_agent})
    
           with request.urlopen(req) as response:
               data = json.loads(response.read().decode())
               jobs = data['jobs']
               for i in range(0, len(jobs)):
                   title = jobs[i]['name']
                   if stripped.lower() in title.lower():
                       url = "%s/job/%s" % (baseurl, title)
                       results.append(Item(id=__prettyname__,
                               icon=iconPath,
                               text=title,
                               subtext="Open job %s" % title,
                               completion=title,
                               actions=[
                                   UrlAction("Job", url),
                                   UrlAction("Last build", "%s/lastBuild/" % url),
                                   UrlAction("Last failed build", "%s/lastFailedBuild/" % url),
                                   UrlAction("Last successful build", "%s/lastSuccessfulBuild/" % url),
                                   UrlAction("Job configuration", "%s/configure" % url),
                                   ClipAction("Copy job URL", url)
                               ]))
           if results:
               return results
    
           return Item(id=__prettyname__,
               icon=iconPath,
               text="Search '%s'" % query.string,
               subtext="No job found matching %s" % query.string,
               completion=query.rawString,
               actions=[UrlAction("Open Jenkins", baseurl)])
       else:
           return Item(id=__prettyname__,
               icon=iconPath,
               text="Open Jenkins job",
               completion=query.rawString)

