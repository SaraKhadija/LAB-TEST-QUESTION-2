import streamlit as st
import json
import operator

# Load rules from JSON (embedded here for exam simplicity)
rules = [
    {
        "name": "Windows open → turn AC off",
        "priority": 100,
        "conditions": [["windows_open", "==", True]],
        "action": {
            "ac_mode": "OFF",
            "fan_speed": "LOW",
            "setpoint": None,
            "reason": "Windows are open"
        }
    },
    {
        "name": "No one home → eco mode",
        "priority": 90,
        "conditions": [["occupancy", "==", "EMPTY"], ["temperature", ">=", 24]],
        "action": {
            "ac_mode": "ECO",
            "fan_speed": "LOW",
            "setpoint": 27,
            "reason": "Home empty; save energy"
        }
    },
    {
        "name": "Hot & humid (occupied) → cool strong",
        "priority": 80,
        "conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", ">=", 30],
            ["humidity", ">=", 70]
        ],
        "action": {
            "ac_mode": "COOL",
            "fan_speed": "HIGH",
            "setpoint": 23,
            "reason": "Hot and humid"
        }
    },
    {
        "name": "Night (occupied) → sleep mode",
        "priority": 75,
        "conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["time_of_day", "==", "NIGHT"],
            ["temperature", ">=", 26]
        ],
        "action": {
            "ac_mode": "SLEEP",
            "fan_speed": "LOW",
            "setpoint": 26,
            "reason": "Night comfort"
        }
    },
    {
        "name": "Hot (occupied) → cool",
        "priority": 70,
        "conditions": [["occupancy", "==", "OCCUPIED"], ["temperature", ">=", 28]],
        "action": {
            "ac_mode": "COOL",
            "fan_speed": "MEDIUM",
            "setpoint": 24,
            "reason": "Temperature high"
        }
    },
    {
        "name": "Slightly warm (occupied) → gentle cool",
        "priority": 60,
        "conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", ">=", 26],
            ["temperature", "<", 28]
        ],
        "action": {
            "ac_mode": "COOL",
            "fan_speed": "LOW",
            "setpoint": 25,
            "reason": "Slightly warm"
        }
    },
    {
        "name": "Too cold → turn off",
        "priority": 85,
        "conditions": [["temperature", "<=", 22]],
        "action": {
            "ac_mode": "OFF",
            "fan_speed": "LOW",
            "setpoint": None,
            "reason": "Already cold"
        }
    }
]

ops = {
    "==": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,
    "<": operator.lt
}

def evaluate_rules(facts):
    sorted_rules = sorted(rules, key=lambda r: r["priority"], reverse=True)
    for rule in sorted_rules:
        if all(ops[cond[1]](facts[cond[0]], cond[2]) for cond in rule["conditions"]):
            return rule
    return None

# Streamlit UI
st.title("Rule-Based Smart Home AC Controller")

facts = {
    "temperature": st.slider("Temperature (°C)", 16, 40, 22),
    "humidity": st.slider("Humidity (%)", 0, 100, 46),
    "occupancy": st.selectbox("Occupancy", ["OCCUPIED", "EMPTY"]),
    "time_of_day": st.selectbox("Time of Day", ["MORNING", "AFTERNOON", "EVENING", "NIGHT"]),
    "windows_open": st.checkbox("Windows Open")
}

if st.button("Evaluate AC Decision"):
    rule = evaluate_rules(facts)
    if rule:
        action = rule["action"]
        st.success(f"""
        **Rule Applied:** {rule['name']}

        **AC Mode:** {action['ac_mode']}  
        **Fan Speed:** {action['fan_speed']}  
        **Setpoint:** {action['setpoint']}  
        **Reason:** {action['reason']}
        """)
    else:
        st.warning("No rule matched.")
