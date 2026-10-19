"""Calendar arithmetic preserving source date precision."""
import calendar
import re
from datetime import date,datetime,timedelta


def date_bounds(value):
    if not value: return None
    value=value.strip()
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}",value):
            day=date.fromisoformat(value); return day,day
        if re.fullmatch(r"\d{4}-\d{2}",value):
            year,month=map(int,value.split("-")); return date(year,month,1),date(year,month,calendar.monthrange(year,month)[1])
        for pattern in ("%B %Y","%b %Y","%B %d, %Y","%b %d, %Y","%d %B %Y","%d %b %Y"):
            try: parsed=datetime.strptime(value,pattern).date()
            except ValueError: continue
            if "%d" not in pattern: return parsed,date(parsed.year,parsed.month,calendar.monthrange(parsed.year,parsed.month)[1])
            return parsed,parsed
    except (ValueError,OverflowError): return None
    return None


def date_in_quote(value,quote):
    if not value: return False
    if value.casefold() in quote.casefold(): return True
    bounds=date_bounds(value)
    if not bounds: return False
    first,last=bounds
    # Validate normalized metadata against the source's own month/day/year.
    month=re.search(r"\b(?:"+first.strftime("%B")+"|"+first.strftime("%b")+r")\b",quote,re.I)
    year=str(first.year) in quote
    if first!=last: return bool(month and year)
    return bool(month and year and re.search(r"\b0?"+str(first.day)+r"\b",quote))


def window_start(reference,amount,unit):
    unit=unit.lower().rstrip("s")
    if unit in {"day","week"}: return reference-timedelta(days=amount*(7 if unit=="week" else 1))
    months=amount*(12 if unit=="year" else 1)
    year,month=divmod(reference.year*12+reference.month-1-months,12); month+=1
    return date(year,month,min(reference.day,calendar.monthrange(year,month)[1]))
