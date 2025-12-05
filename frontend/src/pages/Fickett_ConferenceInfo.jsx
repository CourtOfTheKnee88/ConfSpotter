import { useState, useEffect } from "react";

function ConferenceInfo() {
  const [apiBase] = useState("http://localhost:5001");
  const [query, setQuery] = useState("");
  const [conferences, setConferences] = useState([]);
  const [detail, setDetail] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    listAll();
  }, []);

  const fetchJson = async (path) => {
    const resp = await fetch(apiBase + path);
    if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`);
    return await resp.json();
  };

  const listAll = async () => {
    setMessage("Loading...");
    try {
      const data = await fetchJson("/conferences");
      setConferences(data);
      setMessage(`${data.length} total conferences`);
    } catch (e) {
      setMessage("Error fetching conferences");
    }
  };

  const searchConferences = async () => {
    setMessage("Searching...");
    try {
      const q = query.trim();
      const data = await fetchJson(
        "/conferences" + (q ? `?query=${encodeURIComponent(q)}` : "")
      );
      setConferences(data);
      setMessage(`${data.length} result(s)`);
    } catch (e) {
      setMessage("Error searching conferences");
    }
  };

  const loadDetail = async (id) => {
    setMessage("Loading details...");
    try {
      const data = await fetchJson(`/conferences/${id}`);
      setDetail(data);
      setMessage("");
    } catch (e) {
      setMessage("Error loading details");
    }
  };

  const hideDetail = () => setDetail(null);

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Conference Search</h1>
      <input
        style={{ padding: 8, marginRight: 8, width: "60%" }}
        placeholder="Search by name, acronym, or location"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") searchConferences();
        }}
      />
      <button onClick={searchConferences} style={{ marginRight: 4 }}>
        Search
      </button>
      <button onClick={listAll}>List All</button>
      <div style={{ marginTop: 12, color: "#555" }}>{message}</div>

      {conferences.length > 0 && (
        <table
          style={{ width: "100%", marginTop: 12, borderCollapse: "collapse" }}
        >
          <thead>
            <tr>
              <th>Conference</th>
              <th>Location</th>
              <th>Dates</th>
            </tr>
          </thead>
          <tbody>
            {conferences.map((c) => (
              <tr
                key={c.id}
                style={{ cursor: "pointer" }}
                onClick={() => loadDetail(c.id)}
              >
                <td>
                  {c.name}
                  <div style={{ fontSize: 12, color: "#888" }}>{c.acronym}</div>
                </td>
                <td style={{ fontSize: 12 }}>{c.location}</td>
                <td style={{ fontSize: 12 }}>
                  {c.start_date}
                  {c.end_date ? " - " + c.end_date : ""}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {detail && (
        <div
          style={{
            marginTop: 12,
            padding: 12,
            border: "1px solid #eee",
            borderRadius: 6,
            background: "#f8f8f8",
          }}
        >
          <h3>{detail.name}</h3>
          <div style={{ fontSize: 12, color: "#888" }}>{detail.acronym}</div>
          <p>
            <strong>Location:</strong> {detail.location}
          </p>
          <p>
            <strong>Dates:</strong> {detail.start_date}
            {detail.end_date ? " - " + detail.end_date : ""}
          </p>
          <p>
            <strong>URL:</strong>{" "}
            {detail.url ? (
              <a href={detail.url} target="_blank" rel="noopener noreferrer">
                {detail.url}
              </a>
            ) : (
              "N/A"
            )}
          </p>
          <p style={{ fontSize: 12, color: "#888" }}>
            Created: {detail.created_at}
          </p>
          <button onClick={hideDetail}>Close</button>
        </div>
      )}
    </div>
  );
}

export default ConferenceInfo;
