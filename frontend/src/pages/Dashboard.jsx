import { useEffect, useState } from "react";

const Dashboard = () => {
  const [conferences, setConferences] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Load conferences from Flask + MySQL API
  useEffect(() => {
    fetch("http://localhost:5000/conferences")
      .then((res) => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then((data) => {
        setConferences(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Unable to load conferences.");
        setLoading(false);
      });
  }, []);

  // Toggle starred conferences (client-side only)
  const toggleFavorite = (CID) => {
    if (favorites.includes(CID)) {
      setFavorites(favorites.filter((id) => id !== CID));
      setSuccess("Removed from starred conferences.");
    } else {
      setFavorites([...favorites, CID]);
      setSuccess("Conference starred!");
    }
    setTimeout(() => setSuccess(""), 2000);
  };

  // Search filter
  const filteredConferences = conferences.filter((conf) =>
    conf.Title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Starred conferences
  const starredConfs = conferences.filter((conf) =>
    favorites.includes(conf.CID)
  );

  // Upcoming conferences (future dates only)
  const upcomingConfs = [...conferences]
    .filter((conf) => new Date(conf.Start_Date) > new Date())
    .sort(
      (a, b) => new Date(a.Start_Date) - new Date(b.Start_Date)
    )
    .slice(0, 3);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          User Dashboard
        </h1>
        <p className="text-gray-600 mb-6">
          Track conferences, explore upcoming events, and manage your favorites.
        </p>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-sm text-gray-500">All Conferences</h3>
            <p className="text-2xl font-bold">{conferences.length}</p>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-sm text-gray-500">Starred Conferences</h3>
            <p className="text-2xl font-bold">{favorites.length}</p>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-sm text-gray-500">Upcoming Events</h3>
            <p className="text-2xl font-bold">{upcomingConfs.length}</p>
          </div>
        </div>

        {/* Messages */}
        {loading && <p className="text-gray-500 mb-4">Loading conferences...</p>}

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-100 text-green-700 rounded">
            {success}
          </div>
        )}

        {/* Search */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="Search conferences..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full p-3 rounded-md border border-gray-300 focus:ring-2 focus:ring-blue-500 outline-none"
          />
        </div>

        {/* Starred Conferences */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4">
            Your Starred Conferences
          </h2>

          {starredConfs.length === 0 ? (
            <p className="text-gray-500">
              You haven’t starred any conferences yet.
            </p>
          ) : (
            <div className="space-y-3">
              {starredConfs.map((conf) => (
                <div
                  key={conf.CID}
                  className="bg-white p-4 rounded shadow"
                >
                  <h3 className="font-semibold">{conf.Title}</h3>
                  <p className="text-sm text-gray-600">
                    Starts:{" "}
                    {new Date(conf.Start_Date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Upcoming Conferences */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4">
            Upcoming Conferences
          </h2>

          {upcomingConfs.length === 0 ? (
            <p className="text-gray-500">
              No upcoming conferences found.
            </p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {upcomingConfs.map((conf) => (
                <div
                  key={conf.CID}
                  className="bg-white p-4 rounded shadow"
                >
                  <h3 className="font-semibold">{conf.Title}</h3>
                  <p className="text-sm">
                    Starts:{" "}
                    {new Date(conf.Start_Date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* All Conferences */}
        <section>
          <h2 className="text-xl font-semibold mb-4">All Conferences</h2>

          <div className="space-y-4">
            {filteredConferences.map((conf) => (
              <div
                key={conf.CID}
                className="bg-white p-4 rounded shadow flex justify-between items-center"
              >
                <div>
                  <h3 className="font-semibold">{conf.Title}</h3>
                  <p className="text-sm text-gray-600">
                    Starts:{" "}
                    {new Date(conf.Start_Date).toLocaleDateString()}
                  </p>
                </div>

                <button
                  onClick={() => toggleFavorite(conf.CID)}
                  className={`px-4 py-2 rounded text-sm font-medium ${
                    favorites.includes(conf.CID)
                      ? "bg-yellow-400 text-black"
                      : "bg-blue-600 text-white hover:bg-blue-700"
                  }`}
                >
                  {favorites.includes(conf.CID)
                    ? "★ Starred"
                    : "Star"}
                </button>
              </div>
            ))}
          </div>
        </section>

      </div>
    </div>
  );
};

export default Dashboard;
