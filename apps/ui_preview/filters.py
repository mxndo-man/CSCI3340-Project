"""Discover's filters: the query-string keys, and a plain-Python version of the filtering.

The keys are Posting's field names and the values are the contracts' choice values, so
a saved search (SavedSearch.filters) can store the same dict Discover reads. A list
travels as one comma-separated value: ?citizenship=NOT_SPECIFIED,WORK_AUTHORIZATION.

It's a reference for apps/postings/filters.py::filter_postings (contracts section 2.6),
which does the same thing with a queryset. The preview runs it on fake postings.
"""

from datetime import date
from urllib.parse import urlencode

LIST_KEYS = ("citizenship", "clearance", "degree_levels", "work_mode")
SORTS = ("closing", "newest", "pay")

# Every key, empty. "q" searches the title, organization and location.
EMPTY = {
    "q": "",
    "paid": False,
    "deadline_within_days": None,
    "citizenship": [],
    "clearance": [],
    "degree_levels": [],
    "work_mode": [],
    "start_term": "",
}

# What Discover shows when you arrive without choosing anything (the prototype's default).
DEFAULT_FILTERS = {
    "paid": True,
    "clearance": ["NONE_MENTIONED"],
    "deadline_within_days": 30,
}

DEGREE_RANK = {"HS": 0, "ASSOCIATE": 1, "BACHELOR": 2, "MASTER": 3, "PHD": 4}


def parse_filters(params):
    """Read the filters from request.GET.

    With no filter keys at all, Discover uses DEFAULT_FILTERS. The form always sends
    applied=1, so unticking every chip really shows everything.
    """
    if "applied" not in params and not any(key in params for key in EMPTY):
        return {**EMPTY, **DEFAULT_FILTERS}
    days = params.get("deadline_within_days", "")
    filters = {
        **EMPTY,
        "q": params.get("q", "").strip(),
        "paid": params.get("paid") == "1",
        "deadline_within_days": int(days) if days.isdigit() else None,
        "start_term": params.get("start_term", "").strip(),
    }
    for key in LIST_KEYS:
        filters[key] = [value for value in params.get(key, "").split(",") if value]
    return filters


def compact(filters):
    """Only the filters that are set: what a SavedSearch stores."""
    return {key: value for key, value in filters.items() if value}


def filters_to_query(filters):
    """The query string for a filters dict, e.g. for a saved search's Discover link."""
    pairs = [("applied", "1")]
    for key, value in compact(filters).items():
        if key == "paid":
            pairs.append((key, "1"))
        elif key in LIST_KEYS:
            pairs.append((key, ",".join(value)))
        else:
            pairs.append((key, str(value)))
    return urlencode(pairs)


def matches(posting, filters, today: date):
    """Does one posting pass the filters? Closed postings never do."""
    if posting.status == "CLOSED" or (posting.deadline and posting.deadline < today):
        return False
    days = filters.get("deadline_within_days")
    if days is not None and (
        posting.deadline is None or (posting.deadline - today).days > days
    ):
        return False
    if filters.get("paid") and not posting.pay_max:
        return False
    # A null field hasn't been read yet, so it can't match a choice.
    for key in ("citizenship", "clearance", "work_mode"):
        wanted = filters.get(key)
        if wanted and getattr(posting, key) not in wanted:
            return False
    # "I'm working toward a bachelor's": hide postings whose lowest accepted degree is
    # higher. An empty degree_levels list means any degree.
    mine = filters.get("degree_levels")
    if mine and posting.degree_levels:
        lowest = min(DEGREE_RANK[level] for level in posting.degree_levels)
        if lowest > max(DEGREE_RANK[level] for level in mine):
            return False
    if filters.get("start_term") and posting.start_term != filters["start_term"]:
        return False
    text = filters.get("q", "").lower()
    searchable = f"{posting.title} {posting.organization} {posting.location}".lower()
    return not text or text in searchable


def filter_postings(postings, filters, today: date, sort="closing"):
    """The postings that match, in the chosen order."""
    found = [p for p in postings if matches(p, filters, today)]
    if sort == "newest":
        return sorted(found, key=lambda p: p.first_seen_at, reverse=True)
    if sort == "pay":
        return sorted(found, key=lambda p: p.pay_max or 0, reverse=True)
    return sorted(found, key=lambda p: (p.deadline is None, p.deadline or today))
