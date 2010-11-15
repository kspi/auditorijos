# -*- coding: utf-8-unix -*-
"""Čia pagrindinė funkcija get_hours"""

from BeautifulSoup import BeautifulSoup
import re

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


_weekre = re.compile('\( ([12]) \)')
def _get_week(row):
    text = ''.join(map(unicode, row.contents[1].contents))
    try:
        return int(re.findall(weekre, text)[0])
    except:
        return None

class Lecture:
    def __init__(self, day, row):
        self.day = day
        (from_h, from_m, to_h, to_m) = _get_times(row)
        week = _get_week(row)
        self.from_h = from_h
        self.from_m = from_m
        self.to_h = to_h
        self.to_m = to_m
        self.week = week

    def is_alternative(self, other):
        return ((self.day == other.day)
                and (self.from_h == other.from_h)
                and (self.from_m == other.from_m)
                and (self.to_h == other.to_h)
                and (self.to_m == other.to_m)
                and (((self.week == 1) and (other.week == 2))
                     or ((self.week == 2) and (other.week == 1))))

    def hours(self):
        start = self.from_h
        end = self.to_h
        if self.to_m != 0:
            end = end + 1
        return range(start, end + 1)
                
    def __str__(self):
        ret = u'%s: %02d:%02d - %02d:%02d' % (self.day,
                                              self.from_h,
                                              self.from_m,
                                              self.to_h,
                                              self.to_m)
        if self.week:
            ret = u'%s (%d)' % (ret, self.week)
        return ret.encode('utf-8')
        

def get_hours(doc):
    """Ima string su tinklalapiu ir grąžina dict su raktais - savaitės
    dienomis (unicode tipo, mažosiomis raidėmis) ir reikšmėm - aibe
    užimtų valandų."""
    
    soup = BeautifulSoup(doc)
    table = soup.find('table', { 'class' : 'aud2' })

    day = None
    days = []
    lectures = {}
    for row in table.contents:
        try:
            c = row.next['class']
        except:
            c = None

        if c == 'diena':
            day = row.next.contents[0].lower().strip()
            days.append(day)
            lectures[day] = []
        elif c == 'laikas2':
            lecture = Lecture(day, row)
            lectures[day].append(lecture)
                    
    for day in days:
        remove_lectures = []
        for i in xrange(len(lectures[day]) - 1):
            for j in xrange(i + 1, len(lectures[day])):
                if lectures[day][i].is_alternative(lectures[day][j]):
                    lectures[day][i].week = None
                    remove_lectures.append(j)
                    continue

        ofs = 0
        for i in remove_lectures:
            del(lectures[day][i - ofs])
            ofs = ofs + 1

    hours = {}
    for day in days:
        for lecture in lectures[day]:
            hourset = set(lecture.hours())
            hours[day] = hours.get(day, set()).union(hourset)
        
    return hours
