import os
import hashlib

class Password:
    """ Class for password hashing """

    @staticmethod
    def hashPass(password):
        """ Hash the password using sha256 """

        # create salt so if same password indi siya same hash
        salt = os.urandom(16)
        # create hash object
        hashObj = hashlib.sha256()
        # update the hash object with the salt and password
        hashObj.update(salt)
        # then update the hash object with the password
        # the .encode is to convert the string to bytes
        # then the 'utf-8' is the encoding of the string
        hashObj.update(password.encode('utf-8'))
        # then the .digest() is to return the digest of the data passed to the update() method so that it will return the hash value of the password
        passwordHash = hashObj.digest()
        # then return the salt and password hash in hex format
        return (salt + passwordHash).hex()

    def verifyPass(password,storedHashHex):
        """ Verify the password """
        try:
            #
            storedBytes = bytes.fromhex(storedHashHex)
            
            salt = storedBytes[:16]
            storedHash = storedBytes[16:]
            
            hashObj = hashlib.sha256()
            hashObj.update(salt)
            hashObj.update(password.encode('utf-8'))
            checkHash = hashObj.digest()
            
            return checkHash == storedHash
        except:
            return False
