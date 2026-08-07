"""Wiki catalog models and store (Phase 1: Category:Absorption).

Catalog holds indexed Superpower Wiki rows. It does not mutate CoreState.
See docs/SUPERPOWER_WIKI_INGESTION.md and docs/CATALOG_VS_WALK.md.
"""

from nexus.catalog.batch_report import (
    BatchReportInput,
    BatchWriteResult,
    ConsoleSnapshot,
    batch_number_for_ability_index,
    write_batch_from_catalog,
    write_batch_report,
)
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
from nexus.catalog.walk_queue import QueueItem, WalkQueue, open_walk_queue, walkable_entries

__all__ = [
    "POLICY_TAGS",
    "BatchReportInput",
    "BatchWriteResult",
    "CatalogCursor",
    "CatalogEntry",
    "CatalogStore",
    "CategoryMember",
    "ClassifyReport",
    "ClassifyResult",
    "ConsoleSnapshot",
    "EnrichReport",
    "PageDocument",
    "QueueItem",
    "SchemaDraft",
    "SyncReport",
    "WalkQueue",
    "WalkRef",
    "absorption_root",
    "batch_number_for_ability_index",
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
    "open_walk_queue",
    "pages_only",
    "quarantined_ability_names",
    "subcats_only",
    "sync_absorption_catalog",
    "walkable_entries",
    "write_batch_from_catalog",
    "write_batch_report",
]
