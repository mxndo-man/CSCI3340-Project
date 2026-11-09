"""Fake objects shaped like the models in docs/contracts.md, made from the prototype's data.

Field names and choice values follow the contracts exactly, so a template that works on
these works on the real models. Dates are counted from today, so the countdowns look the
same whenever you open the preview. Every company, person and posting here is made up.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any

from django.urls import reverse
from django.utils import timezone

# ---- The objects ------------------------------------------------------------------------


@dataclass
class FakeUser:
    """accounts.CustomUser"""

    id: int
    username: str
    display_name: str
    graduation_term: str = ""
    time_zone: str = "America/Chicago"
    email: str = ""
    is_authenticated: bool = True
    is_anonymous: bool = False

    def __str__(self) -> str:
        return self.username


@dataclass
class FakeSource:
    """ingestion.Source"""

    id: int
    provider: str  # GREENHOUSE, LEVER or ASHBY
    token: str
    organization: str
    enabled: bool = True
    last_synced_at: datetime | None = None
    last_error: str = ""


@dataclass
class FakePosting:
    """postings.Posting"""

    id: int
    title: str
    organization: str
    source: FakeSource | None
    source_url: str
    source_text: str
    deadline: date | None
    deadline_type: str | None  # FIXED, ROLLING or UNKNOWN
    start_term: str
    degree_levels: list[str]
    citizenship: str | None
    clearance: str | None
    location: str
    work_mode: str | None
    pay_min: Decimal | None
    pay_max: Decimal | None
    pay_period: str | None
    skills: list[str]
    field_sources: dict[str, str]
    field_details: dict[str, dict[str, Any]]
    first_seen_at: datetime
    status: str = "OPEN"
    closed_at: datetime | None = None
    extraction_status: str = "DONE"
    verified: bool = False
    added_by: FakeUser | None = None

    def get_absolute_url(self) -> str:
        return reverse("ui_preview:posting_detail", args=[self.id])


@dataclass
class FakeFieldReview:
    """postings.FieldReview: one field the AI wasn't sure about."""

    id: int
    posting: FakePosting
    field_name: str
    proposed_value: Any
    confidence: float
    evidence: str
    status: str = "PENDING"

    def get_absolute_url(self) -> str:
        return f"{self.posting.get_absolute_url()}#fact-{self.field_name}"


# ---- The data ---------------------------------------------------------------------------

PEOPLE = {
    # initials: (id, username, display_name, graduation_term)
    "LR": (1, "liamr", "Liam R.", "Fall 2027"),
    "MK": (2, "mayak", "Maya K.", "Spring 2028"),
    "AP": (3, "arjunp", "Arjun P.", "Fall 2027"),
    "JS": (4, "jordans", "Jordan S.", "Spring 2027"),
    "TN": (5, "tessn", "Tess N.", "Fall 2028"),
    "DO": (6, "devo", "Dev O.", "Spring 2028"),
    "RB": (7, "rosab", "Rosa B.", "Fall 2027"),
}

