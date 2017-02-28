# -*- coding: utf-8 -*-
__author__ = 'laura'
import re


class Crawler():

    def get_prop_span(self, a, prop):
        if prop == "text":
            return a.get_text().encode("ascii", "ignore").strip() if a is not None else ""
        elif prop == "clean_text":
            text = a.get_text().encode("ascii", "ignore").strip() if a is not None else ""
            rgx = re.compile("([\w]*\w)")
            words = rgx.findall(text)
            words = " ".join(words)
            return words
        else:
            return a[prop].encode("ascii", "ignore") if a is not None else ""

    def crawler(self):
        for number_page in range(1, self.max_number_pages + 1):
            self.crawler_page(number_page)




