from datetime import date
import re
from dateutil.relativedelta import relativedelta
from edtf_date import EDTFDate, PRECISION_DAY, PRECISION_MONTH, PRECISION_SEASON, \
    PRECISION_YEAR, PRECISION_DECADE, PRECISION_CENTURY, PRECISION_MILLENIUM
import edtf_exceptions

# me no work python modules good
ParseError = edtf_exceptions.ParseError

class EDTFInterval(object):
    """
    An interval of two EDTFDates, or 'unknown'/'open'
    """

    def __init__(self, text=None):
        # after init, start and end will always be
        # 'unknown', 'open' or an EDTFDate
        self.start = None
        self.end = None

        if not text:
            text = "open/open"
        self.parse_text(text)

    def parse_text(self, text):
        parts = re.match(r'([^/]+)/([^/]+)', text)
        if parts:
            self.start = self.parse_part(parts.group(1))
            self.end = self.parse_part(parts.group(2))
        else:
            raise ParseError("An interval needs to contain a '/'")

    def parse_part(self, part):
        if part in ['open', 'unknown']:
            return part
        return EDTFDate(part)

    def __unicode__(self):
        return u"%s/%s" % (self.start, self.end)

    @staticmethod
    def _get_unknown_offset(precision):
        if precision == PRECISION_DAY:
            return relativedelta(months=1)
        if precision == PRECISION_MONTH:
            return relativedelta(years=1)
        if precision == PRECISION_SEASON:
            return relativedelta(months=18)
        if precision == PRECISION_YEAR:
            return relativedelta(years=5)
        if precision == PRECISION_DECADE:
            return relativedelta(years=25)
        if precision == PRECISION_CENTURY:
            return relativedelta(years=250)
        if precision == PRECISION_MILLENIUM:
            return relativedelta(years=2500)

    def start_earliest_date(self):
        if self.start in ['open', 'unknown'] \
                and self.end in ['open', 'unknown']:
            return date.min

        if self.start == "unknown":
            return self.end.earliest_date() - \
                self._get_unknown_offset(self.end.precision)
        elif self.start == "open":
            return date.min
        else:
            return self.start.earliest_date()

    def start_latest_date(self):
        if self.start in ['open', 'unknown'] \
                and self.end in ['open', 'unknown']:
            return date.max

        if self.start == "unknown":
            return self.end.latest_date()
        elif self.start == "open":
            return self.end.latest_date()
        else:
            return self.start.latest_date()

    def end_earliest_date(self):
        if self.start in ['open', 'unknown'] \
                and self.end in ['open', 'unknown']:
            return date.min

        if self.end == "unknown":
            return self.start.earliest_date()
        elif self.end == "open":
            return self.start.earliest_date()
        else:
            return self.end.earliest_date()

    def end_latest_date(self):
        if self.start in ['open', 'unknown'] \
                and self.end in ['open', 'unknown']:
            return date.max

        if self.end == "unknown":
            return self.start.latest_date() + self._get_unknown_offset(self.start.precision)
        elif self.end == "open":
            return date.max
        else:
            return self.end.latest_date()

    def sort_date(self):
        if self.start not in ['unknown', 'open']:
            return self.start.sort_date()
        elif self.end not in ['unknown', 'open']:
            return self.end.sort_date()
        else:
            return date.max