/**
 * QuizScreen.js
 * Multi-step preference quiz that collects user priorities.
 *
 * Each question has a type:
 *   'slider'  – importance rating 1–5
 *   'number'  – numeric input (distance, cost)
 *   'choice'  – multiple-choice single answer
 *
 * On completion the answers are saved to AsyncStorage and the quiz
 * completion flag is set so the banner on HomeScreen disappears.
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  TextInput,
  SafeAreaView,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { savePreferences, setQuizCompleted } from '../storage/storage';

// ─── Constants ────────────────────────────────────────────────────────────────

const GREEN = '#25995e';
const LIGHT_GREEN = '#e8f5e9';

// ─── Quiz Questions ───────────────────────────────────────────────────────────

const QUESTIONS = [
  {
    id: 'importanceRanking',
    type: 'slider',
    title: 'How important is university ranking to you?',
    subtitle: '1 = Not important  ·  5 = Extremely important',
  },
  {
    id: 'importanceCourseQuality',
    type: 'slider',
    title: 'How important is course / teaching quality?',
    subtitle: '1 = Not important  ·  5 = Extremely important',
  },
  {
    id: 'importanceSatisfaction',
    type: 'slider',
    title: 'How important is overall student satisfaction?',
    subtitle: '1 = Not important  ·  5 = Extremely important',
  },
  {
    id: 'importanceCost',
    type: 'slider',
    title: 'How important is a low cost of living?',
    subtitle: '1 = Not important  ·  5 = Extremely important',
  },
  {
    id: 'importanceNightlife',
    type: 'slider',
    title: 'How important is nightlife and social scene?',
    subtitle: '1 = Not important  ·  5 = Extremely important',
  },
  {
    id: 'maxDistanceKm',
    type: 'number',
    title: 'What is the maximum distance from home you are willing to travel?',
    subtitle: 'Enter a distance in kilometres (e.g. 300)',
    placeholder: '300',
    unit: 'km',
  },
  {
    id: 'maxCostOfLiving',
    type: 'number',
    title: 'What is your maximum acceptable monthly cost of living?',
    subtitle: 'Enter a monthly budget in GBP (e.g. 700)',
    placeholder: '700',
    unit: '£ / month',
  },
  {
    id: 'homeCity',
    type: 'choice',
    title: 'Which region are you travelling from?',
    subtitle: 'Used to estimate distances to universities',
    options: [
      { label: 'London',          lat: 51.5074,  lon: -0.1278  },
      { label: 'Birmingham',      lat: 52.4862,  lon: -1.8904  },
      { label: 'Manchester',      lat: 53.4808,  lon: -2.2426  },
      { label: 'Leeds',           lat: 53.8008,  lon: -1.5491  },
      { label: 'Glasgow',         lat: 55.8642,  lon: -4.2518  },
      { label: 'Edinburgh',       lat: 55.9533,  lon: -3.1883  },
      { label: 'Bristol',         lat: 51.4545,  lon: -2.5879  },
      { label: 'Somewhere else',  lat: 52.4862,  lon: -1.8904  }, // default centre of England
    ],
  },
];

// ─── Defaults ─────────────────────────────────────────────────────────────────

const DEFAULT_ANSWERS = {
  importanceRanking: 3,
  importanceCourseQuality: 3,
  importanceSatisfaction: 3,
  importanceCost: 3,
  importanceNightlife: 2,
  maxDistanceKm: 400,
  maxCostOfLiving: 700,
  homeCity: 'London',
  homeLatitude: 51.5074,
  homeLongitude: -0.1278,
};

// ─── Component ────────────────────────────────────────────────────────────────

export default function QuizScreen({ navigation }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState({ ...DEFAULT_ANSWERS });

  const question = QUESTIONS[currentStep];
  const isLast = currentStep === QUESTIONS.length - 1;

  // ── Answer handlers ──────────────────────────────────────────────────────

  const setSlider = (value) => {
    setAnswers((prev) => ({ ...prev, [question.id]: value }));
  };

  const setNumber = (text) => {
    const num = parseInt(text, 10);
    if (!isNaN(num)) {
      setAnswers((prev) => ({ ...prev, [question.id]: num }));
    }
  };

  const setChoice = (option) => {
    setAnswers((prev) => ({
      ...prev,
      homeCity: option.label,
      homeLatitude: option.lat,
      homeLongitude: option.lon,
    }));
  };

  // ── Navigation ───────────────────────────────────────────────────────────

  const goNext = () => {
    if (isLast) {
      finishQuiz();
    } else {
      setCurrentStep((s) => s + 1);
    }
  };

  const goBack = () => {
    if (currentStep > 0) setCurrentStep((s) => s - 1);
  };

  const finishQuiz = async () => {
    await savePreferences(answers);
    await setQuizCompleted();
    Alert.alert(
      'Quiz Complete!',
      'Your preferences have been saved. Head to Recommendations to see your personalised university rankings.',
      [{ text: 'View Recommendations', onPress: () => navigation.navigate('MainTabs', { screen: 'Recommendations' }) }]
    );
  };

  // ── Render question types ────────────────────────────────────────────────

  const renderSlider = () => {
    const value = answers[question.id];
    return (
      <View style={styles.sliderContainer}>
        <Text style={styles.sliderValue}>{value} / 5</Text>
        <View style={styles.sliderButtons}>
          {[1, 2, 3, 4, 5].map((n) => (
            <TouchableOpacity
              key={n}
              style={[styles.sliderBtn, value === n && styles.sliderBtnActive]}
              onPress={() => setSlider(n)}
            >
              <Text style={[styles.sliderBtnText, value === n && styles.sliderBtnTextActive]}>
                {n}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
        <View style={styles.sliderLabels}>
          <Text style={styles.sliderLabelText}>Not important</Text>
          <Text style={styles.sliderLabelText}>Very important</Text>
        </View>
      </View>
    );
  };

  const renderNumber = () => (
    <View style={styles.numberContainer}>
      <View style={styles.numberInputRow}>
        <TextInput
          style={styles.numberInput}
          keyboardType="numeric"
          defaultValue={String(answers[question.id])}
          onChangeText={setNumber}
          maxLength={6}
        />
        <Text style={styles.unitLabel}>{question.unit}</Text>
      </View>
    </View>
  );

  const renderChoice = () => (
    <View style={styles.choiceContainer}>
      {question.options.map((option) => {
        const selected = answers.homeCity === option.label;
        return (
          <TouchableOpacity
            key={option.label}
            style={[styles.choiceBtn, selected && styles.choiceBtnActive]}
            onPress={() => setChoice(option)}
          >
            <Text style={[styles.choiceBtnText, selected && styles.choiceBtnTextActive]}>
              {option.label}
            </Text>
            {selected && <Ionicons name="checkmark-circle" size={20} color={GREEN} />}
          </TouchableOpacity>
        );
      })}
    </View>
  );

  // ── Render ───────────────────────────────────────────────────────────────

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* Progress bar */}
      <View style={styles.progressBar}>
        <View
          style={[
            styles.progressFill,
            { width: `${((currentStep + 1) / QUESTIONS.length) * 100}%` },
          ]}
        />
      </View>
      <Text style={styles.progressText}>
        Question {currentStep + 1} of {QUESTIONS.length}
      </Text>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Question */}
        <Text style={styles.questionTitle}>{question.title}</Text>
        <Text style={styles.questionSubtitle}>{question.subtitle}</Text>

        {/* Answer input */}
        <View style={styles.answerSection}>
          {question.type === 'slider' && renderSlider()}
          {question.type === 'number' && renderNumber()}
          {question.type === 'choice' && renderChoice()}
        </View>
      </ScrollView>

      {/* Navigation buttons */}
      <View style={styles.navRow}>
        <TouchableOpacity
          style={[styles.navBtn, styles.backBtn, currentStep === 0 && styles.navBtnDisabled]}
          onPress={goBack}
          disabled={currentStep === 0}
        >
          <Ionicons name="arrow-back" size={20} color={currentStep === 0 ? '#ccc' : GREEN} />
          <Text style={[styles.navBtnText, currentStep === 0 && { color: '#ccc' }]}>Back</Text>
        </TouchableOpacity>

        <TouchableOpacity style={[styles.navBtn, styles.nextBtn]} onPress={goNext}>
          <Text style={styles.nextBtnText}>{isLast ? 'Finish' : 'Next'}</Text>
          <Ionicons name={isLast ? 'checkmark' : 'arrow-forward'} size={20} color="#fff" />
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

