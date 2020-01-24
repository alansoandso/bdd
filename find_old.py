import os
import fnmatch


def find_old(directory):
    """
    Recursively walk from directory downwards looking for backup feature files
    Return
    """
    paths = []
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, '*old'):
            fp = os.path.join(path, filename)
            paths.append(fp)
            os.unlink(fp)

    return paths


if __name__ == '__main__':
    p = '.'
    p = '/Users/alan/workspace/qa-cucumber-jvm/src/test'
    # p = '/Users/alan/workspace/plutus-partner-accounts/partner-accounts-test/src/test'
    old = find_old(p)
    print(old)
    print(len(old))