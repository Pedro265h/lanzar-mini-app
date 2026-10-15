// Capturas con Chrome sin ventana por el protocolo de DevTools: viewport de celular (o ANCHO/ALTO) y pasos.
// Uso: node cdp2.mjs pasos.json carpeta-salida
import { spawn } from "node:child_process";
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [pasosArchivo, salida] = process.argv.slice(2);
const pasos = JSON.parse(readFileSync(pasosArchivo, "utf8"));
mkdirSync(salida, { recursive: true });
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const perfil = mkdtempSync(join(tmpdir(), "cdp-"));
const chrome = spawn(CHROME, ["--headless=new", "--disable-gpu", "--hide-scrollbars", "--remote-debugging-port=9333", `--user-data-dir=${perfil}`, "about:blank"], { stdio: "ignore" });
const dormir = (ms) => new Promise((r) => setTimeout(r, ms));

let ws;
for (let i = 0; i < 40 && !ws; i++) {
  try {
    const lista = await (await fetch("http://127.0.0.1:9333/json")).json();
    const pagina = lista.find((x) => x.type === "page");
    if (pagina) ws = new WebSocket(pagina.webSocketDebuggerUrl);
  } catch {
    await dormir(250);
  }
}
await new Promise((ok) => ws.addEventListener("open", ok));
let n = 0;
const pendientes = new Map();
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pendientes.has(m.id)) {
    pendientes.get(m.id)(m);
    pendientes.delete(m.id);
  }
});
const cdp = (method, params = {}) =>
  new Promise((ok, mal) => {
    const id = ++n;
    pendientes.set(id, (m) => (m.error ? mal(new Error(`${method}: ${m.error.message}`)) : ok(m.result)));
    ws.send(JSON.stringify({ id, method, params }));
  });

try {
  await cdp("Page.enable");
  await cdp("Runtime.enable");
  if (process.env.UA) await cdp("Network.setUserAgentOverride", { userAgent: process.env.UA });
  await cdp("Emulation.setDeviceMetricsOverride", { width: Number(process.env.ANCHO || 390), height: Number(process.env.ALTO || 844), deviceScaleFactor: process.env.ANCHO ? 1 : 2, mobile: !process.env.ANCHO });
  for (const p of pasos) {
    if (p.ir) {
      await cdp("Page.navigate", { url: p.ir });
      await dormir(p.esperar ?? 1500);
    } else if (p.js) {
      const r = await cdp("Runtime.evaluate", { expression: p.js, awaitPromise: true, returnByValue: true });
      if (r.exceptionDetails) console.log("error js:", p.js.slice(0, 60), r.exceptionDetails.exception?.description?.slice(0, 200));
      else if (r.result?.value !== undefined) console.log("js →", JSON.stringify(r.result.value).slice(0, 400));
      await dormir(p.esperar ?? 700);
    } else if (p.foto) {
      const r = await cdp("Page.captureScreenshot", { format: "png", captureBeyondViewport: !!p.completa });
      writeFileSync(join(salida, `${p.foto}.png`), Buffer.from(r.data, "base64"));
      console.log("foto", p.foto);
    }
  }
} catch (err) {
  console.log("se detuvo:", err.message);
} finally {
  ws.close();
  chrome.kill();
}
