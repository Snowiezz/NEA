/**
 * RecommendationsScreen.js
 * Displays a ranked list of universities based on the user's saved preferences.
 *
 * Uses rankUniversities() from the recommendation engine to compute scores,
 * then renders each university as a card showing:
 *   - rank position
 *   - match score (0–100)
 *   - key reasons it was recommended
 *   - distance from home
 */

import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  SafeAreaView,
  ActivityIndicator,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { loadPreferences } from '../storage/storage';
import { rankUniversities } from '../logic/recommendationEngine';

const GREEN = '#25995e';

function scoreColor(score) {
  if (score >= 75) return '#25995e';
  if (score >= 55) return '#f59e0b';
  return '#ef4444';
}

export default function RecommendationsScreen({ navigation }) {
  const [ranked, setRanked] = useState([]);
  const [loading, setLoading] = useState(true);
  const [hasPreferences, setHasPreferences] = useState(true);

  useFocusEffect(
    useCallback(() => {
      const load = async () => {
        setLoading(true);
        const prefs = await loadPreferences();
        if (!prefs) {
          setHasPreferences(false);
          setLoading(false);
          return;
        }
        setHasPreferences(true);
        setRanked(rankUniversities(prefs));
        setLoading(false);
      };
      load();
    }, [])
  );

  if (loading) {
    return (
      <SafeAreaView style={styles.centred}>
        <ActivityIndicator size="large" color={GREEN} />
      </SafeAreaView>
    );
  }

  if (!hasPreferences) {
    return (
      <SafeAreaView style={styles.centred}>
        <Ionicons name="clipboard-outline" size={60} color="#ccc" />
        <Text style={styles.emptyTitle}>No preferences yet</Text>
        <Text style={styles.emptyBody}>
          Take the preference quiz so we can calculate your personalised rankings.
        </Text>
        <TouchableOpacity style={styles.quizBtn} onPress={() => navigation.navigate('Quiz')}>
          <Text style={styles.quizBtnText}>Take Quiz</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  const renderItem = ({ item, index }) => {
    const { university: uni, score, reasons, distance } = item;
    const color = scoreColor(score);
    return (
      <TouchableOpacity
        style={styles.card}
        onPress={() => navigation.navigate('UniversityDetail', { university: uni })}
        activeOpacity={0.85}
      >
        <View style={[styles.rankBadge, index < 3 && styles.rankBadgeTop]}>
          <Text style={styles.rankText}>#{index + 1}</Text>
        </View>
        <View style={styles.cardBody}>
          <Text style={styles.uniName}>{uni.name}</Text>
          <Text style={styles.uniLocation}>
            <Ionicons name="location-outline" size={13} color="#888" /> {uni.location}
          </Text>
          <View style={styles.scoreRow}>
            <Text style={[styles.scoreLabel, { color }]}>Match: {score}%</Text>
            <View style={styles.scoreBarBg}>
              <View style={[styles.scoreBarFill, { width: `${score}%`, backgroundColor: color }]} />
            </View>
          </View>
          <Text style={styles.distanceText}>~{distance} km from home</Text>
          <View style={styles.reasonsBox}>
            {reasons.slice(0, 3).map((reason, i) => (
              <View key={i} style={styles.reasonRow}>
                <Ionicons name="checkmark-circle" size={15} color={GREEN} />
                <Text style={styles.reasonText}>{reason}</Text>
              </View>
            ))}
          </View>
        </View>
        <Ionicons name="chevron-forward" size={20} color="#ccc" />
      </TouchableOpacity>
    );
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Recommendations</Text>
        <Text style={styles.headerSub}>Ranked by match to your preferences</Text>
      </View>
      <FlatList
        data={ranked}
        keyExtractor={(item) => String(item.university.id)}
        renderItem={renderItem}
        contentContainerStyle={styles.listContent}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#f5f5f5' },
  centred: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 32 },
  header: { backgroundColor: GREEN, paddingTop: 16, paddingBottom: 20, paddingHorizontal: 20 },
  headerTitle: { fontSize: 26, fontWeight: 'bold', color: '#fff' },
  headerSub: { fontSize: 14, color: '#c8e6c9', marginTop: 4 },
  listContent: { padding: 16, paddingBottom: 32 },
  card: {
    flexDirection: 'row', alignItems: 'flex-start', backgroundColor: '#fff',
    borderRadius: 14, padding: 16, marginBottom: 12,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.07, shadowRadius: 4, elevation: 2, gap: 12,
  },
  rankBadge: { width: 40, height: 40, borderRadius: 20, backgroundColor: '#f0f0f0', justifyContent: 'center', alignItems: 'center', marginTop: 2 },
  rankBadgeTop: { backgroundColor: '#fff9c4' },
  rankText: { fontSize: 14, fontWeight: 'bold', color: '#333' },
  cardBody: { flex: 1 },
  uniName: { fontSize: 17, fontWeight: '700', color: '#1a1a1a', marginBottom: 3 },
  uniLocation: { fontSize: 13, color: '#888', marginBottom: 10 },
  scoreRow: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 4 },
  scoreLabel: { fontSize: 13, fontWeight: '700', width: 80 },
  scoreBarBg: { flex: 1, height: 8, backgroundColor: '#f0f0f0', borderRadius: 4, overflow: 'hidden' },
  scoreBarFill: { height: 8, borderRadius: 4 },
  distanceText: { fontSize: 12, color: '#999', marginBottom: 10 },
  reasonsBox: { gap: 5 },
  reasonRow: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  reasonText: { fontSize: 13, color: '#444', flex: 1 },
  emptyTitle: { fontSize: 20, fontWeight: '700', color: '#333', marginTop: 16, marginBottom: 8 },
  emptyBody: { fontSize: 15, color: '#777', textAlign: 'center', lineHeight: 22, marginBottom: 24 },
  quizBtn: { backgroundColor: GREEN, paddingVertical: 14, paddingHorizontal: 32, borderRadius: 12 },
  quizBtnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
});
