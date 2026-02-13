export async function llmDecision(player, ctx, baseDecision = null) {
  const res = await fetch("http://127.0.0.1:5055/decide", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      player,
      ctx,
      baseDecision,
    }),
  });

  // If the server errors, fall back to the baseline decision if we have one.
  if (!res.ok) {
    return baseDecision ?? { action: "fold" };
  }

  const decision = await res.json();

  // Minimal validation / fallback
  if (!decision || typeof decision.action !== "string") {
    return baseDecision ?? { action: "fold" };
  }

  return decision;
}