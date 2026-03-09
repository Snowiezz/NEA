/**
 * SavedScreen.js
 * Displays universities the user has bookmarked/saved.
 *
 * Features:
 *   - List of saved universities
 *   - Remove from saved list
 *   - View personal notes per university
 *   - Navigate to university detail
 */

import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  SafeAreaView,
  Alert,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import UNIVERSITIES from '../data/universities';
import { loadSavedUniversities, removeSavedUniversity, loadNotes } from '../storage/storage';

const GREEN = '#25995e';

export default function SavedScreen({ navigation }) {
  const [savedUnis, setSavedUnis] = useState([]);
  const [notes, setNotes] = useState({});

  useFocusEffect(
    useCallback(() => {
      const load = async () => {
        const ids = await loadSavedUniversities();
        setSavedUnis(UNIVERSITIES.filter((u) => ids.includes(u.id)));
        setNotes(await loadNotes());
      };
      load();
    }, [])
  );

  const handleRemove = (uni) => {
    Alert.alert('Remove from Saved', `Remove ${uni.name} from your saved list?`, [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Remove', style: 'destructive',
        onPress: async () => {
          await removeSavedUniversity(uni.id);
          setSavedUnis((prev) => prev.filter((u) => u.id !== uni.id));
        },
      },
    ]);
  };

  const renderItem = ({ item }) => {
    const noteText = notes[item.id];
    return (
      <TouchableOpacity
        style={styles.card}
        onPress={() => navigation.navigate('UniversityDetail', { university: item })}
        activeOpacity={0.85}
      >
        <View style={styles.cardBody}>
          <Text style={styles.uniName}>{item.name}</Text>
          <Text style={styles.uniLocation}>
            <Ionicons name="location-outline" size={13} color="#888" /> {item.location}
          </Text>
          <View style={styles.statsRow}>
            <View style={styles.stat}>
              <Ionicons name="trophy-outline" size={14} color={GREEN} />
              <Text style={styles.statText}>Rank #{item.ranking}</Text>
            </View>
            <View style={styles.stat}>
              <Ionicons name="star-outline" size={14} color={GREEN} />
              <Text style={styles.statText}>{item.courseQualityRating}/5 quality</Text>
            </View>
            <View style={styles.stat}>
              <Ionicons name="cash-outline" size={14} color={GREEN} />
              <Text style={styles.statText}>£{item.costOfLiving}/mo</Text>
            </View>
          </View>
          {noteText ? (
            <View style={styles.noteBox}>
              <Ionicons name="document-text-outline" size={14} color="#888" />
              <Text style={styles.noteText} numberOfLines={2}>{noteText}</Text>
            </View>
          ) : null}
        </View>
        <TouchableOpacity style={styles.removeBtn} onPress={() => handleRemove(item)} hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}>
          <Ionicons name="bookmark" size={22} color={GREEN} />
        </TouchableOpacity>
      </TouchableOpacity>
    );
  };

  if (savedUnis.length === 0) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Saved Universities</Text>
          <Text style={styles.headerSub}>Your bookmarked universities</Text>
        </View>
        <View style={styles.empty}>
          <Ionicons name="bookmark-outline" size={60} color="#ccc" />
          <Text style={styles.emptyTitle}>No saved universities</Text>
          <Text style={styles.emptyBody}>Open any university from the Recommendations screen and tap Save.</Text>
          <TouchableOpacity style={styles.exploreBtn} onPress={() => navigation.navigate('Recommendations')}>
            <Text style={styles.exploreBtnText}>View Recommendations</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Saved Universities</Text>
        <Text style={styles.headerSub}>{savedUnis.length} saved</Text>
      </View>
      <FlatList
        data={savedUnis}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderItem}
        contentContainerStyle={styles.listContent}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { backgroundColor: GREEN, paddingTop: 16, paddingBottom: 20, paddingHorizontal: 20 },
  headerTitle: { fontSize: 26, fontWeight: 'bold', color: '#fff' },
  headerSub: { fontSize: 14, color: '#c8e6c9', marginTop: 4 },
  listContent: { padding: 16, paddingBottom: 32 },
  card: {
    flexDirection: 'row', alignItems: 'flex-start', backgroundColor: '#fff',
    borderRadius: 14, padding: 16, marginBottom: 12,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.07, shadowRadius: 4, elevation: 2, gap: 12,
  },
  cardBody: { flex: 1 },
  uniName: { fontSize: 17, fontWeight: '700', color: '#1a1a1a', marginBottom: 3 },
  uniLocation: { fontSize: 13, color: '#888', marginBottom: 10 },
  statsRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginBottom: 8 },
  stat: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  statText: { fontSize: 13, color: '#444' },
  noteBox: { flexDirection: 'row', alignItems: 'flex-start', gap: 6, backgroundColor: '#f9f9f9', borderRadius: 8, padding: 8, marginTop: 4 },
  noteText: { fontSize: 13, color: '#666', flex: 1, fontStyle: 'italic' },
  removeBtn: { padding: 4, marginTop: 2 },
  empty: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 32 },
  emptyTitle: { fontSize: 20, fontWeight: '700', color: '#333', marginTop: 16, marginBottom: 8 },
  emptyBody: { fontSize: 15, color: '#777', textAlign: 'center', lineHeight: 22, marginBottom: 24 },
  exploreBtn: { backgroundColor: GREEN, paddingVertical: 14, paddingHorizontal: 32, borderRadius: 12 },
  exploreBtnText: { color: '#fff', fontSize: 16, fontWeight: '700' },
});
