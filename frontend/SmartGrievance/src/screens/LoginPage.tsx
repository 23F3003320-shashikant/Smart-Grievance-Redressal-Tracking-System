
import React, { useState }from "react";
import { View, Text, StyleSheet, TextInput, TouchableOpacity, KeyboardType} from "react-native";


export default function LoginPage() {

    const [phoneNumber, setPhoneNumber] = useState("")
    const [step, setStep] = useState("PhoneNumber")

return  (
<View style={styles.container}>
    <Text style={styles.title}>Smart Grievance System</Text>

    {step === "PhoneNumber" ? (
        <View>
            <Text style={styles.label}>Enter Phone Number</Text>
            <TextInput 
            style={styles.input}
            placeholder="Enter phone number" 
            keyboardType="phone-pad" maxLength={10} 
            value={phoneNumber}
            onChangeText={(text) => setPhoneNumber(text)}/>

            <TouchableOpacity
            style={styles.button}
                onPress={() => {setStep("OTP")}}>
                <Text style={styles.btnText}>Send OTP</Text>
            </TouchableOpacity>
        </View>
    ) : (
        <View>
            <Text style={styles.subtitle}>OTP Sent to {phoneNumber}</Text>

            <TextInput style={styles.input} placeholder="6-digit OTP"
            keyboardType="number-pad" maxLength={6}/>

            <TouchableOpacity
            style={styles.button}
            onPress={() =>{
                alert("Login Sucessfull!")
            }}>
                <Text>Verify OTP</Text>
            </TouchableOpacity>

            <TouchableOpacity
            style={styles.button}
            onPress={() => setStep("PhoneNumber")}>
                <Text style={styles.btnText}>Change phone number</Text>
            </TouchableOpacity>
        </View>
    )}
</View>
);
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