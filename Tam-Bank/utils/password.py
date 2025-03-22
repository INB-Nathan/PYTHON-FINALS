import os
import hashlib

class Password:
    """ Class for password hashing """
    
    @staticmethod
    def hashPass(password):
        """ Hash the password using sha256 """
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def verifyPass(password,hash):
        """ Verify the password """
        import hashlib
        attempt = hashlib.sha256(password.encode()).hexdigest()
        return attempt == hash
