import requests
import lxml.html as html




webresources_list = ["http://grantist.com/scholarships/vse-stipendii/"]
title_xp = ''


def main():
    for webresource in webresources_list:
        resp = requests.get(webresource)
        if resp.ok:
            tree = html.fromstring(resp.text)
        else:
            print("Problems with getting a response from %s" % webresource)
            continue


if __name__ == '__main__':

    main()
