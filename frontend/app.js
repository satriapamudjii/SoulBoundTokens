import React, { useEffect, useState } from 'react';

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL;

const App = () => {
  const [tokenDetails, setTokenDetails] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(true);

  const fetchApi = async (url, options = {}) => {
    try {
      const response = await fetch(url, options);
      const data = await response.json();
      return { data, error: null };
    } catch (error) {
      console.error('API error:', error);
      return { data: null, error };
    }
  };

  const handleIssueToken = async () => {
    const { data, error } = await fetchApi(`${BASE_API_URL}/issue-token`, { method: 'POST' });
    if (!error && data.token) {
      console.log('Token issued', data.token);
    }
  };

  const handleVerifyToken = async (token) => {
    const { data, error } = await fetchApi(`${BASE_API_URL}/verify-token?token=${token}`);
    if (!error) {
      const message = data.valid ? 'Token is valid' : 'Token is not valid';
      console.log(message);
    }
  };

  const fetchTokenDetails = async () => {
    const { data, error } = await fetchApi(`${BASE_API_URL}/token-details`);
    if (!error) {
      setTokenDetails(data);
      setLoadingDetails(false);
    }
  };

  useEffect(() => {
    fetchTokenDetails();
  }, []);

  return (
    <div>
      <h1>Token Management</h1>
      <button onClick={handleIssueToken}>Issue Token</button>
      <button onClick={() => handleVerifyToken('your_token_here')}>Verify Token</button>
      <div>
        <h2>Token Details</h2>
        {loadingDetails ? (
          <p>Loading token details...</p>
        ) : (
          <pre>{JSON.stringify(tokenDetails, null, 2)}</pre>
        )}
      </div>
    </div>
  );
};

export default App;