import requests
import lxml.html as html
import copy
import pandas as pd
import time
import datetime


level_keywords = ['бакалав', 'магист', 'аспиран', 'доктор']
levels_eng = ['Bachelor', 'Master’s', 'PhD', 'PhD']
requirements_keywords = ['могут претендовать', 'Требования к кандидатам', 'студентам необходимо']
webresources_list = ["http://grantist.com/scholarships/vse-stipendii/"]
title_xp = './/h1[@class="entry-title"]'
address_xp = './/div[@class="entry-content"]/p[*[contains(text(), "Адрес")]]'
phone_xp = './/div[@class="entry-content"]/p[*[contains(text(), "Телефон")]]'
country_xp = './/p[span[@class="icon where"]]/a'
link_xp = './/a[contains(text(), "на") and contains(text(), "сайте")]/@href'
deadline_xp = 'substring-after(.//h4[contains(text(), "Дедлайн: ")], "Дедлайн: ")'
level_xp = './/div[@class="entry-content"]//*[contains(text(), "%s")]'
requirements_xp = './/*[contains(text(), "%s")]/following-sibling::*[1]/li'
img_url = './/div[@class="entry-content"]//img/@src'


"""Title	Country	Level	Deadline	Min. IELTS	Min. ibt TOEFL	ACT/SAT	GMAT/GRE	
Eligibility	Majors	Documents	Award	Number of Scholarships	Link to admissions
"""

headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",
            'Accept-Language': "en-US,en;q=0.5",
            'Content-Type': 'application/json; charset=utf-8'
        }

def main():
    scholarships = []
    scholarship = {'Title': '', 'Country': '', 'Phone': '', 'Address': '', 'Level': '', 'Deadline': '', 'Link': '',
                   'Requirements': ''}

    num = 9
    base_url = 'http://grantist.com/scholarships/vse-stipendii/page/'
    page_num = 1
    while page_num <= num:
        print('Page Number: %s' % page_num)
        resp = requests.get(base_url + str(page_num), headers=headers)
        page_num += 1
        tr = html.fromstring(resp.text)
        urls = tr.xpath('.//div[@class="site-content"]//h2[@class="entry-title"]/a/@href')
        for url in urls:
            resp = requests.get(url, headers=headers)
            if resp.ok:
                sc = copy.deepcopy(scholarship)
                tree = html.fromstring(resp.text)
                try:
                    title = tree.xpath(title_xp)[0].text_content().strip()
                    sc['Title'] = title
                except Exception as e:
                    print(e)
                try:
                    country = tree.xpath(country_xp)[0].text_content().strip()
                    sc['Country'] = country
                except Exception as e:
                    print(e)
                try:
                    phone = tree.xpath(phone_xp)[0].text_content().strip()
                    phone = phone.replace('Телефон', '').replace(':', '')
                    sc['Phone'] = phone
                except Exception as e:
                    print(e)
                try:
                    address = tree.xpath(address_xp)[0].text_content().strip()
                    address = address.replace('Адрес', '').replace(':', '')
                    sc['Address'] = address
                except Exception as e:
                    print(e)
                levels = []
                for i, level_keyword in enumerate(level_keywords):
                    level = tree.xpath(level_xp % level_keyword)
                    if len(level) > 0:
                        levels.append(levels_eng[i])
                levels = list(set(levels))
                if len(levels) > 0:
                    levels = ', '.join(levels)
                    sc['Level'] = levels

                deadline = tree.xpath(deadline_xp)
                if len(deadline) > 0:
                    deadline = deadline[0]
                    sc['Deadline'] = deadline
                link = tree.xpath(link_xp)
                if len(link) > 0:
                    link = link[0]
                    sc['Link'] = link
                for requirements_keyword in requirements_keywords:
                    reqs = tree.xpath(requirements_xp % requirements_keyword)
                    if len(reqs) < 1:
                        continue
                    requirements = [req.text_content().strip() for req in reqs]
                    requirements = '\n'.join(requirements)
                    sc['Requirements'] = requirements
                scholarships.append(sc)
                print(sc)
            else:
                print("Problems with getting a response from %s" % url)
    return scholarships


if __name__ == '__main__':
    res = main()
    df = pd.DataFrame(res)
    df.to_excel('%s.xlsx' % str(datetime.datetime.now().strftime('%m:%d:%Y:%H:%M')))
