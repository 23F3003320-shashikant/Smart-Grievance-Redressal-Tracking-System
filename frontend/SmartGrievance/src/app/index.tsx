import React from "react";
import { Text, ScrollView, StyleSheet } from "react-native";
import LoginScreen from "../component/login";
export default function Index() {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text>Hello, World!</Text>
      <LoginScreen />

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
});
