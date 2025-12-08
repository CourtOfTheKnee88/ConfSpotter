function Banner() {
  const handleLogout = () => {
    // Clear any stored user data
    localStorage.clear();
    sessionStorage.clear();

    // Redirect to login page
    window.location.href = "/";
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container px-20 py-6 mx-auto">
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center space-x-4">
            <h1 className="text-3xl font-bold text-gray-900">
              Conference Spotter
            </h1>
            <span className="text-gray-500 text-sm pt-[4px]">
              Helping You Find Your Next Academic Conference
            </span>
          </div>

          <button
            onClick={handleLogout}
            className="text-gray-600 hover:text-blue-600 transition-colors"
          >
            Log Out
          </button>
        </div>
      </div>
    </header>
  );
}

export default Banner;
