#!/usr/bin/env python2
# -*- coding: utf-8-unix -*-

import urllib2
import re
import common
import time

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

def idify(x):
    return 'x%x' % hash(x)

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

with file('output/index.html', 'w') as f:
    def output_aud(name):
        f.write('<tr class="%s"><td><a href="http://kedras.mif.vu.lt/tvark/?type=auditor&amp;anr=%s">%s</a></td>' 
                % (idify(get_aud_type(aud_name)),
                   urllib2.quote(aud_name),
                   aud_name))
        for hour in all_hours:
            status = timetable.get_status(aud_name, day_name, hour)
            f.write('<td class="')
            if (hour / 2) % 2:
                f.write('odd ')
            if status == common.TAKEN_ALWAYS:
                f.write('taken">U')
            elif status:
                f.write('half">%d' % status)
            else:
                f.write('free">L')
            f.write('</td>')
        f.write('</tr>')

    f.write('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
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
<h2>Nustatymai</h2>
<p><label>Rodyti dieną:
<select onchange="selectDay()">''')
    for day_name in day_names:
        f.write('<option value="%s">%s</option>'
                % (idify(day_name), day_name))
    f.write('''</select></label>
<p>Rodyti auditorijas iš:
<ul>''')

    checked = ' checked'
    for aud_type in aud_types:
        f.write('<li><label><input onchange="selectAud(this)" id="%s" type="checkbox" %s>%s</label>'
            % (idify(aud_type), checked, aud_type))
        checked = ''
    
    f.write('''</ul></div>
<div class="float">''')

    for day_name in day_names:
        f.write('<div class="diena" id="%s"><h2>%s</h2>'
                % (idify(day_name), titlecase(day_name)))
        f.write('<table>')
        f.write('<tr class="theader"><td>Valandos →<br>Auditorijos ↓</td>')
        for hour in all_hours:
            f.write('<td>%02d</td>' % hour)
        f.write('</tr>')
        for aud_type in aud_types:
            f.write('<tr class="%s"><td class="audtype" colspan="%d">%s</td></tr>'
                    % (idify(aud_type),
                       len(all_hours) + 1,
                       aud_type))
            for aud_name in timetable.aud_names:
                if get_aud_type(aud_name) == aud_type:
                    output_aud(aud_name)
        f.write('</table></div>')

    f.write('''<p id="footer">Atnaujinta: %s</p>'''
            % time.strftime('%F', time.localtime(time.time())))
        
    f.write('''</div></body></html>''')
