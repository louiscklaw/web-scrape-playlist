#!/usr/bin/env python

import os,sys
from pprint import pprint
from string import Template
import datetime
import random
import time

import yfinance as yf

html_template=Template('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <table>
    <tbody>
      $LAST_UPDATE_TABLE
    </tbody>
  </table>
  <table>
    <tbody>
      $TABLE_HEAD
      $TABLE_BODY
    </tbody>
  </table>
</body>
</html>
'''.strip())

template_content='''
<tr>
<td>
$SYMBOL
</td>
<td>
$ASK
</td>
<td>
$BID
</td>
</tr>
'''.strip()

table_row_template=Template(template_content)

last_update_table_template=Template('''
<tr>
  <th>
    last update
  </th>
  <th>
    $LAST_UPDATE_TIMESTAMP
  </th>
</tr>
'''.strip())

def getLastUpdateTimeStamp():
  return '<div>LAST UPDATE</div><div>'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'</div>'

def updateLabel(o_string, label, value):
  return o_string.replace('$'+label,label).replace(label, str(value))

def getTableRow(stock_info):
  label_value_pair = [
    ['SYMBOL', stock_info.info['symbol']],
    ['ASK', stock_info.info['ask']],
    ['BID', stock_info.info['bid']]
  ]
  temp_string = template_content
  for label, value in label_value_pair:
    temp_string = updateLabel(temp_string, label, value)

  return temp_string

def getRandomDataTableRow():
  return table_row_template.substitute(
    SYMBOL='random',
    ASK=random.randrange(100,200,3),
    BID=random.randrange(100,200,3)
  )

def getHeaderRow():
  return template_content.replace('td','th').replace('$','')

def getLastUpdateTable():
  return last_update_table_template.substitute(
    LAST_UPDATE_TIMESTAMP=datetime.datetime.now().strftime('%Y%M%D-%H%M%S')
  )

def getWholeTable(stock_infos):
  return html_template.substitute(
    LAST_UPDATE_TIMESTAMP=getLastUpdateTimeStamp(),
    TABLE_HEAD=getHeaderRow(),
    TABLE_BODY=' '.join([getTableRow(stock_info) for stock_info in stock_infos]+[getRandomDataTableRow()]),
    LAST_UPDATE_TABLE=getLastUpdateTable()
  )


while True:
  text_stock_list = ''
  with open('./stock_list.txt','r') as fi:
    text_stock_list = map(lambda y: y.strip(),
      filter(lambda x: x!='', fi.readlines())
    )

  begin_time = datetime.datetime.now()

  stock_list = []
  last_successful_fetch = []
  temp_html=''
  last_successful_html = ''
  try:

    stock_list = [yf.Ticker(text_stock_code) for text_stock_code in text_stock_list]

    last_successful_fetch= stock_list.copy()




    # get stock info
    temp_html = getWholeTable(stock_list)
    last_successful_html = temp_html

  except Exception as e:
    stock_list = last_successful_fetch.copy()
    temp_html = last_successful_html


  run_take_time = datetime.datetime.now() - begin_time

  with open('/tmp/test.html','r+') as fo:
    fo.truncate(0)
    fo.write(temp_html)

  print('done, last run takes {}, sleeping'.format(run_take_time))
  time.sleep(3)