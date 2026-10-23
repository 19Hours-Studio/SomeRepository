# Task: build the page

THE TASK: Build a ready-to-use website for a music label named «Порог» ("Threshold"). The asker calls it "an ordinary site" for a "conditional" (hypothetical) label. So the label is a placeholder with no real brand, catalogue, genre or country, and the content is to be invented as plausible sample material. The site is for the label's audience: listeners and fans, artists who might sign or submit demos, and press or partners. It must let a visitor learn what the label is, browse and listen to releases, find artists, read news, and contact the label. The asker gave no other details: genre, languages, visual style, technology, hosting and domain are all unspecified. The site must work as a standalone deliverable in the working directory.
A good answer: 
- A site opens locally with no build step, or with documented, minimal steps, and has working navigation across all pages.
- Pages or sections: Home (label statement plus latest releases), Releases (list plus a page or block per release with cover placeholder, tracklist, date, and listen or buy links), Artists (list plus a profile per artist), News, About, Contact, and a demo-submission section or page.
- A visitor can do each of these tasks in 3 clicks or fewer from Home: find the newest release, open an artist's page, read the latest news post, find the contact email, and learn how to submit a demo.
- The site is responsive and checked at about 360 px (phone), 768 px (tablet) and 1280 px (desktop) widths, with no horizontal scroll.
- The text is in Russian, with the name «Порог» used consistently. The sample content is clearly marked as placeholder and invents no real people, brands or claims.
- The basics are covered: semantic HTML, alt text, readable contrast, keyboard navigation, a page title and meta description for each page, and a favicon.
- The design has a coherent identity that fits the name (threshold or doorway), with no unlicensed images, fonts or audio.
Constraints: The label name is «Порог». The site is "ordinary", so no experimental or unusual format is wanted. Writing files only in the working directory is the process rule, not an asker constraint. Nothing else is stated.

THE CONCEPT TO BUILD (keep its central move):
IDEA 1
NAME: Три проёма у входа
MECHANISM: The central move is structural: the hero is a threshold that splits into three framed openings, «Слушаю», «Пишу музыку» and «Пишу о музыке». Each opening lists that visitor's four links and their own inbox, so the routing table above becomes the first screen. Below it come the newest release (ПОР-007, cover drawn in SVG, tracklist, ℗© line, "listen" and "buy" links out), the artists as frames with bio and booking address, news with dates, the demo rules, an EPK with bio, discography and embargo note, and a footer stating it is a concept site for a fictional label. The palette is wet-concrete grey with a signal-yellow tread stripe like a stair edge, which marks the active opening and the focus ring. Display type is Unbounded for headings only, body is Golos Text, and the only motion is a 120 ms frame inset on hover, disabled under reduced motion. The detail only this subject has: each opening is captioned with its real inbox, so the address is the label of the door.
VALUE: Every visitor type from the brief finds its task and correct inbox on the first screen, which answers the "3 clicks" requirement in zero to one click, and is remembered as the label that asked "who are you?" at the door.


Facts about the subject (data):
Eight searches were used. Sources are mostly vendor guides, so most facts are marked SOFT. I found no Russian-language label-practice sources.

