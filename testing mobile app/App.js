/**
 * App.js
 * Root component of the University Picker application.
 *
 * Sets up:
 *   - SafeAreaProvider (required by react-native-safe-area-context)
 *   - NavigationContainer (required by React Navigation)
 *   - AppNavigator (the app's screen hierarchy)
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import AppNavigator from './src/navigation/AppNavigator';

export default function App() {
  return (
    <SafeAreaProvider>
      {/* Green status bar to match the app header colour */}
      <StatusBar style="light" backgroundColor="#25995e" />
      <NavigationContainer>
        <AppNavigator />
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
