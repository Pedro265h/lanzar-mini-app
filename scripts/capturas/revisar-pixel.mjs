// Abre una URL en Chrome sin ventana y lista las llamadas al píxel de Meta y a /api/.
import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
const [url, esperaMs = "8000"] = process.argv.slice(2);
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", ["--headless=new", "--disable-gpu", "--remote-debugging-port=9334", `--user-data-dir=${mkdtempSync(join(tmpdir(), "cdp-"))}`, "about:blank"], { stdio: "ignore" });
const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
let ws;
for (let i = 0; i < 40 && !ws; i++) { try { const l = await (await fetch("http://127.0.0.1:9334/json")).json(); const p = l.find((x) => x.type === "page"); if (p) ws = new WebSocket(p.webSocketDebuggerUrl); } catch { await dormir(250); } }
await new Promise((ok) => ws.addEventListener("open", ok));
let n = 0; const pend = new Map();
const cdp = (method, params = {}) => new Promise((ok) => { const id = ++n; pend.set(id, ok); ws.send(JSON.stringify({ id, method, params })); });
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pend.has(m.id)) { pend.get(m.id)(m.result); pend.delete(m.id); }
  if (m.method === "Network.requestWillBeSent") {
    const u = m.params.request.url;
    if (/facebook/.test(u)) {
      const q = new URL(u).searchParams;
      console.log("META", m.params.type, u.includes("/tr") ? `${u.split("?")[0]} id=${q.get("id")} ev=${q.get("ev")}` : u.split("?")[0].slice(0,90));
    }
    if (u.includes("/api/")) console.log("API ", m.params.request.method, new URL(u).pathname);
  }
});
await cdp("Network.enable"); await cdp("Page.enable");
await cdp("Emulation.setUserAgentOverride", { userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1" });
await cdp("Page.navigate", { url });
await dormir(Number(esperaMs));
const r = await cdp("Runtime.evaluate", { expression: "JSON.stringify({webdriver: navigator.webdriver, fbq: typeof fbq, version: window.fbq && fbq.version, pixeles: window.fbq && fbq.instance ? Object.keys(fbq.instance.pixelsByID || {}) : null, cola: window.fbq && fbq.queue ? fbq.queue.length : null})", returnByValue: true });
console.log("ESTADO", r?.result?.value);
ws.close(); chrome.kill();
