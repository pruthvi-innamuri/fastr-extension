// Content script for the extension (manages the user's browser content)

const detectUserSearch = (event: KeyboardEvent): string | undefined => {
  if (event.key === 'Tab') {
    const selectedText = window.getSelection()?.toString();
    if (selectedText && selectedText.trim() !== '') {
      event.preventDefault(); // Prevent the default tab behavior
      return selectedText;
    }
  }
  return undefined;
}

const handleUserSearch = (event: KeyboardEvent): undefined => {
  const selectedText = detectUserSearch(event);
  if (selectedText) {
    try {
      chrome.storage.local.set({ current_selection: selectedText }, () => {
        console.log('Stored the following selected text: ' + selectedText);
      });

      chrome.runtime.sendMessage({ action: 'SearchSelect'}, (response) => {
        console.log('response', response);
      });

    } catch (error) {
      console.error('Extension context invalidated:', error);
      document.removeEventListener('keydown', handleUserSearch);
      setTimeout(initializeContentScript, 1000);
    }
  }
  return undefined;
}

const initializeContentScript = () => {
  console.log('Content script loaded');
  document.addEventListener('keydown', handleUserSearch);
}

initializeContentScript();