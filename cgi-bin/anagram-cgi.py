#!/usr/bin/python
# -*- coding: utf-8 -*-

from string import *
from itertools import *
from copy import copy
from datetime import date
import sys, os, codecs, locale
import cgi, cgitb; cgitb.enable()  # for troubleshooting

# Required header that tells the browser how to render the text.
print "Content-Type: text/html; charset=UTF-8"

print """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<center>
<title>PŘESMYČKY</title> <!-- nazov okna -->
</head>
<meta name="description" content="Vyhledávač českých křestních jmen v přesmyčkách" />
<body bgcolor="#E6E6E6">
  <h2> PŘESMYČKY </h2> <!-- nadpis -->
  <h4> Vyhledávač českých křestních jmen v přesmyčkách </h4><hr noshade size=4><br><br>
"""

form = cgi.FieldStorage()
INPUT = form.getvalue("INPUT", "")

print """
  <form method="get" accept-charset="UTF-8" action="anagram-cgi.py"/>
    Zadej výraz : <input type="text" name="INPUT"/>
    <input type="submit" value="Hledej" />
  </form><br>
""" 

INPUT_without_spaces = replace(INPUT.lower(),' ','')
INPUT_unicode = INPUT_without_spaces.decode('utf-8')
LETTERS = list(INPUT_unicode)
NUM_LETTERS = len(LETTERS)

if NUM_LETTERS > 0:
  if NUM_LETTERS < 6: 
    print """
      <p><font color="#ff0000"><b> Příliš krátký výraz. Zadej alespoň 6 písmen! </b></font></p>
    """
  else:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') # aby spravne zoradil UNICODE
    NAMES = codecs.open('jmena.txt', 'r','utf-8')
    N = NAMES.readlines()
    NAMES.close()
    NAME = {}
    for line in N: 
      w = split(line)
      j = list(w[0].lower())
      k = sorted(j, cmp = locale.strcoll)  # aby spravne zoradil UNICODE
      NAME[tuple(k)] = ''.join(w[0])

    COMBINATION_LENGTH = range(3,NUM_LETTERS-2)
    OUTPUT = [[],[]]
    for n in COMBINATION_LENGTH:
      for c in combinations(LETTERS,n): 
        i = list(c)
        k = sorted(i, cmp = locale.strcoll)  # aby spravne zoradil UNICODE
        k1 = tuple(k)
        if k1 in NAME:
          j = NAME[k1]
          if j not in OUTPUT[0]: 
            OUTPUT[0].append(j)
            REST = copy(LETTERS)
            for L in c: REST.remove(L)
            OUTPUT[1].append(''.join(REST))

    if len(OUTPUT[0]) == 0:
      print """
        <font color="#ff0000"><b><p>
        Bohužel :-( <br> Zkus něco jiné.
        </p></b></font>
      """
    else:
      print """
        <table align = "center" border = "2" cellpadding= "3" cellspacing = "5" width = "45%s"/>
          <caption> Ve výrazu <i>" %s"</i> (%d písmen) jsem našel tyto jména :</caption> 
          <tr>
	  <th width = "50%s"> Jméno </th>
          <th> zbylá písmena </th>
          </tr>
      """ % ('%', INPUT, NUM_LETTERS, '%')
      bg_color = ["#AAAAA","#E6E6E6"]
      for x in range(len(OUTPUT[0])): 
        background_color = bg_color[x%2]
        print """
          <tr bgcolor="%s"> 
          <td> %s </td>
          <td> %s </td>
          </tr>
        """ % (background_color, OUTPUT[0][x].encode('utf-8'), OUTPUT[1][x].encode('utf-8'))

      print """
        </table>
      """

IP = open('anagram-ip.txt','a')
write_date = date.today()
IP.write(cgi.escape(os.environ["REMOTE_ADDR"])+' '+write_date.isoformat()+'\n')
IP.close()


COUNTER = open('anagram-counter.txt', 'r')
line = COUNTER.readline()
COUNTER.close()
w = split(line)
counter = long(w[0])
c = str(counter)
if INPUT == '': 
  COUNTER = open('anagram-counter.txt', 'w')
  counter += 1
  c = str(counter)
  COUNTER.write(c)
  COUNTER.close()

#print """
#<p> %s </p>
#""" % c

print """
<footer><i><small>
Last updated on %s <br>
Maintained by Jarka </small> </i>
</footer>
</body>
</center>
</html>
""" % write_date
