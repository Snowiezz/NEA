/**
 * UniversityDetailScreen.js
 * Full detail view for a single university.
 *
 * Features:
 *   - All university metrics displayed clearly
 *   - Save / unsave button
 *   - Add / edit personal notes
 *   - Full description and financial support info
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  SafeAreaView,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import {
  loadSavedUniversities,
  saveUniversity,
  removeSavedUniversity,
  loadNotes,
  saveNote,
} from '../storage/storage';

// ─── Constants ────────────────────────────────────────────────────────────────

const GREEN = '#25995e';

// ─── Metric row helper ────────────────────────────────────────────────────────

function MetricRow({ icon, label, value }) {
  return (
    <View style={styles.metricRow}>
      <View style={styles.metricIcon}>
        <Ionicons name={icon} size={20} color={GREEN} />
      </View>
      <Text style={styles.metricLabel}>{label}</Text>
      <Text style={styles.metricValue}>{value}</Text>
    </View>
  );
}

// ─── Star rating display ──────────────────────────────────────────────────────

function StarRating({ rating, max = 5 }) {
  const full  = Math.floor(rating);
  const empty = max - full;
  return (
    <View style={{ flexDirection: 'row', gap: 2 }}>
      {Array.from({ length: full  }).map((_, i) => <Ionicons key={`f${i}`} name="star"         size={16} color="#f59e0b" />)}
      {Array.from({ length: empty }).map((_, i) => <Ionicons key={`e${i}`} name="star-outline" size={16} color="#ccc" />)}
      <Text style={{ fontSize: 14, color: '#555', marginLeft: 4 }}>{rating}/{max}</Text>
    </View>
  );
}

// ─── Component ────────────────────────────────────────────────────────────────

export default function UniversityDetailScreen({ route }) {
  const { university: uni } = route.params;

  const [isSaved,   setIsSaved]   = useState(false);
  const [noteText,  setNoteText]  = useState('');
  const [editMode,  setEditMode]  = useState(false);
  const [draftNote, setDraftNote] = useState('');

  // ── Load saved state and notes on mount ──────────────────────────────────
  useEffect(() => {
    const load = async () => {
      const ids = await loadSavedUniversities();
      setIsSaved(ids.includes(uni.id));
      const notes = await loadNotes();
      setNoteText(notes[uni.id] ?? '');
    };
    load();
  }, [uni.id]);

  // ── Save / unsave ────────────────────────────────────────────────────────
  const toggleSaved = async () => {
    if (isSaved) {
      await removeSavedUniversity(uni.id);
      setIsSaved(false);
      Alert.alert('Removed', `${uni.name} removed from saved.`);
    } else {
      await saveUniversity(uni.id);
      setIsSaved(true);
      Alert.alert('Saved!', `${uni.name} added to your saved list.`);
    }
  };

  // ── Notes ────────────────────────────────────────────────────────────────
  const startEdit = () => {
    setDraftNote(noteText);
    setEditMode(true);
  };

  const saveNoteHandler = async () => {
    await saveNote(uni.id, draftNote);
    setNoteText(draftNote);
    setEditMode(false);
  };

  // ── Render ───────────────────────────────────────────────────────────────

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView contentContainerStyle={styles.scrollContent}>
          {/* University banner */}
          <View style={styles.banner}>
            <Text style={styles.bannerName}>{uni.name}</Text>
            <Text style={styles.bannerLocation}>
              <Ionicons name="location-outline" size={15} color="#c8e6c9" /> {uni.location}
            </Text>
            <View style={styles.bannerRankRow}>
              <View style={styles.rankBadge}>
                <Text style={styles.rankBadgeText}>UK Rank #{uni.ranking}</Text>
              </View>
            </View>
          </View>

          {/* Save button */}
          <TouchableOpacity style={[styles.saveBtn, isSaved && styles.saveBtnActive]} onPress={toggleSaved}>
            <Ionicons name={isSaved ? 'bookmark' : 'bookmark-outline'} size={22} color={isSaved ? '#fff' : GREEN} />
            <Text style={[styles.saveBtnText, isSaved && { color: '#fff' }]}>
              {isSaved ? 'Saved' : 'Save University'}
            </Text>
          </TouchableOpacity>

          {/* Description */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>About</Text>
            <Text style={styles.descriptionText}>{uni.description}</Text>
          </View>

          {/* Key metrics */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Key Metrics</Text>
            <View style={styles.metricsCard}>
              <MetricRow icon="trophy-outline"     label="UK Ranking"           value={`#${uni.ranking}`} />
              <MetricRow icon="school-outline"     label="Course Quality"       value={`${uni.courseQualityRating}/5`} />
              <MetricRow icon="happy-outline"      label="Student Satisfaction" value={`${uni.studentSatisfaction}/5`} />
              <MetricRow icon="moon-outline"       label="Nightlife"            value={`${uni.nightlifeRating}/5`} />
              <MetricRow icon="cash-outline"       label="Cost of Living"       value={`£${uni.costOfLiving}/month`} />
              <MetricRow icon="home-outline"       label="Accommodation"        value={`£${uni.accommodationCost}/week`} />
              <MetricRow icon="document-outline"   label="Entry Requirements"   value={`${uni.entryRequirements} UCAS pts`} />
            </View>
          </View>

          {/* Ratings visualised */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Ratings</Text>
            <View style={styles.metricsCard}>
              <View style={styles.ratingRow}>
                <Text style={styles.ratingLabel}>Course Quality</Text>
                <StarRating rating={uni.courseQualityRating} />
              </View>
              <View style={styles.ratingRow}>
                <Text style={styles.ratingLabel}>Satisfaction</Text>
                <StarRating rating={uni.studentSatisfaction} />
              </View>
              <View style={styles.ratingRow}>
                <Text style={styles.ratingLabel}>Nightlife</Text>
                <StarRating rating={uni.nightlifeRating} />
              </View>
            </View>
          </View>

          {/* Financial support */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Financial Support</Text>
            <View style={styles.infoBox}>
              <Ionicons name="card-outline" size={22} color={GREEN} />
              <Text style={styles.infoText}>{uni.financialSupport}</Text>
            </View>
          </View>

          {/* Personal notes */}
          <View style={styles.section}>
            <View style={styles.notesHeader}>
              <Text style={styles.sectionTitle}>Personal Notes</Text>
              {!editMode && (
                <TouchableOpacity onPress={startEdit}>
                  <Ionicons name="pencil-outline" size={20} color={GREEN} />
                </TouchableOpacity>
              )}
            </View>

            {editMode ? (
              <View>
                <TextInput
                  style={styles.noteInput}
                  multiline
                  value={draftNote}
                  onChangeText={setDraftNote}
                  placeholder="Add your personal notes about this university…"
                  autoFocus
                />
                <View style={styles.noteActions}>
                  <TouchableOpacity style={styles.cancelBtn} onPress={() => setEditMode(false)}>
                    <Text style={styles.cancelBtnText}>Cancel</Text>
                  </TouchableOpacity>
                  <TouchableOpacity style={styles.saveNoteBtn} onPress={saveNoteHandler}>
                    <Text style={styles.saveNoteBtnText}>Save Note</Text>
                  </TouchableOpacity>
                </View>
              </View>
            ) : (
              <TouchableOpacity style={styles.noteDisplayBox} onPress={startEdit}>
                <Text style={[styles.noteDisplayText, !noteText && styles.notePlaceholder]}>
                  {noteText || 'Tap to add personal notes…'}
                </Text>
              </TouchableOpacity>
            )}
          </View>

          <View style={{ height: 32 }} />
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#f5f5f5' },
  scrollContent: { paddingBottom: 40 },
  banner: {
    backgroundColor: GREEN,
    padding: 24,
    paddingTop: 28,
  },
  bannerName: { fontSize: 26, fontWeight: 'bold', color: '#fff', marginBottom: 6 },
  bannerLocation: { fontSize: 15, color: '#c8e6c9', marginBottom: 12 },
  bannerRankRow: { flexDirection: 'row' },
  rankBadge: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 20,
    paddingVertical: 4,
    paddingHorizontal: 14,
  },
  rankBadgeText: { fontSize: 14, fontWeight: '700', color: '#fff' },
  saveBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    margin: 16,
    padding: 14,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: GREEN,
    backgroundColor: '#fff',
  },
  saveBtnActive: { backgroundColor: GREEN },
  saveBtnText: { fontSize: 16, fontWeight: '700', color: GREEN },
  section: { paddingHorizontal: 16, marginBottom: 20 },
  sectionTitle: { fontSize: 18, fontWeight: '700', color: '#1a1a1a', marginBottom: 10 },
  descriptionText: { fontSize: 15, color: '#444', lineHeight: 23 },
  metricsCard: {
    backgroundColor: '#fff',
    borderRadius: 14,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 3,
    elevation: 1,
  },
  metricRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderBottomWidth: 1,
    borderColor: '#f0f0f0',
    gap: 12,
  },
  metricIcon: {
    width: 36,
    height: 36,
    borderRadius: 10,
    backgroundColor: '#e8f5e9',
    justifyContent: 'center',
    alignItems: 'center',
  },
  metricLabel: { flex: 1, fontSize: 15, color: '#444' },
  metricValue: { fontSize: 15, fontWeight: '700', color: '#1a1a1a' },
  ratingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 14,
    borderBottomWidth: 1,
    borderColor: '#f0f0f0',
  },
  ratingLabel: { fontSize: 15, color: '#444' },
  infoBox: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
  },
  infoText: { fontSize: 15, color: '#444', flex: 1, lineHeight: 22 },
  notesHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  noteInput: {
    backgroundColor: '#fff',
    borderRadius: 12,
    borderWidth: 2,
    borderColor: GREEN,
    padding: 14,
    fontSize: 15,
    color: '#1a1a1a',
    minHeight: 120,
    textAlignVertical: 'top',
  },
  noteActions: { flexDirection: 'row', justifyContent: 'flex-end', gap: 10, marginTop: 10 },
  cancelBtn: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 10,
    backgroundColor: '#f0f0f0',
  },
  cancelBtnText: { fontSize: 15, color: '#555', fontWeight: '600' },
  saveNoteBtn: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 10,
    backgroundColor: GREEN,
  },
  saveNoteBtnText: { fontSize: 15, color: '#fff', fontWeight: '600' },
  noteDisplayBox: {
    backgroundColor: '#fff',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    padding: 14,
    minHeight: 80,
  },
  noteDisplayText: { fontSize: 15, color: '#1a1a1a', lineHeight: 22 },
  notePlaceholder: { color: '#bbb', fontStyle: 'italic' },
});
