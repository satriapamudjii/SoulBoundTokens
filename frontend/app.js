import React, { useEffect, useState } from 'react';

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL;

const App = () => {
  const [tokenDetails, setTokenDetails] = useState(null);

  const handleIssueToken = async () => {
    try {
      const response = await fetch(`${BASE_API_URL}/issue-token`, { method: 'POST' });
      const data = await response.json();
      if (data.token) {
        console.log('Token issued', data.token);
      }
    } catch (error) {
      console.error('Error issuing token:', error);
    }
  };

  const handleVerifyToken = async (token) => {
    try {
      const response = await fetch(`${BASE_API_URL}/verify-token?token=${token}`);
      const data = await response.json();
      if (data.valid) {
        console.log('Token is valid');
      } else {
        console.log('Token is not valid');
      }
    } catch (error) {
      console.error('Error verifying token:', error);
    }
  };

  const fetchTokenDetails = async () => {
    try {
      const response = await fetch(`${BASE_API_URL}/token-details`);
      const data = await response.json();
      setTokenDetails(data);
    } catch (error) {
      console.error('Error fetching token details:', error);
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
        {tokenDetails ? (
          <pre>{JSON.stringify(tokenDetails, null, 2)}</pre>
        ) : (
          <p>Loading token details...</p>
        )}
      </div>
    </div>
  );
};

export default App;