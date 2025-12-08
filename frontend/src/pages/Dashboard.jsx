import { useEffect, useState } from "react";
import ConferenceInfo from "./Fickett_ConferenceInfo";
import Banner from "../components/Banner";

const Dashboard = () => {
  const [conferences, setConferences] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedConference, setSelectedConference] = useState(null);
  const [recommendedConferences, setRecommendedConferences] = useState([]);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Get user ID from localStorage
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const userId = user.ID;

  // Load conferences from Flask + MySQL API
  useEffect(() => {
    fetch("http://localhost:5001/api/conferences")
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

  // Load user's favorites
  useEffect(() => {
    if (userId) {
      fetch(`http://localhost:5001/api/users/${userId}/favorites`)
        .then((res) => {
          if (!res.ok) throw new Error();
          return res.json();
        })
        .then((data) => {
          setFavorites(data.favorites || []);
        })
        .catch(() => {
          console.error("Unable to load favorites.");
        });
    }
  }, [userId]);

  // Load personalized recommendations
  useEffect(() => {
    if (userId) {
      fetch(`http://localhost:5001/api/users/${userId}/recommendations`)
        .then((res) => {
          if (!res.ok) throw new Error();
          return res.json();
        })
        .then((data) => {
          setRecommendedConferences(data.recommendations || []);
        })
        .catch(() => {
          console.error("Unable to load recommendations.");
        });
    }
  }, [userId]);

  // Load conference details
  const loadConferenceDetails = async (id) => {
    try {
      const res = await fetch(`http://localhost:5001/api/conferences/${id}`);
      if (!res.ok) throw new Error();
      const data = await res.json();
      setSelectedConference(data);
    } catch {
      setError("Unable to load conference details.");
    }
  };

  // Close detail modal
  const closeDetails = () => {
    setSelectedConference(null);
  };

  // Toggle starred conferences (save to backend)
  const toggleFavorite = async (CID) => {
    if (!userId) {
      setError("Please log in to star conferences.");
      return;
    }

    try {
      if (favorites.includes(CID)) {
        // Remove from favorites
        const res = await fetch(
          `http://localhost:5001/api/users/${userId}/favorites/${CID}`,
          { method: "DELETE" }
        );
        if (!res.ok) throw new Error();

        setFavorites(favorites.filter((id) => id !== CID));
        setSuccess("Removed from starred conferences.");
      } else {
        // Add to favorites
        const res = await fetch(
          `http://localhost:5001/api/users/${userId}/favorites/${CID}`,
          { method: "POST" }
        );
        if (!res.ok) throw new Error();

        setFavorites([...favorites, CID]);
        setSuccess("Conference starred!");
      }
      setTimeout(() => setSuccess(""), 2000);
    } catch {
      setError("Unable to update favorites. Please try again.");
      setTimeout(() => setError(""), 2000);
    }
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
    .sort((a, b) => new Date(a.Start_Date) - new Date(b.Start_Date))
    .slice(0, 3);

  return (
    <div className="min-h-screen bg-blue-200">
      <Banner />
      <div className="max-w-6xl mx-auto p-6">
        {/* Header */}
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          User Dashboard
        </h1>
        <p className="text-gray-600 mb-6">
          Track conferences, explore upcoming events, and manage your favorites.
        </p>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white p-4 rounded-md shadow-md hover:shadow-lg hover:scale-105 transition">
            <h3 className="text-sm text-gray-500">All Conferences</h3>
            <p className="text-2xl font-bold">{conferences.length}</p>
          </div>

          <div className="bg-white p-4 rounded-md shadow-md hover:shadow-lg hover:scale-105 transition">
            <h3 className="text-sm text-gray-500">Starred Conferences</h3>
            <p className="text-2xl font-bold">{favorites.length}</p>
          </div>

          <div className="bg-white p-4 rounded-md shadow-md hover:shadow-lg hover:scale-105 transition">
            <h3 className="text-sm text-gray-500">Upcoming Events</h3>
            <p className="text-2xl font-bold">{upcomingConfs.length}</p>
          </div>
        </div>

        {/* Messages */}
        {loading && (
          <p className="text-gray-500 mb-4">Loading conferences...</p>
        )}

        {error && (
          <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-md">
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
                  className="bg-white p-4 rounded-md shadow-md cursor-pointer hover:bg-gray-50 transition hover:shadow-lg hover:scale-105"
                  onClick={() => loadConferenceDetails(conf.CID)}
                >
                  <h3 className="font-semibold">{conf.Title}</h3>
                  <p className="text-sm text-gray-600">
                    Starts: {new Date(conf.Start_Date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Upcoming Conferences */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4">Upcoming Conferences</h2>

          {upcomingConfs.length === 0 ? (
            <p className="text-gray-500">No upcoming conferences found.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {upcomingConfs.map((conf) => (
                <div
                  key={conf.CID}
                  className="bg-white p-4 rounded-md shadow-md cursor-pointer hover:bg-gray-50 transition hover:shadow-lg hover:scale-105"
                  onClick={() => loadConferenceDetails(conf.CID)}
                >
                  <h3 className="font-semibold">{conf.Title}</h3>
                  <p className="text-sm">
                    Starts: {new Date(conf.Start_Date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Recommended Conferences */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4">
            Recommended Conferences
          </h2>

          {recommendedConferences.length === 0 ? (
            <p className="text-gray-500">No recommended conferences found.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {recommendedConferences.map((conf) => (
                <div
                  key={conf.CID}
                  className="bg-white p-4 rounded-md shadow-md cursor-pointer hover:bg-gray-50 transition hover:shadow-lg hover:scale-105"
                  onClick={() => loadConferenceDetails(conf.CID)}
                >
                  <h3 className="font-semibold">{conf.Title}</h3>
                  <p className="text-sm">
                    Starts: {new Date(conf.Start_Date).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* All Conferences */}
        <section>
          <h2 className="text-xl font-semibold mb-4">All Conferences</h2>

          {filteredConferences.length === 0 ? (
            <p className="text-gray-500">
              No conferences found matching your search.
            </p>
          ) : (
            <div className="space-y-4">
              {filteredConferences.map((conf) => (
                <div
                  key={conf.CID}
                  className="bg-white p-4 rounded-md shadow-md flex justify-between items-center hover:bg-gray-50 transition"
                >
                  <div
                    className="flex-1 cursor-pointer"
                    onClick={() => loadConferenceDetails(conf.CID)}
                  >
                    <h3 className="font-semibold">{conf.Title}</h3>
                    <p className="text-sm text-gray-600">
                      Starts: {new Date(conf.Start_Date).toLocaleDateString()}
                    </p>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleFavorite(conf.CID);
                    }}
                    className={`px-4 py-2 rounded-md text-sm font-medium ${
                      favorites.includes(conf.CID)
                        ? "bg-yellow-400 text-black"
                        : "bg-blue-600 text-white hover:bg-blue-700"
                    }`}
                  >
                    {favorites.includes(conf.CID) ? "★ Starred" : "Star"}
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Conference Detail Modal */}
        {selectedConference && (
          <div>
            <ConferenceInfo
              selectedConference={selectedConference}
              closeDetails={closeDetails}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
