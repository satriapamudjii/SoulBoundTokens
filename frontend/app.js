import React, { useEffect, useState } from 'react';

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL;

// Utility for simple data caching with expiry
const cache = {
  data: null,
  lastFetch: 0,
  // Time in milliseconds, adjust based on acceptable staleness of your data
  cacheDuration: 1000 * 60 * 5, // 5 minutes cache duration
  isStale() {
    return Date.now() - this.lastFetch > this.cacheDuration;
  },
  update(data) {
    this.data = data;
    this.lastFetch = Date.now();
  },
  get() {
    return this.data;
  },
};

const App = () => {
  const [tokenDetails, setTokenDetails] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(true);
  const [error, setError] = useState(null);

  const fetchApi = async (url, options = {}, bypassCache = false) => {
    try {
      // Utilize cached data for token-details if available and not stale
      if (url.includes('/token-details') && cache.data && !cache.isStale() && !bypassCache) {
        console.log('Returning cached token details');
        return { data: cache.get(), error: null };
      }

      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      // Update cache if fetching token-details
      if (url.includes('/token-details')) {
        cache.update(data);
      }

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
      // Invalidate cache as the token state might change and fetch new details
      fetchTokenDetails(true);
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
      // Invalidate cache as a verification might impact token state/details
      fetchTokenDetails(true);
    }
  };

  const fetchTokenDetails = async (bypassCache = false) => {
    setLoadingDetails(true);
    const { data, error } = await fetchApi(`${BASE_API_URL}/token-details`, {}, bypassCache);
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