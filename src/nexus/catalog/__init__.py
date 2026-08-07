"""Wiki catalog models and store (Phase 1: Category:Absorption).

Catalog holds indexed Superpower Wiki rows. It does not mutate CoreState.
See docs/SUPERPOWER_WIKI_INGESTION.md and docs/CATALOG_VS_WALK.md.
"""

from nexus.catalog.classify import (
    ClassifyReport,
    ClassifyResult,
    classify_entry,
    classify_index,
    classify_text,
)
from nexus.catalog.discover import (
    CategoryMember,
    discover_absorption_members,
    discover_category_members,
    pages_only,
    subcats_only,
)
from nexus.catalog.enrich import EnrichReport, enrich_absorption_pages
from nexus.catalog.models import (
    POLICY_TAGS,
    CatalogCursor,
    CatalogEntry,
    SchemaDraft,
    WalkRef,
)
from nexus.catalog.pages import PageDocument, fetch_one_page, fetch_page_documents
from nexus.catalog.paths import (
    absorption_root,
    default_repo_root,
    ensure_absorption_layout,
)
from nexus.catalog.quarantine_names import quarantined_ability_names
from nexus.catalog.store import CatalogStore
from nexus.catalog.sync import SyncReport, merge_members_into_index, sync_absorption_catalog

__all__ = [
    "POLICY_TAGS",
    "CatalogCursor",
    "CatalogEntry",
    "CatalogStore",
    "CategoryMember",
    "ClassifyReport",
    "ClassifyResult",
    "EnrichReport",
    "PageDocument",
    "SchemaDraft",
    "SyncReport",
    "WalkRef",
    "absorption_root",
    "classify_entry",
    "classify_index",
    "classify_text",
    "default_repo_root",
    "discover_absorption_members",
    "discover_category_members",
    "enrich_absorption_pages",
    "ensure_absorption_layout",
    "fetch_one_page",
    "fetch_page_documents",
    "merge_members_into_index",
    "pages_only",
    "quarantined_ability_names",
    "subcats_only",
    "sync_absorption_catalog",
]
