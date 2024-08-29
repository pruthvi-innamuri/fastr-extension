// Background script for the extension

console.log('Background script loaded and extension_open set to false');
// The extension is initially closed
chrome.storage.local.set({extension_open: false}, () => {
  console.log('extension_open set to false');
});

// Function to open the popup
const openPopup = () => {
  console.log('Checking if popup is open');
  chrome.storage.local.get(['extension_open'], (result) => {
    const popupIsOpen = result.extension_open;
    if (!popupIsOpen) {
      console.log('Opening popup');
      chrome.action.openPopup();
    } else {
      console.log('Popup is already open');
      chrome.runtime.sendMessage({ action: 'NewTextSelected' });
    }
  });
}


// Event listeners
chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
  console.log('request', request);
  if (request.action === 'SearchSelect') {
    openPopup();
    sendResponse({ success: true });
  }
});

chrome.runtime.onConnect.addListener((port) => {
  if (port.name === 'popup') {
    console.log('Popup opened');
    chrome.storage.local.set({ extension_open: true }, () => {
      console.log('extension_open set to true');
    });

    port.onDisconnect.addListener(() => {
      console.log('Popup closed');
      chrome.storage.local.set({ extension_open: false }, () => {
        console.log('extension_open set to false');
      });
    });
  }
});