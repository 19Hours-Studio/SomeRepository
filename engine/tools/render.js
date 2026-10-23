// Render a page the way the Artifact viewer wraps it (doctype, charset, viewport-fit=cover meta, small reset) at desktop
// and phone width in light and dark, save screenshots, and report what breaks: horizontal overflow and the elements that
// cause it, console and script errors, failed loads, the page title and whether body has its own background.
// Usage: node render.js <page.html> <outdir>. The sandbox cannot load web fonts or CDN scripts (network policy), so
// screenshots show fallback fonts; that is not a defect of the page.
const puppeteer = require("puppeteer-core");
const fs = require("fs");
const path = require("path");

const CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const SKELETON = (body) =>
  `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` +
  `<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}` +
  `body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>${body}</body></html>`;
const VIEWS = [[1280, 900, "desktop"], [390, 844, "phone"]];

(async () => {
  const [src, out] = process.argv.slice(2);
  if (!src || !out) { console.error("usage: node render.js <page.html> <outdir>"); process.exit(2); }
  fs.mkdirSync(out, { recursive: true });
  const raw = fs.readFileSync(src, "utf8");
  const tmp = path.resolve(out, "_wrapped.html");
  fs.writeFileSync(tmp, SKELETON(raw));
  const browser = await puppeteer.launch({ executablePath: CHROME, args: ["--no-sandbox"] });
  const report = { page: path.resolve(src), bytes: Buffer.byteLength(raw), has_own_doctype: /<!doctype|<html|<head|<body/i.test(raw.slice(0, 2000)),
                   note: "web fonts and CDN scripts cannot load in this sandbox; screenshots use fallback fonts", views: [] };
  for (const [w, h, name] of VIEWS) for (const scheme of ["light", "dark"]) {
    const page = await browser.newPage(); const errors = [], failed = [];
    page.on("console", (m) => { if (m.type() === "error") errors.push(m.text().slice(0, 200)); });
    page.on("pageerror", (e) => errors.push(String(e).slice(0, 200)));
    page.on("requestfailed", (r) => { const u = r.url(); if (!/fonts\.(googleapis|gstatic)\.com/.test(u)) failed.push(u.slice(0, 120)); });
    await page.setViewport({ width: w, height: h });
    await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: scheme }]);
    await page.goto("file://" + tmp, { waitUntil: "load", timeout: 30000 }).catch((e) => errors.push("load: " + e.message));
    await new Promise((r) => setTimeout(r, 600));
    const m = await page.evaluate(() => {
      const d = document.documentElement, cw = d.clientWidth;
      const wide = [...document.querySelectorAll("body *")].filter((e) => {
        const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
        return r.width > 0 && r.right > cw + 1 && cs.position !== "fixed" && !e.closest("[style*='overflow'], pre, table");
      }).slice(0, 6).map((e) => e.tagName.toLowerCase() + (typeof e.className === "string" && e.className ? "." + e.className.split(" ")[0] : ""));
      return { scrollW: d.scrollWidth, clientW: cw, height: d.scrollHeight, wide, title: document.title,
               body_bg: getComputedStyle(document.body).backgroundColor, text_color: getComputedStyle(document.body).color };
    });
    const shot = path.resolve(out, `${name}-${scheme}.png`);
    await page.screenshot({ path: shot });
    if (scheme === "light") await page.screenshot({ path: path.resolve(out, `${name}-light-full.png`), fullPage: true });
    report.views.push({ view: `${name}-${scheme}`, width: w, overflow_px: m.scrollW - m.clientW, wider_than_screen: m.wide, page_height: m.height,
                        title: m.title, body_bg: m.body_bg, text_color: m.text_color, console_errors: errors.slice(0, 6), failed_loads: failed.slice(0, 6),
                        screenshot: shot });
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(path.resolve(out, "report.json"), JSON.stringify(report, null, 1));
  console.log(JSON.stringify(report, null, 1));
})();
