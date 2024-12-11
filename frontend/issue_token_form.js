import React, { useState } from 'react';

const IssueTokenForm = () => {
  const initialFormData = {
    tokenName: '',
    metadata: '',
    ownerAddress: '',
  };

  const [formData, setFormData] = useState(initialFormData);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const validateFormData = ({ tokenName, metadata, ownerAddress }) => {
    const errors = {};
    if (!tokenName.trim()) {
      errors.tokenName = "Token name is required.";
    }
    if (!metadata.trim()) {
      errors.metadata = "Metadata is required.";
    }
    if (!ownerAddress.trim()) {
      errors.ownerAddress = "Owner address is required.";
    }
    const isValidEthereumAddress = /^0x[a-fA-F0-9]{40}$/.test(ownerAddress);
    if (!isValidEthereumAddress) {
      errors.ownerAddress = "Invalid Ethereum address.";
    }
    return errors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errors = validateFormData(formData);
    if (Object.keys(errors).length === 0) {
      console.log("Form Data:", formData);
      setFormData(initialFormData);
    } else {
      console.error("Validation Errors:", errors);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="tokenName">Token Name:</label>
        <input
          id="tokenName"
          name="tokenName"
          type="text"
          value={formData.tokenName}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="metadata">Metadata:</label>
        <input
          id="metadata"
          name="metadata"
          type="text"
          value={formData.metadata}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="ownerAddress">Owner Address:</label>
        <input
          id="ownerAddress"
          name="ownerAddress"
          type="text"
          value={formData.ownerAddress}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Issue Token</button>
    </form>
  );
};

export default IssueTokenForm;