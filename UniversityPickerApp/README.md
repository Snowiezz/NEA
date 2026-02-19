# University Picker – React Native Mobile App

A cross-platform mobile application built with **React Native + Expo** to help A-Level students choose the right university. Designed as a high-grade A-Level Computer Science NEA project.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [How to Run](#how-to-run)
4. [Architecture Overview](#architecture-overview)
5. [Screens](#screens)
6. [Recommendation Algorithm](#recommendation-algorithm)
7. [Data Persistence](#data-persistence)

---

## Features

| Feature | Description |
|---|---|
| **Home Dashboard** | Quick-action cards for all major features |
| **Preference Quiz** | 8-question quiz collecting user priorities |
| **Smart Recommendations** | Scored and ranked university list with reasons |
| **Side-by-Side Comparison** | Compare up to 3 universities on all metrics |
| **Save & Favourite** | Bookmark universities and add personal notes |
| **University Detail** | Full metrics, ratings, financial support info |
| **Settings** | View/edit preferences, reset data |
| **Full Persistence** | All data survives app restarts via AsyncStorage |

---

## Project Structure

```
UniversityPickerApp/
├── App.js                          # Root component, sets up Navigation
├── app.json                        # Expo configuration
├── babel.config.js                 # Babel preset for Expo
├── package.json                    # Dependencies
│
└── src/
    ├── data/
    │   └── universities.js         # Database of 15 UK universities
    │
    ├── storage/
    │   └── storage.js              # Persistent storage abstraction (AsyncStorage)
    │
    ├── logic/
    │   └── recommendationEngine.js # Scoring & ranking algorithm
    │
    ├── navigation/
    │   └── AppNavigator.js         # React Navigation stack + bottom tabs
    │
    └── screens/
        ├── HomeScreen.js           # Dashboard with quick-action cards
        ├── QuizScreen.js           # Multi-step preference quiz
        ├── RecommendationsScreen.js# Ranked list with match scores
        ├── CompareScreen.js        # Side-by-side comparison table
        ├── SavedScreen.js          # Saved/bookmarked universities
        ├── UniversityDetailScreen.js # Full university detail + notes
        └── SettingsScreen.js       # Preferences summary + reset
```

---

## How to Run

### Prerequisites

- [Node.js](https://nodejs.org/) v18 or higher
- [Expo Go](https://expo.dev/client) app on your phone (iOS or Android)

### Steps

```bash
# 1. Navigate to the app directory
cd UniversityPickerApp

# 2. Install dependencies
npm install

# 3. Start the Expo development server
npm start

# 4. Scan the QR code with Expo Go on your phone
#    OR press 'a' for Android emulator / 'i' for iOS simulator
```

### Running on Emulator

```bash
# Android emulator (requires Android Studio)
npm run android

# iOS simulator (macOS + Xcode required)
npm run ios
```

---

## Architecture Overview

The app follows a **clean, modular architecture**:

### Separation of Concerns

| Layer | Location | Responsibility |
|---|---|---|
| **Data** | `src/data/` | Static university database |
| **Storage** | `src/storage/` | All AsyncStorage read/write operations |
| **Logic** | `src/logic/` | Scoring algorithm, business rules |
| **Navigation** | `src/navigation/` | Screen routing and tab setup |
| **Screens** | `src/screens/` | UI components and user interaction |

### Key Design Patterns

- **Storage Abstraction**: All AsyncStorage calls are centralised in `storage.js`. If you ever want to switch to SQLite, only this file needs changing.
- **Modular Engine**: `recommendationEngine.js` is a pure function module — it takes preferences as input and returns ranked results. No side effects.
- **React Hooks**: Every screen uses `useState` and `useEffect`/`useFocusEffect` for state management.

---

## Screens

### Home Screen
The main dashboard. Shows a banner if the quiz hasn't been taken yet. Quick-action cards navigate to every feature.

### Quiz Screen
An 8-step multi-question quiz. Includes:
- **Slider questions** (1–5 importance scale) for ranking, quality, satisfaction, cost, and nightlife
- **Number inputs** for max distance and max monthly cost
- **Multiple choice** for home city/region

Answers are persisted immediately to AsyncStorage.

### Recommendations Screen
Loads user preferences and runs the scoring algorithm. Each result shows:
- Rank position and match percentage (0–100%)
- Colour-coded progress bar (green/amber/red)
- Distance from home
- 3 key reasons for recommendation

### Compare Screen
Select 2–3 universities via a modal picker. Renders a horizontal-scrollable comparison table covering all 9 key metrics.

### Saved Screen
Lists all bookmarked universities loaded from AsyncStorage. Shows personal notes inline. Long-press remove option.

### University Detail Screen
Shows every data field for a university, with:
- Star rating visualisation
- Save/unsave toggle (persisted)
- Editable personal notes (persisted)

### Settings Screen
Shows a summary of saved preferences, allows retaking the quiz, and provides a data reset option.

---

## Recommendation Algorithm

**File**: `src/logic/recommendationEngine.js`

### How It Works

1. **User preferences** (from the quiz) provide 5 importance weights (1–5 scale).
2. Each university is scored across 6 criteria:

| Criterion | Max Points | Direction |
|---|---|---|
| UK Ranking | 20 | Lower rank number = higher score |
| Course Quality | 20 | Higher rating = higher score |
| Student Satisfaction | 20 | Higher = better |
| Cost of Living | 20 | Lower cost = higher score |
| Nightlife | 10 | Higher = better |
| Distance from Home | 10 | Closer = better; >maxKm penalised |

3. Each sub-score is **normalised** against min/max values across all universities, so no single outlier skews results.
4. Importance weights scale the max contribution of each criterion.
5. Scores are scaled to **0–100** and sorted descending.
6. A `buildReasons()` function generates human-readable explanations.

---

## Data Persistence

**File**: `src/storage/storage.js`

All data is persisted using `@react-native-async-storage/async-storage`.

| Key | Data Stored |
|---|---|
| `@unipicker_preferences` | Quiz answers and importance weights |
| `@unipicker_saved` | Array of saved university IDs |
| `@unipicker_notes` | Map of university ID → note text |
| `@unipicker_quiz_completed` | Boolean flag |
| `@unipicker_settings` | App settings |

The storage module exports individual functions for each operation, keeping the persistence layer completely decoupled from the UI.
