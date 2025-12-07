import { useEffect, useState } from "react";

export default function PaperPage() {
  const [papers, setPapers] = useState([]);
  const [form, setForm] = useState({
    title: "",
    abstract: "",
    person_id: "",
    conference_id: "",
  });
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  // Fetch papers
  const fetchPapers = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:5001/api/papers");
      if (!res.ok) throw new Error("Failed to fetch papers");
      const data = await res.json();
      setPapers(data);
    } catch (err) {
      console.error(err);
      setError("Error loading papers");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchPapers();
  }, []);

  // Handle form input changes
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Submit new paper
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    // Basic validation
    if (!form.title || !form.abstract || !form.person_id || !form.conference_id) {
      setError("All fields are required");
      setSubmitting(false);
      return;
    }

    try {
      const res = await fetch("http://localhost:5001/api/papers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          person_id: Number(form.person_id),
          conference_id: Number(form.conference_id),
        }),
      });

      if (!res.ok) throw new Error("Failed to create paper");

      // Clear form and refresh papers list
      setForm({ title: "", abstract: "", person_id: "", conference_id: "" });
      await fetchPapers();
    } catch (err) {
      console.error(err);
      setError("Error creating paper");
    }
    setSubmitting(false);
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Paper Management</h1>

      {/* Form */}
      <div className="bg-white shadow-md rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Create Paper</h2>
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-2 rounded mb-4">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            name="title"
            placeholder="Title"
            value={form.title}
            onChange={handleChange}
            className="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="abstract"
            placeholder="Abstract"
            value={form.abstract}
            onChange={handleChange}
            className="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="person_id"
            placeholder="Person ID"
            type="number"
            value={form.person_id}
            onChange={handleChange}
            className="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <input
            name="conference_id"
            placeholder="Conference ID"
            type="number"
            value={form.conference_id}
            onChange={handleChange}
            className="border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
          <button
            type="submit"
            disabled={submitting}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
          >
            {submitting ? "Submitting..." : "Add Paper"}
          </button>
        </form>
      </div>

      {/* Existing Papers */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Existing Papers</h2>
        {loading ? (
          <p>Loading papers...</p>
        ) : papers.length === 0 ? (
          <p>No papers found</p>
        ) : (
          <ul className="space-y-3">
            {papers.map((p) => (
              <li
                key={p.paper_id}
                className="border border-gray-200 rounded p-3 bg-gray-50"
              >
                <strong className="block text-lg">{p.title}</strong>
                <p className="text-gray-700 mb-1">{p.abstract}</p>
                <span className="text-sm text-gray-500">
                  Person ID: {p.person_id}, Conference ID: {p.conference_id}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
