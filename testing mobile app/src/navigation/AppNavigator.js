/**
 * AppNavigator.js
 * Sets up the root React Navigation stack for the University Picker app.
 *
 * Structure:
 *   - Bottom Tab Navigator (main app)
 *       HomeScreen
 *       RecommendationsScreen
 *       CompareScreen
 *       SavedScreen
 *       SettingsScreen
 *   - Stack screens accessible from within tabs:
 *       QuizScreen     (pushed from HomeScreen)
 *       UniversityDetailScreen (pushed from any screen)
 */

import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';

import HomeScreen from '../screens/HomeScreen';
import QuizScreen from '../screens/QuizScreen';
import RecommendationsScreen from '../screens/RecommendationsScreen';
import CompareScreen from '../screens/CompareScreen';
import SavedScreen from '../screens/SavedScreen';
import SettingsScreen from '../screens/SettingsScreen';
import UniversityDetailScreen from '../screens/UniversityDetailScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

/** Brand green colour used throughout the app */
const BRAND_GREEN = '#25995e';

// ─── Bottom Tab Navigator ─────────────────────────────────────────────────────

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: BRAND_GREEN,
        tabBarInactiveTintColor: '#888',
        tabBarStyle: { backgroundColor: '#fff', borderTopColor: '#e0e0e0' },
        tabBarIcon: ({ focused, color, size }) => {
          const icons = {
            Home:            focused ? 'home'         : 'home-outline',
            Recommendations: focused ? 'star'         : 'star-outline',
            Compare:         focused ? 'git-compare'  : 'git-compare-outline',
            Saved:           focused ? 'bookmark'     : 'bookmark-outline',
            Settings:        focused ? 'settings'     : 'settings-outline',
          };
          return <Ionicons name={icons[route.name] || 'ellipse'} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Home"            component={HomeScreen} />
      <Tab.Screen name="Recommendations" component={RecommendationsScreen} />
      <Tab.Screen name="Compare"         component={CompareScreen} />
      <Tab.Screen name="Saved"           component={SavedScreen} />
      <Tab.Screen name="Settings"        component={SettingsScreen} />
    </Tab.Navigator>
  );
}

// ─── Root Stack Navigator ─────────────────────────────────────────────────────

export default function AppNavigator() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: BRAND_GREEN },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' },
      }}
    >
      {/* Main tabs as the root screen */}
      <Stack.Screen
        name="MainTabs"
        component={MainTabs}
        options={{ headerShown: false }}
      />

      {/* Quiz is a full-screen modal pushed from HomeScreen */}
      <Stack.Screen
        name="Quiz"
        component={QuizScreen}
        options={{ title: 'Preference Quiz', headerBackTitle: 'Back' }}
      />

      {/* Detail screen for a single university */}
      <Stack.Screen
        name="UniversityDetail"
        component={UniversityDetailScreen}
        options={({ route }) => ({
          title: route.params?.university?.name ?? 'University',
          headerBackTitle: 'Back',
        })}
      />
    </Stack.Navigator>
  );
}
