# -*- coding: utf-8 -*-
#
# Copyright 2019 Ricequant, Inc
#
# * Commercial Usage: please contact public@ricequant.com
# * Non-Commercial Usage:
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import bcolz
import pandas as pd
from dateutil.parser import parse
from .const import TRADE_DATE
import datetime
class TradingDatesStore(object):
    def __init__(self, f):
        temp = bcolz.open(f, 'r')[TRADE_DATE]
        self._dates = [] 
        for i in range(len(temp)):
            year = int(temp[i]/10000)
            month = int((temp[i] - year * 10000)/100)
            day = temp[i] % 100
            self._dates.append(datetime.datetime(year,month,day))
    def get_trading_calendar(self,start,end):
        if type(start) == int:
            
            start = parse(str(start))
            end = parse(str(end))
        ind_s = 0
        n = len(self._dates)
        ind_e = n
        for i in range(n):
            if self._dates[i] >= start:
                ind_s = i
                break
        for i in range(n):
            if self._dates[n-i-1] <= end:
                ind_e = n - i - 1
                break
                
        return self._dates[ind_s : ind_e + 1]

