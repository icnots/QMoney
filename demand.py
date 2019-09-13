
## MAKING QMONEY -- THE RISE OF QUBITCOINS (copyrights by KAMIL BUBAK)

bank_dictionary = [] # prefer a dict but just prototyping
client = 'A'
client_wallet = []


from qiskit import *

def randomBitstring(n):
    ## Creates a random bitstring of length n
    
    bitstring = []
    qr = QuantumRegister(1)
    cr = ClassicalRegister(n)
    circuit = QuantumCircuit(qr,cr)
    for i in range(n):
        circuit.h(qr[0])
        circuit.measure(qr[0],cr[i])
    result = execute(circuit, backend=Aer.get_backend('qasm_simulator'), shots=1).result()
    counts = result.get_counts()
    for k in counts:
        for char in k:
            if char == '0':
                bitstring.append(0)
            elif char == '1':
                bitstring.append(1)
            else:
                print("Errror")
    return bitstring
                
def demandQMoney(n=4):
    ## Mint: the bank creates some money for the client
    ## returns a state and the reference z (for now the circuit is a circuit)
    qr = QuantumRegister(n)
    cr = ClassicalRegister(n)
    circuit = QuantumCircuit(qr, cr)
    
    x = randomBitstring(n)
    y = randomBitstring(n)
    z = len(bank_dictionary)

    bank_dictionary.append((x,y,z))

    for i,_ in enumerate(x):
        if x[i] == 0 and y[i] == 0:
            pass
        elif x[i] == 0 and y[i] == 1:
            circuit.x(i)
        elif x[i] == 1 and y[i] == 0:
            circuit.h(i)
        else:
            circuit.x(i)
            circuit.h(i)
    return circuit, z


def getxy(z):
    ## search for z in the bank register
    ## returns the corresponding x and y
    for a,b,c in bank_dictionary:
        if c == z:
            return a,b
    return False, False

def verifyQMoney(cash, z):
    ## bank verifies the validity of the cash based on the reference z
    ## returns either true or false
    
    # find z with grover search if z is a bitstring
    # find z with divide and conquer if z is an integer
    x, y = getxy(z)
    if x == False:
        return False

    # the way the bank verifies the circuit is by adding the inverse gates corresponding to x and y
    for i,_ in enumerate(x):
        if x[i] == 0 and y[i] == 0:
            pass
        elif x[i] == 0 and y[i] == 1:
            cash.x(i)
        elif x[i] == 1 and y[i] == 0:
            cash.h(i)
        else:
            cash.h(i)
            cash.x(i)
    
    allQubits = [i for i,_ in enumerate(x)]
    cash.measure(allQubits, allQubits)
    result = execute(cash, backend=Aer.get_backend('qasm_simulator'), shots=1).result()
    compare = result.get_counts()
    for k in compare:
        if k == '0'*len(x):
            return True
        else:
            return False


## LET THE SIMULATION BEGIN
n = 10
euro1,z = demandQMoney(n)
client_wallet.append([euro1,z])
euro2,z = demandQMoney(n)
client_wallet.append([euro2,z])

# verify legitimate money
print("first qmoney:")
print(verifyQMoney(client_wallet[0][0],client_wallet[0][1]))

print("second qmoney:")
print(verifyQMoney(client_wallet[1][0],client_wallet[1][1]))

# verify fake money based on fake reference
print("fake reference:")
print(verifyQMoney(client_wallet[0][0],client_wallet[0][1]+1))

# verify fake money based on wrong state
print("fake state:")
print(verifyQMoney(demandQMoney(10)[0],client_wallet[0][1]))

# bank register
print(bank_dictionary)