# The prototype's postings. posted: days ago. deadline: days from today. pay: dollars an
# hour (0 = unpaid). provider None means a student added it by hand.
POSTINGS: list[dict[str, Any]] = [
    {
        "title": "Software Engineering Intern",
        "organization": "Example Corp",
        "location": "Austin, TX",
        "work_mode": "HYBRID",
        "posted": 13,
        "deadline": 12,
        "pay": (25, 32),
        "clearance": "NONE_MENTIONED",
        "citizenship": "US_CITIZEN",
        "degree_levels": ["BACHELOR"],
        "start_term": "Summer 2027",
        "provider": "GREENHOUSE",
        "summary": "Join a product team that builds the internal tools 4,000 employees use every day. You'll ship real features with a mentor and demo your project to the company at the end of the summer.",
        "skills": [
            "Coursework in data structures and algorithms",
            "Some experience with JavaScript, Go or Python",
            "Clear written communication",
        ],
    },
    {
        "title": "Data Science Intern",
        "organization": "Northwind Labs",
        "location": "Remote (US)",
        "work_mode": "REMOTE",
        "posted": 16,
        "deadline": 6,
        "pay": (30, 30),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": ["BACHELOR"],
        "start_term": "Summer 2027",
        "provider": "LEVER",
        "summary": "Work with the analytics team to predict which customers might leave, then build the dashboards the sales team checks every Monday.",
        "skills": [
            "Python and SQL",
            "An intro statistics course",
            "Patience with messy data",
        ],
    },
    {
        "title": "Cybersecurity Research Intern",
        "organization": "Mesa Ridge National Lab",
        "location": "Albuquerque, NM",
        "work_mode": "ONSITE",
        "posted": 22,
        "deadline": 17,
        "pay": (28, 28),
        "clearance": "ABLE_TO_OBTAIN",
        "citizenship": "US_CITIZEN",
        "degree_levels": ["BACHELOR"],
        "start_term": "Summer 2027",
        "provider": None,
        "summary": "Research defenses for the control systems that run power plants and water treatment, alongside lab scientists. Most work happens on-site in a secure building.",
        "skills": [
            "Networking fundamentals",
            "C or Python",
            "Able to get a security clearance",
        ],
    },
    {
        "title": "Machine Learning Intern",
        "organization": "Brightwater Health",
        "location": "Boston, MA",
        "work_mode": "HYBRID",
        "posted": 25,
        "deadline": 3,
        "pay": (35, 35),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": ["MASTER"],
        "start_term": "Summer 2027",
        "provider": "ASHBY",
        "summary": "Help train and test models that spot at-risk patients earlier, with a focus on making them fair across different hospitals.",
        "skills": [
            "PyTorch or a similar library",
            "Linear algebra and probability",
            "Master's students preferred; strong juniors considered",
        ],
    },
    {
        "title": "Embedded Software Intern",
        "organization": "Lumen Analytics",
        "location": "San Diego, CA",
        "work_mode": "ONSITE",
        "posted": 19,
        "deadline": 4,
        "pay": (31, 31),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": ["BACHELOR"],
        "start_term": "Summer 2027",
        "provider": "GREENHOUSE",
        "summary": "Write firmware for low-power air-quality sensors and test it on real hardware in the San Diego lab.",
        "skills": [
            "C or C++",
            "Comfort with a multimeter and a soldering iron",
            "Computer or electrical engineering coursework",
        ],
    },
    {
        "title": "Grid Software Intern",
        "organization": "Sable Point Energy",
        "location": "Denver, CO",
        "work_mode": "HYBRID",
        "posted": 10,
        "deadline": 15,
        "pay": (29, 29),
        "clearance": "NONE_MENTIONED",
        "citizenship": "US_PERSON",
        "degree_levels": ["BACHELOR"],
        "start_term": "Summer 2027",
        "provider": "LEVER",
        "summary": "Build tools that forecast power demand for a regional utility, from the data pipeline to the web app that grid operators use.",
        "skills": ["Python", "Some web development", "Interest in clean energy"],
    },
    {
        "title": "Robotics Software Intern",
        "organization": "Tallgrass Robotics",
        "location": "Remote (US)",
        "work_mode": "REMOTE",
        "posted": 7,
        "deadline": 25,
        "pay": (33, 33),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": ["BACHELOR"],
        "start_term": "Summer 2027",
        "provider": "ASHBY",
        "summary": "Work on path planning for warehouse robots. The role is remote, with one paid week on-site in Kansas City for testing.",
        "skills": ["C++ or Python", "Linear algebra", "ROS experience is a plus"],
    },
    {
        "title": "Product Design Intern",
        "organization": "Fernwood Studio",
        "location": "Portland, OR",
        "work_mode": "HYBRID",
        "posted": 1,
        "deadline": 28,
        "pay": (25, 29),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": [],
        "start_term": "Summer 2027",
        "provider": None,
        "summary": "Design screens for a small studio's client apps, from research sessions to polished prototypes you present to clients.",
        "skills": [
            "A portfolio with two or three projects",
            "Figma",
            "Comfort presenting your work",
        ],
    },
    {
        "title": "Quantitative Research Intern",
        "organization": "Copperline Finance",
        "location": "Chicago, IL",
        "work_mode": "ONSITE",
        "posted": 29,
        "deadline": 39,
        "pay": (55, 55),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": ["MASTER"],
        "start_term": "Summer 2027",
        "provider": "GREENHOUSE",
        "summary": "Research trading signals with a small team. Expect statistics, Python and a lot of reading papers.",
        "skills": [
            "Probability and statistics",
            "Python",
            "Master's students preferred",
        ],
    },
    {
        "title": "Data Analyst Intern",
        "organization": "Alder & Finch Foundation",
        "location": "Remote (US)",
        "work_mode": "REMOTE",
        "posted": 14,
        "deadline": 22,
        "pay": (0, 0),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": [],
        "start_term": "Spring 2027",
        "provider": "LEVER",
        "summary": "Help a small foundation measure how well its reading programs work. Unpaid, about 10 hours a week, fully remote.",
        "skills": ["Spreadsheets", "Basic SQL", "Interest in education"],
    },
    {
        "title": "Frontend Engineering Intern",
        "organization": "Juniper Labs",
        "location": "New York, NY",
        "work_mode": "HYBRID",
        "posted": 5,
        "deadline": 73,
        "pay": (34, 34),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": ["BACHELOR"],
        "start_term": "Summer 2027",
        "provider": "ASHBY",
        "summary": "Build accessible interface components for a design system that five product teams rely on.",
        "skills": [
            "HTML, CSS and JavaScript",
            "React is a plus",
            "An eye for detail",
        ],
    },
    {
        "title": "Mobile Engineering Intern",
        "organization": "Riverbend Games",
        "location": "Seattle, WA",
        "work_mode": "ONSITE",
        "posted": 34,
        "deadline": -3,
        "pay": (30, 30),
        "clearance": "NONE_MENTIONED",
        "citizenship": "NOT_SPECIFIED",
        "degree_levels": ["BACHELOR"],
        "start_term": "Summer 2027",
        "provider": "GREENHOUSE",
        "summary": "Build features for a mobile puzzle game played by two million people.",
        "skills": ["Swift or Kotlin", "A shipped side project", "Love of games"],
    },
]

