chrome.action.onClicked.addListener((tab) => {
  console.log("Credible.io extension clicked!");

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content.js"]
  });
});

chrome.runtime.onMessage.addListener((message, sender) => {
  if (message.type === "PAGE_TEXT") {
    console.log("Sending text to /repair endpoint...");

    fetch("http://127.0.0.1:8000/repair", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(message.payload)
    })
      .then(res => res.json())
      .then(data => {
        console.log("Repair response:", data);

        chrome.tabs.sendMessage(sender.tab.id, {
          type: "SHOW_REPAIR",
          payload: data
        });
      })
      .catch(err => {
        console.error("Repair request failed:", err);
      });
  }
});