const ALLOWED_HOSTS = ["mobile-api.hitv.ltd"];
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "*",
  "Access-Control-Max-Age": "86400"
};

export default {
  async fetch(request) {
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
    const url = new URL(request.url);

    if (url.pathname === "/" || url.pathname === "/health")
      return json({ status: "ok", service: "savita-proxy" });

    let target;
    if (url.pathname === "/proxy") target = url.searchParams.get("url");
    else if (request.method === "POST" && url.pathname === "/api/request") {
      try { target = (await request.json()).url; } catch { return json({ error: "bad json" }, 400); }
    }
    if (!target) return json({ error: "missing url" }, 400);

    let t;
    try { t = new URL(target); } catch { return json({ error: "bad url" }, 400); }
    if (!ALLOWED_HOSTS.includes(t.hostname)) return json({ error: "host blocked" }, 403);

    const fwd = new Headers();
    const skip = ["host", "origin", "referer"];
    for (const [k, v] of request.headers.entries())
      if (!skip.includes(k.toLowerCase())) fwd.set(k, v);

    try {
      const r = await fetch(t.toString(), { method: "GET", headers: fwd });
      const h = new Headers(r.headers);
      Object.entries(CORS).forEach(([k, v]) => h.set(k, v));
      return new Response(r.body, { status: r.status, headers: h });
    } catch (e) {
      return json({ error: "fetch failed", detail: e.message }, 502);
    }
  }
};

function json(o, s = 200) {
  return new Response(JSON.stringify(o), {
    status: s, headers: { "Content-Type": "application/json", ...CORS }
  });
}
