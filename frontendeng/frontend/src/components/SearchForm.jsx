import React, { useState } from "react";

export default function SearchForm() {
  const [formData, setFormData] = useState({
    lat: 0,
    lon: 0,
    elevation: 0,
    start_time: 0,
    end_time: 0,
    whitelisted_event_types: "",
  });

  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

const handleChange = (e) => {
  const { name, value, type } = e.target;
  setFormData(prev => ({
    ...prev,
    [name]: type === "number" ? (value === "" ? null : Number(value)) : value,
  }));
};

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError(null);

  try {
    const payload = {
      start_time: formData.start_time || 0,
      end_time: formData.end_time || 0,
      lon: formData.lon || 0,
      lat: formData.lat || 0,
      elevation: formData.elevation || 0,
      whitelisted_event_types: formData.whitelisted_event_types
        ? [formData.whitelisted_event_types]
        : [],
      event_specific_criteria: [],
    };

    const response = await fetch("http://localhost:8000/event/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    setResponseData(data);
  } catch (err) {
    console.error(err);
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="number" name="lon" value={formData.lon} onChange={handleChange} />
        <input type="number" name="lat" value={formData.lat} onChange={handleChange} />
        <input type="number" name="elevation" value={formData.elevation} onChange={handleChange} />
        <input type="number" name="start_time" value={formData.start_time} onChange={handleChange} />
        <input type="number" name="end_time" value={formData.end_time} onChange={handleChange} />
        <select
          name="whitelisted_event_types"
          value={formData.whitelisted_event_types}
          onChange={e =>
            setFormData(prev => ({
              ...prev,
              whitelisted_event_types: Array.from(e.target.selectedOptions, o => o.value)
            }))
          }
          multiple
        >
          <option value="A">A</option>
          <option value="B">B</option>
        </select>
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Submit"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>Error: {error}</p>}

      {responseData && (
        <pre>{JSON.stringify(responseData, null, 2)}</pre>
      )}
    </div>
  );
}
