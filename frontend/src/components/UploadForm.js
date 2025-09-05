import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
  const [dataset, setDataset] = useState("air_quality");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

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
      const res = await axios.post(
        "https://<YOUR-BACKEND-URL>.onrender.com/upload-csv/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setMessage(res.data.message);
    } catch (err) {
      setMessage("Upload failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Select Dataset:
        <select value={dataset} onChange={(e) => setDataset(e.target.value)}>
          <option value="air_quality">Air Quality</option>
          <option value="finance">Finance</option>
          <option value="flight_performance">Flight Performance</option>
        </select>
      </label>
      <br /><br />

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br /><br />

      <button type="submit">Upload CSV</button>

      {message && <p>{message}</p>}
    </form>
  );
}

export default UploadForm;
