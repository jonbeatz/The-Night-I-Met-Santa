# DIGITAL-FLIPBOOK-WATCH.md — Optional web gift (post-print)

**Status:** WATCH / later — **do not** block Aug 15 print path.  
**Source notes:** `.cursor/docs/book/Childrens_Book_Webpage.md` (Jon 2026-07-15)  
**Use when:** Want a shareable flipping-page site for family *after* Lulu gift is locked.

---

## What we verified (2026-07-15)

| Claim in notes | Verdict |
|----------------|---------|
| Combine PDF engine + page-flip for Next.js | Sound pattern in principle |
| Avoid **turn.js** (jQuery) in modern Next | Agree |
| Use `dynamic(..., { ssr: false })` for canvas flip libs | Agree — browser APIs only |
| Prefer **pre-converted page images** over live PDF parse for UX | Agree (also matches our print pipeline: already flat page images) |
| `react-pageflip` is “most modern / actively maintained” | **Overstated** — npm last published ~5 years (v2.0.3); still usable but aged; check forks/alts before building |
| `react-pdf-flipbook-viewer` all-in-one | Candidate only if we want PDF-in without image prebuild |
| Puppeteer / PDFKit / pdfmake / MinerU / Docling | Useful Hermes tooling elsewhere — **not** for Lulu interior; we already use Pillow → img2pdf / pikepdf / PyMuPDF |

---

## Recommended path *if* we build later

1. **Reuse** `Pages/*.jpg` (or optimized web WebP from those) — skip client-side PDF.js for the gift flipbook.
2. Host on **JonBeatz.dev** (or private Vercel) with:
   - `react-pageflip` **or** a maintained StPageFlip fork / newer flip component (re-check at build time)
   - `next/dynamic` + `ssr: false`
   - Tailwind wrapper + soft book-shadow; `size="stretch"` for mobile
3. Do **not** put Jack photos or purchase links live without Jon’s privacy call.

---

## Out of scope for this book sprint

- Flipbook is **not** a Lulu deliverable.
- Do not start a Next.js book site until hardcover proof is ordered / approved.

---

## Links (from notes — keep as bookmarks)

- https://github.com/Nodlik/react-pageflip  
- https://nodlik.github.io/StPageFlip/  
- https://mozilla.github.io/pdf.js/  
- https://www.lulu.com/create (pricing / templates)
