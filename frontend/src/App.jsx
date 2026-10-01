import { useState } from "react";

import {
  Activity,
  BarChart3,
  Brain,
  ChevronDown,
  Moon,
  Smartphone,
  Target,
  TrendingDown,
  TrendingUp,
  UserRound,
  Users,
  Sparkles,
} from "lucide-react";

import {
  BarChart,
  Bar,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";


/* =========================
   STATIC DATA
========================= */

const platformData = [
  { name: "Instagram", value: 0.62 },
  { name: "YouTube", value: 0.48 },
  { name: "TikTok", value: 0.41 },
  { name: "Others", value: 0.23 },
];

const previewRows = [
  [20, "Male", "India", "Undergraduate", "Instagram", "4.5", "64.8"],
  [21, "Female", "India", "Undergraduate", "YouTube", "3.5", "72.3"],
  [19, "Male", "India", "High School", "TikTok", "5.0", "48.6"],
  [22, "Female", "India", "Graduate", "Instagram", "2.0", "78.9"],
  [20, "Male", "India", "Undergraduate", "YouTube", "4.0", "56.7"],
];


/* =========================
   SELECT FIELD
========================= */

function SelectField({
  label,
  value,
  onChange,
  options,
}) {
  return (
    <label className="field">

      <span className="field-label">
        {label}
      </span>

      <span className="select-wrap">

        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
        >

          {options.map((option) => (
            <option
              key={option}
              value={option}
            >
              {option}
            </option>
          ))}

        </select>

        <ChevronDown size={15} />

      </span>

    </label>
  );
}


/* =========================
   METRIC CARD
========================= */

function MetricCard({
  icon: Icon,
  title,
  value,
  tone = "blue",
}) {
  return (
    <div className={`metric-card ${tone}`}>

      <div className="metric-icon">
        <Icon size={20} />
      </div>

      <div>
        <div className="metric-title">
          {title}
        </div>

        <div className="metric-value">
          {value}
        </div>
      </div>

    </div>
  );
}


/* =========================
   MAIN APP
========================= */

export default function App() {

  /* =========================
     FORM DATA
  ========================= */

  const [form, setForm] = useState({

    Age: 20,

    Gender: "Male",

    Country: "India",

    Academic_Level: "Undergraduate",

    Most_Used_Platform: "Instagram",

    Purpose_Of_Use: "Entertainment",

    Avg_Daily_Usage_Hours: 4.5,

    Daily_Unlocks: 80,

    Study_Hours: 4,

    Physical_Activity_Hours: 1.5,

    Sleep_Hours_Per_Night: 7,

    Stress_Level: "Medium",

  });


  /* =========================
     PREDICTION STATE
  ========================= */

  const [score, setScore] = useState(null);

  const [category, setCategory] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  /* =========================
     FORM UPDATE
  ========================= */

  const update = (key) => (value) => {

    const numericFields = [
      "Age",
      "Avg_Daily_Usage_Hours",
      "Daily_Unlocks",
      "Study_Hours",
      "Physical_Activity_Hours",
      "Sleep_Hours_Per_Night",
    ];

    const finalValue = numericFields.includes(key)
      ? Number(value)
      : value;

    setForm((prev) => ({
      ...prev,
      [key]: finalValue,
    }));

  };


  /* =========================
     FASTAPI PREDICTION
  ========================= */

  const handlePredict = async () => {

    setLoading(true);

    setError("");

    setScore(null);

    setCategory("");


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(form),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail || "Prediction failed"
        );

      }


      console.log(
        "FastAPI response:",
        data
      );


      setScore(
        data.mental_health_score
      );

      setCategory(
        data.category
      );


    } catch (err) {

      console.error(
        "Prediction error:",
        err
      );

      setError(
        err.message ||
        "Unable to connect to FastAPI."
      );


    } finally {

      setLoading(false);

    }

  };


  /* =========================
     UI
  ========================= */

  return (

    <div className="app">

      {/* =========================
          MAIN LAYOUT
      ========================= */}

      <div className="layout">

        <main className="content">

          {/* =========================
              HERO
          ========================= */}

          <section className="hero" id="home">

            <div>

              <h1>
                Predict Your Mental Health Score
              </h1>



            </div>


            <div className="hero-art">

              <Brain
                size={82}
                strokeWidth={1.6}
              />

              <div>

                <strong>
                  Smarter Predictions
                </strong>

                <span>
                  for a Healthier You
                </span>

              </div>

            </div>

          </section>


          {/* =========================
              DASHBOARD
          ========================= */}

          <section className="dashboard-grid">


            {/* =========================
                LEFT COLUMN
            ========================= */}

            <div className="left-column">


              {/* =========================
                  FORM
              ========================= */}

              <section className="panel form-panel" id="predictor">

                <h2>
                  Student Profile & Lifestyle Input
                </h2>


                {/* BASIC INFORMATION */}

                <div className="form-section">

                  <h3>
                    <UserRound size={21} />

                    1. Basic Information
                  </h3>


                  <div className="form-grid four">


                    <SelectField
                      label="Age"
                      value={form.Age}
                      onChange={update("Age")}
                      options={[
                        "18",
                        "19",
                        "20",
                        "21",
                        "22",
                        "23",
                        "24",
                        "25",
                        "26",
                        "27",
                        "28",
                        "29",
                        "30",
                      ]}
                    />


                    <SelectField
                      label="Gender"
                      value={form.Gender}
                      onChange={update("Gender")}
                      options={[
                        "Male",
                        "Female",
                        "Other",
                      ]}
                    />


                    <SelectField
                      label="Country"
                      value={form.Country}
                      onChange={update("Country")}
                      options={[
                        "India",
                        "USA",
                        "UK",
                        "Canada",
                        "Australia",
                        "Germany",
                        "Other",
                      ]}
                    />


                    <SelectField
                      label="Academic Level"
                      value={form.Academic_Level}
                      onChange={update("Academic_Level")}
                      options={[
                        "High School",
                        "Undergraduate",
                        "Graduate",
                        "Postgraduate",
                      ]}
                    />

                  </div>

                </div>


                {/* SOCIAL MEDIA */}

                <div className="form-section">

                  <h3>
                    <Smartphone size={21} />

                    2. Social Media Usage
                  </h3>


                  <div className="form-grid four">


                    <SelectField
                      label="Most Used Platform"
                      value={form.Most_Used_Platform}
                      onChange={update(
                        "Most_Used_Platform"
                      )}
                      options={[
                        "Instagram",
                        "YouTube",
                        "TikTok",
                        "Facebook",
                        "Twitter",
                        "Other",
                      ]}
                    />


                    <SelectField
                      label="Purpose of Use"
                      value={form.Purpose_Of_Use}
                      onChange={update(
                        "Purpose_Of_Use"
                      )}
                      options={[
                        "Entertainment",
                        "Education",
                        "Communication",
                        "Socializing",
                        "News",
                        "Other",
                      ]}
                    />


                    <SelectField
                      label="Daily Usage Hours"
                      value={
                        form.Avg_Daily_Usage_Hours
                      }
                      onChange={update(
                        "Avg_Daily_Usage_Hours"
                      )}
                      options={[
                        "0.5",
                        "1",
                        "1.5",
                        "2",
                        "2.5",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                      ]}
                    />


                    <SelectField
                      label="Daily Unlocks"
                      value={form.Daily_Unlocks}
                      onChange={update(
                        "Daily_Unlocks"
                      )}
                      options={[
                        "10",
                        "20",
                        "30",
                        "40",
                        "50",
                        "60",
                        "80",
                        "100",
                        "120",
                        "150",
                      ]}
                    />

                  </div>

                </div>


                {/* SLEEP / STUDY / ACTIVITY */}

                <div className="form-section">

                  <h3>
                    <Moon size={21} />

                    3. Sleep, Study & Physical Activity
                  </h3>


                  <div className="form-grid three">


                    <SelectField
                      label="Sleep Hours"
                      value={
                        form.Sleep_Hours_Per_Night
                      }
                      onChange={update(
                        "Sleep_Hours_Per_Night"
                      )}
                      options={[
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                      ]}
                    />


                    <SelectField
                      label="Study Hours"
                      value={form.Study_Hours}
                      onChange={update(
                        "Study_Hours"
                      )}
                      options={[
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "10",
                      ]}
                    />


                    <SelectField
                      label="Physical Activity Hours"
                      value={
                        form.Physical_Activity_Hours
                      }
                      onChange={update(
                        "Physical_Activity_Hours"
                      )}
                      options={[
                        "0",
                        "0.5",
                        "1",
                        "1.5",
                        "2",
                        "2.5",
                        "3",
                        "4",
                      ]}
                    />

                  </div>

                </div>


                {/* STRESS */}

                <div className="form-section">

                  <h3>
                    <Activity size={21} />

                    4. Mental Health Factor
                  </h3>


                  <div className="form-grid three">


                    <SelectField
                      label="Stress Level"
                      value={form.Stress_Level}
                      onChange={update(
                        "Stress_Level"
                      )}
                      options={[
                        "Low",
                        "Medium",
                        "High",
                      ]}
                    />

                  </div>

                </div>


                {/* PREDICT BUTTON */}

                <button
                  className="predict-btn"
                  onClick={handlePredict}
                  disabled={loading}
                >

                  <Sparkles size={19} />

                  {loading
                    ? "Predicting..."
                    : "Predict Mental Health Score"}

                </button>


                {/* LOADING */}

                {loading && (

                  <p className="loading-text">
                    Connecting to ML model...
                  </p>

                )}


                {/* ERROR */}

                {error && (

                  <p className="error-text">
                    ❌ {error}
                  </p>

                )}

              </section>


              {/* =========================
                  PREDICTION RESULT
              ========================= */}



            </div>


            {/* =========================
                RIGHT COLUMN
            ========================= */}

            <div className="right-column">


              {/* DATASET INSIGHTS */}




              {/* CHART */}




              {/* DATASET PREVIEW */}




              {/* KEY TAKEAWAYS */}

              <section className="takeaways" id="takeaways">
                <section className="prediction-card" id="model-performance">

                  <div className="prediction-main">

                    <div className="prediction-icon">
                      <Brain size={31} />
                    </div>


                    <div>

                      <div className="prediction-label">
                        Predicted Mental Health Score
                      </div>


                      <div className="big-score">

                        {score !== null
                          ? Number(score).toFixed(2)
                          : "--"}

                        <span>
                          {" "} / 100
                        </span>

                      </div>


                      {category && (

                        <div className="risk-badge">
                          {category}
                        </div>

                      )}


                      <p>
                        This score is based on our trained
                        machine learning model and may not
                        be a definitive diagnosis.
                        Consider professional help if needed.
                      </p>

                    </div>

                  </div>


                  <div className="model-performance">

                    <h3>
                      Model Performance
                    </h3>


                    <div className="perf-row">

                      <Target size={22} />

                      <div>

                        <small>
                          Mean Absolute Error (MAE)
                        </small>

                        <strong>
                          6.42
                        </strong>

                      </div>

                    </div>


                    <div className="perf-row">

                      <BarChart3 size={22} />

                      <div>

                        <small>
                          R² Score
                        </small>

                        <strong>
                          0.68
                        </strong>

                      </div>

                    </div>

                  </div>

                </section>
                <br></br>
                <h2>
                  <Sparkles size={19} />
                  Key Takeaways

                </h2>


                <ul>

                  <li>
                    Social media usage can be
                    analyzed together with other
                    lifestyle factors.
                  </li>

                  <li>
                    Sleep and physical activity
                    are included as model inputs.
                  </li>

                  <li>
                    Stress level is included as
                    an important prediction feature.
                  </li>

                </ul>

              </section>

            </div>

          </section>

        </main>

      </div>

    </div>

  );
}