import { useEffect, useState } from "react";

export default function PaperPage() {
  const [papers, setPapers] = useState([]);
  const [form, setForm] = useState({
    title: "",
    abstract: "",
    person_id: "",
    conference_id: ""
  });

  // Load papers
  useEffect(() => {
    fetch("http://localhost:5001/papers")
      .then((res) => res.json())
      .then((data) => setPapers(data))
      .catch((err) => console.error("Error fetching papers:", err));
  }, []);

  // Form values
  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  // Submit new paper
  function handleSubmit(e) {
    e.preventDefault();

    fetch("http://localhost:5001/papers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    })
      .then(() => window.location.reload())
      .catch((err) => console.error("Error creating paper:", err));
  }

  return (
    <div style={{ padding: "20px" }}>
      <h1>Paper Entity</h1>

      <h2>Create Paper</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input name="title" placeholder="Title" onChange={handleChange} />
        <input name="abstract" placeholder="Abstract" onChange={handleChange} />
        <input name="person_id" placeholder="Person ID" onChange={handleChange} />
        <input
          name="conference_id"
          placeholder="Conference ID"
          onChange={handleChange}
        />
        <button type="submit">Add Paper</button>
      </form>

      <h2>Existing Papers</h2>
      <ul>
        {papers.map((p) => (
          <li key={p.paper_id}>
            <strong>{p.title}</strong> — {p.abstract}<br />
            Person: {p.person_id}, Conference: {p.conference_id}
          </li>
        ))}
      </ul>
    </div>
  );
}
