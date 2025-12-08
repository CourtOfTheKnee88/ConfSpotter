import { useState, useEffect } from "react";

function ConferenceInfo({ selectedConference, closeDetails }) {
  const [papers, setPapers] = useState([]);
  const [paperLoading, setPaperLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch papers when conference is selected
  useEffect(() => {
    if (selectedConference?.CID || selectedConference?.id) {
      fetchPapers(selectedConference.CID || selectedConference.id);
    }
  }, [selectedConference]);

  // Fetch papers for the selected conference
  const fetchPapers = async (conferenceId) => {
    setPaperLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `http://localhost:5001/api/papers?conferenceId=${conferenceId}`
      );
      if (!response.ok) throw new Error("Failed to fetch papers");
      const data = await response.json();
      setPapers(data);
    } catch (err) {
      setError(err.message);
      setPapers([]);
    }
    setPaperLoading(false);
  };

  if (!selectedConference) return null;

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
      onClick={closeDetails}
    >
      <div
        className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto m-4"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-start mb-4">
            <h2 className="text-2xl font-bold text-gray-800">
              {selectedConference.name || selectedConference.Title}
            </h2>
            <button
              onClick={closeDetails}
              className="text-gray-500 text-2xl font-bold hover:text-red-600"
            >
              ✖
            </button>
          </div>

          {/* Conference Details */}
          <div className="space-y-3 mb-6">
            <div>
              <span className="font-semibold text-gray-700">Start Date: </span>
              <span className="text-gray-600">
                {new Date(
                  selectedConference.start_date || selectedConference.Start_Date
                ).toLocaleDateString()}
              </span>
            </div>

            <div>
              <span className="font-semibold text-gray-700">End Date: </span>
              <span className="text-gray-600">
                {new Date(
                  selectedConference.end_date || selectedConference.End_Date
                ).toLocaleDateString()}
              </span>
            </div>

            {(selectedConference.location || selectedConference.Location) && (
              <div>
                <span className="font-semibold text-gray-700">Location: </span>
                <span className="text-gray-600">
                  {selectedConference.location || selectedConference.Location}
                </span>
              </div>
            )}

            {(selectedConference.description || selectedConference.Descrip) && (
              <div>
                <span className="font-semibold text-gray-700">
                  Description:{" "}
                </span>
                <p className="text-gray-600 mt-1">
                  {selectedConference.description || selectedConference.Descrip}
                </p>
              </div>
            )}

            {(selectedConference.url ||
              selectedConference.URL ||
              selectedConference.link) && (
              <div>
                <span className="font-semibold text-gray-700">Website: </span>
                <a
                  href={
                    selectedConference.url ||
                    selectedConference.URL ||
                    selectedConference.link
                  }
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline break-all"
                >
                  {selectedConference.url ||
                    selectedConference.URL ||
                    selectedConference.link}
                </a>
              </div>
            )}
          </div>

          {/* Papers Section */}
          <div className="border-t pt-4">
            <h3 className="text-xl font-semibold mb-3">Associated Papers</h3>

            {paperLoading && <p className="text-gray-500">Loading papers...</p>}

            {error && (
              <p className="text-red-600">Error loading papers: {error}</p>
            )}

            {!paperLoading && !error && papers.length === 0 && (
              <p className="text-gray-500">
                No papers found for this conference.
              </p>
            )}

            {!paperLoading && papers.length > 0 && (
              <ul className="space-y-2">
                {papers.map((paper, index) => (
                  <li
                    key={paper.PID || index}
                    className="p-3 bg-gray-50 rounded hover:bg-gray-100 transition"
                  >
                    <div className="font-medium text-gray-800">
                      {paper.Topic}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">
                      Type: {paper.TypeOfPaper}
                    </div>
                    {paper.DueDate && (
                      <div className="text-sm text-gray-600">
                        Due Date: {new Date(paper.DueDate).toLocaleDateString()}
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ConferenceInfo;
