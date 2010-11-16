# -*- coding: utf-8-unix -*-

import urllib2
import re
import pickle
from BeautifulSoup import BeautifulSoup

def _get_times(row):
    t = row.next
    from_hours = int(t.contents[0])
    from_minutes = int(t.contents[1].contents[0])
    to_hours = int(t.contents[2][13:])
    to_minutes = int(t.contents[3].contents[0])
    return (from_hours,
            from_minutes,
            to_hours,
            to_minutes)

TAKEN_ODD = 1
TAKEN_EVEN = 2
TAKEN_ALWAYS = 3

_weekre = re.compile(r'\( ([12]) \)')
def _get_week(row):
    text = ''.join(map(unicode, row.contents[1].contents))
    try:
        return int(re.findall(_weekre, text)[0])
    except IndexError:
        return TAKEN_ALWAYS

class Lecture:
    def __init__(self, row):
        (from_h, from_m, to_h, to_m) = _get_times(row)
        week = _get_week(row)
        self.from_h = from_h
        self.from_m = from_m
        self.to_h = to_h
        self.to_m = to_m
        self.week = week

    def taken_hours(self):
        """Grąžina sąrašą valandų, kuriomis auditorija yra užimta."""
        start = self.from_h
        end = self.to_h
        if self.to_m != 0:
            end = end + 1
        return range(start, end)
    
class Day:
    def __init__(self):
        self.taken = {}

    def take_hours(self, lecture):
        for hour in lecture.taken_hours():
            if (lecture.week == TAKEN_ALWAYS) or (not self.taken.has_key(hour)):
                self.taken[hour] = lecture.week
            elif lecture.week == TAKEN_ODD:
                if self.taken[hour] == TAKEN_EVEN:
                    self.taken[hour] = TAKEN_ALWAYS
                elif not self.taken[hour]:
                    self.taken[hour] = TAKEN_ODD
            elif lecture.week == TAKEN_EVEN:
                if self.taken[hour] == TAKEN_ODD:
                    self.taken[hour] = TAKEN_ALWAYS
                elif not self.taken[hour]:
                    self.taken[hour] = TAKEN_EVEN

    def pr(self):
        print self.taken
                    
    def get_status(self, hour):
        """Grąžina True, jei auditorija tą valandą užimta visada, 1
        jei nelyginėmis savaitėmis, 2 jei lyginėmis savaitėmis ir
        False, jei neužimta."""
        return self.taken.get(hour, False)

class Aud:
    def __init__(self):
        self.days = {}

    def take_hours(self, day, lecture):
        if not self.days.has_key(day):
            self.days[day] = Day()
        self.days[day].take_hours(lecture)

    def pr(self):
        for day in self.days:
            print day
            self.days[day].pr()

    def get_status(self, day, hour):
        try:
            return self.days[day].get_status(hour)
        except KeyError:
            return False
        
def get_week_from_doc(doc):
    """Ima string su tinklalapiu ir grąžina vienos auditorijos
    savaitės tvarkaraštį."""
    
    soup = BeautifulSoup(doc)
    table = soup.find('table', { 'class' : 'aud2' })

    day_name = None
    aud = Aud()
    for row in table.contents:
        try:
            c = row.find('td')['class']
        except:
            c = None

        if c == 'diena':
            day_name = row.find('td').text.lower().strip().encode('utf8')
        elif c == 'laikas2':
            lecture = Lecture(row)
            aud.take_hours(day_name, lecture)
                    
    return aud

def get_week_from_name(aud):
    """Grąžina užimtumą pagal auditorijos pavadinimą."""
    url = 'http://kedras.mif.vu.lt/tvark/?type=auditor&anr=%s' \
        % urllib2.quote(aud)
    doc = urllib2.urlopen(url)
    print "   * %s" % (aud)
    return get_week_from_doc(doc)

def get_aud_names():
    """Visų auditorijų sąrašas."""
    doc = urllib2.urlopen('http://kedras.mif.vu.lt/tvark/?type=auditorija')
    soup = BeautifulSoup(doc)
    ul = soup.find('ul')
    return [li.find('a').text.encode('utf-8')
            for li in ul.findAll('li')]

class Timetable:
    def __init__(self):
        self.aud_names = get_aud_names()
        self.auds = {}
        for aud_name in self.aud_names:
            self.auds[aud_name] = get_week_from_name(aud_name)

    def pr(self):
        print
        for aud in self.auds:
            print aud
            self.auds[aud].pr()
                
    def get_status(self, aud_name, day, hour):
        return self.auds[aud_name].get_status(day, hour)

def dump_timetable():
    print 'Renkami tvarkaraščiai:'
    data = Timetable()
    print 'Saugomi duomenys į "timetable.txt" ...'
    with file('timetable.txt', 'w') as f:
        pickle.dump(data, f)
    print 'Baigta.'

def load_timetable():
    try:
        with file('timetable.txt') as f:
            return pickle.load(f)
    except IOError as e:
        if e.errno == 2:
            raise Exception(
                'Nesukurtas "timetable.txt", paleiskite "dump_timetable.py"'
                )
        else:
            raise
