import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic.list import ListView

from .models import blogurls


###################################################
# VIEW
###################################################
def home(request):
    """ Shows a menu of views for the user to try """
    return render(request, 'solosandbox/index.html')


###################################################
# VIEW
###################################################
def homepagesoup(request):
    """ Demonstrates scraping posts from the home page"""
    try:
        r = requests.get("https://istayhomeandbakecookies.blogspot.com")
        soup = BeautifulSoup(r.text, 'html.parser')

        anchor_links = sorted(soup.find_all('a'), key=lambda elem: elem.text)
        counter = 0
        anchlinklist = ""  # will build a list of anchor text
        title = soup.title.text
        for anchlink in anchor_links:

            if anchlink.parent.name == 'h3':
                counter += 1
                anchlinklist = anchlinklist + str(anchlink) + "<br>"

        return render(request, 'solosandbox/homepagesoup.html',
                      {'title': title, 'mylist': anchlinklist, 'count': counter})
    except requests.ConnectionError:

        return render(request, 'solosandbox/error_page.html')


###################################################
# VIEW
###################################################
def getfeedchron(request):
    """ Demonstrates getting posts from the RSS Feed """
    global i
    import feedparser
    feed = (feedparser.parse(
        'https://istayhomeandbakecookies.blogspot.com/feeds/posts/default?start-index=1&max-results=1000'))
    feed_html = ""
    newfeed = list(feed.entries)
    for i, post in enumerate(newfeed):
        i = i + 1
        feed_html = feed_html + "<a href=" + post.link + ">" + post.title + "</a><br>"
    return render(request, 'solosandbox/getfeedchron.html', {'myfeed': feed_html, 'numposts': i})


###################################################
# VIEW
###################################################
def getfeedalpha(request):
    """ Demonstrates getting posts from the RSS Feed and alphabetizes them """
    global i
    import feedparser
    feed = (feedparser.parse(
        'https://istayhomeandbakecookies.blogspot.com/feeds/posts/default?start-index=1&max-results=1000'))
    feed_html = ""
    from operator import itemgetter
    newfeed = sorted(feed.entries, key=itemgetter('title'))
    for i, post in enumerate(newfeed):
        i = i + 1  # counting the recipes here
        feed_html = feed_html + " <a href=" + post.link + ">" + post.title + "</a> " + "<br>"
    return render(request, 'solosandbox/getfeedalpha.html', {'myfeed': feed_html, 'numposts': i})


###################################################
# VIEW
###################################################
""" This view uses the Google Blogger API to scrape all the posts. All I needed was an API key. 

I then wanted to write code in this view that would update each post with a print button, 
but I learned that an API key is not enough for updating a post. I would need an OAuth Client
ID, which turned out to be too complicated. So in the end, all this view does is fetch the
posts. See my experiments view called "request_one_post" for my attempts to update even just 
one post without an OAuth. It fails with a 401.

Info:
  #1) My Google API Dashboard is 
      https://console.developers.google.com/apis/credentials?pli=1&creatingProject=true&project=addprintbuttontoexistingposts&folder&organizationId
  #2) My Api key=AIzaSyAJUzDRE0vfQFXPMmJ52W6YNRgxkj_lmg
  #3) My Project Name is AddPrintButtonToExistingPosts
  #4) My Project ID is addprintbuttontoexistingposts
  #5) My recipe blog is 639737653225043728 (istayhomeandbakecookies.com)
  #6) Here's the code suggested by the API documentation:
      GET https://www.googleapis.com/blogger/v3/blogs/2399953/posts?key=YOUR-API-KEY
  #7) Here's my code. It works in the browser, too: 
      https://www.googleapis.com/blogger/v3/blogs/639737653225043728/posts?key=AIzaSyAJUzDRE0vfQFXPMmJ52W6YNRgxkj_lmg8
"""

