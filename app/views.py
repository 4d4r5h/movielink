from django.shortcuts import render, HttpResponse
from bs4 import BeautifulSoup as bs  # pip install beautifulsoup4
from urllib.request import Request, urlopen
import requests  # pip install requests
from googlesearch import search  # pip install google
from selenium import webdriver  # pip install selenium
from decouple import config  # pip install python-decouple
# pip install webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Create your views here.


def nollyverse(name):
    query = "site:nollyverse.com/movie download " + name.strip()
    url = ""
    try:
        for result in search(query, tld="com", num=10, stop=10, pause=2):
            if "www.nollyverse.com" in result:
                url = result
                break
        if url == "":
            return [["Nollyverse has no such movie.", 0, 0]]
        if "/download/" not in url:
            url = url + "/download/"
    except:
        try:
            query = (name + " download").strip().replace(" ", "%20")
            cx = config('cx_nollyverse', default='')
            key = config('key', default='')
            url = f"https://customsearch.googleapis.com/customsearch/v1?cx={cx}&gl=in&num=10&q={query}&key={key}"
            headers = {'Accept': 'application/json'}
            req = requests.get(url=url, headers=headers)
            content = req.json()
            for result in content["items"]:
                if "www.nollyverse.com" in result["link"]:
                    url = result["link"]
                    break
            if url == "":
                return [["Nollyverse has no such movie.", 0, 0]]
            if "/download/" not in url:
                url = url + "/download/"
        except:
            return [["Google API is currently not working.", 0, 0]]
    page = None
    try:
        req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
    except:
        return [["Unable to load the Nollyverse URL.", 0, 0]]
    else:
        soup = bs(page, features="html.parser")
        download = None
        try:
            download = soup.find(
                "table", class_="table table-striped").tbody.find_all("tr")
        except:
            return [["Nollyverse has no links for the given movie.", 0, 0]]
        else:
            links = []
            other = ""
            try:
                other = soup.find("p", class_="lead").text.strip()
            except:
                other = "No additional information available."
            try:
                image = soup.find(
                    "div", class_="page-header-bg")["style"][23:-3]
                links.append([image, 2, other])
            except:
                links.append(["/static/error-loading-image.png", 2, other])
            try:
                for link in download:
                    text = ""
                    try:
                        text = link.td.text.strip()
                        text = text + " - "
                    except:
                        pass
                    links.append(
                        [link.find("td", class_="text-right").a["href"], 1, text])
                return links
            except:
                return [["Nollyverse has no links for the given movie.", 0, 0]]
    return


