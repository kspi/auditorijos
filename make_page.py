#!/usr/bin/env python2
# -*- coding: utf-8-unix -*-
# Ši programa sugeneruoja puslapį į stdout.

import urllib2
import re
import common

all_hours = range(8, 22)
day_names = ['pirmadienis',
             'antradienis',
             'trečiadienis',
             'ketvirtadienis',
             'penktadienis']
aud_types = ['Naugardukas',
             'Baltūpiai',
             'ITC',
             'kitos']

timetable = common.load_timetable()

def titlecase(s):
    return s.decode('utf-8').title().encode('utf-8')

naugardukas_re = re.compile(r'^\d\d\d( \(MMT.*)?$')
baltupiai_re = re.compile(r'\(balt\.\)')
itc_re = re.compile(r'^(\d{1,2}|\d{1,2}, \d{1,2})( \(MMT.*)?$')
def get_aud_type(name):
    if re.search(naugardukas_re, name):
        return 'Naugardukas'
    elif re.search(baltupiai_re, name):
        return 'Baltūpiai'
    elif re.search(itc_re, name):
        return 'ITC'
    else:
        return 'kitos'

def output_aud(name):
    print '<tr class="%s"><td><a href="http://kedras.mif.vu.lt/tvark/?type=auditor&anr=%s">%s</a></td>' \
        % (get_aud_type(aud_name),
           urllib2.quote(aud_name),
           aud_name),
    for hour in all_hours:
        status = timetable.get_status(aud_name, day_name, hour)
        print '<td class="',
        if (hour / 2) % 2:
            print 'odd',
        if status == common.TAKEN_ALWAYS:
            print 'taken">U',
        elif status:
            print 'half">%d' % status,
        else:
            print 'free">L',
        print '</td>',
    print '</tr>'
    
print '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<script type="text/javascript" src="jquery.js"></script>
<script type="text/javascript" src="script.js"></script>
<link rel="stylesheet" type="text/css" href="style.css">
<title>Auditorijų užimtumas</title>
</head>
<body>

<h1>Auditorijų užimtumas</h1>
<div class="float">
<h2>Legenda</h2>
<ul>
<li><span class="taken">U</span> &ndash; užimta,
<li><span class="half">1</span>, <span class="half">2</span>
        &ndash; užimta tik nelyginėmis arba lyginėmis savaitėmis,
<li><span class="free">L</span> &ndash; laisva.
</ul>
<form name="settings">
<h2>Nustatymai</h2>
<p><label>Rodyti dieną:
<select name="day" onchange="selectDay()">'''
for day_name in day_names:
    print '<option>%s</option>' % day_name
print '''</select></label>
<p>Rodyti auditorijas iš:
<ul>'''
checked = ' checked'
for aud_type in aud_types:
    print '<li><label><input id="%s" type="checkbox" %s>%s</label>' \
        % (aud_type, checked, aud_type)
    checked = ''
print '''</ul></form></div>
<div class="float">
'''
for day_name in day_names:
    print '<div class="diena" id="%s"><h2>%s</h2>' \
        % (day_name, titlecase(day_name))
    print '<table>'
    print '<tr class="darken"><td>Auditorijos ↓ / valandos →</td>',
    for hour in all_hours:
        print '<td>%02d</td>' % hour,
    print '</tr>'
    for aud_type in aud_types:
        print '<tr class="%s"><td class="darken" colspan="%d">%s</td></tr>'\
            % (aud_type, len(all_hours) + 1, aud_type)
        for aud_name in timetable.aud_names:
            if get_aud_type(aud_name) == aud_type:
                output_aud(aud_name)
    print '</table></div>'

print """</div></body></html>"""
