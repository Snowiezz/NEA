/**
 * recommendationEngine.js
 * Scoring and ranking algorithm for the University Picker app.
 *
 * ALGORITHM OVERVIEW
 * ------------------
 * Each university is scored on a scale of 0–100 by combining
 * weighted sub-scores across several criteria.  The weights are
 * determined by the user's quiz answers (their stated importance
 * levels for each factor).
 *
 * Criteria and their maximum weight contributions:
 *   - ranking             (up to 20 points)
 *   - courseQualityRating (up to 20 points)
 *   - studentSatisfaction (up to 20 points)
 *   - costOfLiving        (up to 20 points)  — lower cost = higher score
 *   - nightlifeRating     (up to 10 points)
 *   - distance            (up to 10 points)  — closer = higher score
 *
 * Each sub-score is normalised against the best/worst values across
 * ALL universities so that no single outlier dominates the result.
 */

import UNIVERSITIES from '../data/universities';

// ─── Constants ───────────────────────────────────────────────────────────────

/** Maximum score a university can achieve (all criteria perfectly match prefs) */
const MAX_SCORE = 100;

// ─── Haversine distance formula ──────────────────────────────────────────────

/**
 * Calculates the straight-line distance (km) between two lat/lon points.
 * Used to compute how far each university is from the user's home.
 *
 * @param {number} lat1
 * @param {number} lon1
 * @param {number} lat2
 * @param {number} lon2
 * @returns {number} distance in km
 */
function haversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth radius in km
  const toRad = (deg) => (deg * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// ─── Normalisation helpers ────────────────────────────────────────────────────

/**
 * Returns a value in [0,1] where 1 = best (highest value is best).
 */
function normaliseHigh(value, min, max) {
  if (max === min) return 1;
  return (value - min) / (max - min);
}

/**
 * Returns a value in [0,1] where 1 = best (lowest value is best, e.g. cost).
 */
function normaliseLow(value, min, max) {
  if (max === min) return 1;
  return (max - value) / (max - min);
}

// ─── Importance weight mapping ────────────────────────────────────────────────

/**
 * Converts a 1–5 importance slider value to a weight multiplier (0.2 – 1.0).
 * A user who rates something 1/5 still contributes a small weight so that
 * the factor is never completely ignored.
 *
 * @param {number} importance - integer 1–5
 * @returns {number} weight multiplier in [0.2, 1.0]
 */
function importanceToWeight(importance) {
  return importance / 5;
}

// ─── Main Scoring Function ────────────────────────────────────────────────────

/**
 * Scores and ranks all universities based on user preferences.
 *
 * @param {Object} preferences - user preferences from the quiz:
 *   {
 *     homeLatitude:            number,  // user's home latitude
 *     homeLongitude:           number,  // user's home longitude
 *     maxDistanceKm:           number,  // max acceptable distance (km)
 *     importanceRanking:       number,  // 1–5
 *     importanceCourseQuality: number,  // 1–5
 *     importanceSatisfaction:  number,  // 1–5
 *     importanceCost:          number,  // 1–5
 *     importanceNightlife:     number,  // 1–5
 *   }
 *
 * @returns {Array<{university, score, breakdown, reasons}>} sorted best-first
 */
export function rankUniversities(preferences) {
  const {
    homeLatitude = 51.5074,   // default: London
    homeLongitude = -0.1278,
    maxDistanceKm = 600,
    importanceRanking = 3,
    importanceCourseQuality = 3,
    importanceSatisfaction = 3,
    importanceCost = 3,
    importanceNightlife = 3,
  } = preferences;

  // ── 1. Pre-compute stats across all universities ──────────────────────────

  const rankings      = UNIVERSITIES.map((u) => u.ranking);
  const qualities     = UNIVERSITIES.map((u) => u.courseQualityRating);
  const satisfactions = UNIVERSITIES.map((u) => u.studentSatisfaction);
  const costs         = UNIVERSITIES.map((u) => u.costOfLiving);
  const nightlifes    = UNIVERSITIES.map((u) => u.nightlifeRating);

  const distances = UNIVERSITIES.map((u) =>
    haversineDistance(homeLatitude, homeLongitude, u.latitude, u.longitude)
  );

  const stats = {
    ranking:  { min: Math.min(...rankings),      max: Math.max(...rankings) },
    quality:  { min: Math.min(...qualities),     max: Math.max(...qualities) },
    sat:      { min: Math.min(...satisfactions), max: Math.max(...satisfactions) },
    cost:     { min: Math.min(...costs),         max: Math.max(...costs) },
    nightlife:{ min: Math.min(...nightlifes),    max: Math.max(...nightlifes) },
    distance: { min: Math.min(...distances),     max: Math.max(...distances) },
  };

  // ── 2. Weights ────────────────────────────────────────────────────────────

  const wRanking  = importanceToWeight(importanceRanking)       * 20;
  const wQuality  = importanceToWeight(importanceCourseQuality) * 20;
  const wSat      = importanceToWeight(importanceSatisfaction)  * 20;
  const wCost     = importanceToWeight(importanceCost)          * 20;
  const wNight    = importanceToWeight(importanceNightlife)     * 10;
  const wDistance = 10; // distance weight is fixed (based on max preference)

  const totalPossibleWeight = wRanking + wQuality + wSat + wCost + wNight + wDistance;

  // ── 3. Score each university ──────────────────────────────────────────────

  const results = UNIVERSITIES.map((uni, index) => {
    const distance = distances[index];

    // Normalised sub-scores (0–1)
    const rankScore    = normaliseLow(uni.ranking,             stats.ranking.min,   stats.ranking.max);
    const qualityScore = normaliseHigh(uni.courseQualityRating, stats.quality.min,  stats.quality.max);
    const satScore     = normaliseHigh(uni.studentSatisfaction, stats.sat.min,      stats.sat.max);
    const costScore    = normaliseLow(uni.costOfLiving,        stats.cost.min,      stats.cost.max);
    const nightScore   = normaliseHigh(uni.nightlifeRating,    stats.nightlife.min, stats.nightlife.max);

    // Distance score: penalise universities beyond maxDistanceKm
    const distancePenalty = distance > maxDistanceKm ? 0.2 : 1;
    const distScore = normaliseLow(distance, stats.distance.min, stats.distance.max) * distancePenalty;

    // Weighted total
    const rawScore =
      rankScore    * wRanking  +
      qualityScore * wQuality  +
      satScore     * wSat      +
      costScore    * wCost     +
      nightScore   * wNight    +
      distScore    * wDistance;

    // Normalise to 0–100
    const score = Math.round((rawScore / totalPossibleWeight) * MAX_SCORE);

    // Build a breakdown for the UI
    const breakdown = {
      ranking:      Math.round(rankScore    * wRanking),
      courseQuality:Math.round(qualityScore * wQuality),
      satisfaction: Math.round(satScore     * wSat),
      cost:         Math.round(costScore    * wCost),
      nightlife:    Math.round(nightScore   * wNight),
      distance:     Math.round(distScore    * wDistance),
    };

    // Human-readable reasons for recommendation
    const reasons = buildReasons(uni, breakdown, distance, maxDistanceKm, preferences);

    return { university: uni, score, breakdown, distance: Math.round(distance), reasons };
  });

  // ── 4. Sort descending by score ───────────────────────────────────────────
  return results.sort((a, b) => b.score - a.score);
}

// ─── Reason Builder ───────────────────────────────────────────────────────────

/**
 * Generates human-readable reasons explaining why a university scored well.
 *
 * @param {Object} uni
 * @param {Object} breakdown - per-category score contributions
 * @param {number} distance - km from home
 * @param {number} maxDistanceKm
 * @param {Object} preferences
 * @returns {string[]} array of reason strings
 */
function buildReasons(uni, breakdown, distance, maxDistanceKm, preferences) {
  const reasons = [];

  if (uni.ranking <= 5) {
    reasons.push(`Top ${uni.ranking} university in the UK`);
  } else if (uni.ranking <= 10) {
    reasons.push(`Highly ranked (#${uni.ranking} in the UK)`);
  }

  if (uni.courseQualityRating >= 4.5) {
    reasons.push(`Excellent course quality (${uni.courseQualityRating}/5)`);
  } else if (uni.courseQualityRating >= 4.0) {
    reasons.push(`Strong course quality (${uni.courseQualityRating}/5)`);
  }

  if (uni.studentSatisfaction >= 4.2) {
    reasons.push(`Outstanding student satisfaction (${uni.studentSatisfaction}/5)`);
  } else if (uni.studentSatisfaction >= 4.0) {
    reasons.push(`Good student satisfaction (${uni.studentSatisfaction}/5)`);
  }

  if (uni.costOfLiving <= 550) {
    reasons.push(`Low cost of living (~£${uni.costOfLiving}/month)`);
  } else if (uni.costOfLiving <= 650) {
    reasons.push(`Moderate cost of living (~£${uni.costOfLiving}/month)`);
  }

  if (uni.nightlifeRating >= 4.5 && preferences.importanceNightlife >= 4) {
    reasons.push(`Excellent nightlife and social scene (${uni.nightlifeRating}/5)`);
  }

  if (distance <= maxDistanceKm) {
    reasons.push(`Within your preferred distance (~${Math.round(distance)} km)`);
  }

  if (reasons.length === 0) {
    reasons.push('Good all-round university matching your preferences');
  }

  return reasons;
}
