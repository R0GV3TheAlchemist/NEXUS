"""Discover Superpower Wiki category members (I2).

Uses the MediaWiki API (categorymembers) with pagination.
Network I/O is isolated behind a fetch callable so tests stay offline.
Does not mutate CoreState. Does not classify policy tags (I4).
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from urllib.parse import quote

DEFAULT_API = "https://powerlisting.fandom.com/api.php"
DEFAULT_CATEGORY = "Category:Absorption"
DEFAULT_USER_AGENT = "NEXUS-catalog/0.1 (+https://github.com/R0GV3TheAlchemist/NEXUS; research index)"
WIKI_PAGE_BASE = "https://powerlisting.fandom.com/wiki/"

FetchFn = Callable[[str], bytes]

# typing alias without importing Mapping only for runtime clarity
MappingLike = Any


@dataclass(frozen=True)
class CategoryMember:
    """One categorymembers row."""

    pageid: int | None
    title: str
    ns: int
    member_type: str  # "page" | "subcat" | "file" | "unknown"

    @property
    def is_subcategory(self) -> bool:
        return self.member_type == "subcat" or self.ns == 14

    @property
    def is_page(self) -> bool:
        return self.member_type == "page" or (self.ns == 0 and not self.is_subcategory)

    @property
    def url(self) -> str:
        return WIKI_PAGE_BASE + quote(self.title.replace(" ", "_"), safe=":/")


def default_fetch(url: str, timeout: float = 30.0) -> bytes:
    """HTTP GET with a descriptive User-Agent."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return resp.read()


def build_categorymembers_url(
    *,
    api_root: str = DEFAULT_API,
    category_title: str = DEFAULT_CATEGORY,
    cmcontinue: str | None = None,
    cmlimit: int = 500,
    cmtype: str = "page|subcat",
) -> str:
    params: dict[str, str] = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category_title,
        "cmlimit": str(min(max(cmlimit, 1), 500)),
        "cmtype": cmtype,
        "format": "json",
        "formatversion": "2",
    }
    if cmcontinue:
        params["cmcontinue"] = cmcontinue
    return f"{api_root}?{urllib.parse.urlencode(params)}"


def _member_type(row: dict[str, Any]) -> str:
    raw = row.get("type")
    if isinstance(raw, str) and raw:
        return raw
    ns = int(row.get("ns", -1))
    if ns == 14:
        return "subcat"
    if ns == 0:
        return "page"
    if ns == 6:
        return "file"
    return "unknown"


def parse_categorymembers_payload(payload: MappingLike) -> tuple[list[CategoryMember], str | None]:
    """Parse one API JSON object into members + optional cmcontinue."""
    if isinstance(payload, (bytes, bytearray)):
        data = json.loads(payload.decode("utf-8"))
    elif isinstance(payload, str):
        data = json.loads(payload)
    else:
        data = dict(payload)

    query = data.get("query") or {}
    rows = query.get("categorymembers") or []
    members: list[CategoryMember] = []
    for row in rows:
        title = str(row.get("title") or "").strip()
        if not title:
            continue
        pageid = row.get("pageid")
        members.append(
            CategoryMember(
                pageid=int(pageid) if pageid is not None else None,
                title=title,
                ns=int(row.get("ns", 0)),
                member_type=_member_type(row),
            )
        )

    cont = data.get("continue") or {}
    cmcontinue = cont.get("cmcontinue")
    if cmcontinue is not None:
        cmcontinue = str(cmcontinue)
    return members, cmcontinue


def discover_category_members(
    *,
    category_title: str = DEFAULT_CATEGORY,
    api_root: str = DEFAULT_API,
    fetch: FetchFn | None = None,
    cmlimit: int = 500,
    max_pages: int = 50,
    pause_seconds: float = 0.0,
) -> list[CategoryMember]:
    """Paginate categorymembers until exhausted or max_pages.

    pause_seconds > 0 adds a polite delay between page requests (live runs).
    """
    fetch_fn = fetch or default_fetch
    all_members: list[CategoryMember] = []
    cmcontinue: str | None = None

    for _ in range(max_pages):
        url = build_categorymembers_url(
            api_root=api_root,
            category_title=category_title,
            cmcontinue=cmcontinue,
            cmlimit=cmlimit,
        )
        try:
            raw = fetch_fn(url)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"categorymembers HTTP {exc.code} for {url}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"categorymembers network error: {exc}") from exc

        batch, cmcontinue = parse_categorymembers_payload(raw)
        all_members.extend(batch)
        if not cmcontinue:
            break
        if pause_seconds > 0:
            time.sleep(pause_seconds)
    else:
        raise RuntimeError(
            f"categorymembers pagination exceeded max_pages={max_pages}"
        )

    return all_members


def discover_absorption_members(
    *,
    fetch: FetchFn | None = None,
    pause_seconds: float = 0.5,
) -> list[CategoryMember]:
    """Convenience: Category:Absorption with a default polite pause."""
    return discover_category_members(
        category_title=DEFAULT_CATEGORY,
        fetch=fetch,
        pause_seconds=pause_seconds if fetch is None else 0.0,
    )


def pages_only(members: Iterable[CategoryMember]) -> list[CategoryMember]:
    return [m for m in members if m.is_page and not m.title.startswith("Category:")]


def subcats_only(members: Iterable[CategoryMember]) -> list[CategoryMember]:
    return [m for m in members if m.is_subcategory]
