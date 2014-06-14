# -*- coding: utf-8 -*-

import unittest

from dateparser_ptbr import parse_date, to_str

sp_timezone = 'America/Sao_Paulo'


class TestUnicodeToStrDates(unittest.TestCase):
    """Tests a pre-parsing on the date string, required to overcome a \
    'limitation' of `python-dateutil`, which is not fully supported on Python\
    2.x. So, we pre-parse the unicode date string to a str, and then we can\
    use `python-dateutil`.
    """

    def test_saturday_pt(self):
        self.assertEqual("Sabado", to_str(u"Sábado"))
        self.assertEqual("sabado", to_str(u"sábado"))

    def test_tuesday_pt(self):
        self.assertEqual("Terca", to_str(u"Terça"))
        self.assertEqual("terca", to_str(u"terça"))
        self.assertEqual("Terca-feira", to_str(u"Terça-feira"))
        self.assertEqual("terca-feira", to_str(u"terça-feira"))

    def test_march_pt(self):
        self.assertEqual("Marco", to_str(u"Março"))
        self.assertEqual("marco", to_str(u"março"))


class TestParseDateFormats(unittest.TestCase):
    """Tests for :func:`tarantula.html_utils.strip_html`
    """

    def assert_date(self, expected_date, date_to_parse):
        parsed_date = parse_date(date_to_parse, sp_timezone)
        self.assertEqual(expected_date, parsed_date)

    def test_unicode_date(self):
        self.assert_date(
            '2013-05-13T19:35:00-03:00',
            u'13 de maio de 2013 - 19h35'
        )

    def test_str_date(self):
        self.assert_date(
            '2013-05-13T19:35:00-03:00',
            u'13 de maio de 2013 - 19h35'
        )

    def test_parse_date_with_special_char_weekday1(self):
        self.assert_date(
            '2012-06-26T16:02:00-03:00',
            u'Terça, 26 Junho 2012 16:02'
        )

    def test_parse_date_with_special_char_weekday2(self):
        self.assert_date(
            '2012-06-26T08:36:00-03:00',
            u'Terça, 26 Junho 2012 08:36'
        )

    def test_parse_date1(self):
        self.assert_date(
            '2013-05-13T19:35:00-03:00',
            u'13 de maio de 2013 - 19h35'
        )

    def test_parse_date2(self):
        self.assert_date(
            '2013-05-21T19:20:00-03:00',
            u'21 de maio de 2013 - 19h20'
        )

    def test_parse_date3(self):
        self.assert_date(
            '2013-02-20T14:15:00-03:00',
            u'20 de fevereiro de 2013 - 14h15'
        )

    def test_parse_date4(self):
        self.assert_date(
            '2012-06-26T00:00:00-03:00',
            u'26/06/2012'
        )

    def test_parse_date5(self):
        self.assert_date(
            '2012-06-25T15:27:00-03:00',
            u'Segunda, 25 Junho 2012 15:27'
        )

    def test_parse_date6(self):
        self.assert_date(
            '2012-06-25T19:01:51-03:00',
            u'25/06/2012 19:01:51'
        )

    def test_parse_date7(self):
        self.assert_date(
            '2012-06-05T14:36:08-03:00',
            u'05/06/2012 14:36:08'
        )

    def test_parse_date8(self):
        self.assert_date(
            '2012-06-17T13:22:51-03:00',
            u'17/06/2012 13:22:51'
        )

    def test_parse_date9(self):
        self.assert_date(
            '2012-04-26T00:00:00-03:00',
            u'26  de  abril  de  2012'
        )

    def test_parse_date10(self):
        self.assert_date(
            '2009-07-22T14:24:00-03:00',
            u'quinta-feira, 22 de julho de 2009 | 14:24'
        )

    def test_parse_date11(self):
        self.assert_date(
            '2013-06-12T11:00:00-03:00',
            u'12/06/13 11:00'
        )

    def test_parse_date12(self):
        self.assert_date(
            '2006-09-12T18:21:00-03:00',
            u'12/09/06 18:21'
        )

    def test_parse_date13(self):
        self.assert_date(
            '2007-02-01T19:56:00-02:00',  # -2h because of Daylight Saving Time
            u'01/02/07 19:56'
        )

    def test_parse_date14(self):
        self.assert_date(
            '2013-06-25T00:00:00-03:00',
            u'Penal   |   Publicação em 25.06.13'
        )

    def test_parse_date15(self):
        self.assert_date(
            '2013-06-21T00:00:00-03:00',
            u'Artigos   |   Publicação em 21.06.13'
        )

    def test_parse_date16(self):
        self.assert_date(
            '2013-06-11T00:00:00-03:00',
            u'Trabalhista   |   Publicação em 11.06.13'
        )

    def test_parse_date17(self):
        self.assert_date(
            '2013-05-31T00:00:00-03:00',
            u'31 Mai 2013'
        )

    def test_parse_date18(self):
        self.assert_date(
            '2013-08-27T21:18:00-03:00',
            u'27/08/2013 - 21:18 |Por Comunicação'
        )

    def test_parse_date19(self):
        self.assert_date(
            '2013-09-25T00:00:00-03:00',
            u'TST - 25/09/2013'
        )

    def test_parse_date20(self):
        self.assert_date(
            '2013-09-18T00:00:00-03:00',
            u'TRT - 2ª Região - SP - 18/09/2013'
        )
