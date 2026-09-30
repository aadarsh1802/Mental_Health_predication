# MindTrack AI React UI

## Setup

```bash
npm install
npm run dev
```

Open the Vite URL shown in the terminal.

## Dependencies

- React
- Vite
- Lucide React
- Recharts

This version recreates the supplied MindTrack AI dashboard UI and includes working form interactions and a demo prediction calculation.

## Connect your real ML model

Replace `handlePredict()` in `src/App.jsx` with a fetch request to your FastAPI backend:

```js
const response = await fetch("http://127.0.0.1:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(form)
});

const data = await response.json();
setScore(data.mental_health_score);
```
