// Minimal background script for nav_nav
chrome.runtime.onInstalled.addListener(() => {
  console.log("nav_nav extension installed.");

  // Initialize default settings if not present
  chrome.storage.local.get(["position", "urls"], (result) => {
    if (!result.position) {
      chrome.storage.local.set({ position: "bottom-left" });
    }
    if (!result.urls) {
      chrome.storage.local.set({ urls: [] });
    }
  });
});
