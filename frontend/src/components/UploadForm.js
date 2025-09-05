import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
  const [dataset, setDataset] = useState("air_quality");
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [polling, setPolling] = useState(false);

  const API_URL = "https://tsf-demo-backend.onrender.com";

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("dataset", dataset);
    formData.append("file", file);

    try {
      setMessages(["🚀 Upload started..."]);
      const res = await axios.post(`${API_URL}/upload-csv/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const taskId = res.data.task_id;
      setMessages((prev) => [...prev, "📡 Tracking progress..."]);
      setPolling(true);

      // Poll every 1s for progress updates
      const interval = setInterval(async () => {
        const progressRes = await axios.get(`${API_URL}/progress/${taskId}`);
        const status = progressRes.data.status;
        setMessages((prev) => [...prev, status]);

        if (status.includes("✅") || status.includes("❌")) {
          clearInterval(interval);
          setPolling(false);
        }
      }, 1000);
    } catch (err) {
      console.error(err);
      setMessages(["❌ Upload failed: " + (err.response?.data?.detail || err.message)]);
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
        <button type="submit" disabled={polling}>
          {polling ? "Processing..." : "Upload CSV"}
        </button>
      </form>

      <div>
        <h4>Status:</h4>
        <ul>
          {messages.map((msg, i) => (
            <li key={i}>{msg}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default UploadForm;
