import React from 'react';
import { useState } from "react";
import axios from "axios";

const SearchBar = ({ onResults }) => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const searchAI = async () => {
    if (!query.trim()) {
      alert("Please enter a search query");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/search", { query });
      console.log("Received Data:", response.data);
      onResults(response.data.results);
    } catch (error) {
      console.error("Error fetching search results:", error);
      alert("Failed to fetch results.");
    }

    setLoading(false);
  };

  return (
    <div className="text-center my-8">
      <h1 className="text-4xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
        AI Search
      </h1>
      <div className="flex justify-center items-center gap-2">
        <input
          type="text"
          className="border-2 border-gray-300 p-3 w-2/3 rounded-lg focus:outline-none focus:border-blue-500 shadow-sm transition-all text-black"
          placeholder="Enter your search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={searchAI}
          className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-lg hover:from-blue-600 hover:to-purple-600 transition-all shadow-lg disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>
    </div>
  );
};

export default SearchBar;