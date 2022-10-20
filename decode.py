import jwt

public_key = """
    -----BEGIN RSA PRIVATE KEY-----
    MIICXAIBAAKBgQC+u8jneDNPvJXz5o3vLI55IP3IJW6V2TT8VTFu/6dXA0DOlstt
    IF7AJza7wRbKWeii6Yf25+B2IsDnFWDqpGUeuPm//t5YXJI0D4YrJTOGOuOB7diD
    LvWSy6JiBI20ZhAVcz1TaviXmJ1bJApExGg2sSZ8Ze1Q7WDiS5l2xQAJ9wIDAQAB
    AoGAZbB+u5IlYUS9eg0Y7USHLWN+isASRohIrKPLOE/LayPL4JkbGjJg8fe2QcH/
    oaDv3DPADs6vqKx8xndqdY9ybVM9Mgdi/YNCIXPjHUCdyE0YmQU22UaQjVY1xYf+
    8JSIWsph9xg6hQx+nIIAiJoo52j5YhE0tWrMYJ2HS1o0YDECQQDyD6Mc1aFivue4
    gOwXTgLqR0BMTZkSRqyFvsYoTgzcwtiDzQ8Gwow++kJU8SJINpVexhdjfeJ4Oydr
    F+JYIjQJAkEAybd/mugrqldgqfQwWgjhFQJJSAqZerjKix4g6eyNL7CqWmyDLebO
    Au3I3RHcvOCFJtm7Dnl+Y6rjeXyr++vN/wJAD2udmYWmfVLqEh/samOm3ePiHbpH
    yRlFflOz7fdi7GFhR6w1i9my84Qf26ds5qrLgzkdXlIzrjMehL0Fx1WOeQJBAMSF
    ctuPgCMXt8Q8c/LznZ4jORPnx7mJWUMKGlTssmyY+I7aEz9gEqtF0KCYa27UasT7
    8ULb2OfvMGlGriPkiy8CQAxgeJYbRPArUjMkv0wODMEpWbcZ++aWyR11oR27ZVpX
    Cylusngl13N03OiSmvhIvdtIAbf2Ab3Aj60I2cEzgck=
    -----END RSA PRIVATE KEY-----
    """

key = "\n".join([l.lstrip() for l in public_key.split("\n")])

class DecodeToken():
    def decode(token):
        decoded = jwt.decode(token, key, algorithms=['RS256'], options={"verify_signature": False})
        return decoded