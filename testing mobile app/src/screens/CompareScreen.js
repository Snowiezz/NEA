/**
 * CompareScreen.js
 * Side-by-side university comparison table.
 *
 * The user selects 2–3 universities from a picker modal,
 * then a scrollable table shows all key metrics in columns.
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  SafeAreaView,
  Modal,
  FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import UNIVERSITIES from '../data/universities';

const GREEN = '#25995e';
const MAX_COMPARE = 3;

const ROWS = [
  { label: 'Location',             key: 'location',            format: (v) => v },
  { label: 'UK Ranking',           key: 'ranking',             format: (v) => `#${v}` },
  { label: 'Course Quality',       key: 'courseQualityRating', format: (v) => `${v}/5 ⭐` },
  { label: 'Student Satisfaction', key: 'studentSatisfaction', format: (v) => `${v}/5 ⭐` },
  { label: 'Nightlife',            key: 'nightlifeRating',     format: (v) => `${v}/5 🎉` },
  { label: 'Cost of Living',       key: 'costOfLiving',        format: (v) => `£${v}/mo` },
  { label: 'Accommodation',        key: 'accommodationCost',   format: (v) => `£${v}/wk` },
  { label: 'Entry Requirements',   key: 'entryRequirements',   format: (v) => `${v} UCAS pts` },
  { label: 'Financial Support',    key: 'financialSupport',    format: (v) => v },
];

export default function CompareScreen({ navigation }) {
  const [selected, setSelected] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);

  const addUniversity = (uni) => {
    if (selected.find((u) => u.id === uni.id)) return;
    if (selected.length >= MAX_COMPARE) return;
    setSelected((prev) => [...prev, uni]);
    setModalVisible(false);
  };

  const removeUniversity = (id) => setSelected((prev) => prev.filter((u) => u.id !== id));

  const colWidth = selected.length === 2 ? 140 : 120;

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Compare Universities</Text>
        <Text style={styles.headerSub}>Select up to {MAX_COMPARE} universities</Text>
      </View>

      {/* Selected university chips */}
      <View style={styles.chipsRow}>
        {selected.map((uni) => (
          <View key={uni.id} style={styles.chip}>
            <Text style={styles.chipText} numberOfLines={1}>{uni.name}</Text>
            <TouchableOpacity onPress={() => removeUniversity(uni.id)}>
              <Ionicons name="close-circle" size={18} color="#555" />
            </TouchableOpacity>
          </View>
        ))}
        {selected.length < MAX_COMPARE && (
          <TouchableOpacity style={styles.addChip} onPress={() => setModalVisible(true)}>
            <Ionicons name="add-circle-outline" size={18} color={GREEN} />
            <Text style={styles.addChipText}>Add</Text>
          </TouchableOpacity>
        )}
      </View>

      {selected.length < 2 ? (
        <View style={styles.placeholder}>
          <Ionicons name="git-compare-outline" size={60} color="#ccc" />
          <Text style={styles.placeholderTitle}>Select at least 2 universities</Text>
          <Text style={styles.placeholderBody}>Tap the Add button above to choose universities to compare.</Text>
        </View>
      ) : (
        <ScrollView style={styles.tableScroll}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            <View>
              <View style={styles.tableRow}>
                <View style={styles.rowLabelCell}><Text style={styles.rowLabelHeader}>Criteria</Text></View>
                {selected.map((uni) => (
                  <TouchableOpacity
                    key={uni.id}
                    style={[styles.cell, styles.headerCell, { width: colWidth }]}
                    onPress={() => navigation.navigate('UniversityDetail', { university: uni })}
                  >
                    <Text style={styles.headerCellText} numberOfLines={2}>{uni.name}</Text>
                    <Ionicons name="open-outline" size={13} color="#c8e6c9" />
                  </TouchableOpacity>
                ))}
              </View>
              {ROWS.map((row, rowIndex) => (
                <View key={row.key} style={[styles.tableRow, rowIndex % 2 === 0 && styles.tableRowAlt]}>
                  <View style={styles.rowLabelCell}><Text style={styles.rowLabel}>{row.label}</Text></View>
                  {selected.map((uni) => (
                    <View key={uni.id} style={[styles.cell, { width: colWidth }]}>
                      <Text style={styles.cellText}>{row.format(uni[row.key])}</Text>
                    </View>
                  ))}
                </View>
              ))}
            </View>
          </ScrollView>
        </ScrollView>
      )}

      <Modal visible={modalVisible} animationType="slide" presentationStyle="pageSheet" onRequestClose={() => setModalVisible(false)}>
        <SafeAreaView style={styles.modalSafe}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Select a University</Text>
            <TouchableOpacity onPress={() => setModalVisible(false)}>
              <Ionicons name="close" size={26} color="#333" />
            </TouchableOpacity>
          </View>
          <FlatList
            data={UNIVERSITIES}
            keyExtractor={(item) => String(item.id)}
            renderItem={({ item }) => {
              const alreadyAdded = !!selected.find((u) => u.id === item.id);
              return (
                <TouchableOpacity
                  style={[styles.modalItem, alreadyAdded && styles.modalItemDisabled]}
                  onPress={() => addUniversity(item)}
                  disabled={alreadyAdded}
                >
                  <View style={{ flex: 1 }}>
                    <Text style={styles.modalItemName}>{item.name}</Text>
                    <Text style={styles.modalItemLocation}>{item.location}</Text>
                  </View>
                  {alreadyAdded
                    ? <Ionicons name="checkmark-circle" size={22} color={GREEN} />
                    : <Ionicons name="add-circle-outline" size={22} color={GREEN} />
                  }
                </TouchableOpacity>
              );
            }}
          />
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { backgroundColor: GREEN, paddingTop: 16, paddingBottom: 20, paddingHorizontal: 20 },
  headerTitle: { fontSize: 26, fontWeight: 'bold', color: '#fff' },
  headerSub: { fontSize: 14, color: '#c8e6c9', marginTop: 4 },
  chipsRow: { flexDirection: 'row', flexWrap: 'wrap', padding: 12, gap: 8, backgroundColor: '#fff', borderBottomWidth: 1, borderColor: '#eee' },
  chip: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#e8f5e9', borderRadius: 20, paddingVertical: 6, paddingHorizontal: 12, gap: 6, maxWidth: 180 },
  chipText: { fontSize: 13, color: '#1a1a1a', flex: 1 },
  addChip: { flexDirection: 'row', alignItems: 'center', borderWidth: 2, borderColor: GREEN, borderStyle: 'dashed', borderRadius: 20, paddingVertical: 6, paddingHorizontal: 12, gap: 4 },
  addChipText: { fontSize: 13, color: GREEN, fontWeight: '600' },
  placeholder: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 32 },
  placeholderTitle: { fontSize: 20, fontWeight: '700', color: '#333', marginTop: 16, marginBottom: 8 },
  placeholderBody: { fontSize: 15, color: '#777', textAlign: 'center', lineHeight: 22 },
  tableScroll: { flex: 1 },
  tableRow: { flexDirection: 'row', borderBottomWidth: 1, borderColor: '#e0e0e0' },
  tableRowAlt: { backgroundColor: '#fafafa' },
  rowLabelCell: { width: 120, padding: 12, justifyContent: 'center', borderRightWidth: 1, borderColor: '#e0e0e0', backgroundColor: '#f5f5f5' },
  rowLabelHeader: { fontSize: 13, fontWeight: '700', color: '#555' },
  rowLabel: { fontSize: 13, color: '#444', fontWeight: '500' },
  cell: { padding: 12, justifyContent: 'center', alignItems: 'center', borderRightWidth: 1, borderColor: '#e0e0e0' },
  headerCell: { backgroundColor: GREEN, alignItems: 'center', gap: 4 },
  headerCellText: { fontSize: 13, fontWeight: '700', color: '#fff', textAlign: 'center' },
  cellText: { fontSize: 13, color: '#333', textAlign: 'center' },
  modalSafe: { flex: 1, backgroundColor: '#fff' },
  modalHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 20, borderBottomWidth: 1, borderColor: '#eee' },
  modalTitle: { fontSize: 20, fontWeight: '700', color: '#1a1a1a' },
  modalItem: { flexDirection: 'row', alignItems: 'center', padding: 16, borderBottomWidth: 1, borderColor: '#f0f0f0', gap: 12 },
  modalItemDisabled: { opacity: 0.5 },
  modalItemName: { fontSize: 15, fontWeight: '600', color: '#1a1a1a' },
  modalItemLocation: { fontSize: 13, color: '#888', marginTop: 2 },
});
