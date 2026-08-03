# Type inventory scripts (PS → InDesign)

See **`.cursor/docs/PS-TO-ID-TYPE-HANDOFF.md`** for the full handoff.

| npm | Script |
|-----|--------|
| `book:type:export` | `export_type_inventory_from_psb.py` |
| `book:type:export:split` | same + `Media/development/{unit}/type-inventory.json` |
| `book:type:validate` | `validate_type_inventory.py` |
| `book:type:page-map` | `build_indesign_page_map.py` |
| `book:type:apply` | `apply_type_inventory_to_indd.py` → `_generated/apply-type-inventory.jsx` |
| `book:type:styles` | ensure style kit JSX only |
| `book:type:pipeline` | export → page-map → validate → apply emit |

Fleet mirrors: `_core-scripts/shared-profile-content/scripts/picture-book-*-type*` (prefer project `scripts/` when present).
