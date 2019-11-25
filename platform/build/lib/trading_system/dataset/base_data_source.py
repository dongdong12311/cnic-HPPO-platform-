# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:00:43 2019

@author: Administrator
"""


import os
import six
import numpy as np
from .datetime_func import convert_date_to_int, convert_int_to_date
from .py2 import lru_cache

from .converter import StockBarConverter,IndexBarConverter
from .const import trading_calendar_path,daily_data_path,stock_index_path
from .day_bar_store import DayBarStore
from .trading_dates_store import TradingDatesStore

class BaseDataSource():
    def __init__(self, path):
        if not os.path.exists(path):
            raise RuntimeError('bundle path {} not exist'.format(os.path.abspath(path)))

        def _p(name):
            return os.path.join(path, name)

        self._day_bars = [
            DayBarStore(_p(daily_data_path), StockBarConverter),
            DayBarStore(_p(stock_index_path),IndexBarConverter)
        ]
        self._trading_dates = TradingDatesStore(_p(trading_calendar_path))
        
    def get_trading_calendar(self,start,end):
        return self._trading_dates.get_trading_calendar(start,end)

    def get_all_instruments(self):
        return self._instruments.get_all_instruments()

    def get_share_transformation(self, order_book_id):
        return self._share_transformation.get_share_transformation(order_book_id)

    def is_suspended(self, order_book_id, dates):
        return self._suspend_days.contains(order_book_id, dates)

    def is_st_stock(self, order_book_id, dates):
        return self._st_stock_days.contains(order_book_id, dates)

    def get_day_bars(self):
        return self._day_bars
    @lru_cache(None)
    def _all_day_bars_of(self,code,i,trade_date = 'date'):
        #i = self._index_of(instrument)
        return self._day_bars[i].get_bars(code, None,trade_date)

    @lru_cache(None)
    def _filtered_day_bars(self, code,i,trade_date = 'date',volume = 'volume'):
        bars = self._all_day_bars_of(code,i,trade_date)
        if bars is None:
            return None
        return bars[bars[volume] > 0]

    def get_bar(self, code, dt, frequency):
        if frequency != '1d':
            raise NotImplementedError

        bars = self._all_day_bars_of(code,0)
        if bars is None:
            return
        dt = np.uint64(convert_date_to_int(dt))
        pos = bars['datetime'].searchsorted(dt)
        if pos >= len(bars) or bars['datetime'][pos] != dt:
            return None

        return bars[pos]

    def stock_index_bars(self,code,bar_count,frequency,fields,dt):
        if frequency != '1d':
            raise NotImplementedError        
        bars = self._filtered_day_bars(code,1,'trade_date','vol')
        if bars is None:
            return None
        dt = np.uint64(convert_date_to_int(dt))
        i = bars['datetime'].searchsorted(dt, side='right')
        left = i - bar_count if i >= bar_count else 0
        bars = bars[left:i]
        return bars if fields is None else bars[fields]
    def history_bars(self, code, bar_count, frequency, fields, dt,
                     skip_suspended=False, include_now=False,
                     adjust_type='none', adjust_orig=None):
        if frequency != '1d':
            raise NotImplementedError

        if skip_suspended :
            bars = self._filtered_day_bars(code,0)
        else:
            bars = self._all_day_bars_of(code,0)

        if bars is None:
            return None
        dt = np.uint64(convert_date_to_int(dt))
        i = bars['datetime'].searchsorted(dt, side='right')
        left = i - bar_count if i >= bar_count else 0
        bars = bars[left:i]
        if adjust_type == 'none':
            return bars if fields is None else bars[fields]




    def available_data_range(self, frequency):
        if frequency in ['tick', '1d']:
            s, e = self._day_bars[self.INSTRUMENT_TYPE_MAP['INDX']].get_date_range('000001.XSHG')
            return convert_int_to_date(s).date(), convert_int_to_date(e).date()



