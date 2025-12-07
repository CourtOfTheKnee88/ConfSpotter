import { useState } from "react";

function ConferenceInfo() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [papers, setPapers] = useState([]);
  const [popupOpen, setPopupOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [paperLoading, setPaperLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch conferences
  const searchConferences = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/conferences?search=${encodeURIComponent(query)}`
      );
      if (!response.ok) throw new Error("Failed to fetch conferences");
      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  // Fetch papers for a specific conference
  const fetchPapers = async (conferenceId) => {
    setPaperLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/papers?conferenceId=${conferenceId}`
      );
      if (!response.ok) throw new Error("Failed to fetch papers");
      const data = await response.json();
      setPapers(data);
      setPopupOpen(true);
    } catch (err) {
      setError(err.message);
    }
    setPaperLoading(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Conference Search</h1>

      <input
        type="text"
        placeholder="Search conferences..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={searchConferences}>Search</button>

      {loading && <p>Loading conferences...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {results.map((conf) => (
          <li key={conf.id} style={{ marginTop: "10px" }}>
            <strong>{conf.name}</strong> — {conf.year}
            <button
              onClick={() => fetchPapers(conf.id)}
              style={{ marginLeft: "10px" }}
            >
              View Papers
            </button>
          </li>
        ))}
      </ul>

      {/* Popup */}
      {popupOpen && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            background: "rgba(0,0,0,0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            style={{
              background: "white",
              padding: "20px",
              borderRadius: "8px",
              width: "400px",
              maxHeight: "70%",
              overflowY: "auto",
            }}
          >
            <h2>Papers</h2>
            <button
              onClick={() => setPopupOpen(false)}
              style={{ float: "right", marginTop: "-40px" }}
            >
              ✖ Close
            </button>

            {paperLoading && <p>Loading papers...</p>}

            <ul>
              {papers.map((paper) => (
                <li key={paper.id} style={{ marginTop: "10px" }}>
                  <strong>{paper.title}</strong>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default ConferenceInfo;
