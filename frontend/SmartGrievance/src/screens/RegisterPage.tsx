import React, {useState} from "react";

import { View, Text, StyleSheet, TextInput, TouchableOpacity } from "react-native";

export default function RegisterPage() {
    const [fullName, setFullName] = useState("");
    const [PhoneNumber, setPhoneNumber] = useState("");
    const [step, setStep] = useState("PhoneNumber");

    return (
        <View >
            <Text style={styles.title}>Smart Grievance Redressal</Text>

            {step === "PhoneNumber" ? (
            <View>
            <Text>Full Name</Text>
            <TextInput placeholder="Full name"
            style={styles.input}
            keyboardType="phone-pad"
            value={fullName}
            onChangeText={(text)=> setFullName(text)}

            />

            <Text>Phone Number</Text>
            <TextInput placeholder="Phone number"
            style={styles.input}
            keyboardType="phone-pad"
            maxLength={10}
            value={PhoneNumber}
            onChangeText={(text)=> setPhoneNumber(text)} />

            <TouchableOpacity 
            style={styles.button}
            onPress={()=> {setStep("OTP")}}>
                <Text>Send OTP</Text>
            </TouchableOpacity>
            </View>
            ) : (
                <Text>OTP Sent to {PhoneNumber}</Text>
            )}
        </View>
    )
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 24,
    justifyContent: 'center'
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#1e3a5f',
    marginBottom: 8
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    color: '#666',
    marginBottom: 40
  },
  label: {
    fontSize: 16,
    color: '#333',
    marginBottom: 8
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 10,
    padding: 14,
    fontSize: 16,
    marginBottom: 16,
    backgroundColor: '#f9f9f9'
  },
  button: {
    backgroundColor: '#2563EB',
    padding: 16,
    borderRadius: 10,
    alignItems: 'center',
    marginBottom: 12
  },
  btnText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold'
  },
  link: {
    color: '#2563EB',
    textAlign: 'center',
    fontSize: 14,
    marginTop: 8
  }
})