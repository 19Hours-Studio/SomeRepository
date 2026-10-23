=== BUILD ===
FILE: /home/user/SomeRepository/engine/runs/porog/final/index.html

FIXED:
- Listener door promised concerts that didn't exist → added a «Концерты» block (`#shows`) with three made-up dates and venues, plus a news post announcing them. The door link now points there, the section and nav item are called «Новости и концерты», and the footer disclaimer now mentions concerts and venues.
- Newest release was far below the fold on phones →
  - The hero now has a strip above the three doors: mini cover, «ПОР-007 · Тамбур — «Ступени»» and a «Слушать» button, so the release is on the first screen at every width.
  - Below 900 px the doors are smaller: thinner frames, smaller headings, links as wrapping chips, inbox on one line.
  - On phones the main cover is capped at 62% width and artist placeholders are shorter.
  - The phone page is about the same length as before (11,527 px vs 11,511 px), because the concerts block added height.
- ПОР-005 copy error → now reads «По треку от каждого из четырёх артистов лейбла. «Следующая» Тамбура — неизданная демо-версия.», which matches the four-track list.
- Grey-plus-yellow template palette → new colours taken from a Russian apartment stairwell (подъезд): whitewash background, oil-paint green door frames and rules, and a full-width painted lower band under the doors. The yellow stair-edge stripe stays for the active door and the focus ring. Dark mode is a night stairwell in the same colours, and the ПОР-007 cover was recoloured to match.

KEPT: The three labelled doors, each captioned with its own inbox; the catalogue numbers; ℗© lines; the demo form that writes the letter text; the press kit and embargo note; the footer notice that the label is fictional.

NOT FIXED:
- The "choose your path" three-column hero is a familiar pattern → it is the concept's central move, so it stays.

CHECKS:
- Three render rounds. Horizontal overflow is 0 px at 1280 light and dark and at 390 light and dark, with no console errors and no failed loads.
- After the third render I added `preserveAspectRatio="xMidYMid slice"` to the four artist placeholder images. The last screenshots showed them letterboxed on phones, and this should make them fill the frame. That change was not rendered again because the three rounds were used up.
- 768 px was not rendered; the tool only renders 390 and 1280.