"""
# Note: I had to lower the number of maxPosts above because the requests.get was throwing a server 500 error with too
 many posts. It
# turns out that requests is much slower than urllib.request.urlopen. This is because
# it doesn't use persistent connections: that is, it sends the header
# "Connection: close". This forces the server to close the connection immediately, so that TCP FIN comes quickly. 
You can reproduce
# this in Requests by sending that same header. Like this: r = requests.post(url=url, data=body, 
headers={'Connection':'close'})
#
# Note: I was able to improve the api call to fetchbodies = false, which speeds up the loading to some degree.
 Now I can allow for 200 posts
# instead of 100 posts. I have this fixed in bloggerapiget both in repl.it and in windows. I need to make the equivalent
 fix in the funwithmodels
# view.
"""


def bloggerapigetalpha(request):

    def request_by_year(edate, sdate):

        # Initially I did the entire request at once, but I had to chunk it into years because it was timing out in
        # windows.

        import json
        import requests



        url_part_1 = "https://www.googleapis.com/blogger/v3/blogs/639737653225043728/posts?endDate="
        url_part_2 = edate + "&fetchBodies=false&maxResults=500&startDate=" + sdate
        url_part_3 = "&status=live&view=READER&fields=items(title%2Curl)&key=AIzaSyDleLQNXOzdCSTGhu5p6CPyBm92we3balg"
        url=url_part_1 + url_part_2 + url_part_3





        r = requests.get(url, stream=True)
        q = json.loads(r.text)  # this is the better way to unstring it
        if not q:
            s = []
        else:
            s = q['items']

        return s

    accum_list = []
    import datetime as d
    c_year = int(d.datetime.now().year)

    for the_year in range(2014, c_year + 1):
        enddate = str(the_year) + "-12-31T00%3A00%3A00-00%3A00"
        startdate = str(the_year) + "-01-01T00%3A00%3A00-00%3A00"

        t = request_by_year(enddate, startdate)
        accum_list = accum_list + t

    from operator import itemgetter
    sorteditems = sorted(accum_list, key=itemgetter('title'), reverse=True)
    counter = 0
    newstring = " "
    for mylink in sorteditems:
        counter += 1
        newstring = "<a href=" + mylink['url'] + ">" + mylink['title'] + "</a>" + "<br>" + newstring

    return render(request, 'solosandbox/bloggerapigetalpha.html', {'allofit': newstring, 'count': counter})


###############################
# BLOGGERAPIGETCHRON
###############################


# Note: I had to lower the number of maxPosts above because the requests.get was throwing a server 500 error with too many posts. It
# turns out that requests is much slower than urllib.request.urlopen. This is because
# it doesn't use persistent connections: that is, it sends the header
# "Connection: close". This forces the server to close the connection immediately, so that TCP FIN comes quickly. You can reproduce
# this in Requests by sending that same header. Like this: r = requests.post(url=url, data=body, headers={'Connection':'close'})
#
# Note: I was able to improve the api call to fetchbodies = false, which speeds up the loading to some degree. Now I can allow for 200 posts
# instead of 100 posts.
def bloggerapigetchron(request):
    def request_by_year(edate, sdate):
        # Initially I did the entire request at once, but I had to chunk it into years because it was timing out in windows.

        import json
        import requests
        url = "https://www.googleapis.com/blogger/v3/blogs/639737653225043728/posts?endDate=" + edate + "&fetchBodies=false&maxResults=500&startDate=" + sdate + "&status=live&view=READER&fields=items(title%2Curl)&key=AIzaSyDleLQNXOzdCSTGhu5p6CPyBm92we3balg"
        r = requests.get(url, stream=True)
        q = json.loads(r.text)  # this is the better way to unstring it
        if not q:
            s = []
        else:
            s = q['items']
        return (s)

    accum_list = []

    import datetime as d
    c_year = int(d.datetime.now().year)
    for the_year in range(2014, c_year + 1):
        enddate = str(the_year) + "-12-31T00%3A00%3A00-00%3A00"
        startdate = str(the_year) + "-01-01T00%3A00%3A00-00%3A00"
        t = request_by_year(enddate, startdate)
        accum_list = t + accum_list

    # from operator import itemgetter
    # sorteditems=sorted(accum_list,  key=itemgetter('title'), reverse=True)
    counter = 0
    newstring = " "
    for mylink in accum_list:
        counter += 1
        newstring = "<a href=" + mylink['url'] + ">" + mylink['title'] + "</a>" + "<br>" + newstring

    # return render(request, 'solosandbox/bloggerapigetchron.html', {'allofit': t})
    return render(request, 'solosandbox/bloggerapigetchron.html', {'allofit': newstring, 'count': counter})


