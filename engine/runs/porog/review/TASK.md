# Task: blind review of built pages - find what would make each fail its visitors or look generic

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

Below are 2 pages built for this task. You are the toughest competent outside reviewer: a designer and front-end
engineer who will put their name on the one that ships. Do NOT fix the pages; find their defects and rank them.
Work only in `/home/user/SomeRepository/engine/runs/porog/review/` (write files only there, do not commit). Tools: Read, Write, Bash.

For each page:
1. Render it: `node /home/user/SomeRepository/engine/tools/render.js <its index.html> /home/user/SomeRepository/engine/runs/porog/review/shots_<k>`. Read report.json and look at the screenshots
   (desktop and phone, light and dark, plus the full-page shot) with the Read tool. Web fonts cannot load here; judge the
   type by the CSS, not by the fallback in the screenshots.
2. Read the HTML. Check the platform rules below line by line.
3. Judge it as a visitor: can they find releases, artists, shows and how to get in touch within seconds? Is the copy
   plain, specific and free of errors? Is it memorable for this subject, or does it look like a template or one of the
   AI-made looks listed below?
Severity: FATAL = breaks a platform rule, horizontal scroll at phone width, a script error that breaks content,
unreadable text in either theme, or a visitor task impossible; MAJOR = a visitor task slow or hidden, a generic look, a
weak hierarchy, a copy error; MINOR = polish. A defect needs evidence (a screenshot, a report line or a code line).

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


Final answer (text only), exactly this format:
=== REVIEW ===
IDEA 1: <page name>
DEFECT | <FATAL/MAJOR/MINOR> | <one sentence: what is wrong> | <evidence>
(as many DEFECT lines as needed, most severe first)
FIT | <number of requirements met> of <number of requirements in the task> | <one line>
SURVIVES | <what works, one line>
KNOWN | <yes / partly / no: does it look like an existing template or a well-known site?> | <which>
(same for the other pages, in the same order as below)

THE 2 PAGES:
PAGE 1
FILE: /home/user/SomeRepository/engine/runs/porog/build/b1/index.html
CONCEPT: Три проёма у входа: The central move is structural: the hero is a threshold that splits into three framed openings, «Слушаю», «Пишу музыку» and «Пишу о музыке». Each opening lists that visitor's four links and their own inbox, so the routing table above becomes the first screen. Below it come the newest release (ПОР-007, cover drawn in SVG, tracklist, ℗© line, "listen" and "buy" links out), the artists as frames with bio and booking address, news with dates, the demo rules, an EPK with bio, discography and embargo note, and a footer stating it is a concept site for a fictional label. The palette is wet-concrete grey with a signal-yellow tread stripe like a stair edge, which marks the active opening and the focus ring. Display type is Unbounded for headings only, body is Golos Text, and the only motion is a 120 ms frame inset on hover, disabled under reduced motion. The detail only this subject has: each opening is captioned with its real inbox, so the address is the label of the door.

PAGE 2
FILE: /home/user/SomeRepository/engine/runs/porog/build/b2/index.html
CONCEPT: Каталог ПОР как оглавление: The page is organised as the label's catalogue ledger, and the catalogue number is the navigation. Every release is ПОР-001, ПОР-002 and so on, the prefix being the first three letters of «Порог», with a format suffix (ПОР-007LP, ПОР-008MC), and a sticky index rail lists these numbers next to the sections Новое, Релизы, Артисты, Новости, Демо, Контакты. From top to bottom: - a two-line statement of the label; - the newest release, open in full, with an SVG cover built from nested rectangular frames, a tracklist with durations, the date, the format and run ("180 г, 300 экз., пронумерованы"), credits, the ℗© line, a placeholder player marked "образец", and plain links to listen or buy; - the older releases as collapsible ledger rows (`<details>`); - artist profiles cross-linked to their catalogue numbers; - dated news; - demo rules: the label accepts unsolicited demos, wants one to three tracks as a private link, and replies within two weeks; - separate inboxes for demos, press and booking, shown as selectable text. The palette is index-card stock grey-blue with ink-navy text and one rubber-stamp maroon used only on catalogue numbers. Unbounded is the display face, set only for numbers and headings, with Golos Text for body copy and JetBrains Mono for the ledger. The detail only this subject would have is the "ПОР-" numbering that encodes release order and format.

