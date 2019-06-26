import se_code


def test_fn():
    for fn in se_code.attrs['fn'] + se_code.attrs['add']:
        assert fn(1, 1) == 2


def test_other():
    print(se_code.orig.__main__)
    print(se_code.attrs['__main__'])
