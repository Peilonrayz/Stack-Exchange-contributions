import module_utils
se_code = module_utils.attr_import('se_code')
attrs = se_code.attrs()


def test_fn():
    for fn in attrs['fn'] + attrs['add']:
        assert fn(1, 1) == 2


def test_other():
    print(se_code.orig.__main__)
    print(attrs['__main__'])
