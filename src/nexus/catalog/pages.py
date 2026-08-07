"""Fetch and parse Superpower Wiki page summaries (I3 / I3.1).

Primary source: MediaWiki prop=extracts (batched). Fandom can return blank
extracts, so I3.1 falls back to action=parse per affected title and derives a
bounded plain-text first paragraph from returned HTML.

Network I/O is injectable for offline tests. No CoreState mutation. No policy
classification happens here.
"""

from __future__ import annotations

import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Callable, Iterable
from urllib.parse import quote, unquote

from nexus.catalog.discover import DEFAULT_API, DEFAULT_USER_AGENT

FetchFn = Callable[[str], bytes]
WIKI_PAGE_BASE = "https://powerlisting.fandom.com/wiki/"


@dataclass(frozen=True)
class PageDocument:
    title: str
    pageid: int | None
    url: str
    summary: str
    extract_html: str = ""
    categories: tuple[str, ...] = ()
    raw_query: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"title": self.title, "pageid": self.pageid, "url": self.url, "summary": self.summary, "extract_html": self.extract_html, "categories": list(self.categories)}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PageDocument":
        return cls(title=str(data.get("title") or "").strip(), pageid=int(data["pageid"]) if data.get("pageid") is not None else None, url=str(data.get("url") or ""), summary=str(data.get("summary") or ""), extract_html=str(data.get("extract_html") or ""), categories=tuple(str(c) for c in (data.get("categories") or [])))


def slugify_title(title: str) -> str:
    t = unquote(quote(title.strip().replace(" ", "_"), safe=":/()!'*_"))
    return re.sub(r"[^A-Za-z0-9._()-]+", "_", t).strip("_") or "page"


def page_url(title: str) -> str:
    return WIKI_PAGE_BASE + quote(title.replace(" ", "_"), safe=":/")


def default_fetch(url: str, timeout: float = 30.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT, "Accept": "application/json"}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return resp.read()


def build_extracts_url(titles: Iterable[str], *, api_root: str = DEFAULT_API, exintro: bool = True, explaintext: bool = True) -> str:
    title_list = "|".join(t.strip() for t in titles if t.strip())
    if not title_list:
        raise ValueError("titles must be non-empty")
    params = {"action": "query", "prop": "extracts|categories|info", "exintro": "1" if exintro else "0", "explaintext": "1" if explaintext else "0", "redirects": "1", "cllimit": "50", "titles": title_list, "format": "json", "formatversion": "2"}
    return f"{api_root}?{urllib.parse.urlencode(params)}"


def build_parse_url(title: str, *, api_root: str = DEFAULT_API) -> str:
    title = title.strip()
    if not title:
        raise ValueError("title must be non-empty")
    params = {"action": "parse", "page": title, "prop": "text|categories", "redirects": "1", "format": "json", "formatversion": "2"}
    return f"{api_root}?{urllib.parse.urlencode(params)}"


def _clean_summary(text: str, max_len: int = 2000) -> str:
    text = re.sub(r"\s+", " ", html.unescape((text or "").strip()))
    return text[: max_len - 1].rstrip() + "…" if len(text) > max_len else text


class _FirstParagraphText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._in_p = False
        self._complete = False
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "p" and not self._complete:
            self._in_p = True
        elif tag.lower() == "br" and self._in_p:
            self._parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "p" and self._in_p:
            self._in_p = False
            if _clean_summary("".join(self._parts)):
                self._complete = True

    def handle_data(self, data: str) -> None:
        if self._in_p and not self._complete:
            self._parts.append(data)

    @property
    def text(self) -> str:
        return _clean_summary("".join(self._parts))


def html_to_first_paragraph(html_text: str) -> str:
    parser = _FirstParagraphText()
    try:
        parser.feed(html_text or "")
        parser.close()
    except Exception:
        pass
    return parser.text or _clean_summary(re.sub(r"<[^>]+>", " ", html_text or ""))


def _categories(raw: Any) -> tuple[str, ...]:
    out: list[str] = []
    for item in raw or []:
        title = str(item.get("title") if isinstance(item, dict) else item or "")
        if title.startswith("Category:"):
            title = title[len("Category:"):]
        if title:
            out.append(title)
    return tuple(out)


def _payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, (bytes, bytearray)):
        return json.loads(payload.decode("utf-8"))
    if isinstance(payload, str):
        return json.loads(payload)
    return dict(payload)


def parse_extracts_payload(payload: Any) -> list[PageDocument]:
    docs: list[PageDocument] = []
    for page in (_payload(payload).get("query") or {}).get("pages") or []:
        if page.get("missing") is True:
            continue
        title = str(page.get("title") or "").strip()
        if title:
            docs.append(PageDocument(title=title, pageid=int(page["pageid"]) if page.get("pageid") is not None else None, url=page_url(title), summary=_clean_summary(str(page.get("extract") or "")), categories=_categories(page.get("categories")), raw_query=page if isinstance(page, dict) else None))
    return docs


def parse_parse_payload(payload: Any) -> PageDocument | None:
    parsed = _payload(payload).get("parse") or {}
    title = str(parsed.get("title") or "").strip()
    if not title:
        return None
    raw_html = parsed.get("text") or ""
    if isinstance(raw_html, dict):
        raw_html = raw_html.get("*") or ""
    return PageDocument(title=title, pageid=int(parsed["pageid"]) if parsed.get("pageid") is not None else None, url=page_url(title), summary=html_to_first_paragraph(str(raw_html)), extract_html=str(raw_html), categories=_categories(parsed.get("categories")), raw_query=parsed if isinstance(parsed, dict) else None)


def _fetch_bytes(fetch_fn: FetchFn, url: str, label: str) -> bytes:
    try:
        return fetch_fn(url)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"{label} HTTP {exc.code} for {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{label} network error: {exc}") from exc


def fetch_page_documents(titles: list[str], *, fetch: FetchFn | None = None, api_root: str = DEFAULT_API, batch_size: int = 10, pause_seconds: float = 0.5, fallback_parse: bool = True) -> list[PageDocument]:
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")
    fetch_fn = fetch or default_fetch
    clean = [t.strip() for t in titles if t and t.strip()]
    out: list[PageDocument] = []
    for i in range(0, len(clean), batch_size):
        raw = _fetch_bytes(fetch_fn, build_extracts_url(clean[i:i + batch_size], api_root=api_root), "extracts")
        out.extend(parse_extracts_payload(raw))
        if pause_seconds > 0 and i + batch_size < len(clean) and fetch is None:
            time.sleep(pause_seconds)
    if not fallback_parse:
        return out
    replacements: dict[str, PageDocument] = {}
    for doc in out:
        if doc.summary:
            continue
        parsed = parse_parse_payload(_fetch_bytes(fetch_fn, build_parse_url(doc.title, api_root=api_root), "parse"))
        if parsed is not None and parsed.summary:
            replacements[doc.title.casefold()] = PageDocument(title=parsed.title, pageid=parsed.pageid or doc.pageid, url=parsed.url or doc.url, summary=parsed.summary, extract_html=parsed.extract_html, categories=parsed.categories or doc.categories, raw_query=parsed.raw_query)
        if pause_seconds > 0 and fetch is None:
            time.sleep(pause_seconds)
    return [replacements.get(doc.title.casefold(), doc) for doc in out]


def fetch_one_page(title: str, *, fetch: FetchFn | None = None, api_root: str = DEFAULT_API) -> PageDocument | None:
    docs = fetch_page_documents([title], fetch=fetch, api_root=api_root, pause_seconds=0.0)
    return docs[0] if docs else None