###################################################
# Get posts by label This is hardcoded
###################################################

def get_recipe_by_label(request):
    import feedparser
    feed_html = ""
    thestart = 'https://www.blogger.com/feeds/639737653225043728/posts/default/-'
    thelabels = '/Sour Cream/Indian/'
    therest = '?start-index=1&max-results=1000'
    thelink = thestart + thelabels + therest
    # Here's how to construct it:'https://www.blogger.com/feeds/639737653225043728/posts/default/-/Indian/Non-dairy/?start-index=1&max-results=1000'
    from requests.utils import requote_uri
    newurl = (requote_uri(thelink))
    tempfeed = (feedparser.parse(newurl))

    # from operator import itemgetter
    # feed.entries is a list of dictionaries. Below I'm sorting by title using itemgetter. Alternatively,
    # I could have sorted using lambda, but couldn't figure it out.
    newfeed = list(tempfeed.entries)

    i = 0
    for i, post in enumerate(newfeed):
        i = i + 1
        feed_html = feed_html + "<p><a href=" + post.link + ">" + post.title + "</a></p>"
    return render(request, 'solosandbox/get_recipe_by_label.html', {'myfeed': feed_html, 'numposts': i})


#
###################################################
# ERRORS: puts up a generic error page
###################################################
def errors(request):
    return (render(request, 'solosandbox/error_page.html'))


########################################################
# Show Label List#
########################################################
def show_label_list(request):
    try:
        labelstring = "<table><br><br>"
        dictmap = dict()
        r = requests.get("https://istayhomeandbakecookies.blogspot.com")
        soup = BeautifulSoup(r.text, 'html.parser')
        somehtml = soup.find("div", {"class": "widget Label"})
        for num, label in enumerate(somehtml.find_all('a'), start=1):
            if not (str(label.text[0])).isalnum():           break  # the last label is a long blank!
            labelstring = labelstring + "<td>" '''<input type="checkbox" name="label" value=''' + str(num) + ">" + str(
                label.text) + "    " + "</td>"

            if num % 5 == 0 and num != 0:
                labelstring = labelstring + "</tr><tr>"
            dictmap[num] = str(label.text)
            labelstring = labelstring
        # put a blank before submit button
        labelstring = labelstring + "</table>"
        labelstring = labelstring + '<br>' '''<input type="hidden" name="dictmap" value=''' + str(dictmap) + ">"
        labelstring = labelstring + '<input type="submit" value="Send Your Choices">'

        title = soup.title.text
        return render(request, 'solosandbox/show_label_list.html',
                      {'title': title, 'mylist': labelstring, 'dictmap': dictmap})
    except requests.ConnectionError:
        return render(request, 'solosandbox/error_page.html')


######################################################################
# Purpose: See what boxes the user checked and display all the recipes
#
######################################################################
def showallrecipeschosen(request):
    import feedparser
    from operator import itemgetter
    getchosenlabels = request.POST.getlist('label')
    labeldict = (request.POST.getlist('dictmap'))

    import ast
    newdict = ast.literal_eval(labeldict[0])

    userchoices = ""
    thelabels = "/"
    thestart = ""
    for choice in getchosenlabels:
        intchoice = int(choice)
        newstring = str(newdict[intchoice])
        # newstring=newstring.replace(" ", "%20") # I improved this. See the next two lines.
        from requests.utils import requote_uri
        newstring = requote_uri(newstring)

        # Some labels are two words such as corned beef
        userchoices = userchoices + newstring
        thelabels = thelabels + newstring + '/'
        # thelabels='/Indian/Non-dairy/'
        thestart = 'https://www.blogger.com/feeds/639737653225043728/posts/default/-'
    # thelabels=thelabels+ "\'"
    therest = '?start-index=1&max-results=1000'
    thelink = thestart + thelabels + therest

    tempfeed1 = (feedparser.parse(thelink))

    tempfeed2 = sorted(tempfeed1.entries, key=itemgetter('title'))

    newfeed = list(tempfeed2)

    i = 0
    feed_html = ""
    for i, post in enumerate(newfeed):
        i = i + 1
        feed_html = feed_html + "<p><a href=" + post.link + ">" + post.title + "</a></p>"

    return render(request, 'solosandbox/showallrecipeschosen.html',
                  {'checkthem': getchosenlabels, 'getdict': feed_html, 'numposts': i})