// ─── Styles ───────────────────────────────────────────────────────────────────

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  progressBar: {
    height: 6,
    backgroundColor: '#e0e0e0',
  },
  progressFill: {
    height: 6,
    backgroundColor: GREEN,
    borderRadius: 3,
  },
  progressText: {
    textAlign: 'center',
    fontSize: 13,
    color: '#888',
    marginTop: 8,
  },
  scrollContent: {
    padding: 24,
    paddingBottom: 16,
  },
  questionTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: '#1a1a1a',
    marginBottom: 8,
    lineHeight: 30,
  },
  questionSubtitle: {
    fontSize: 15,
    color: '#666',
    marginBottom: 32,
  },
  answerSection: {
    marginTop: 8,
  },
  // Slider
  sliderContainer: {
    alignItems: 'center',
  },
  sliderValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: GREEN,
    marginBottom: 20,
  },
  sliderButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  sliderBtn: {
    width: 56,
    height: 56,
    borderRadius: 28,
    borderWidth: 2,
    borderColor: '#ccc',
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  sliderBtnActive: {
    borderColor: GREEN,
    backgroundColor: GREEN,
  },
  sliderBtnText: {
    fontSize: 20,
    fontWeight: '600',
    color: '#555',
  },
  sliderBtnTextActive: {
    color: '#fff',
  },
  sliderLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginTop: 12,
    paddingHorizontal: 4,
  },
  sliderLabelText: {
    fontSize: 12,
    color: '#999',
  },
  // Number input
  numberContainer: {
    alignItems: 'center',
  },
  numberInputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  numberInput: {
    width: 140,
    height: 64,
    borderWidth: 2,
    borderColor: GREEN,
    borderRadius: 12,
    textAlign: 'center',
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1a1a1a',
    backgroundColor: '#fff',
  },
  unitLabel: {
    fontSize: 18,
    color: '#555',
    fontWeight: '600',
  },
  // Choice
  choiceContainer: {
    gap: 10,
  },
  choiceBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#fff',
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#e0e0e0',
    padding: 16,
  },
  choiceBtnActive: {
    borderColor: GREEN,
    backgroundColor: '#e8f5e9',
  },
  choiceBtnText: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  choiceBtnTextActive: {
    color: GREEN,
    fontWeight: '700',
  },
  // Navigation
  navRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 20,
    borderTopWidth: 1,
    borderColor: '#eee',
    backgroundColor: '#fff',
  },
  navBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingVertical: 14,
    paddingHorizontal: 24,
    borderRadius: 12,
  },
  backBtn: {
    backgroundColor: '#f0f0f0',
  },
  nextBtn: {
    backgroundColor: GREEN,
  },
  navBtnDisabled: {
    opacity: 0.5,
  },
  navBtnText: {
    fontSize: 16,
    fontWeight: '600',
    color: GREEN,
  },
  nextBtnText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
});
