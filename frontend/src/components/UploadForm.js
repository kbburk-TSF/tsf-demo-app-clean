import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
  const [dataset, setDataset] = useState("air_quality");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  // Fixed: use your actual backend Render URL
  const API_URL = "https://tsf-demo-backend.onrender.com";

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("dataset", dataset);
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_URL}/datasets/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("Upload successful: " + res.data.message);
    } catch (err) {
      console.error(err);
      setMessage(
        "Upload failed: " + (err.response?.data?.error || err.message)
      );
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>Select Dataset:</label>
        <select value={dataset} onChange={(e) => setDataset(e.target.value)}>
          <option value="air_quality">Air Quality</option>
          <option value="sales">Sales</option>
          <option value="weather">Weather</option>
        </select>
        <br />
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          accept=".csv"
        />
        <br />
        <button type="submit">Upload CSV</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default UploadForm;
