import React from "react";
import UploadForm from "./components/UploadForm";

function App() {
  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", textAlign: "center" }}>
      <h1>TSF Demo App</h1>
      <p>Upload CSV files to populate demo datasets</p>
      <UploadForm />
    </div>
  );
}

export default App;
