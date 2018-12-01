from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import zlib
import base64
import crypto

def Keys():
    key = RSA.generate(2048, e=65537)
    return key, key.publickey()

def GenerateKeys(prefix):
    pri, pub = Keys()
    private_key = pri.exportKey("PEM")
    public_key  = pub.exportKey("PEM")

    print(private_key)
    fd = open(".test/{0}_private.pem".format(prefix), "wb")
    fd.write(private_key)
    fd.close()

    print(public_key)
    fd = open(".test/{0}_public.pem".format(prefix), "wb")
    fd.write(public_key)
    fd.close()

    public_ssh_key  = pub.exportKey("OpenSSH")
    print(public_ssh_key)
    fd = open(".test/{0}_public.pub".format(prefix), "wb")
    fd.write(public_ssh_key)
    fd.close()


def PairKey(plain=False, size=2048):
    """ Genera par de claves RSA """
    key = RSA.generate(size)
    return (key, key.publickey()) if plain else (key.exportKey("PEM"), key.publickey().exportKey('OpenSSH'))

def ed(token):
    print(token, "encrypt->")
    ciphertext = encrypt('.test/plataforma_public.pem', token)
    print(ciphertext)
    print(".decrypt->")
    print(decrypt('.test/plataforma_private.pem', ciphertext))
    print("------------")

def tests():
    GenerateKeys("plataforma")
    print("\n\n")
    with open(".test/plataforma_public.pub", "rb") as f:
        token = f.read()
    print("len:",len(token))
    ed(token)
    print("=======================\n")
    token2 = b"usuarios@dominios.totp.ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmyEmBfjgnHvasVKDKm3z0qtgZPclcqfnKnZ95TgfTA/0OoayjdZz8p3xnR0cWeroaiDvBBVKy0lD2oj484h/mD/UkXLVHZBKYTEPklw3GU0nYteSVWU6a8Uht5OLzHU58QM7FtDyvFtqXJBeKVWhbqBn6SLNjaG1CoolkC+TNt5moRvKllp8jY1ohgek96qi1V+CBZVlJlfxRY8eCjcGN1wmsbM5WN7HmSZhfFw4hJYR3LTRSw/EVg/MtKofaOVl7Pr2i1I5Wj2aiHsKpjl8WF5g3L/5OIPEpskxhv42QeEhBCgT0R2f1DMQ7YS0noS3LUSsTKnPqjsqYnqd190AX"
    ed(token2)
tok = b"usuarios@dominios.totp.ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmyEmBfjgnHvasVKDKm3z0qtgZPclcqfnKnZ95TgfTA/0OoayjdZz8p3xnR0cWeroaiDvBBVKy0lD2oj484h/mD/UkXLVHZBKYTEPklw3GU0nYteSVWU6a8Uht5OLzHU58QM7FtDyvFtqXJBeKVWhbqBn6SLNjaG1CoolkC+TNt5moRvKllp8jY1ohgek96qi1V+CBZVlJlfxRY8eCjcGN1wmsbM5WN7HmSZhfFw4hJYR3LTRSw/EVg/MtKofaOVl7Pr2i1I5Wj2aiHsKpjl8WF5g3L/5OIPEpskxhv42QeEhBCgT0R2f1DMQ7YS0noS3LUSsTKnPqjsqYnqd190AX"
encrypted = crypto.AE('.test/plataforma_public.pem', tok)
print(encrypted)
print(".....")
print(crypto.AD('.test/plataforma_private.pem',encrypted))

print(crypto.AD('.test/plataforma_private.pem',"eJw9iMmWojAARX+l95wuxigcN52giBKtpBl1UweRQWROMZivb2vT923uuzyt/ox1/JGyDf+vX2/dKOp7G8aK3wOLf8E3SD3z2JRfibL7uVtIIfrJkJqNVTT1ES8T6etFVE1bYBeLjwYRgHM10/bmq8nTAaeLK8RralvBoByyUJ5JpDf2oXyGrnTm9JoUVdYd088rOulZ5Kw9zyZCP02nMd/WBGSv5dIPeMQ3zVs/Miy3XQtZun8ZQJs5s7jiK1yIH2MBZWL8ReL94Nyh1KJZwrKoVAh3+9SkGlxF+lQH451GYEqB7eOO2dU8wDyFrhcq6VCpUhBgVgsniWwX8rgWwXheqGjcnFVLJrkX1yhIdiLaU3fyd6bR6GjZNgFHrSY1Ef0EYX0v1cE5Xva5mSxRVOZaC7R8nKqVTV/e04mbMwCGapVupnl9GWbfyrc+DIIoz/6xazHD/wASNIeX"))

#crypto.AD('.test/plataforma_private.pem',"eJw9iMmWojAARX+l95wuxigcN52giBKtpBl1UweRQWROMZivb2vT923uuzyt/ox1/JGyDf+vX2/dKOp7G8aK3wOLf8E3SD3z2JRfibL7uVtIIfrJkJqNVTT1ES8T6etFVE1bYBeLjwYRgHM10/bmq8nTAaeLK8RralvBoByyUJ5JpDf2oXyGrnTm9JoUVdYd088rOulZ5Kw9zyZCP02nMd/WBGSv5dIPeMQ3zVs/Miy3XQtZun8ZQJs5s7jiK1yIH2MBZWL8ReL94Nyh1KJZwrKoVAh3+9SkGlxF+lQH451GYEqB7eOO2dU8wDyFrhcq6VCpUhBgVgsniWwX8rgWwXheqGjcnFVLJrkX1yhIdiLaU3fyd6bR6GjZNgFHrSY1Ef0EYX0v1cE5Xva5mSxRVOZaC7R8nKqVTV/e04mbMwCGapVupnl9GWbfyrc+DIIoz/6xazHD/wASNIeX")