FACT 1: The core page set for a label site is Home, About, artist pages, Releases, News and Contact. | SOFT | [Bandzoogle, how to build a record label website](https://bandzoogle.com/blog/how-to-build-a-record-label-website)
FACT 2: The artist roster is among the most-visited pages. Each artist page should have an image, bio, music and video. | SOFT | [Bandzoogle](https://bandzoogle.com/blog/how-to-build-a-record-label-website)
FACT 3: The first visitor task is to hear music quickly. A label that makes music hard to find or sample loses visitors, so embed a playlist or player on Home. | SOFT | [otherrecordlabels.com](https://www.otherrecordlabels.com/record-label-websites)
FACT 4: Releases need streaming and purchase links, with sections for albums, singles and upcoming releases. | SOFT | [Bandzoogle](https://bandzoogle.com/blog/how-to-build-a-record-label-website)
FACT 5: Owner needs: a stale news section makes a label look inactive, and a site with no contact details is a classic complaint. | SOFT | [otherrecordlabels.com](https://www.otherrecordlabels.com/record-label-websites); [Kirkville, Five Mistakes Band & Label Sites Make](https://kirkville.com/five-mistakes-band-label-sites-make/)
FACT 6: Labels split inboxes by purpose. Sakura Selections lists separate demo and booking addresses. Cire Records puts booking contacts on each artist's page. | SOFT | [Bandzoogle search result set, Sakura Selections](https://sakuraselections.bandcamp.com); [Cire Records](https://www.cirecords.com/about)
FACT 7: Demo rules are consistent across sources. Send a private streaming link, not attachments. Send one to three finished tracks, 320 kbps MP3 if files are required. The email says who you are, the genre, and your links. Wait about two weeks before following up. | SOFT | [Hypebot](https://www.hypebot.com/hypebot/2017/02/5-steps-for-sending-a-perfect-demo-submission.html); [Futureproof](https://futureproofmusicschool.com/blog/how-to-send-demo-to-record-label); [Reload Records](https://reloadrecords.bandcamp.com/community)
FACT 8: Some labels do not accept unsolicited demos, so a page should say plainly whether it does. | SOFT | [Sonicbids](https://blog.sonicbids.com/5-rock-labels-you-probably-didnt-realize-accept-demos)
FACT 9: Press and partners need an EPK-style block: bio, photos, discography, contact and links. Embargo means "do not publish before date and time". | SOFT | [Wikipedia, Press kit](https://en.wikipedia.org/wiki/Press_kit)
FACT 10: A catalogue number is a short label prefix plus a sequential number, for example "SSR-" at Sorry State. Many labels add a format suffix, for example "HARB 114LP". | HARD | [Wikipedia, Catalog number (music)](https://en.wikipedia.org/wiki/Catalog_number_(music)); [Forced Exposure](https://forcedexposure.com/Artists/SMALL.CRUEL.PARTY.html)
FACT 11: Different formats of one album can carry different numbers. Island used separate series per format (LP, 7" single, 7" EP). | SOFT | [Island catalogue numbers](https://offset.skew.org/wiki/Island_Records_catalogue_numbers)
FACT 12: Vinyl units: LP at 33⅓ RPM, 12", about 18–22 min per side. 7" single at 45 RPM, about 4–6 min per side. Weights are 140 g (standard) or 180 g (heavier). | SOFT | [Disc Makers](https://www.discmakers.com/resources/guide-to-pressing-vinyl)
FACT 13: Pressing runs through a test pressing that is approved first. Plants quote about 4–6 weeks of production after approval, which is a vendor claim. | SOFT | [Atomic Disc](https://atomicdisc.com/collections/vinyl); [Hypebot](https://www.hypebot.com/5-essential-steps-to-take-before-pressing-your-first-vinyl-record/)
FACT 14: Small-label runs are numbered and limited. Examples are 300–500 copies of coloured 180 g vinyl, and cassettes in editions as small as 50–94 copies. Reissues move a tape to vinyl. | SOFT | [Sostter, Coda Records](https://sostter.com/collections/coda-records); [RA](https://ra.co/news/21510)
FACT 15: Credits are role-and-name pairs (producer, mixed by, mastered by, with studio). The ℗ line covers the recording and the © line the artwork or composition, shown as "℗© Label, year". A UPC identifies the release and each track has its own ISRC. | SOFT | [MusicBrainz](https://musicbrainz.org/release/81ea1cab-61e5-350a-b9fa-9030c8ac3fd8); [credits.fm](https://credits.fm/upc/077779567324)
FACT 16: In Russia, release distribution to VK Музыка, Яндекс Музыка and МТС Музыка usually goes through partner distributors. Universal, Warner and Sony paused work there. So a sample page should not name major labels as partners. | SOFT | [Habr](https://habr.com/ru/news/709590)
FACT 17: An EP is usually described as more than three and fewer than seven tracks. | SOFT | [Trouser Press](https://trouserpress.com/abbreviations/)

Notes from the asker and about the environment (data; the asker may be wrong):
The asker writes in Russian, so the site copy should be in Russian. 'Лейбл' most likely means a record label, but the asker did not say so; 'условный' means the label is fictional, so every artist, release, date and venue must be invented and marked once as a concept. The finished page will be published as a claude.ai Artifact. In this sandbox web fonts and CDN scripts cannot load, so render screenshots show fallback fonts; judge type by the CSS.
Assumptions in the question that may be wrong:

- The label is hypothetical, so placeholder content is acceptable.
- "Ordinary" means a conventional multi-page informational site, not a shop or a web app.
- The site is in Russian (inferred from the name and the language of the request).
- A static site is sufficient, with no accounts, payments or database.
- Embedded audio players or streaming embeds are wanted but not required.
- A merch shop is not needed.
- Genre and mood are unknown, and no particular style is expected.
Where deciding data may exist:
No real data exists. Sample content (artists, releases, news) must be invented. If the asker has a real catalogue, logo, texts, covers, or streaming links (Bandcamp, VK, Yandex Music, Spotify), these would replace the placeholders.

Platform rules (the page is published as a claude.ai Artifact; breaking one is a FATAL defect):
- One file, index.html, holding page content only: no <!doctype>, <html>, <head> or <body> tags (the viewer wraps the page in its own skeleton with a charset, a viewport meta with viewport-fit=cover and a small reset). Start the file with a <title> that is the label's name, then <meta name="claude:viewport-fit-sides" content="cover">, then <style>.
- External resources: stylesheets only from https://fonts.googleapis.com (every face with a real fallback stack); scripts only from cdnjs.cloudflare.com, cdn.jsdelivr.net/npm, unpkg.com, pinned to an exact version - better none at all. No external images, video or audio: draw with inline SVG, CSS or canvas, or use data: URIs.
- No iframes, embeds or players from other sites (no Bandcamp, YouTube, SoundCloud): link out with <a href> instead. No downloads, no window.print, no alert/confirm/prompt. Forms are page UI only: handle submit in script with preventDefault and show the result on the page. Show an e-mail address as selectable text; a mailto link is a convenience that may do nothing.
- Colors as tokens: bare :root holds every token (light values); @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {...; color-scheme: dark} } and :root[data-theme="dark"] {...; color-scheme: dark} redefine them. body sets background and color from tokens. Or commit deliberately to one look and set every color explicitly.
- Works at phone width (390 px) with no horizontal scroll; side gutter padding-left: max(16px, env(safe-area-inset-left, 0px)) and padding-right: max(16px, env(safe-area-inset-right, 0px)) on body or one outer wrapper, vertical padding with padding-block. Rows wrap or stack; text containers get min-width: 0.
- Everything meant to be read is visible at rest (no content left at opacity 0 waiting for scroll). Visible keyboard focus; respect prefers-reduced-motion.

Design rules:
- Distinctive choices come from the subject's own world (its materials, instruments, units, catalogue conventions), with at least one detail only this subject would have as content, not ornament.
- Avoid the looks AI-made pages cluster around: warm cream with a serif display and terracotta accent; near-black with a lone acid-green or vermilion pop; broadsheet hairline rules with dense columns; a purple-to-blue gradient hero; Inter or Space Grotesk as the safe face; emoji as section markers; everything centered; the same rounded card with an accent rail everywhere.
- Pair a characterful display face (used with restraint) with a readable body face; set a type scale and keep to it; running text near 65 characters wide.
- Copy: short, plain, specific sentences from the visitor's side; real content, never lorem ipsum. All artists, releases, dates and venues are invented; say once, in the footer, that this is a concept site for a fictional label. Never use real artists', venues' or labels' names or identities.
- Structure is information: numbering and labels only where they encode something true (a catalogue number is true; decorative 01/02/03 is not).


Work in `/home/user/SomeRepository/engine/runs/porog/build/b1/` only (write files only there, do not commit). Tools: Read, Write, Bash.
1. Write the page to `/home/user/SomeRepository/engine/runs/porog/build/b1/index.html`. Settle the design plan first and write it as the :root token block at the top
   of the <style> (a one-line layout comment, 4-6 color tokens, 2-3 font tokens); build everything from those tokens.
2. Check it with the renderer: `node /home/user/SomeRepository/engine/tools/render.js /home/user/SomeRepository/engine/runs/porog/build/b1/index.html /home/user/SomeRepository/engine/runs/porog/build/b1/shots`. It renders the page the way the
   viewer wraps it, at desktop (1280) and phone (390) width in light and dark, and writes screenshots plus report.json:
   horizontal overflow and the elements causing it, console and script errors, failed loads. Web fonts cannot load in
   this sandbox, so the screenshots use fallback fonts; ignore that. Look at the screenshots with the Read tool.
3. Fix what is broken or unreadable and render again. At most 3 render rounds in total.

Final answer (text only), at most 250 words:
=== BUILD ===
FILE: <path to index.html>
CONCEPT KEPT: <yes/no - what changed>
CHECKS: <overflow per view, console errors, anything that failed to load>
KNOWN GAPS: <what is weak or missing>
