**Visitor tasks, paths and inboxes.** On one page every task is one anchor jump from the top bar, and opening a release's details is a second click.

| Visitor | Task | Path from the top | Inbox (placeholder) |
|---|---|---|---|
| Listener | Newest release | first item in the hero, 0–1 clicks | — |
| Listener | Artist profile | «Артисты» → card, 2 clicks | — |
| Listener | Latest news | «Новости», 1 click, first post | — |
| Artist | Demo policy | «Демо», 1 click | demo@porog.example |
| Press | EPK | «Пресса», 1 click | press@porog.example |
| Promoter | Booking | artist card, 2 clicks | booking@porog.example |
| Anyone | General contact | footer or «Контакты», 1 click | hello@porog.example |

The `.example` domain is reserved, so these addresses can never point at a real company.

The demo policy states five things in plain words:
- the label accepts unsolicited demos;
- send a private link, not attachments;
- send 1–3 finished tracks;
- include who you are, your genre and your links;
- expect a reply within 14 days, and don't write again before then.

=== IDEAS ===

IDEA 1
NAME: Три проёма у входа
MECHANISM: The central move is structural: the hero is a threshold that splits into three framed openings, «Слушаю», «Пишу музыку» and «Пишу о музыке». Each opening lists that visitor's four links and their own inbox, so the routing table above becomes the first screen. Below it come the newest release (ПОР-007, cover drawn in SVG, tracklist, ℗© line, "listen" and "buy" links out), the artists as frames with bio and booking address, news with dates, the demo rules, an EPK with bio, discography and embargo note, and a footer stating it is a concept site for a fictional label. The palette is wet-concrete grey with a signal-yellow tread stripe like a stair edge, which marks the active opening and the focus ring. Display type is Unbounded for headings only, body is Golos Text, and the only motion is a 120 ms frame inset on hover, disabled under reduced motion. The detail only this subject has: each opening is captioned with its real inbox, so the address is the label of the door.
VALUE: Every visitor type from the brief finds its task and correct inbox on the first screen, which answers the "3 clicks" requirement in zero to one click, and is remembered as the label that asked "who are you?" at the door.

IDEA 2
NAME: Каталог ПОР-001…ПОР-012
MECHANISM: The central move is the catalogue number as the page's spine: a left rail (a top strip on phones) lists ПОР-001 to ПОР-012 with a format suffix (LP, 7", CS), and every release, artist and news item is linked to a number. Top to bottom: a two-line label statement, then the latest number expanded as a full release sheet with format, 180 g, a numbered run of 300, date, UPC/ISRC placeholders, credits as role–name pairs and link-outs. After that come the compact catalogue table, artists with "appears on ПОР-…", news dated to pressing events (test pressing approved, upcoming release), demos, press and a contacts table. The look is a cold blue-grey index-card stock with ink-navy text and one ochre stamp colour. IBM Plex Mono is used for numbers and Golos Text for prose, with no motion beyond focus states. The detail only this subject has: an "upcoming" row shows a reserved number, ПОР-013, with "тест-прессинг на утверждении".
VALUE: A visitor reads the label's entire output as a real catalogue in seconds and opens any release in one tap, and the depth of the catalogue detail is what sets it apart from a template.

IDEA 3
NAME: Порог срабатывания
MECHANISM: The central move borrows the noise-gate threshold from audio. A horizontal dB line runs across the hero, and the placeholder player is an SVG waveform marked «образец, звук не подключён». Peaks above the line are filled and peaks below it are hatched. Sections follow as releases (each with its waveform thumbnail, tracklist, durations and link-outs), artists, news, «Демо — выше порога» with the five rules as gate settings («формат: ссылка», «треков: 1–3», «ответ: 14 дней»), press and split contacts. The palette is graphite on pale mint-grey with a magenta meter colour. Unbounded is used sparingly for headings, Golos Text carries the body, and tabular figures are used for times. Static drawings replace the animated meter under reduced motion. The detail only this subject has: tracklist durations are drawn to scale against an LP side's roughly 20-minute limit, so each side visibly fits its vinyl.
VALUE: Listeners see the music first and artists see exactly what clears the bar, all in one scroll with clear links, and the gate line makes the name «Порог» audible rather than literal.