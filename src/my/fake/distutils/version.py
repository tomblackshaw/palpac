'''
'''


def is_str_version_greater_lesser_or_equal(strA, strB):
    assert(type(strA) is str)
    assert(type(strB) is str)
    verno_A = int(strA) if '.' not in strA else int(strA[:strA.index('.')])
    verno_B = int(strB) if '.' not in strB else int(strB[:strB.index('.')])
    if verno_A < verno_B:
        return -1
    elif verno_A > verno_B:
        return 1
    else:
        if '.' in strA and '.' in strB:
            return is_str_version_greater_lesser_or_equal(strA[strA.index('.')+1:], strB[strB.index('.')+1:])
        elif '.' in strB and '.' not in strA:
            return -1
        elif '.' in strA and '.' not in strB:
            return 1
        else:
            return 0


class LooseVersion:

    def __init__(self, loose_ver_str):
        self.vstring = loose_ver_str.strip(' ')
        self.version = self.vstring.split('.')
        super().__init__()

    def __gt__(self, other_version):
        return True if is_str_version_greater_lesser_or_equal(self.vstring, other_version.vstring) > 0 else False

    def __eq__(self, other_version):
        return True if is_str_version_greater_lesser_or_equal(self.vstring, other_version.vstring) == 0 else False

    def __lt__(self, other_version):
        return True if is_str_version_greater_lesser_or_equal(self.vstring, other_version.vstring) < 0 else False