####################################################
# Work with models
# This starts out as a dupe of bloggerapiget
###################################################
def modelfun(request):
    def request_by_year(edate, sdate):
        # Initially I did the entire request at once, but I had to chunk it into years because it was timing out in windows.
        import json
        import requests
        url = "https://www.googleapis.com/blogger/v3/blogs/639737653225043728/posts?endDate=" + edate + "&fetchBodies=false&maxResults=500&startDate=" + sdate + "&status=live&view=READER&fields=items(title%2Curl)&key=AIzaSyDleLQNXOzdCSTGhu5p6CPyBm92we3balg"
        r = requests.get(url, stream=True)
        q = json.loads(r.text)  # this is the better way to unstring it
        if not q:
            s = []
        else:
            s = q['items']

        return (s)

    accum_list = []
    import datetime as d
    c_year = int(d.datetime.now().year)

    for the_year in range(2014, c_year + 1):
        enddate = str(the_year) + "-12-31T00%3A00%3A00-00%3A00"
        startdate = str(the_year) + "-01-01T00%3A00%3A00-00%3A00"
        t = request_by_year(enddate, startdate)
        accum_list = accum_list + t

    from operator import itemgetter
    sorteditems = sorted(accum_list, key=itemgetter('title'), reverse=True)
    counter = 0
    newstring = " "
    for mylink in sorteditems:
        counter += 1
        newstring = "<a href=" + mylink['url'] + ">" + mylink['title'] + "</a>" + "<br>" + newstring

    # newstring = "<a href="+ mylink['url'] + ">" + mylink['title'] + "</a>"  + "<br>"
    from .models import blogurls
    myblogurls = blogurls(website=newstring, numurls=counter)
    blogurls.objects.all().delete()  # delete what was there
    myblogurls.save('website')  # This performs a SQL insert
    return render(request, 'solosandbox/modelfun.html', {'allofit': newstring, 'count': counter})


####################################################
# Now retrieve the urls in the model using a function-based view
####################################################

def get_the_model_data(request):
    from .models import blogurls
    instance = blogurls.objects.values_list('website', flat=True).distinct()
    counter = blogurls.objects.values_list('numurls', flat=True).distinct()
    return render(request, 'solosandbox/get_the_model_data.html', {'allofit': instance[0], 'counter': counter[0]})


####################################################
# Now retrieve the models using class-based views (ListView)
####################################################
class ModelList(ListView):

    model = blogurls # This tells Django what model to use for the view
    context_object_name = 'all_model_recipes' # This tells Django what to name the queryset


################
# ROTO EXPERIMENT
################
def roto(request):
    """ Demonstrates scraping posts from the home page"""
    try:
        payload = {'userid': 'mikemorannj1', 'password': '0yZo092fJx'}
        first_half="https://www.cbssports.com/login?product_abbrev=mgmt&xurl=http%3A%2F%2"
        second_half="Fmoran.baseball.cbssports.com%2F&master_product=25924"
        form_url=first_half+second_half

        login_url = "https://www.cbssports.com/login"
        protectedurl = "https://moran.baseball.cbssports.com"
        with requests.Session() as s:
            p = s.get(form_url)
            q = s.post(login_url, data=payload)
            r = s.get(protectedurl)
            soup = BeautifulSoup(r.content, 'html.parser')

            title = soup.title.text

            return render(request, 'solosandbox/roto.html',
                          {'history': r.history, 'title': title, 'thepage': soup, 'count': r.status_code})
    except requests.ConnectionError:

        return render(request, 'solosandbox/error_page.html')
