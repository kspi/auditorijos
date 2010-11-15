#!/usr/bin/env python2
# -*- coding: utf-8-unix -*-

import hours
import urllib2
from BeautifulSoup import BeautifulSoup

def hours_aud(aud):
    """Grąžina užimtumą pagal auditorijos pavadinimą."""
    url = 'http://kedras.mif.vu.lt/tvark/?type=auditor&anr=%s' \
        % urllib2.quote(aud)
    doc = urllib2.urlopen(url)
    return hours.get_hours(doc)

def visos_aud():
    """Visų auditorijų sąrašas."""
    doc = urllib2.urlopen('http://kedras.mif.vu.lt/tvark/?type=auditorija')
    soup = BeautifulSoup(doc)
    ul = soup.find('ul')
    return [li.next.contents[0] for li in ul.findAll('li')]

def get_data():
    """Sąrašas porų [auditorijos pavadinimas, užimtumas]."""
    return [[aud, hours_aud(aud)] for aud in visos_aud()]

# Įrašome visus duomenis į bylą vėlesniam naudojimui (kad nereikėtų
# veltui apkrauti tvarkaraščių serverio):
with file('dump.txt', 'w') as f:
    f.write(repr(get_data()))
