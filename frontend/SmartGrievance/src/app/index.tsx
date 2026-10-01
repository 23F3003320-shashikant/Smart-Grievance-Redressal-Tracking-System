import React from "react";
import { Text, ScrollView, StyleSheet } from "react-native";

import LoginPage from "../screens/LoginPage"

import RegisterPage from "../screens/RegisterPage"



export default function Index() {
  return (
    <ScrollView>
      <RegisterPage />
      <LoginPage />
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
