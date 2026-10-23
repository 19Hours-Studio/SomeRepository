Proposal: the site is one `index.html` (Artifact) with a fixed top menu: **Релизы · Артисты · Новости · Демо · О лейбле · Контакты**. Each item is a hash anchor, and each release and artist has its own `#id` target. Every task from Home therefore takes at most 2 clicks.

**Shared content model** (one `<script>` object, and one `render()` that builds every section):

- **release**: `{cat:"ПОР-004", fmt:"LP", title, artist, date, format:"12\" 33⅓, 180 г", run:"300 нум. экз.", tracks:[{t, dur, isrc:"XX-POR-26-00041"}], credits:[[роль, имя]], pc:"℗© Порог, 2026", links:[{label:"Bandcamp", href:"#"}], sample:true}`
- **artist**: `{id, name, city, bio, booking}`. The artist's releases are derived from `release.artist`, so the discography is never typed twice.
- **news**: `{date, title, text, ref:"ПОР-004"}`
- **links**: when `sample:true`, links render as inert "ссылка-образец" text. ISRCs keep the "XX" country code, which is reserved for non-real codes.
- **footer**: the single footer statement ("концепт-сайт вымышленного лейбла") is also generated from the flags. Placeholder marking is a property of the data, not of hand-written HTML, so it cannot be forgotten.

=== IDEAS ===

IDEA 1
NAME: Линия порога
MECHANISM: The central move is structural. One thick horizontal "sill" line runs through the page and splits time: above it is what has been released, below it is what is "за порогом": upcoming releases, then the demo call. The page runs as follows:
- Header with the label statement ("Порог выпускает первые записи тех, кто только переступает").
- The latest release with a placeholder audio bar.
- Released catalogue, newest at the sill.
- The sill itself, labelled with today's date.
- Upcoming items with embargo dates.
- Demo rules: accepted / not accepted, 1–3 tracks, private link only, reply in 2 weeks.
- Artists, news, about, and contacts split into demo@ / press@ / booking@.

The palette is cool concrete grey (#d9dcd8) with graphite text and a single deep-ultramarine sill line. Display type is Unbounded, used only for catalogue numbers and section names; body type is Golos Text. Motion is none beyond focus states. The subject-only detail is that each release's position relative to the line is computed from its date, so the sill is a true timeline.
VALUE: A visitor sees at a glance what is out, what is coming, and how to cross into the label themselves, and they remember the line they literally scroll over.

IDEA 2
NAME: Ступени каталога
MECHANISM: The central move is typographic. The catalogue numbers ПОР-001…ПОР-009 form a staircase: each release row is indented one step further right on desktop and collapses to a stepped left rule on phones, so the label's history reads as climbing. The page runs as follows:
- A short manifesto and the newest release at the top step.
- The full stair of releases. Each row is a `<details>` that opens to tracklist, durations, format, run size, credits and the ℗© line.
- Artist profiles, each listing its own steps.
- News tied to catalogue numbers.
- Demo section, about, and contacts.

The palette is pale limestone with near-black ink and an oxide-red step riser. Display type is IBM Plex Mono for numbers and suffixes (LP, 7", MC); body type is Literata. Motion is only an instant open/close, disabled under reduced motion. The subject-only detail is that format suffixes and separate numbers per format follow real catalogue practice.
VALUE: A visitor can find any release by its number in seconds and leaves remembering a label whose catalogue is drawn as stairs to a threshold.

IDEA 3
NAME: Надпись на прогоне
MECHANISM: The central move is visual and taken from vinyl. Every release cover is an inline-SVG disc, and the label's identity lives in the run-out groove: the etched matrix text "ПОР-004 A · порог" circles the inner edge, and each side's tracklist sits beside its own label (A/B with timings within 18–22 min). The page runs as follows:
- Hero disc of the newest release with a placeholder play bar.
- A grid of discs, each opening an insert with credits, run ("300 нум. экз., 180 г"), ℗© line and outbound links.
- Artists with booking contacts.
- News.
- A demo panel framed as a "тестовый оттиск" checklist.
- About and contacts.

The palette is blue-grey sleeve board, navy ink and a signal-orange centre label, with dark-mode tokens. Display type is Prata, used sparingly; body type is Onest. Motion is a slow disc rotation on hover only, removed under reduced motion. The subject-only detail is the etched matrix number and the side timings, which no generic template has.
VALUE: A visitor browses and samples releases as physical records with full pressing detail, and remembers the etched run-out text as the label's signature.