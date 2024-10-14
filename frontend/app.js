import React, { useEffect, useState } from 'react';

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL;

const App = () => {
  const [tokenDetails, setTokenDetails] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(true);
  const [error, setError] = useState(null);

  const fetchApi = async (url, options = {}) => {
    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return { data, error: null };
    } catch (error) {
      console.error('API error:', error);
      return { data: null, error };
    }
  };

  const handleIssueToken = async () => {
    const { data, error } = await fetchApi(`${BASE_API_URL}/issue-token`, { method: 'POST' });
    if (error) {
      setError("Failed to issue token");
      return;
    }
    if (!error && data.token) {
      console.log('Token issued', data.token);
      setError(null); // Reset error state if operation was successful
    }
  };

  const handleVerifyToken = async (token) => {
    const { data, error } = await fetchApi(`${BASE_API_URL}/verify-token?token=${token}`);
    if (error) {
      setError("Failed to verify token");
      return;
    }
    if (!error) {
      const message = data.valid ? 'Token is valid' : 'Token is not valid';
      console.log(message);
      setError(null); // Reset error state if operation was successful
    }
  };

  const fetchTokenDetails = async () => {
    const { data, error } = await fetchApi(`${BASE_API_URL}/token-details`);
    if (error) {
      setError("Failed to fetch token details");
      setLoadingDetails(false);
      return;
    }
    if (!error) {
      setTokenDetails(data);
      setLoadingDetails(false);
      setError(null); // Reset error state if operation was successful
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
      {error && <p style={{color: 'red'}}>Error: {error}</p>}
      <div>
        <h2>Token Details</h2>
        {loadingDetails ? (
          <p>Loading token details...</p>
        ) : tokenDetails ? (
          <pre>{JSON.stringify(tokenDetails, null, 2)}</pre>
        ) : (
          <p>No token details available.</p>
        )}
      </div>
    </div>
  );
};

export default App;