CITIZENSHIP_EVIDENCE = {
    "NOT_SPECIFIED": None,
    "US_PERSON": "Applicants must be US citizens or permanent residents.",
    "US_CITIZEN": "This role is open to US citizens only.",
}
CLEARANCE_EVIDENCE = {
    "NONE_MENTIONED": None,
    "ABLE_TO_OBTAIN": "You must be able to get a security clearance.",
}
DEGREE_EVIDENCE = {
    "BACHELOR": "Currently pursuing a bachelor's degree in a related field.",
    "MASTER": "Currently pursuing a master's degree; strong bachelor's students may apply.",
}


def _long_date(day: date) -> str:
    return f"{day:%B} {day.day}, {day.year}"


def _sources_and_details(
    spec: dict[str, Any], deadline: date
) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    """Where each field came from (field_sources) and the AI's confidence and evidence
    (field_details), following the prototype: API fields from the job board, the rest
    read by the AI, degree checked by a student."""
    api = spec["provider"] is not None
    sources = {
        "title": "api" if api else "user",
        "organization": "api" if api else "user",
    }
    details: dict[str, dict[str, Any]] = {}

    def model(name: str, confidence: float, evidence: str | None = None) -> None:
        sources[name] = "model"
        details[name] = {"confidence": confidence, "evidence": evidence}

    if api:
        sources.update(deadline="api", work_mode="api", location="api")
    else:
        model("deadline", 0.92, f"Applications close {_long_date(deadline)}.")
        model("work_mode", 0.92)
        model("location", 0.92)
    high = spec["pay"][1]
    if high:
        model("pay", 0.94, f"The hourly rate for this role is ${high}.")
    else:
        model("pay", 0.94, "This is a volunteer role.")
    model("citizenship", 0.91, CITIZENSHIP_EVIDENCE.get(spec["citizenship"]))
    model("clearance", 0.97, CLEARANCE_EVIDENCE.get(spec["clearance"]))
    sources["degree_levels"] = "user"
    levels = spec["degree_levels"]
    details["degree_levels"] = {
        "confidence": 0.9,
        "evidence": DEGREE_EVIDENCE.get(levels[0]) if levels else None,
    }
    model(
        "start_term",
        0.88,
        f"This is a 12-week internship starting in {spec['start_term'].lower()}.",
    )
    return sources, details


