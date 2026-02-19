/**
 * SettingsScreen.js
 * App settings and user preferences management.
 *
 * Features:
 *   - Display current preference summary
 *   - Retake the preference quiz
 *   - Clear all saved data (reset)
 *   - About section
 */

import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  Alert,
  Switch,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { loadPreferences, clearAllData } from '../storage/storage';

// ─── Constants ────────────────────────────────────────────────────────────────

const GREEN = '#25995e';

// ─── Component ────────────────────────────────────────────────────────────────

export default function SettingsScreen({ navigation }) {
  const [preferences, setPreferences] = useState(null);

  useFocusEffect(
    useCallback(() => {
      const load = async () => {
        const prefs = await loadPreferences();
        setPreferences(prefs);
      };
      load();
    }, [])
  );

  const handleRetakeQuiz = () => {
    navigation.navigate('Quiz');
  };

  const handleClearData = () => {
    Alert.alert(
      'Reset All Data',
      'This will delete all your preferences, saved universities, and notes. This cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          style: 'destructive',
          onPress: async () => {
            await clearAllData();
            setPreferences(null);
            Alert.alert('Done', 'All data has been cleared.');
          },
        },
      ]
    );
  };

  // ── Importance label helper ──────────────────────────────────────────────

  const importanceLabel = (value) => {
    const labels = { 1: 'Not important', 2: 'Slightly', 3: 'Moderate', 4: 'Important', 5: 'Very important' };
    return labels[value] ?? String(value);
  };

  // ── Render ───────────────────────────────────────────────────────────────

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Settings</Text>
        <Text style={styles.headerSub}>Manage your preferences</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>

        {/* ── Current Preferences ── */}
        <Text style={styles.groupLabel}>YOUR PREFERENCES</Text>
        <View style={styles.card}>
          {preferences ? (
            <>
              <PrefRow label="Home City"            value={preferences.homeCity ?? 'Not set'} />
              <PrefRow label="Max Distance"         value={`${preferences.maxDistanceKm} km`} />
              <PrefRow label="Max Monthly Cost"     value={`£${preferences.maxCostOfLiving}`} />
              <PrefRow label="Ranking Importance"   value={importanceLabel(preferences.importanceRanking)} />
              <PrefRow label="Course Quality"       value={importanceLabel(preferences.importanceCourseQuality)} />
              <PrefRow label="Satisfaction"         value={importanceLabel(preferences.importanceSatisfaction)} />
              <PrefRow label="Cost of Living"       value={importanceLabel(preferences.importanceCost)} />
              <PrefRow label="Nightlife"            value={importanceLabel(preferences.importanceNightlife)} />
            </>
          ) : (
            <View style={styles.noPrefBox}>
              <Ionicons name="clipboard-outline" size={30} color="#ccc" />
              <Text style={styles.noPrefText}>No preferences saved yet.</Text>
            </View>
          )}
        </View>

        {/* ── Actions ── */}
        <Text style={styles.groupLabel}>ACTIONS</Text>
        <View style={styles.card}>
          <SettingsButton
            icon="refresh-outline"
            label="Retake Preference Quiz"
            description="Update your priorities and get new recommendations"
            color={GREEN}
            onPress={handleRetakeQuiz}
          />
        </View>

        {/* ── Danger zone ── */}
        <Text style={styles.groupLabel}>DANGER ZONE</Text>
        <View style={styles.card}>
          <SettingsButton
            icon="trash-outline"
            label="Reset All Data"
            description="Delete all preferences, saved universities, and notes"
            color="#ef4444"
            onPress={handleClearData}
          />
        </View>

        {/* ── About ── */}
        <Text style={styles.groupLabel}>ABOUT</Text>
        <View style={styles.card}>
          <View style={styles.aboutRow}>
            <Text style={styles.aboutLabel}>App Version</Text>
            <Text style={styles.aboutValue}>1.0.0</Text>
          </View>
          <View style={styles.aboutRow}>
            <Text style={styles.aboutLabel}>Built with</Text>
            <Text style={styles.aboutValue}>React Native + Expo</Text>
          </View>
          <View style={styles.aboutRow}>
            <Text style={styles.aboutLabel}>Purpose</Text>
            <Text style={styles.aboutValue}>A-Level CS NEA Project</Text>
          </View>
        </View>

        <View style={{ height: 32 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function PrefRow({ label, value }) {
  return (
    <View style={styles.prefRow}>
      <Text style={styles.prefLabel}>{label}</Text>
      <Text style={styles.prefValue}>{value}</Text>
    </View>
  );
}

function SettingsButton({ icon, label, description, color, onPress }) {
  return (
    <TouchableOpacity style={styles.settingsBtn} onPress={onPress} activeOpacity={0.8}>
      <View style={[styles.settingsBtnIcon, { backgroundColor: color + '1a' }]}>
        <Ionicons name={icon} size={22} color={color} />
      </View>
      <View style={styles.settingsBtnText}>
        <Text style={[styles.settingsBtnLabel, { color }]}>{label}</Text>
        <Text style={styles.settingsBtnDesc}>{description}</Text>
      </View>
      <Ionicons name="chevron-forward" size={18} color="#ccc" />
    </TouchableOpacity>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#f5f5f5' },
  header: {
    backgroundColor: GREEN,
    paddingTop: 16,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  headerTitle: { fontSize: 26, fontWeight: 'bold', color: '#fff' },
  headerSub: { fontSize: 14, color: '#c8e6c9', marginTop: 4 },
  scrollContent: { padding: 16 },
  groupLabel: {
    fontSize: 12,
    fontWeight: '700',
    color: '#888',
    letterSpacing: 0.8,
    marginBottom: 8,
    marginTop: 16,
    marginLeft: 4,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 14,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 3,
    elevation: 1,
  },
  // Preference rows
  prefRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 14,
    borderBottomWidth: 1,
    borderColor: '#f0f0f0',
  },
  prefLabel: { fontSize: 15, color: '#444' },
  prefValue: { fontSize: 15, fontWeight: '600', color: '#1a1a1a' },
  noPrefBox: {
    padding: 24,
    alignItems: 'center',
    gap: 8,
  },
  noPrefText: { fontSize: 15, color: '#aaa' },
  // Settings buttons
  settingsBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    gap: 14,
    borderBottomWidth: 1,
    borderColor: '#f0f0f0',
  },
  settingsBtnIcon: {
    width: 44,
    height: 44,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  settingsBtnText: { flex: 1 },
  settingsBtnLabel: { fontSize: 15, fontWeight: '600' },
  settingsBtnDesc: { fontSize: 13, color: '#888', marginTop: 2 },
  // About
  aboutRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 14,
    borderBottomWidth: 1,
    borderColor: '#f0f0f0',
  },
  aboutLabel: { fontSize: 15, color: '#555' },
  aboutValue: { fontSize: 15, color: '#888' },
});
