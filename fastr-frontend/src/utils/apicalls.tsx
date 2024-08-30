const getPageContent = async (): Promise<string> => {
  try {
    const tabs = await chrome.tabs.query({active: true, currentWindow: true});
    if (!tabs[0]?.id) return '';

    return new Promise((resolve) => {
      chrome.tabs.sendMessage(
        tabs[0].id!,
        {action: "getPageContent"},
        (response) => {
          resolve(response?.content || '');
        }
      );
    });
  } catch (error) {
    console.error('Error getting page content:', error);
    return '';
  }
};


export const apiCall = async (inputText: string) => {
  
  try { 
    const context = await getPageContent();
    console.log('Context', context);
  
    const payload = {
      query_text: inputText,
      context: context,
    };
  
    const response = await fetch('http://localhost:8000/rag_call', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Data', data);
    return data.response;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
};

export const originalApiCall = async (inputText: string, url: string, api_key: string) => {
  const payload = {
    messages: [
      {
        role: "user",
        content: inputText + ' Keep under 300 characters!',
      },
    ],
    model: "llama3-8b-8192",
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${api_key}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    console.error(`Error: ${response.status}`);
    const errorData = await response.json();
    console.error(errorData);
    return undefined;
    
  } else {
    return response;
  }
};