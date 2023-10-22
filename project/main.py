import random
import math
import os
def generatePrivateKey(n):
    A = [random.randint(1,10)]
    for i in range(n-1):
        a = random.randint(sum(A) + 1, sum(A) + random.randint(1, 10))
        A.append(a)
        #print(A)
    return A
def generateMOpen(A):
    M = random.randint(sum(A) + 1, sum(A) + random.randint(1, 10))
    #print("M: ", M)
    return M

def generateWClose(M):
    w = random.randint(1, 100)
   # print("w: ", w)
    while math.gcd(M, w) != 1:
        w = random.randint(1, 100)
    return w
def generateOpenKey(n, A, w, M):
    B = []
    for i in range(n):
        B.append((A[i] * w) % M)
   # print ("B : ", B)
    return B
def cryptMessage(message, B, M):
    binaryMess = list(f"{ord(i):08b}" for i in message)
    print(binaryMess)
    crypMess = []
    for i in range(len(binaryMess)):
        binarySym = binaryMess[i]
        temp = 0
        for j in range(len(binarySym)):
            if binarySym[j] == '1':
                temp += B[j]
        temp = temp % M
        crypMess.append(temp)
    print(crypMess)
    return crypMess

def deCryptMessage(message, A,w , M):
    A.reverse()
    messBi = []
    mess = []
    for i in range(len(message)):
        decMes = (message[i] * bezout_recursive(w, M)) % M
       # print("decmes ; " , decMes)
       #print( "rev A: " , A)
        temp = 0
        cr = ""
        for j in range(len(A)):
            if A[j] + temp <= decMes:
                temp = temp + A[j]
                cr += "1"
            else:
                cr += "0"

        messBi.append(cr[::-1])
    print(messBi)
    mess = "".join(messBi)
    str = ""
    for i in range(0, len(mess), 8):
        binc = mess[i:i + 8]
        num = int(binc, 2)
        str += chr(num)
    print(str)


def BinaryToDecimal(binary):
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return (decimal)
def bezout_recursive(a, b):
    x = 1
    while (a * x) % b != 1:
        x += 1
    return x



privateKey = generatePrivateKey(8) #часть закрытого ключа
M = generateMOpen(privateKey) #часть открытого ключа
w = generateWClose(M) #часть закрытого ключа
openKey = generateOpenKey(8, privateKey, w, M) #часть открытого ключа
#textFromKeyboard = input("Введите сообщение: ")
textFromKeyboard = os.getenv("tmp_value")

chipMess = cryptMessage(textFromKeyboard, openKey, M)
deCryptMessage(chipMess, privateKey, w, M)

