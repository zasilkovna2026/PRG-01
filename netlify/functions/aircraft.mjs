export default async (req, context) => {
  const url = "https://api.adsb.lol/v2/point/50.0755/14.4378/100";
  try {
    const r = await fetch(url, { headers: { "User-Agent": "PRG-01/1.0" } });
    const body = await r.text();
    return new Response(body, {
      status: r.status,
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "public, max-age=5"
      }
    });
  } catch (e) {
    return Response.json({ error: String(e) }, { status: 502 });
  }
};