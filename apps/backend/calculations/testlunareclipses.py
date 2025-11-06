import pytest
import skyfield
import datetime
import sys
from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84
from skyfield import eclipselib
from lunareclipses import checkValidDate, checkEndAfterBegin
from fullmoon import checkLunarValidDate
def test_day_checkValidDate():
    """check day validity works"""
    assert checkValidDate(1,1,2025) == True
    assert checkValidDate(2,30,2025) == False
    assert checkValidDate(1,-1,2025) == False

def test_month_checkValidDate():
    """check month validity works"""
    assert checkValidDate(6,15,2027) ==True
    assert checkValidDate(13,12,2027) ==False
    assert checkValidDate(12,7,2027) ==True
def test_year_checkValidDate():
    """check year validity works"""
    assert checkValidDate(3,15,2024) ==True
    assert checkValidDate(10,15,2190) ==True
    assert checkValidDate(5,30,1000) ==True

def test_month_checkEndAfterBegin():
    """verify month differences work"""
    assert checkEndAfterBegin(11,3,2020,3,3,2020) == False
    assert checkEndAfterBegin(5, 6, 2013,6,6,2013) == True
    assert checkEndAfterBegin(5,12,2025,5,13,2025) == True

def test_day_checkEndAfterBegin():
    """check day differences work"""
    assert checkEndAfterBegin(11,5,2024,11,28,2024) == True
    assert checkEndAfterBegin(4,14,2007,4,7,2007) == False
    assert checkEndAfterBegin(5,5,2025,5,6,2025) == True

def test_year_checkEndAfterBegin():
    """check year differences work"""
    assert checkEndAfterBegin(9,11,2001,9,11,2002) == True
    assert checkEndAfterBegin(5,6,2010,10,20,2010) == True
    assert checkEndAfterBegin(6,9,2025,6,9,420) == False

def test_month_lunardate():
    """check month date fullmoon"""
    assert checkLunarValidDate(1,12,2018) == True
    assert checkLunarValidDate(1,31,2018) ==True
    assert checkLunarValidDate(-1,20,2018) ==True

def test_day_lunardate():
    """check day date fullmoon"""
    assert checkLunarValidDate(5,1,2020) ==True
    assert checkLunarValidDate(5,31,2020) ==True
    assert checkLunarValidDate(9,-1,2020) == False

def test_year_lunardate():
    """check year date fullmoon"""
    assert checkLunarValidDate(5,13,2025) == True
    assert checkLunarValidDate(12,25,2030) == True
    assert checkLunarValidDate(1,29,-20) ==True