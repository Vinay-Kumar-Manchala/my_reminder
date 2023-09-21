from common_utilities.aes_encryption import AESCipher

decrypted_password = AESCipher(key="I Seek Vengeance").decrypt("ImVc0dsbgq4Serf6K0219G9JFAYxMVt9boH+JHV/v5c=")
print(decrypted_password)
print(f"the decrypted password is {decrypted_password}")