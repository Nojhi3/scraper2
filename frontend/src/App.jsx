import React from "react";
import SearchBar from "./components/SearchBar";
import Results from "./components/Results";
import { useState } from "react";

function App() {
  const [results, setResults] = useState(null);

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <div className="max-w-4xl mx-auto">
        <SearchBar onResults={setResults} />
        <Results results={results} />
      </div>
    </div>
  );
}

export default App;