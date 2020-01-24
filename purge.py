import shutil


def purge_stepdefs(fp, lines):
    fp_backup = fp + '.old'
    shutil.copy(fp, fp_backup)

    with open(fp) as f:
        this_file = f.readlines()

    for line in lines.unused_stepdef_lineno(fp):
        this_file[line] = this_file[line].replace('@', '@X', 1)

    with open(fp, 'w+') as f:
        f.writelines(this_file)


def demo_purge_stepdefs(fp, lines):
    fp_backup = fp + '.old'
    print('copy {}  to {}'.format(fp, fp_backup))

    with open(fp) as f:
        this_file = f.readlines()

    for line in lines.unused_stepdef_lineno(fp):
        print(this_file[line].replace('@', '@@', 1), end='')


if __name__ == '__main__':
    test_path = 'test/steps.scala'
    demo_purge_stepdefs(test_path, [2])