class World:
    """Every fake object, linked together the way the real models would be."""

    def __init__(self) -> None:
        self.today = timezone.localdate()
        self.now = timezone.now()
        self.people = {
            initials: FakeUser(id=pk, username=u, display_name=n, graduation_term=t)
            for initials, (pk, u, n, t) in PEOPLE.items()
        }
        self.me = self.people["LR"]
        self.me.email = "liam@example.edu"
        self.postings = self._build_postings()
        self.reviews = self._build_reviews()

    def days(self, n: int) -> date:
        return self.today + timedelta(days=n)

    def _build_postings(self) -> list[FakePosting]:
        postings = []
        for number, spec in enumerate(POSTINGS, start=1):
            deadline = self.days(spec["deadline"])
            sources, details = _sources_and_details(spec, deadline)
            source = None
            if spec["provider"]:
                token = spec["organization"].split()[0].lower()
                source = FakeSource(
                    id=number,
                    provider=spec["provider"],
                    token=token,
                    organization=spec["organization"],
                    last_synced_at=self.now - timedelta(hours=2),
                )
            low, high = spec["pay"]
            closed = spec["deadline"] < 0
            postings.append(
                FakePosting(
                    id=number,
                    title=spec["title"],
                    organization=spec["organization"],
                    source=source,
                    source_url=f"https://example.com/jobs/{number}",
                    source_text=spec["summary"],
                    deadline=deadline,
                    deadline_type="FIXED",
                    start_term=spec["start_term"],
                    degree_levels=spec["degree_levels"],
                    citizenship=spec["citizenship"],
                    clearance=spec["clearance"],
                    location=spec["location"],
                    work_mode=spec["work_mode"],
                    pay_min=Decimal(low),
                    pay_max=Decimal(high),
                    pay_period="HOUR",
                    skills=spec["skills"],
                    field_sources=sources,
                    field_details=details,
                    first_seen_at=self.now - timedelta(days=spec["posted"]),
                    status="CLOSED" if closed else "OPEN",
                    closed_at=self.now - timedelta(days=-spec["deadline"])
                    if closed
                    else None,
                    added_by=None if spec["provider"] else self.people["MK"],
                )
            )
        # Example Corp matches the extractor stub: everything read by the model, and
        # citizenship flagged for a person to check (see apps/extraction_client).
        example = postings[0]
        example.field_sources.update(
            deadline="model", work_mode="model", location="model", degree_levels="model"
        )
        example.field_details.update(
            deadline={
                "confidence": 0.94,
                "evidence": f"Applications close {_long_date(example.deadline)}.",
            },
            work_mode={"confidence": 0.88, "evidence": "Hybrid, 3 days in office"},
            location={"confidence": 0.97, "evidence": "Location: Austin, TX"},
            pay={"confidence": 0.86, "evidence": "$25 to $32 per hour"},
            clearance={"confidence": 0.91, "evidence": None},
            degree_levels={
                "confidence": 0.90,
                "evidence": "Pursuing a bachelor's degree in computer science",
            },
            start_term={"confidence": 0.95, "evidence": "Summer 2027 internship"},
            citizenship={
                "confidence": 0.62,
                "evidence": "Candidates must be eligible to work in the U.S.",
            },
        )
        return postings

    def _build_reviews(self) -> list[FakeFieldReview]:
        example, fernwood = self.postings[0], self.postings[7]
        return [
            FakeFieldReview(
                id=1,
                posting=example,
                field_name="citizenship",
                proposed_value="US_CITIZEN",
                confidence=0.62,
                evidence="Candidates must be eligible to work in the U.S.",
            ),
            FakeFieldReview(
                id=2,
                posting=fernwood,
                field_name="pay",
                proposed_value={
                    "min": 25,
                    "max": 29,
                    "period": "HOUR",
                    "currency": "USD",
                },
                confidence=0.58,
                evidence="Pay is $25–29 an hour, depending on experience.",
            ),
            FakeFieldReview(
                id=3,
                posting=fernwood,
                field_name="start_term",
                proposed_value="Summer 2027",
                confidence=0.64,
                evidence="Start dates are flexible between May and July.",
            ),
        ]

    def posting(self, pk: int) -> FakePosting | None:
        return next((p for p in self.postings if p.id == pk), None)

    def reviews_for(self, posting: FakePosting) -> list[FakeFieldReview]:
        return [
            r for r in self.reviews if r.posting is posting and r.status == "PENDING"
        ]


def world() -> World:
    """Fresh fake data, counted from today. Cheap enough to build on every request."""
    return World()


def landing_postings() -> list[FakePosting]:
    """The two example cards on the landing page."""
    return world().postings[:2]