def fzmovies(name):
    # return [["Couldn't fetch links from FZMovies due to some probelm with Selenium.", 0, 0]]

    # https://mixedanalytics.com/blog/seo-data-google-custom-search-json-api/
    url = "https://www.fzmovies.net/"
    try:
        r = requests.get(url=url, timeout=10, headers={
                         'User-Agent': 'Mozilla/5.0'})
    except:
        return [["Unable to load FZMovies. Try using VPN.", 0, 0]]
    query = name.strip().replace(" ", "%20")
    cx = config('cx_fzmovies', default='')
    key = config('key', default='')
    url = f"https://customsearch.googleapis.com/customsearch/v1?cx={cx}&gl=in&num=10&q={query}&key={key}"
    # print(url)
    headers = {'Accept': 'application/json'}
    try:
        req = requests.get(url=url, headers=headers)
        content = req.json()
        url = ""
        for result in content["items"]:
            if "fzmovies.net/movie-" in result["link"] and result["link"].endswith(".htm"):
                url = result["link"]
                if "--hmp4" not in url:
                    url = url[:-4]+"--hmp4"+url[-4:]
                break
        if url == "":
            return [["FZMovies has no such movie.", 0, 0]]
    except:
        return [["Google API is currently not working.", 0, 0]]

    # proxies = { 'http': "http://ip:port",    # can open banned sites, but no javascript rendering
    #           'https': "http://ip:port"}
    # page = requests.get(url=url, headers={'User-Agent':'Mozilla/5.0'}, proxies=proxies).text

    # prox = Proxy()    # can render javascript, but can't open banned sites
    # prox.proxy_type = ProxyType.MANUAL
    # prox.http_proxy = "http://ip:port"
    # prox.socks_proxy = "https://ip:port"
    # prox.ssl_proxy = "https://ip:port"
    # prox.socks_version = 5
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # prox.add_to_capabilities(capabilities)

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        browser.get(url)
        page = browser.page_source
    except:
        return [["Either Selenium is not working or a wrong link was fetched.", 0, 0]]
    soup = bs(page, features="html.parser")
    links = []
    other = ""
    try:
        other = soup.find("div", class_="moviename").span.text.strip()
    except:
        other = "No additional information available."
    try:
        image = "https://fzmovies.net" + \
            soup.find("div", class_="moviedesc").span.img["src"]
        links.append([image, 2, other])
    except:
        links.append(["/static/error-loading-image.png", 2, other])
    try:
        download = soup.find_all("a", id="downloadoptionslink2")
    except:
        return [["FZMovies has no links for the given movie.", 0, 0]]
    flag = True
    for url in download:
        text = ""
        try:
            text = url.text.strip() + " - "
        except:
            pass
        try:
            url = "https://fzmovies.net/" + url["href"]
            browser.get(url)
            page = browser.page_source
        except:
            continue
        soup = bs(page, features="html.parser")
        try:
            link = "https://fzmovies.net/" + \
                soup.find("a", id="streamlink")["href"]
            links.append([link, 1, text+"Stream - "])
            flag = False
        except:
            pass
        try:
            url = "https://fzmovies.net/" + \
                soup.find("a", id="downloadlink")["href"]
            browser.get(url)
            page = browser.page_source
        except:
            continue
        soup = bs(page, features="html.parser")
        try:
            # link = soup.find_all("a")
            # for x in link:
            #     if x["href"].startswith("dlink.php?"):
            #         xtext = ""
            #         try:
            #             xtext = x.text.strip() + " - "
            #         except:
            #             pass
            #         links.append(["https://fzmovies.net/" +
            #                      x["href"], 1, text+xtext])
            #         flag = False
            link = soup.find_all("input", {"name": "download1"})
            for x in link:
                links.append([x["value"], 1, text])
                flag = False
        except:
            pass
    browser.quit()
    if flag:
        return [["FZMovies has no links for the given movie.", 0, 0]]
    else:
        return links


def mkvking(name):
    url = "https://84.46.254.230/?s=movie+"+name.strip().replace(" ", "+")
    try:
        req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
    except:
        return [["Unable to load the MKVKing URL.", 0, 0]]
    else:
        soup = bs(page, features="html.parser")
        try:
            url = soup.find(
                "article", class_="col-md-20 item has-post-thumbnail").a["href"]
        except:
            return [["MKVKing has no such movie.", 0, 0]]
        try:
            req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
        except:
            return [["Unable to load the MKVKing URL.", 0, 0]]
        else:
            soup = bs(page, features="html.parser")
            links = []
            other = ""
            try:
                other = soup.find("h1", class_="entry-title").text.strip()
            except:
                other = "No additional information available."
            try:
                image = soup.find(
                    "div", class_="gmr-movie-data clearfix").figure.img["src"]
                links.append([image[:-10]+".jpg", 2, other])
            except:
                links.append(["/static/error-loading-image.png", 2, other])
            try:
                download = soup.find(
                    "ul", class_="list-inline gmr-download-list clearfix").find_all("li")
                for link in download:
                    text = ""
                    try:
                        text = link.a.text.strip()
                        text = text + " - "
                    except:
                        pass
                    links.append([link.a["href"], 1, text])
                return links
            except:
                return [["MKVKing has no links for the given movie.", 0, 0]]
    return


