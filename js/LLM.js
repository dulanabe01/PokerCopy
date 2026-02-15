export async function llmDecision(player, ctx, baseDecision = null) {
  // --- Unpack hole cards like bot.js does ---
  const holeCards = player?.cards
    ? [
        player.cards[0]?.dataset?.value || null,
        player.cards[1]?.dataset?.value || null,
      ]
    : [null, null];

  // --- Collect community cards from DOM (same approach as bot.js) ---
  const communityCards = Array.from(
    document.querySelectorAll("#community-cards .cardslot img")
  )
    .map((img) => {
      const m = img.src.match(/\/cards\/([2-9TJQKA][CDHS])\.svg$/);
      return m ? m[1] : null;
    })
    .filter(Boolean);

  const res = await fetch("http://127.0.0.1:5055/decide", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      player: {
        ...player,
        holeCards,
      },
      ctx: {
        ...ctx,
        communityCards,
      },
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