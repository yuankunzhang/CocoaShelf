# -*- coding: utf-8 -*-
import sys
from urllib2 import urlopen, URLError

from bs4 import BeautifulSoup

categories = (
    '658393051', '658394051', '658395051', '658396051',
    '658397051', '658398051', '658399051', '658400051',
    '658401051', '658402051', '658403051', '658404051',
    '658405051', '658406051', '658407051', '658408051',
    '658409051', '658410051', '658411051', '658412051',
    '658413051', '658414051', '658415051', '658416051',
    '658417051', '658418051', '658419051', '658420051',
    '658421051', '658422051', '658423051', '658424051',
    '658425051', '658426051', '658427051', '658428051',
    '658429051', '658430051', '658431051', '658432051',
    '658433051', '658434051', '658435051', '658436051',
    '658437051', '658438051', '1978287051', '2045366051',
)

max_year = 2013
min_year = 2000
dateop = 'during'

total = 0

file = open('records.txt', 'r+a')

for category in categories:
    for year in range(min_year, max_year+1)[::-1]:
        # skip what we've done
        if category == '658393051' and year > 2010:
            continue

        for month in range(1, 13)[::-1]:
            # skip what we've done
            if category == '658393051' and year == 2010 and month > 5:
                continue

            page = 1

            while (True):
                print '------------------------------------------------------------'
                print "Category: %s, Year: %d, Month: %d, Page: %d, Total: %d" \
                    % (category, year, month, page, total)
                print '------------------------------------------------------------'

                searchurl = 'http://www.amazon.cn/s/?search-alias=books&field-subjectbin=%s&field-dateyear=%d&field-datemod=%d&field-dateop=during&page=%d' % (category, year, month, page)

                try:
                    html_doc = urlopen(searchurl).read()
                except URLError:
                    print URLError
                    page += 1
                    continue

                soup = BeautifulSoup(html_doc, 'html.parser')
                titles = soup.find_all('div', class_='productTitle')
                if titles == []:
                    break

                for t in titles:
                    print t.a['href']
                    file.write(t.a['href'] + '\n')
                    total += 1

                if total >= 10000:
                    sys.exit(0)

                page += 1

file.write(total)
file.close()
