"""Wiki catalog models and store (Phase 1: Category:Absorption).

Catalog holds indexed Superpower Wiki rows. It does not mutate CoreState.
See docs/SUPERPOWER_WIKI_INGESTION.md and docs/CATALOG_VS_WALK.md.
"""

from nexus.catalog.models import (
    POLICY_TAGS,
    CatalogCursor,
    CatalogEntry,
    SchemaDraft,
    WalkRef,
)
from nexus.catalog.paths import (
    absorption_root,
    default_repo_root,
    ensure_absorption_layout,
)
from nexus.catalog.store import CatalogStore

__all__ = [
    "POLICY_TAGS",
    "CatalogCursor",
    "CatalogEntry",
    "CatalogStore",
    "SchemaDraft",
    "WalkRef",
    "absorption_root",
    "default_repo_root",
    "ensure_absorption_layout",
]
