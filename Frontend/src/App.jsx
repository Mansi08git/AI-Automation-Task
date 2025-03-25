//import 
import React, { useState } from "react";
import './index.css';

const CodeAnalyzer = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a file to upload.");
            return;
        }
        
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:8000/analyze-code", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            
            if (data.breakdown) {
                setResult(data);
                setError(null);
            } else {
                setError("Unexpected response format from server.");
            }
        } catch (err) {
            setError("Failed to analyze the file.");
        }
    };

    return (
        <div style={{ padding: '20px', maxWidth: '500px', margin: 'auto', border: '1px solid #ccc', borderRadius: '10px' }}>
            <h1 className="text-xl font-bold">Code Analyzer</h1>
            <input type="file" onChange={handleFileChange} className="border p-2 w-full" />
            <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded mt-2">
                Upload & Analyze
            </button>

            {error && <p className="text-red-500">{error}</p>}

            {result && (
                <div className="mt-4 p-4 border rounded">
                    <h2 className="text-lg font-semibold">Analysis Result</h2>
                    <p><strong>Overall Score:</strong> {result.overall_score}</p>

                    <h3 className="mt-2 font-semibold">Category Breakdown:</h3>
                    <ul className="list-disc pl-5">
                        {Object.entries(result.breakdown).map(([key, value]) => (
                            <li key={key}><strong>{key.replace(/_/g, " ")}:</strong> {value}/20</li>
                        ))}
                    </ul>

                    <h3 className="mt-2 font-semibold">Recommendations:</h3>
                    <ul className="list-disc pl-5">
                        {result.recommendations.map((rec, index) => (
                            <li key={index}>{rec}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default CodeAnalyzer;
