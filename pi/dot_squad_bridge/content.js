const TRUSTED_ORIGINS = [
  "http://localhost",
  "http://127.0.0.1",
  "http://10.0.0.158",
  "http://localhost:5173",
  "null", // For local file:// testing
];

window.addEventListener("message", (event) => {
  console.log("Dot Squad Agent: Received message from origin:", event.origin, event.data);
  if (!TRUSTED_ORIGINS.includes(event.origin)) {
    console.warn("Dot Squad Agent: Origin not trusted", event.origin);
    return;
  }


  if (event.data?.type === "LED_TRIGGER") {
    chrome.runtime.sendMessage(event.data);
    console.log("Dot Squad Agent: Forwarded to runtime", event.data.pattern, event.origin);
  }
});


