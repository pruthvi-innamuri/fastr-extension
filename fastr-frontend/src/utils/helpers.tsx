
// Helper functions

const updateInputText = (setInputText: (text: string) => void) => {
    chrome.storage.local.get(['current_selection'], (result) => {
      if (result.current_selection && result.current_selection.length > 0) {
        const currentSelection = result.current_selection;
        console.log('Current Selection', currentSelection);
        setInputText(currentSelection); 
      } else {
        console.log('Nothing in current_selection');
      }
    });
  };

  export { updateInputText };