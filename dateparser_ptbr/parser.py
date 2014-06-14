# -*- coding: utf-8 -*-

import time
import unicodedata
import re
import logging

from pytz import timezone
from datetime import datetime
from dateutil.parser import parse, parserinfo


class parserinfo_pt(parserinfo):

    JUMP = [" ", ".", ",", ";", "-", "/", "'", "|",
            "de", "feira"]

    WEEKDAYS = [("Seg", "Segunda"),
                ("Tue", "Terca"),
                ("Wed", "Quarta"),
                ("Thu", "Quinta"),
                ("Fri", "Sexta"),
                ("Sat", "Sabado"),
                ("Sun", "Domingo")]
    MONTHS = [("Jan", "Janeiro"),
              ("Fev", "Fevereiro"),
              ("Mar", "Marco"),
              ("Abr", "Abril"),
              ("Mai", "Maio"),
              ("Jun", "Junho"),
              ("Jul", "Julho"),
              ("Ago", "Agosto"),
              ("Set", "Setembro"),
              ("Out", "Outubro"),
              ("Nov", "Novembro"),
              ("Dez", "Dezembro")]

    HMS = [("h", "hora", "horas"),
           ("m", "minuto", "minutos"),
           ("s", "segundo", "segundos")]

    AMPM = [("am", "a"),
            ("pm", "p")]

    UTCZONE = ["UTC", "GMT", "Z"]

    PERTAIN = ["de"]

    TZOFFSET = {}

    def __init__(self, dayfirst=True, yearfirst=False):
        self._jump = self._convert(self.JUMP)
        self._weekdays = self._convert(self.WEEKDAYS)
        self._months = self._convert(self.MONTHS)
        self._hms = self._convert(self.HMS)
        self._ampm = self._convert(self.AMPM)
        self._utczone = self._convert(self.UTCZONE)
        self._pertain = self._convert(self.PERTAIN)

        self.dayfirst = dayfirst
        self.yearfirst = yearfirst

        self._year = time.localtime().tm_year
        self._century = self._year // 100 * 100


def parse_date(date_str, timezone_name='America/Sao_Paulo'):
    """Automagically parses a date. Also adds hour, minute, second and \
    microsecond values from configured timezone from parsed date.

    :param date_str: the string representation of a date.
    :type date_str: str

    :param timezone_name: the name of the timezone.
    :type timezone_name: str

    :returns:  str -- a string representation of the date as defined by \
    `ISO 8601 as suggested by W3C`_

    .. _ISO 8601 as suggested by W3C: http://www.w3.org/TR/NOTE-datetime
    """
    if isinstance(date_str, unicode):
        date_str = to_str(date_str)

    tz = timezone(timezone_name)
    parserinfo = parserinfo_pt()
    d = None

    try:
        d = parse(date_str, parserinfo=parserinfo)
    except ValueError:
        logging.info("Could not parse [%s], trying to parse longest string." % date_str)
        try:
            d = _try_parse_longest_string(date_str, parserinfo)
        except ValueError:
            logging.info("Could not parse [%s], trying to parse string parts." % date_str)
            d = _try_parse_string_parts(date_str, parserinfo)

    tz_aware = tz.localize(d)
    return tz_aware.isoformat()


def _try_parse_longest_string(date_str, parserinfo):
    """Tries to parse the longest substring of date_str, since its beginning.
    """
    best_match_parsed = None
    longest_string = ''
    try:
        for str_part in re.split('\s+', date_str):
            longest_string += str_part + " "
            logging.info("Trying to parse part [%s] " % longest_string)
            try:
                best_match_parsed = parse(longest_string, parserinfo=parserinfo)
            except Exception:
                if best_match_parsed is None:
                    logging.info("Could not parse part [%s]." % longest_string)
                else:
                    return best_match_parsed
    except Exception:
        logging.info("Could not parse the date.")

    if best_match_parsed is not None:
        return best_match_parsed
    else:
        raise ValueError("Could not parse date [%s]" % date_str)


def _try_parse_string_parts(date_str, parserinfo):
    """Tries to parse parts of the string.
    """

    try:
        for str_part in re.split('\s+', date_str):
            if len(str_part) > 5:
                logging.info("Trying to parse part [%s]" % str_part)
                try:
                    return parse(str_part, parserinfo=parserinfo)
                except:
                    logging.info("Could not parse part [%s]." % str_part)
    except:
        logging.info("Could not parse the date.")

    raise ValueError("Could not parse date [%s]" % date_str)


def now(timezone_name='America/Sao_Paulo'):
    tz = timezone(timezone_name)
    return tz.localize(datetime.now()).isoformat()


def to_str(unicode):
    return unicodedata.normalize('NFKD', unicode).encode('ascii', 'ignore')
