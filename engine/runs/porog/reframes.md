**ASSUMPTIONS:**
- "Ordinary site" means static multi-page HTML/CSS that opens from the file system with no build step.
- One generic contact email serves everyone (contradicted: FACT 6 and ATTEMPT 8 say to split demo, press and booking inboxes).
- A demo section can be just an address (contradicted: FACT 7, FACT 8 and ATTEMPT 7 say it needs rules, format, track count, reply time and an accept/decline policy).
- A release block is complete with cover, tracklist, date and links (contradicted: FACT 10, FACT 15 and ATTEMPT 10 add catalogue number, format, run size, credits and the ℗© line).
- Visitors can "listen" on the site (contradicted: no licensed audio exists, so any player must be a marked placeholder; ATTEMPT 5).
- Listen/buy links can point to familiar Western platforms or majors (contradicted for a Russian-language label: FACT 16 points to VK Музыка, Яндекс Музыка and МТС Музыка via distributors, and says not to name majors).
- The name's identity comes from door imagery (contradicted: ATTEMPT 9 and the LESSONS call that literal and clichéd).
- Web fonts and images can be pulled in freely (contradicted by the licensing constraint; only system fonts, OFL fonts or CSS/SVG-drawn covers are allowed).
- A hidden hamburger menu is fine on phones (partly contradicted: ATTEMPT 3 says hidden navigation hurts findability).
- "Plausible" and "clearly placeholder" do not conflict (untested; marking must not break realism or the reverse).
- Responsiveness and accessibility will be "checked" by eye (unstated; the criteria need measurable checks).

**REFRAME 1:** Which visitor tasks and inboxes must the site serve (listener, artist, press), and what is the shortest path from Home to each one, including split contacts and an explicit demo policy? | CHANGES: the unit moves from "pages to build" to "tasks to complete", with the page list derived from them | IMPORTANCE: high | POSSIBILITY: high | WHY: the 3-click criteria and FACTS 3, 5–9 define the tasks directly, so success becomes checkable.

**REFRAME 2:** What single content model (release: ПОР-### number, format, run, credits, ℗©, platform links; artist; news post; each with a placeholder flag) should every page be rendered from, so that detail stays consistent and placeholder marking cannot be forgotten? | CHANGES: the unit moves from page copy to a data schema | IMPORTANCE: high | POSSIBILITY: high | WHY: FACTS 10–17 give concrete fields, which separate the site from a template (ATTEMPTS 1, 10) while keeping the invented content uniform.

**REFRAME 3:** How can "threshold" shape structure and typography (stepped section edges, framed openings, a catalogue-number system, generated covers) using only system or OFL fonts and CSS/SVG, without a literal door? | CHANGES: the means move from imagery to layout and type | IMPORTANCE: medium | POSSIBILITY: high | WHY: it meets both the identity and the licensing criteria, and avoids ATTEMPTS 2 and 9.

**REFRAME 4:** What measurable checks prove the criteria are met: a click-depth map from Home, `scrollWidth ≤ viewport` at 360, 768 and 1280 px in a headless browser, computed contrast ratios, keyboard tab order, and title, meta and favicon on every page? | CHANGES: the target moves from "build it" to "verify it" | IMPORTANCE: high | POSSIBILITY: medium | WHY: it turns soft claims into computed numbers, but depends on a browser being available in the environment.

**REFRAME 5:** How can the site meet "hear music fast" (FACT 3) without any audio, for example with a clearly labelled demo player state plus dummy links to Russian platforms? | CHANGES: the sub-question is isolated | IMPORTANCE: medium | POSSIBILITY: medium | WHY: it settles the one requirement the material shows cannot be met literally.

**KEEP:** 1, 2
