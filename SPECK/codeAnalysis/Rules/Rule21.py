#!/usr/bin/python3

from Rules import *
from FileReader import *
from Parser import *
from R import *
import sys


"""
RULE N°22

+ Use cryptography
** Use a secure random number generator, SecureRandom
-> https://developer.android.com/training/articles/security-tips#Crypto

? Pseudo Code:
	1. If there is KeyGenerator, search for SecureRandom

! Output
	-> NOTHING	: no KeyGenerator found
	-> OK 	   	: KeyGenerator use SecureRandom
	-> CRITICAL	: KeyGenerator doesn't use SecureRandom
"""

# keyGen = KeyGenerator.getInstance("AES");
# sr = SecureRandom.getInstance("SHA1PRNG");
# sr.setSeed(keyStart);
# keyGen.init(128, sr);
# SecretKey secretKey = keyGen.generateKey();


class Rule21(Rules):
    def __init__(
        self,
        directory,
        database,
        verbose=True,
        verboseDeveloper=False,
        storeManager=None,
        flowdroid=False,
        platform="",
        validation=False,
        quiet=True,
    ):
        Rules.__init__(
            self,
            directory,
            database,
            verbose,
            verboseDeveloper,
            storeManager,
            flowdroid,
            platform,
            validation,
            quiet,
        )

        self.AndroidErrMsg = (
            "cryptographic key(s) (don't) use a secure random number generator"
        )
        self.AndroidOkMsg = (
            "cryptographic key(s) use() a secure random number generator"
        )
        self.AndroidText = "https://developer.android.com/training/articles/security-tips#Crypto"

        self.errMsg = "Use a secure random number generator, SecureRandom, to initialize any cryptographic keys generated by KeyGenerator"
        self.category = R.CAT_5

        self.filter("javax.crypto.KeyGenerator")
        self.show(22, "Use cryptography")

    def run(self):
        self.loading()

        for f in self.javaFiles:
            fileReader = FileReader(f)

            found = Parser.finder(
                fileReader,
                [
                    [Parser.findVarName, (["KeyGenerator "], None)],
                    [Parser.findVarName, (["SecureRandom "], None)],
                    [Parser.findVarName, (["KeyGenerator.getInstance"], None)],
                ],
            )

            keyGenerator = Parser.setScopesWith(found[2], found[0])
            secureRandom = found[1]

            keyGenerator = Parser.setScopes(keyGenerator)
            secureRandom = Parser.setScopes(secureRandom)

            In, NotIn = Parser.scopeReachable(keyGenerator, secureRandom)

            # Set log msg
            In = Parser.setMsg(In, R.OK)
            NotIn = Parser.setMsg(NotIn, R.WARNING, self.errMsg)

            self.updateOWN(f, In, NotIn, (len(NotIn) == 0 and len(In) == 0))
            self.loading()
            fileReader.close()

        self.store(
            22,
            self.AndroidOkMsg,
            self.AndroidErrMsg,
            self.AndroidText,
            self.category,
            False,
            [self.errMsg],
        )
        self.display(FileReader)
