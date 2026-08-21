export const runtime = "nodejs";
export const dynamic = "force-dynamic";

/** Does a streamed response actually reach the client unbuffered?
 *
 *  The agent's whole fix rests on that. If the edge buffered the body, every byte would
 *  arrive at once at the end and the connection would sit idle exactly as before — the
 *  bug would look fixed locally and behave identically on a phone. This endpoint emits
 *  five lines 300ms apart so the answer is measurable from outside with curl, without a
 *  PIN and without spending a model call. It carries no data and reveals nothing. */
export async function GET() {
  const enc = new TextEncoder();
  const body = new ReadableStream<Uint8Array>({
    async start(c) {
      for (let i = 1; i <= 5; i++) {
        c.enqueue(enc.encode(JSON.stringify({ i, at: Date.now() }) + "\n"));
        if (i < 5) await new Promise((r) => setTimeout(r, 300));
      }
      c.close();
    },
  });
  return new Response(body, {
    headers: {
      "content-type": "application/x-ndjson; charset=utf-8",
      "cache-control": "no-store, no-transform",
      "x-accel-buffering": "no",
    },
  });
}
