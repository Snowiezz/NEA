/**
 * HomeScreen.js
 * The main dashboard screen of the University Picker app.
 *
 * Shows a welcome greeting and quick-action buttons that navigate
 * to the core features of the app.
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { isQuizCompleted } from '../storage/storage';

// ─── Colour constants ─────────────────────────────────────────────────────────
const GREEN = '#25995e';

// ─── Quick-action button configuration ───────────────────────────────────────

const ACTIONS = [
  {
    label: 'Take Preference Quiz',
    description: 'Tell us what matters to you',
    icon: 'clipboard-outline',
    navigateTo: 'Quiz',
    color: GREEN,
  },
  {
    label: 'Recommendations',
    description: 'See your personalised rankings',
    icon: 'star-outline',
    navigateTo: 'Recommendations',
    color: '#1976d2',
  },
  {
    label: 'Compare Universities',
    description: 'Side-by-side comparison table',
    icon: 'git-compare-outline',
    navigateTo: 'Compare',
    color: '#7b1fa2',
  },
  {
    label: 'Saved Universities',
    description: 'Your favourites and notes',
    icon: 'bookmark-outline',
    navigateTo: 'Saved',
    color: '#e65100',
  },
  {
    label: 'Settings',
    description: 'Set your home location and more',
    icon: 'settings-outline',
    navigateTo: 'Settings',
    color: '#546e7a',
  },
];

// ─── Component ────────────────────────────────────────────────────────────────

export default function HomeScreen({ navigation }) {
  const [quizDone, setQuizDone] = useState(false);

  // Check if the user has already completed the preference quiz
  useEffect(() => {
    const checkQuiz = async () => {
      const done = await isQuizCompleted();
      setQuizDone(done);
    };
    // Re-check every time the screen comes into focus
    const unsubscribe = navigation.addListener('focus', checkQuiz);
    return unsubscribe;
  }, [navigation]);

  const handlePress = (action) => {
    if (action.navigateTo === 'Quiz') {
      navigation.navigate('Quiz');
    } else {
      navigation.navigate(action.navigateTo);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* ── Header ── */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>UniPicker</Text>
        <Text style={styles.headerSubtitle}>Find your perfect university</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* ── Banner: quiz reminder ── */}
        {!quizDone && (
          <TouchableOpacity
            style={styles.banner}
            onPress={() => navigation.navigate('Quiz')}
            activeOpacity={0.85}
          >
            <Ionicons name="information-circle-outline" size={22} color="#fff" />
            <Text style={styles.bannerText}>
              Take the preference quiz to get personalised recommendations!
            </Text>
            <Ionicons name="chevron-forward" size={18} color="#fff" />
          </TouchableOpacity>
        )}

        {/* ── Welcome text ── */}
        <View style={styles.welcomeSection}>
          <Text style={styles.welcomeTitle}>Welcome Back 👋</Text>
          <Text style={styles.welcomeBody}>
            Use the options below to explore universities, compare choices, and
            find the right fit for you.
          </Text>
        </View>

        {/* ── Quick-action cards ── */}
        {ACTIONS.map((action) => (
          <TouchableOpacity
            key={action.label}
            style={styles.card}
            onPress={() => handlePress(action)}
            activeOpacity={0.8}
          >
            <View style={[styles.iconBox, { backgroundColor: action.color + '1a' }]}>
              <Ionicons name={action.icon} size={28} color={action.color} />
            </View>
            <View style={styles.cardText}>
              <Text style={styles.cardLabel}>{action.label}</Text>
              <Text style={styles.cardDescription}>{action.description}</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="#ccc" />
          </TouchableOpacity>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#f5f5f5' },
  header: {
    backgroundColor: GREEN,
    paddingTop: 20,
    paddingBottom: 24,
    paddingHorizontal: 20,
  },
  headerTitle: { fontSize: 34, fontWeight: 'bold', color: '#fff' },
  headerSubtitle: { fontSize: 15, color: '#c8e6c9', marginTop: 4 },
  scrollContent: { padding: 16, paddingBottom: 32 },
  banner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1976d2',
    borderRadius: 12,
    padding: 14,
    marginBottom: 16,
    gap: 10,
  },
  bannerText: { flex: 1, color: '#fff', fontSize: 14, fontWeight: '500' },
  welcomeSection: { marginBottom: 20 },
  welcomeTitle: { fontSize: 22, fontWeight: '700', color: '#1a1a1a', marginBottom: 6 },
  welcomeBody: { fontSize: 15, color: '#555', lineHeight: 22 },
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 14,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.07,
    shadowRadius: 4,
    elevation: 2,
    gap: 14,
  },
  iconBox: {
    width: 52,
    height: 52,
    borderRadius: 13,
    justifyContent: 'center',
    alignItems: 'center',
  },
  cardText: { flex: 1 },
  cardLabel: { fontSize: 16, fontWeight: '600', color: '#1a1a1a', marginBottom: 3 },
  cardDescription: { fontSize: 13, color: '#777' },
});