def skymovieshd(name):
    url = "https://skymovieshd.boats/search.php?search=" + \
        name.strip().replace(" ", "+") + "&cat=All"
    try:
        req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
    except:
        return [["Unable to load the SkyMoviesHD URL.", 0, 0]]
    else:
        soup = bs(page, features="html.parser")
        try:
            url = "https://skymovieshd.boats" + soup.find(
                "div", class_="L").b.a["href"]
        except:
            return [["SkyMoviesHD has no such movie.", 0, 0]]
        try:
            req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
        except:
            return [["Unable to load the SkyMoviesHD URL.", 0, 0]]
        else:
            soup = bs(page, features="html.parser")
            links = []
            other = ""
            try:
                other = soup.find("div", class_="Robiul").text.strip()
            except:
                other = "No additional information available."
            try:
                image = soup.find(
                    "div", class_="movielist").img["src"]
                links.append([image, 2, other])
            except:
                links.append(["/static/error-loading-image.png", 2, other])
            try:
                download = soup.find("div", class_="Bolly").find_all("a")
                for link in download:
                    if len(link["href"]) > 0:
                        text = ""
                        try:
                            text = link.text.strip()
                            text = text + " - "
                        except:
                            pass
                        links.append([link["href"], 1, text])
                newlinks = []
                for link in links:
                    if link not in newlinks:
                        newlinks.append(link)
                return newlinks
            except:
                return [["SkyMoviesHD has no links for the given movie.", 0, 0]]
    return


def megaddl(name):
    url = "https://megaddl.co/?s=" + name.strip().replace(" ", "+")
    try:
        req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
    except:
        return [["Unable to load the MegaDDL URL.", 0, 0]]
    else:
        soup = bs(page, features="html.parser")
        url = ""
        try:
            urls = soup.find_all("div", class_="post-thumbnail")
            for x in urls:
                if "megaddl.co/tv-show/" not in x.a["href"]:
                    url = x.a["href"]
                    break
        except:
            return [["MegaDDL has no such movie.", 0, 0]]
        if url == "":
            try:
                url = soup.find("div", class_="post-thumbnail").a["href"]
            except:
                return [["MegaDDL has no such movie.", 0, 0]]
        try:
            req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
        except:
            return [["Unable to load the MegaDDL URL.", 0, 0]]
        else:
            soup = bs(page, features="html.parser")
            links = []
            other = ""
            try:
                look = ["h1", "post-title entry-title"]
                if "/movies/" in url:
                    look = ["div", "page-title hu-pad group"]
                other = soup.find(look[0], class_=look[1]).text.strip()
            except:
                other = "No additional information available."
            try:
                image = soup.find(
                    "div", class_="image-container").img["data-src"]
                links.append([image, 2, other])
            except:
                links.append(["/static/error-loading-image.png", 2, other])
            try:
                download = soup.find_all("a")
                sites = ["filecrypt.cc", "mega.nz", "go4up.com", "1fichier.com", "rapidgator.net",
                         "nitroflare.com", "openload.co", "multiup.org", "ouo.io"]
                flag = True
                for link in download:
                    try:
                        url = link["href"]
                    except:
                        pass
                    else:
                        text = ""
                        try:
                            text = link.text.strip() + " - "
                        except:
                            pass
                        for site in sites:
                            if site in url:
                                flag = False
                                links.append([url, 1, text])
                                break
                            else:
                                try:
                                    if "download" in link.text.lower() and "how-to-download" not in url:
                                        flag = False
                                        links.append([url, 1, text])
                                except:
                                    pass
                if flag:
                    return [["MegaDDL has no links for the given movie.", 0, 0]]
                else:
                    newlinks = []
                    for link in links:
                        if link not in newlinks:
                            newlinks.append(link)
                    return newlinks
            except:
                return [["MegaDDL has no links for the given movie.", 0, 0]]
    return


def index(request):
    if request.method == "POST":
        name = request.POST.get("name").strip()
        year = request.POST.get("year").strip()
        other = request.POST.get("other").strip()
        link = request.POST.get("link")
        context = {}
        if link == "1":
            context['nollyverse'] = nollyverse(name + " " + year + " " + other)
            context['fzmovies'] = fzmovies(name + " " + year + " " + other)
            return render(request, 'direct_result.html', context)
        else:
            context['mkvking'] = mkvking(name + " " + year)
            context['skymovieshd'] = skymovieshd(name)
            context['megaddl'] = megaddl(name + " " + year + " " + other)
            return render(request, 'indirect_result.html', context)
    return render(request, 'index.html')
