import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
  const [dataset, setDataset] = useState("air_quality");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  // Your backend Render URL
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
      setMessage("");
      setUploading(true);
      setProgress(0);

      const res = await axios.post(`${API_URL}/upload-csv/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percent = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgress(percent);
          }
        },
      });

      setMessage("✅ Upload successful: " + res.data.message);
    } catch (err) {
      console.error(err);
      setMessage(
        "❌ Upload failed: " + (err.response?.data?.detail || err.message)
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>Select Dataset:</label>
        <select value={dataset} onChange={(e) => setDataset(e.target.value)}>
          <option value="air_quality">Air Quality</option>
          <option value="finance">Finance</option>
          <option value="flight_performance">Flight Performance</option>
        </select>
        <br />
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          accept=".csv"
        />
        <br />
        <button type="submit" disabled={uploading}>
          {uploading ? "Uploading..." : "Upload CSV"}
        </button>
      </form>

      {uploading && (
        <div>
          <p>Uploading... {progress}%</p>
          <progress value={progress} max="100">
            {progress}%
          </progress>
        </div>
      )}

      {message && <p>{message}</p>}
    </div>
  );
}

export default UploadForm;
