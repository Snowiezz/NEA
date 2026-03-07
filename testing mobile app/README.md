# University Picker – React Native Mobile App

A cross-platform mobile application built with **React Native + Expo** to help A-Level students choose the right university. Built as a high-grade A-Level Computer Science NEA project.

---

## How to Run

### Prerequisites
- [Node.js](https://nodejs.org/) v18 or higher
- [Expo Go](https://expo.dev/client) app on your phone (iOS or Android)

### Steps

```bash
# 1. Navigate to this folder
cd "testing mobile app"

# 2. Install dependencies
npm install

# 3. Start the development server
npm start

# 4. Scan the QR code with Expo Go on your phone
#    OR press 'a' for Android emulator / 'i' for iOS simulator
```

---

## Project Structure

```
testing mobile app/
├── App.js                          # Root component
├── app.json                        # Expo configuration
├── babel.config.js                 # Babel preset
├── package.json                    # Dependencies
│
└── src/
    ├── data/
    │   └── universities.js         # Database of 15 UK universities
    ├── storage/
    │   └── storage.js              # Persistent storage (AsyncStorage)
    ├── logic/
    │   └── recommendationEngine.js # Weighted scoring algorithm
    ├── navigation/
    │   └── AppNavigator.js         # React Navigation setup
    └── screens/
        ├── HomeScreen.js           # Dashboard
        ├── QuizScreen.js           # 8-step preference quiz
        ├── RecommendationsScreen.js# Ranked recommendations
        ├── CompareScreen.js        # Side-by-side comparison
        ├── SavedScreen.js          # Saved/bookmarked universities
        ├── UniversityDetailScreen.js # Full university detail + notes
        └── SettingsScreen.js       # Preferences + reset
```

---

## Features

| Feature | Description |
|---|---|
| **Preference Quiz** | 8 questions collecting importance weights and home region |
| **Recommendations** | Universities scored 0–100 and ranked by match percentage |
| **Compare** | Side-by-side table comparing up to 3 universities across 9 metrics |
| **Save & Notes** | Bookmark universities and add personal notes |
| **Full Persistence** | All data survives app restarts via AsyncStorage |

---

## Recommendation Algorithm

Each university is scored across 6 criteria:

| Criterion | Max Points | Direction |
|---|---|---|
| UK Ranking | 20 | Lower rank = higher score |
| Course Quality | 20 | Higher = better |
| Student Satisfaction | 20 | Higher = better |
| Cost of Living | 20 | Lower cost = higher score |
| Nightlife | 10 | Higher = better |
| Distance from Home | 10 | Closer = better |

Scores are normalised against dataset min/max, then scaled by the user's importance weights from the quiz (1–5 scale). Distance uses the Haversine formula; universities beyond the user's max distance are penalised.
