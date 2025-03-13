import React from 'react';

const Results = ({ results }) => {
  if (!results || Object.keys(results).length === 0) {
    return <p className="text-center text-gray-600">No results found.</p>;
  }

  const rankedResults = results["ranked"] || [];
  const otherResults = Object.keys(results).filter((source) => source !== "ranked");

  return (
    <div className="flex flex-col items-center mt-8">
      <h2 className="text-2xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
        Top Ranked Results
      </h2>
      <div className="w-full max-w-4xl">
        {rankedResults.length > 0 ? (
          rankedResults
            .sort((a, b) => b.score - a.score)
            .map((result, index) => (
              <div
                key={index}
                className="bg-white shadow-lg p-6 rounded-lg my-4 hover:shadow-xl transition-all duration-300"
              >
                <h3 className="font-semibold text-xl text-blue-800">{result.title}</h3>
                <p className="text-gray-600 mt-2">Score: {result.score}</p>
                <a
                  href={result.link}
                  className="text-blue-500 hover:text-blue-700 mt-2 inline-block"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Read more →
                </a>
              </div>
            ))
        ) : (
          <p className="text-center text-gray-600">No ranked results available.</p>
        )}
      </div>

      <h2 className="text-2xl font-bold mt-10 mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
        Other Results
      </h2>
      <div className="w-full max-w-4xl">
        {otherResults.map((source) => (
          <div key={source} className="mb-8">
            <h3 className="font-semibold text-xl text-purple-800 mb-4">
              {source.toUpperCase()}
            </h3>
            <ul className="space-y-3">
              {results[source].map((result, index) => (
                <li
                  key={index}
                  className="bg-white shadow-md p-4 rounded-lg hover:shadow-lg transition-all duration-300"
                >
                  <a
                    href={result.link}
                    className="text-blue-500 hover:text-blue-700"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {result.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Results;