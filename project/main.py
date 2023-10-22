import random
import math
import os

def generatePrivateKey(n): # функция, которая генерирует часть закрытого ключа (без числа W)
    A = [random.randint(1,10)]
    for i in range(n-1):
        a = random.randint(sum(A) + 1, sum(A) + random.randint(1, 10))
        A.append(a)
        #print(A)
    return A
def generateMOpen(A):     # функция, которая генерирует часть открытого ключа (без пос-ти чисел)
    M = random.randint(sum(A) + 1, sum(A) + random.randint(1, 10))
    #print("M: ", M)
    return M

def generateWClose(M):    # функция, которая генерирует часть закрытого ключа (число W)
    w = random.randint(1, 100)
   # print("w: ", w)
    while math.gcd(M, w) != 1:
        w = random.randint(1, 100)
    return w
def generateOpenKey(n, A, w, M): # функция, которая генерирует часть открытого ключа (без числа M)
    B = []
    for i in range(n):
        B.append((A[i] * w) % M)
   # print ("B : ", B)
    return B
def cryptMessage(message, B, M):    # функция, которая зашифровывает полученно сообщение посредством открытого ключа
    binaryMess = list(f"{ord(i):08b}" for i in message)
    print("Полученное сообщение в двоичной системе: ", binaryMess)
    crypMess = []
    for i in range(len(binaryMess)):
        binarySym = binaryMess[i]
        temp = 0
        for j in range(len(binarySym)):
            if binarySym[j] == '1':
                temp += B[j]
        temp = temp % M
        crypMess.append(temp)
    print("Зашифрованное сообщение: ", crypMess)
    return crypMess

def deCryptMessage(message, A,w , M):  # функция, которая расшифровывает полученно сообщение посредством закрытого ключа
    A.reverse()
    messBi = []
    #mess = []
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
    print("Расшифрованное сообщение в двоичной системе: ", messBi)
    mess = "".join(messBi)
    str = ""
    for i in range(0, len(mess), 8):
        binc = mess[i:i + 8]
        num = int(binc, 2)
        str += chr(num)
    print("Полученное сообщение (расшифрованное) : ", str)


def BinaryToDecimal(binary):  # функция, которая приводит двоичный код в строковое значение
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return (decimal)
def bezout_recursive(a, b): # расширенный алгоритм евклида
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

chipMess = cryptMessage(textFromKeyboard, openKey, M)  # зашифрованное сообщение
deCryptMessage(chipMess, privateKey, w, M) # расшифрованное сообщение
