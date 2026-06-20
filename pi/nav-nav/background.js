
// Minimal background script for Nav-Nav
chrome.runtime.onInstalled.addListener(() => {
  console.log('Nav-Nav extension installed.');
  
  // Initialize default settings if not present
  chrome.storage.local.get(['position', 'urls'], (result) => {
    if (!result.position) {
      chrome.storage.local.set({ position: 'bottom-left' });
    }
    if (!result.urls) {
      chrome.storage.local.set({ urls: [] });
    }
  });
});
