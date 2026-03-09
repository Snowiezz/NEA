/**
 * storage.js
 * Persistent storage abstraction layer using AsyncStorage.
 *
 * All data persistence goes through this module so that the underlying
 * storage mechanism can be swapped out easily (e.g. from AsyncStorage
 * to SQLite) without changing the rest of the app.
 */

import AsyncStorage from '@react-native-async-storage/async-storage';

// ─── Storage Keys ────────────────────────────────────────────────────────────

const KEYS = {
  USER_PREFERENCES: '@unipicker_preferences',
  SAVED_UNIVERSITIES: '@unipicker_saved',
  UNIVERSITY_NOTES: '@unipicker_notes',
  QUIZ_COMPLETED: '@unipicker_quiz_completed',
  SETTINGS: '@unipicker_settings',
};

// ─── Preferences ─────────────────────────────────────────────────────────────

/**
 * Saves the user's quiz preference answers to storage.
 * @param {Object} preferences - key/value map of preference answers
 */
export async function savePreferences(preferences) {
  try {
    await AsyncStorage.setItem(KEYS.USER_PREFERENCES, JSON.stringify(preferences));
  } catch (error) {
    console.error('Error saving preferences:', error);
  }
}

/**
 * Loads the user's saved preferences.
 * @returns {Object|null} preferences object, or null if not yet set
 */
export async function loadPreferences() {
  try {
    const data = await AsyncStorage.getItem(KEYS.USER_PREFERENCES);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    console.error('Error loading preferences:', error);
    return null;
  }
}

// ─── Saved Universities ───────────────────────────────────────────────────────

/**
 * Returns the array of saved university IDs.
 * @returns {number[]} array of university IDs
 */
export async function loadSavedUniversities() {
  try {
    const data = await AsyncStorage.getItem(KEYS.SAVED_UNIVERSITIES);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error('Error loading saved universities:', error);
    return [];
  }
}

/**
 * Saves a university by ID to the saved list (if not already saved).
 * @param {number} universityId
 * @returns {boolean} true if added, false if already existed
 */
export async function saveUniversity(universityId) {
  try {
    const current = await loadSavedUniversities();
    if (current.includes(universityId)) return false;
    const updated = [...current, universityId];
    await AsyncStorage.setItem(KEYS.SAVED_UNIVERSITIES, JSON.stringify(updated));
    return true;
  } catch (error) {
    console.error('Error saving university:', error);
    return false;
  }
}

/**
 * Removes a university from the saved list by ID.
 * @param {number} universityId
 */
export async function removeSavedUniversity(universityId) {
  try {
    const current = await loadSavedUniversities();
    const updated = current.filter((id) => id !== universityId);
    await AsyncStorage.setItem(KEYS.SAVED_UNIVERSITIES, JSON.stringify(updated));
  } catch (error) {
    console.error('Error removing saved university:', error);
  }
}

// ─── Personal Notes ───────────────────────────────────────────────────────────

/**
 * Loads all personal notes (university ID → note text).
 * @returns {Object} notes map
 */
export async function loadNotes() {
  try {
    const data = await AsyncStorage.getItem(KEYS.UNIVERSITY_NOTES);
    return data ? JSON.parse(data) : {};
  } catch (error) {
    console.error('Error loading notes:', error);
    return {};
  }
}

/**
 * Saves a note for a specific university.
 * @param {number} universityId
 * @param {string} noteText
 */
export async function saveNote(universityId, noteText) {
  try {
    const current = await loadNotes();
    const updated = { ...current, [universityId]: noteText };
    await AsyncStorage.setItem(KEYS.UNIVERSITY_NOTES, JSON.stringify(updated));
  } catch (error) {
    console.error('Error saving note:', error);
  }
}

// ─── Quiz Completion Flag ─────────────────────────────────────────────────────

/**
 * Marks the quiz as completed so the app can skip straight to main flow.
 */
export async function setQuizCompleted() {
  try {
    await AsyncStorage.setItem(KEYS.QUIZ_COMPLETED, 'true');
  } catch (error) {
    console.error('Error setting quiz completed:', error);
  }
}

/**
 * Returns whether the user has completed the quiz.
 * @returns {boolean}
 */
export async function isQuizCompleted() {
  try {
    const value = await AsyncStorage.getItem(KEYS.QUIZ_COMPLETED);
    return value === 'true';
  } catch (error) {
    return false;
  }
}

// ─── Settings ─────────────────────────────────────────────────────────────────

/**
 * Saves app settings (home city, notifications, etc.)
 * @param {Object} settings
 */
export async function saveSettings(settings) {
  try {
    await AsyncStorage.setItem(KEYS.SETTINGS, JSON.stringify(settings));
  } catch (error) {
    console.error('Error saving settings:', error);
  }
}

/**
 * Loads app settings.
 * @returns {Object|null}
 */
export async function loadSettings() {
  try {
    const data = await AsyncStorage.getItem(KEYS.SETTINGS);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    return null;
  }
}

/**
 * Clears ALL stored data (used from the Settings screen).
 */
export async function clearAllData() {
  try {
    await AsyncStorage.multiRemove(Object.values(KEYS));
  } catch (error) {
    console.error('Error clearing data:', error);
  }
}
