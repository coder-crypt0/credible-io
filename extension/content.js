(() => {
  // 1. Extract page text and send to background
  const pageText = document.body.innerText;

  chrome.runtime.sendMessage({
    type: "PAGE_TEXT",
    payload: {
      content: pageText,
      source_url: window.location.href
    }
  });

  // 2. Listen for repair result
  chrome.runtime.onMessage.addListener((message) => {
    if (message.type === "SHOW_REPAIR") {
      showRepairPanel(message.payload);
    }
  });

  // 3. Create overlay UI
  function showRepairPanel(data) {
    // Remove existing panel if present
    const existing = document.getElementById("credible-repair-panel");
    if (existing) existing.remove();

    const panel = document.createElement("div");
    panel.id = "credible-repair-panel";

    panel.innerHTML = `
      <h3>Credible.io – Live Misinformation Repair</h3>

      <strong>Original:</strong>
      <p>${truncate(data.original_text)}</p>

      <strong>Repaired:</strong>
      <p>${truncate(data.repaired_text)}</p>

      <strong>Why this was repaired:</strong>
      <p>${data.repair_explanation}</p>

      <button id="credible-close-btn">Close</button>
    `;

    // Styling (inline to avoid CSS injection issues)
    panel.style.position = "fixed";
    panel.style.top = "20px";
    panel.style.right = "20px";
    panel.style.width = "360px";
    panel.style.maxHeight = "80vh";
    panel.style.overflowY = "auto";
    panel.style.background = "#ffffff";
    panel.style.border = "2px solid #333";
    panel.style.padding = "12px";
    panel.style.zIndex = "999999";
    panel.style.fontSize = "14px";
    panel.style.boxShadow = "0 4px 12px rgba(0,0,0,0.3)";

    document.body.appendChild(panel);

    document.getElementById("credible-close-btn").onclick = () => {
      panel.remove();
    };
  }

  // 4. Helper to keep UI readable
  function truncate(text, limit = 400) {
    if (!text) return "";
    return text.length > limit
      ? text.slice(0, limit) + "..."
      : text;
  }
})();
