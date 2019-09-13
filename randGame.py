## Play card games, or roll a die, or anything
import numpy as np

def generateNumber(n):
    N = np.log(n)/np.log(2)
    N = int(N) + 1 # no time to check 
    circuit = QuantumCircuit(N,N)
    a = [i for i in range(N)]
    circuit.h(a)
    circuit.measure(a,a)
    lookFor = -1
    while lookFor not in range(n):
        result = execute(circuit, backend=Aer.get_backend('qasm_simulator'), shots=1).result()
        counts = result.get_counts()
        for k in counts:
            decimal = 0
            for i in k:
                decimal = 2*decimal+int(i)
            lookFor = decimal
    return lookFor

print(generateNumber(52))
