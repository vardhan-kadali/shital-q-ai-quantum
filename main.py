import random
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import FastAPI
from sklearn.ensemble import RandomForestRegressor

# ✅ QISKIT (STABLE)
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

app = FastAPI()

# -------------------------
# DATASET
# -------------------------
data = []

for i in range(100):
    temp = random.uniform(-10, 10)
    time = random.randint(10, 120)
    outside_temp = random.randint(25, 45)

    risk = (outside_temp - temp) * time / 1000
    data.append([temp, time, outside_temp, risk])

df = pd.DataFrame(data, columns=["temp", "time", "outside_temp", "risk"])

# -------------------------
# AI MODEL
# -------------------------
X = df[["temp", "time", "outside_temp"]]
y = df["risk"]

model = RandomForestRegressor()
model.fit(X, y)

# -------------------------
# QUANTUM FUNCTION
# -------------------------
def quantum_route_score(time):

    qc = QuantumCircuit(2)

    qc.h(0)        # superposition
    qc.cx(0, 1)    # entanglement

    qc.measure_all()

    simulator = AerSimulator()
    result = simulator.run(qc).result()
    counts = result.get_counts()

    score = list(counts.values())[0]

    return score - time

# -------------------------
# API
# -------------------------
@app.get("/")
def home():
    return {"message": "SHITAL-Q running"}

@app.get("/compare")
def compare(temp: float, time: int, outside_temp: float):

    ai_risk = model.predict([[temp, time, outside_temp]])[0]
    quantum_score = quantum_route_score(time)

    return {
        "AI_risk": round(ai_risk, 3),
        "Quantum_score": quantum_score
    }

# -------------------------
# GRAPH API (NEW)
# -------------------------
@app.get("/graph")
def graph():

    ai_results = []
    quantum_results = []
    times = list(range(10, 110, 10))

    for t in times:
        ai = model.predict([[5, t, 35]])[0]
        q = quantum_route_score(t)

        ai_results.append(ai)
        quantum_results.append(q)

    plt.figure()
    plt.plot(times, ai_results, label="AI Risk")
    plt.plot(times, quantum_results, label="Quantum Score")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("AI vs Quantum Comparison")
    plt.legend()

    plt.savefig("graph.png")

    return {"message": "Graph generated! Check project folder"}