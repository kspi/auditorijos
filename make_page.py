#!/usr/bin/env python2
# -*- coding: utf-8-unix -*-
# Ši programa sugeneruoja puslapį į stdout.

import urllib2
import common

all_hours = range(8, 23)
timetable = common.load_timetable()

print '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>Auditorijų užimtumas</title>
</head>
<body>

<h1>Auditorijų užimtumas</h1>
<h2>Legenda</h2>
<ul>
<li><div class="taken">U</div> — užimta
<li><div class="free">L</div> — laisva
</ul>
'''

for day_name in timetable.day_names:
    print '<h2>%s</h2>' % day_name.title()
    print '<table>'
    print '<tr class="darken"><td>Auditorijos ↓ / valandos →</td>',
    for hour in all_hours:
        print '<td>%02d</td>' % hour,
    print '</tr>'
    for aud_name in timetable.aud_names:
        print '<tr><td><a href="http://kedras.mif.vu.lt/tvark/?type=auditor&anr=%s">%s</a></td>' % (urllib2.quote(aud_name), aud_name),
        for hour in all_hours:
            status = timetable.get_status(aud_name, day_name, hour)
            print '<td',
            if status == True:
                print 'class="taken">U',
            elif status:
                print 'class="half">%d' % status,
            else:
                print 'class="free">L',
            print '</td>',
        print '</tr>'

    print '</table>'

print """</body></html>"""
