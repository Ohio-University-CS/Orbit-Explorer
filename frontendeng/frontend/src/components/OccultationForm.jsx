import React, { useState, useEffect } from "react";

const OCCULTATION_TOP_LEVEL = [
  { value: "ECLIPSE", label: "Eclipse" },
  { value: "PLANETARY_OCCULTATION", label: "Planetary occultation" },
  { value: "LUNAR_OCCULTATION", label: "Lunar occultation" },
  { value: "ASTEROID_OCCULTATION", label: "Asteroid occultation" },
  { value: "TRANSIT", label: "Transit" },
];

const SOLAR_TYPES = [
  "partial",
  "total",
  "annular",
  "hybrid",
];

const LUNAR_TYPES = [
  "penumbral",
  "partial",
  "total",
];

// For now these are static; later you’ll swap to API calls
const PLANETS = [
  "Mercury",
  "Venus",
  "Earth",
  "Mars",
  "Jupiter",
  "Saturn",
  "Uranus",
  "Neptune",
];

const MAJOR_MOONS = [
  "Moon",
  "Io",
  "Europa",
  "Ganymede",
  "Callisto",
  "Titan",
  "Enceladus",
];

const STARS_PLACEHOLDER = [
  "Any star",
  "Bright catalog star",
];

export default function OccultationForm({ onSubmit }) {
  // Time + location
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [latitude, setLatitude] = useState("");
  const [longitude, setLongitude] = useState("");

  // Occultation type structure
  const [topLevelType, setTopLevelType] = useState("ECLIPSE");
  const [eclipseKind, setEclipseKind] = useState("SOLAR"); // SOLAR or LUNAR
  const [solarSubtype, setSolarSubtype] = useState("total");
  const [lunarSubtype, setLunarSubtype] = useState("total");

  // Planetary / lunar / asteroid / transit subtypes could live here
  const [planetarySubtype, setPlanetarySubtype] = useState("planet-moon"); 
  // e.g. planet-star, planet-planet, planet-moon, etc.

  // Body dropdowns
  const [occultingBodies, setOccultingBodies] = useState([]);
  const [targetBodies, setTargetBodies] = useState([]);
  const [selectedOcculting, setSelectedOcculting] = useState("");
  const [selectedTarget, setSelectedTarget] = useState("");

  // Update available bodies whenever the chosen type changes
  useEffect(() => {
    let occulting = [];
    let targets = [];

    if (topLevelType === "ECLIPSE") {
      if (eclipseKind === "SOLAR") {
        occulting = ["Moon"];
        targets = ["Sun"];
      } else {
        // lunar eclipse: Earth shadow on Moon
        occulting = ["Earth"];
        targets = ["Moon"];
      }
    } else if (topLevelType === "PLANETARY_OCCULTATION") {
      if (planetarySubtype === "planet-moon") {
        occulting = PLANETS;
        targets = MAJOR_MOONS;
      } else if (planetarySubtype === "planet-star") {
        occulting = PLANETS;
        targets = STARS_PLACEHOLDER;
      } else if (planetarySubtype === "planet-planet") {
        occulting = PLANETS;
        targets = PLANETS;
      }
    } else if (topLevelType === "LUNAR_OCCULTATION") {
      occulting = ["Moon"];
      targets = [...PLANETS, ...STARS_PLACEHOLDER];
    } else if (topLevelType === "ASTEROID_OCCULTATION") {
      occulting = ["Any asteroid"]; // TODO: replace with real asteroid list
      targets = STARS_PLACEHOLDER;
    } else if (topLevelType === "TRANSIT") {
      occulting = PLANETS;
      targets = ["Sun", "Star"];
    }

    setOccultingBodies(occulting);
    setTargetBodies(targets);
    setSelectedOcculting(occulting[0] || "");
    setSelectedTarget(targets[0] || "");
  }, [topLevelType, eclipseKind, planetarySubtype]);

  function handleSubmit(e) {
    e.preventDefault();

    const payload = {
      startTime,
      endTime,
      location: {
        latitude,
        longitude,
      },
      occultation: {
        topLevelType,
        eclipseKind: topLevelType === "ECLIPSE" ? eclipseKind : null,
        solarSubtype:
          topLevelType === "ECLIPSE" && eclipseKind === "SOLAR"
            ? solarSubtype
            : null,
        lunarSubtype:
          topLevelType === "ECLIPSE" && eclipseKind === "LUNAR"
            ? lunarSubtype
            : null,
        planetarySubtype:
          topLevelType === "PLANETARY_OCCULTATION" ? planetarySubtype : null,
        occultingBody: selectedOcculting,
        targetBody: selectedTarget,
      },
    };

    if (onSubmit) {
      onSubmit(payload);
    } else {
      // TEMP: just log for now
      console.log("Occultation search:", payload);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="occultation-form">
      <h2>Occultation Search</h2>

      {/* Time range */}
      <section className="occultation-section">
        <h3>Time Range</h3>
        <div>
          <label>
            Start time:
            <input
              type="datetime-local"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              required
            />
          </label>
        </div>
        <div>
          <label>
            End time:
            <input
              type="datetime-local"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              required
            />
          </label>
        </div>
      </section>

      {/* Location */}
      <section className="occultation-section">
        <h3>Observer Location</h3>
        <div>
          <label>
            Latitude:
            <input
              type="number"
              step="0.0001"
              value={latitude}
              onChange={(e) => setLatitude(e.target.value)}
              placeholder="e.g. 39.3292"
              required
            />
          </label>
        </div>
        <div>
          <label>
            Longitude:
            <input
              type="number"
              step="0.0001"
              value={longitude}
              onChange={(e) => setLongitude(e.target.value)}
              placeholder="-82.1013"
              required
            />
          </label>
        </div>
      </section>

      {/* Occultation type selection */}
      <section className="occultation-section">
        <h3>Occultation Type</h3>
        <div>
          <label>
            Category:
            <select
              value={topLevelType}
              onChange={(e) => setTopLevelType(e.target.value)}
            >
              {OCCULTATION_TOP_LEVEL.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
          </label>
        </div>

        {topLevelType === "ECLIPSE" && (
          <>
            <div>
              <label>
                Eclipse kind:
                <select
                  value={eclipseKind}
                  onChange={(e) => setEclipseKind(e.target.value)}
                >
                  <option value="SOLAR">Solar</option>
                  <option value="LUNAR">Lunar</option>
                </select>
              </label>
            </div>

            {eclipseKind === "SOLAR" && (
              <div>
                <label>
                  Solar type:
                  <select
                    value={solarSubtype}
                    onChange={(e) => setSolarSubtype(e.target.value)}
                  >
                    {SOLAR_TYPES.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            )}

            {eclipseKind === "LUNAR" && (
              <div>
                <label>
                  Lunar type:
                  <select
                    value={lunarSubtype}
                    onChange={(e) => setLunarSubtype(e.target.value)}
                  >
                    {LUNAR_TYPES.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            )}
          </>
        )}

        {topLevelType === "PLANETARY_OCCULTATION" && (
          <div>
            <label>
              Planetary subtype:
              <select
                value={planetarySubtype}
                onChange={(e) => setPlanetarySubtype(e.target.value)}
              >
                <option value="planet-star">Planet–star</option>
                <option value="planet-planet">Planet–planet</option>
                <option value="planet-moon">Planet–moon</option>
              </select>
            </label>
          </div>
        )}
      </section>

      {/* Body selection */}
      <section className="occultation-section">
        <h3>Bodies</h3>
        <div>
          <label>
            Occulting body:
            <select
              value={selectedOcculting}
              onChange={(e) => setSelectedOcculting(e.target.value)}
            >
              {occultingBodies.map((body) => (
                <option key={body} value={body}>
                  {body}
                </option>
              ))}
            </select>
          </label>
        </div>

        <div>
          <label>
            Target body:
            <select
              value={selectedTarget}
              onChange={(e) => setSelectedTarget(e.target.value)}
            >
              {targetBodies.map((body) => (
                <option key={body} value={body}>
                  {body}
                </option>
              ))}
            </select>
          </label>
        </div>
      </section>

      <button type="submit">Run occultation calculations</button>
    </form>
  );
}
