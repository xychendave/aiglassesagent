const API_URL = import.meta.env.VITE_API_URL;

export const api = {
  healthCheck: async () => {
    const response = await fetch(`${API_URL}/api/healthz`);
    return response.json();
  },
  
  translate: async (data) => {
    const response = await fetch(`${API_URL}/api/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  // ... 其他 API 方法
}; 