def IntToBinary(num):
    return num.to_bytes(1, byteorder='big')
def ChrToBinary(character):
    return character.encode('utf-8')
def StringToBinary(cadena):
    numero_entero = int(cadena, 2)
    bytes_binarios = numero_entero.to_bytes(1, byteorder='big')

    return bytes_binarios

def BinaryToChr(byte):
    return chr(int.from_bytes(byte, byteorder='big'))
def BinaryToInt(byte):
    return int.from_bytes(byte, byteorder='big')
def BinaryToString(byte):
    cadenaAux = bin(ord(byte))[2:]
    if (len(cadenaAux) < 8):
        cadenaAux = "0" * (8 - len(cadenaAux)) + cadenaAux
    return cadenaAux