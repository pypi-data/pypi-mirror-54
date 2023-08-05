
# Jake Cipher

This encryption algorithm is based in Affine encryption and Ultari encryption.  
Complex encryption algorithm using affine cipher and fence cipher  

=> Don't encrypt spaces, numbers, or special characters.  
=> We encrypt only alphabets.    
=> Apply encryption only sequentially to the alphabet.  
=> 26 character codes are used, uppercase letters are encrypted and lowercase letters are encrypted.  
=> Space padding occurs because it is processed in block units.  
(Space may be added after the decryption statement.)  
(Decrypt function remove the padding in default. If you don't want to remove the padding, add a False parameter at the end.)   

There is no limit on the length of the key, but you must enter an odd number of three or more.  
The key is N in pairs of two affine keys. In addition, add another fence encryption key.
The key pair has a product key and a sum key, so the input value is multiplied by the corresponding value and the sum key is added.
After the affine password, the fence cipher creates a row corresponding to the key value and transposes the data.
The character set used for encryption is a 26-character alphabet and is modulated by a mod 26 operation on the operation value.


아핀암호와 울타리 암호를 응용한 복합 암호화 알고리즘  

=> 공백, 숫자, 특수문자는 암호화 하지 않는다.  
=> 알파벳에만 암호화를 순차적으로 적용한다.  
=> 문자코드는 26개를 사용하며 대문자는 대문자 암호화, 소문자는 소문자로 암호화한다.
=> 블록단위로 처리되기 때문에 space padding이 발생함.   
(암복호화문 뒤에 스페이스가 추가될 수 있음.)  
(복호화 함수는 기본적으로 뒤에 추가한 스페이스를 자동 제거한다. 패딩을 제거하지 않으려면 마지막에 False 파라미터를 추가한다.)  

키의 길이는 제한이 없지만, 3개 이상으로 홀수 개의 수를 리스트로 입력해야 한다.    
키는 아핀키 두 개를 쌍으로 하여 N개를 사용하고, 추가로 울타리 암호키를 하나 더 추가한다.   
아핀 암호의 키 쌍은 곱 키와 합 키가 있어서 입력값에 해당 값을 곱한 후 합 키를 더한다. 그 결과를 알파벳으로 치환한다.    
아핀 암호 후에 울타리 암호로 키값에 해당되는 row를 만들어 데이터를 transpose(전치)한다.  


## Install
> pip install jakecipher  
> or  
> pip install --upgrade jakecipher    


## API description

- make_jake_key(passphase)  
    > 패스워드를 입력받아 키로 변환해 주는 함수로 키 생성을 편하게 지원한다.  
    리턴값 : 생성된 키        
    키 형식 : [K11,K12, K21, K22, K31,K32, ...,Kn1, Kn2, Ku]
        
- jake_encrypt(keys, plaintext)     
    > 입력 스트링을 암호화하여 리턴한다.      
        
- jake_decrypt(keys, encdata, padremove=True)   
    > 입력 스트링을 복호화하여 리턴한다.      
    padremove는 기본값이 True로 공백 패딩을 제거한다.  
    padremove를 False로 하면 울타리암호 키를 블록크기로 하여 공백 패딩을 유지하여 리턴한다.       

## Example

```python

'''
pip install jakecipher
'''
import jakecipher as jc

print('version=', jc.version)

# invfactor()
# Inverse Key Test
multikey=5
invkey = jc.inversefactor(multikey)
print(multikey, " multiply mod 26 inverse key=", invkey)

for pt in range(10):
    ct=pt*multikey % 26
    dt = ct*invkey % 26
    print(pt, ' enc=', ct, 'dec=', dt, '  ',
          'OK' if pt==dt else "FAIL")


plaintext = 'Hello World!!'
print("PLAINTEXT : ", plaintext)

# jake_encrypt() and jake_decrypt()

# manual key
# keys=[5,3, 3,1, 9,7, 5,5, 4]

# key generator :
keys = jc.make_jake_key("myPassword!")
print("KEYS : ", keys)

lastcipher=jc.jake_encrypt(keys, plaintext)
print("ENCRYPT")
print('---', lastcipher, '---  length=', len(lastcipher), sep='')

lastdec=jc.jake_decrypt(keys, lastcipher, False)
print("DECRYPT")
print('---',lastdec, '---  length=', len(lastdec), sep='')
lastdec=jc.jake_decrypt(keys, lastcipher)
print('---',lastdec, '---  length=', len(lastdec), sep='')

if plaintext.rstrip()==lastdec.rstrip():
    print("OK")
else:
    print("FAIL")


# debug list format print
jc.printlist("plain:  ", plaintext, 4, False)
jc.printlist("cipher: ", lastcipher, 4, False)
jc.printlist("decrypt:", lastdec, 4, False)



```

Output

>
 



> Author: crazyj7 and Jake(Jaewook)

