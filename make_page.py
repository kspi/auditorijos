#!/usr/bin/env python2
# -*- coding: utf-8-unix -*-
# Ši programa sugeneruoja puslapį į stdout.

days = [u'pirmadienis',
        u'antradienis',
        u'trečiadienis',
        u'ketvirtadienis',
        u'penktadienis']

with file('dump.txt') as f:
    contents = f.read()
data = eval(contents)

print '''
<!DOCTYPE html>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="style.css">
<title>Auditorijų užimtumas</title>
<h1>Auditorijų užimtumas</h1>

<h2>Legenda</h2>
<ul>
<li><div class="taken">U</div> — užimta
<li><div class="free">L</div> — laisva
</ul>

'''

for day in days:
    print (u'<h2>%s</h2>' % day.title()).encode('utf-8')
    print '<table>'
    print '<tr class="darken"><td>Auditorijos ↓ / valandos →</td>',
    for hour in xrange(8,23):
        print '<td>%02d</td>' % hour,
    print '</tr>'
    for [aud, hours] in data:
        if aud.find('(balt.)') > -1:
            continue
        print '<tr><td>%s</td>' % aud,
        for hour in xrange(8,23):
            taken = False
            try:
                if hour in hours[day]:
                    taken = True
            except KeyError:
                pass
            print '<td',
            if taken:
                print 'class="taken">U',
            else:
                print 'class="free">L',
            print '</td>',
        print '</tr>'

    print '</table>'
