// app/api/pipeline/route.ts  (Server route — runs in the Node container)

const PROXY_TIMEOUT_MS = 65_000;

export async function POST(req: Request) {
  const body = await req.json();
  const backendUrl = process.env.BACKEND_URL ?? "http://backend:8000";

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), PROXY_TIMEOUT_MS);

  let res: Response;
  try {
    res = await fetch(`${backendUrl}/pipeline`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
  } catch (err) {
    clearTimeout(timeout);
    if (err instanceof Error && err.name === "AbortError") {
      return new Response(
        JSON.stringify({ error: "proxy_timeout", message: "Backend request timed out" }),
        { status: 504, headers: { "Content-Type": "application/json" } }
      );
    }
    return new Response(
      JSON.stringify({ error: "proxy_error", message: err instanceof Error ? err.message : "Proxy error" }),
      { status: 502, headers: { "Content-Type": "application/json" } }
    );
  }
  clearTimeout(timeout);

  // pass through status + body verbatim
  return new Response(await res.text(), {
    status: res.status,
    headers: { "Content-Type": "application/json" },
  });
}
