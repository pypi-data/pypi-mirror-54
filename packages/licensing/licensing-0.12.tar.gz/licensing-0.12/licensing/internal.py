# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:12:13 2019

@author: Artem Los
"""
import base64
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import urllib.request
import hashlib
from subprocess import Popen, PIPE

class HelperMethods:
    
    server_address = "https://app.cryptolens.io/api/"
    
    @staticmethod
    def get_SHA256(string):
        """
        Compute the SHA256 signature of a string.
        """
        return hashlib.sha256(string.encode("utf-8")).hexdigest()
    
    @staticmethod
    def verify_signature(response, rsaPublicKey):       
        """
        Verifies a signature from .NET RSACryptoServiceProvider.
        """
        cryptoPubKey = RSA.construct((HelperMethods.base642int(rsaPublicKey.modulus),\
                                      HelperMethods.base642int(rsaPublicKey.exponent)))
        h = SHA256.new(base64.b64decode(response.license_key.encode("utf-8")))
        verifier = PKCS1_v1_5.new(cryptoPubKey)
        return verifier.verify(h, base64.b64decode(response.signature.encode("utf-8")))
    
    @staticmethod
    def int2base64(num):
        return base64.b64encode(int.to_bytes(num), byteorder='big')
    
    @staticmethod
    def base642int(string):
        return int.from_bytes(base64.b64decode((string)), byteorder='big')
    
    @staticmethod
    def send_request(method, params):
        """
        Send a POST request to method in the Web API with the specified
        params and return the response string.
        
            method: the path of the method, eg. key/activate
            params: a dictionary of parameters
        """    
        return urllib.request.urlopen(HelperMethods.server_address + method, \
                                      urllib.parse.urlencode(params)\
                                      .encode("utf-8")).read().decode("utf-8")
        
    @staticmethod 
    def start_process(command):
        
        process = Popen(command, stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        return output.decode("utf-8")

    @staticmethod
    def get_dbus_machine_id():
        try:
            with open("/etc/machine-id") as f:
                return f.read().strip()
        except:
            pass
        try:
            with open("/var/lib/dbus/machine-id") as f:
                return f.read().strip()
        except:
            pass
        return ""

    @staticmethod
    def get_inodes():
        import os
        files = ["/bin", "/etc", "/lib", "/root", "/sbin", "/usr", "/var"]
        inodes = []
        for file in files:
            try:
                inodes.append(os.stat(file).st_ino)
            except: 
                pass
        return "".join([str(x) for x in inodes])

    @staticmethod
    def compute_machine_code():
        return HelperMethods.get_dbus_machine_id() + HelperMethods.get_inodes()
    