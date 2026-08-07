"""Fetch and parse Superpower Wiki page summaries (I3).

Uses MediaWiki API prop=extracts (plain intro text) with optional full wikitext.
Network I/O is injectable for offline tests. Rate limiting is caller-controlled.
Does not mutate CoreState. Does not assign policy tags (I4).
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from urllib.parse import quote, unquote

from nexus.catalog.discover import DEFAULT_API, DEFAULT_USER_AGENT

FetchFn = Callable[[str], bytes]

WIKI_PAGE_BASE = "https://powerlisting.fandom.com/wiki/"


@dataclass(frozen=True)
class PageDocument:
    """Normalized page payload stored under pages/ and merged into index."""

    title: str
    pageid: int | None
    url: str
    summary: str
    extract_html: str = ""
    categories: tuple[str, ...] = ()
    raw_query: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "pageid": self.pageid,
            "url": self.url,
            "summary": self.summary,
            "extract_html": self.extract_html,
            "categories": list(self.categories),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PageDocument:
        cats = data.get("categories") or []
        return cls(
            title=str(data.get("title") or "").strip(),
            pageid=int(data["pageid"]) if data.get("pageid") is not None else None,
            url=str(data.get("url") or ""),
            summary=str(data.get("summary") or ""),
            extract_html=str(data.get("extract_html") or ""),
            categories=tuple(str(c) for c in cats),
        )


def slugify_title(title: str) -> str:
    """Filesystem-safe slug matching wiki underscores."""
    t = title.strip().replace(" ", "_")
    t = quote(t, safe=":/()!'*_")
    t = unquote(t)
    t = re.sub(r"[^A-Za-z0-9._()-]+", "_", t)
    return t.strip("_") or "page"


def page_url(title: str) -> str:
    return WIKI_PAGE_BASE + quote(title.replace(" ", "_"), safe=":/")


def default_fetch(url: str, timeout: float = 30.0) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "application/json"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return resp.read()


def build_extracts_url(
    titles: Iterable[str],
    *,
    api_root: str = DEFAULT_API,
    exintro: bool = True,
    explaintext: bool = True,
) -> str:
    title_list = "|".join(t.strip() for t in titles if t.strip())
    if not title_list:
        raise ValueError("titles must be non-empty")
    params = {
        "action": "query",
        "prop": "extracts|categories|info",
        "exintro": "1" if exintro else "0",
        "explaintext": "1" if explaintext else "0",
        "redirects": "1",
        "cllimit": "50",
        "titles": title_list,
        "format": "json",
        "formatversion": "2",
    }
    return f"{api_root}?{urllib.parse.urlencode(params)}"


def _clean_summary(text: str, max_len: int = 2000) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) > max_len:
        text = text[: max_len - 1].rstrip() + "…"
    return text


def parse_extracts_payload(payload: Any) -> list[PageDocument]:
    """Parse query+extracts JSON into PageDocument list."""
    if isinstance(payload, (bytes, bytearray)):
        data = json.loads(payload.decode("utf-8"))
    elif isinstance(payload, str):
        data = json.loads(payload)
    else:
        data = dict(payload)

    query = data.get("query") or {}
    pages = query.get("pages") or []
    docs: list[PageDocument] = []
    for page in pages:
        if page.get("missing") is True:
            continue
        title = str(page.get("title") or "").strip()
        if not title:
            continue
        cats_raw = page.get("categories") or []
        cat_titles = []
        for c in cats_raw:
            if isinstance(c, dict):
                ct = str(c.get("title") or "")
            else:
                ct = str(c)
            if ct.startswith("Category:"):
                ct = ct[len("Category:") :]
            if ct:
                cat_titles.append(ct)
        extract = _clean_summary(str(page.get("extract") or ""))
        docs.append(
            PageDocument(
                title=title,
                pageid=int(page["pageid"]) if page.get("pageid") is not None else None,
                url=page_url(title),
                summary=extract,
                extract_html="",
                categories=tuple(cat_titles),
                raw_query=page if isinstance(page, dict) else None,
            )
        )
    return docs


def fetch_page_documents(
    titles: list[str],
    *,
    fetch: FetchFn | None = None,
    api_root: str = DEFAULT_API,
    batch_size: int = 10,
    pause_seconds: float = 0.5,
) -> list[PageDocument]:
    """Fetch extracts for titles in batches with optional pause between calls."""
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")
    fetch_fn = fetch or default_fetch
    clean = [t.strip() for t in titles if t and t.strip()]
    out: list[PageDocument] = []

    for i in range(0, len(clean), batch_size):
        chunk = clean[i : i + batch_size]
        url = build_extracts_url(chunk, api_root=api_root)
        try:
            raw = fetch_fn(url)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"extracts HTTP {exc.code} for {url}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"extracts network error: {exc}") from exc
        out.extend(parse_extracts_payload(raw))
        if pause_seconds > 0 and i + batch_size < len(clean) and fetch is None:
            time.sleep(pause_seconds)
    return out


def fetch_one_page(
    title: str,
    *,
    fetch: FetchFn | None = None,
    api_root: str = DEFAULT_API,
) -> PageDocument | None:
    docs = fetch_page_documents([title], fetch=fetch, api_root=api_root, pause_seconds=0.0)
    return docs[0] if docs else None
