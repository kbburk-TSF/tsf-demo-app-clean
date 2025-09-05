import React, { useState } from "react";
import { EventSourcePolyfill } from "event-source-polyfill";

function UploadForm() {
  const [dataset, setDataset] = useState("air_quality");
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);

  // Your backend Render URL
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

    // Connect to the streaming endpoint using EventSourcePolyfill
    const es = new EventSourcePolyfill(`${API_URL}/upload-csv-stream/`, {
      method: "POST",
      body: formData,
    });

    setMessages(["🚀 Upload started..."]);

    es.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
      if (event.data.includes("✅") || event.data.includes("❌")) {
        es.close();
      }
    };

    es.onerror = () => {
      setMessages((prev) => [...prev, "❌ Connection error"]);
      es.close();
    };
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
        <button type="submit">Upload with Realtime Updates</button>
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
