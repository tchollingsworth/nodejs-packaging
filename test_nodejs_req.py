
# Hackery to import nodejs.req as a module (Python 3.4+)
# https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
import importlib.util, importlib.machinery
loader = importlib.machinery.SourceFileLoader('nodejs_req', 'nodejs.req')
spec = importlib.machinery.ModuleSpec('nodejs_req', loader)
nodejs_req = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nodejs_req)

process_dep = nodejs_req.process_dep

def test_process_dep():
    # Single version
    assert process_dep('npm(a)', '1')       == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '=1')      == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', 'v1')      == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '=v1')     == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '1.2')     == '(npm(a) >= 1.2 with npm(a) < 1.3)'
    assert process_dep('npm(a)', '=1.2')    == '(npm(a) >= 1.2 with npm(a) < 1.3)'
    assert process_dep('npm(a)', 'v1.2')    == '(npm(a) >= 1.2 with npm(a) < 1.3)'
    assert process_dep('npm(a)', '=v1.2')   == '(npm(a) >= 1.2 with npm(a) < 1.3)'
    assert process_dep('npm(a)', '1.2.3')   == '(npm(a) >= 1.2.3 with npm(a) < 1.2.4)'
    assert process_dep('npm(a)', '=1.2.3')  == '(npm(a) >= 1.2.3 with npm(a) < 1.2.4)'
    assert process_dep('npm(a)', 'v1.2.3')  == '(npm(a) >= 1.2.3 with npm(a) < 1.2.4)'
    assert process_dep('npm(a)', '=v1.2.3') == '(npm(a) >= 1.2.3 with npm(a) < 1.2.4)'

    # Ranges with one comparator
    assert process_dep('npm(a)', '>1')      == 'npm(a) > 1'
    assert process_dep('npm(a)', '>1.2')    == 'npm(a) > 1.2'
    assert process_dep('npm(a)', '>1.2.3')  == 'npm(a) > 1.2.3'
    assert process_dep('npm(a)', '>=1')     == 'npm(a) >= 1'
    assert process_dep('npm(a)', '>=1.2')   == 'npm(a) >= 1.2'
    assert process_dep('npm(a)', '>=1.2.3') == 'npm(a) >= 1.2.3'
    assert process_dep('npm(a)', '<2')      == 'npm(a) < 2'
    assert process_dep('npm(a)', '<2.3')    == 'npm(a) < 2.3'
    assert process_dep('npm(a)', '<2.3.4')  == 'npm(a) < 2.3.4'
    assert process_dep('npm(a)', '<=2')     == 'npm(a) <= 2'
    assert process_dep('npm(a)', '<=2.3')   == 'npm(a) <= 2.3'
    assert process_dep('npm(a)', '<=2.3.4') == 'npm(a) <= 2.3.4'

    # Ranges with two comparators
    assert process_dep('npm(a)', '>1 <2')           == '(npm(a) > 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '>1.2 <2.3')       == '(npm(a) > 1.2 with npm(a) < 2.3)'
    assert process_dep('npm(a)', '>1.2.3 <2.3.4')   == '(npm(a) > 1.2.3 with npm(a) < 2.3.4)'
    assert process_dep('npm(a)', '>=1 <=2')         == '(npm(a) >= 1 with npm(a) <= 2)'
    assert process_dep('npm(a)', '>=1.2 <=2.3')     == '(npm(a) >= 1.2 with npm(a) <= 2.3)'
    assert process_dep('npm(a)', '>=1.2.3 <=2.3.4') == '(npm(a) >= 1.2.3 with npm(a) <= 2.3.4)'
    assert process_dep('npm(a)', '<2 >1')           == '(npm(a) > 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '<2.3 >1.2')       == '(npm(a) > 1.2 with npm(a) < 2.3)'
    assert process_dep('npm(a)', '<2.3.4 >1.2.3')   == '(npm(a) > 1.2.3 with npm(a) < 2.3.4)'
    assert process_dep('npm(a)', '<=2 >=1')         == '(npm(a) >= 1 with npm(a) <= 2)'
    assert process_dep('npm(a)', '<=2.3 >=1.2')     == '(npm(a) >= 1.2 with npm(a) <= 2.3)'
    assert process_dep('npm(a)', '<=2.3.4 >=1.2.3') == '(npm(a) >= 1.2.3 with npm(a) <= 2.3.4)'

    # Hyphen ranges
    assert process_dep('npm(a)', '1.2.3 - 2.3.4')   == '(npm(a) >= 1.2.3 with npm(a) <= 2.3.4)'
    assert process_dep('npm(a)', '1.2.3 - 2.3')     == '(npm(a) >= 1.2.3 with npm(a) < 2.4)'
    assert process_dep('npm(a)', '1.2.3 - 2')       == '(npm(a) >= 1.2.3 with npm(a) < 3)'
    assert process_dep('npm(a)', '1.2 - 2.3.4')     == '(npm(a) >= 1.2 with npm(a) <= 2.3.4)'
    assert process_dep('npm(a)', '1 - 2.3.4')       == '(npm(a) >= 1 with npm(a) <= 2.3.4)'
    assert process_dep('npm(a)', '1.2 - 2.3')       == '(npm(a) >= 1.2 with npm(a) < 2.4)'
    assert process_dep('npm(a)', '1.2 - 2')         == '(npm(a) >= 1.2 with npm(a) < 3)'
    assert process_dep('npm(a)', '1 - 2.3')         == '(npm(a) >= 1 with npm(a) < 2.4)'
    assert process_dep('npm(a)', '1 - 2')           == '(npm(a) >= 1 with npm(a) < 3)'

    # X-Ranges
    assert process_dep('npm(a)', '1.2.x')   == '(npm(a) >= 1.2 with npm(a) < 1.3)'
    assert process_dep('npm(a)', '1.2.*')   == '(npm(a) >= 1.2 with npm(a) < 1.3)'
    assert process_dep('npm(a)', '1.x')     == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '1.*')     == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '*')       == 'npm(a)'
    assert process_dep('npm(a)', '')        == 'npm(a)'

    # Tilde ranges
    assert process_dep('npm(a)', '~1.2.3')  == '(npm(a) >= 1.2.3 with npm(a) < 1.3)'
    assert process_dep('npm(a)', '~1.2.x')  == '(npm(a) >= 1.2 with npm(a) < 1.3)'
    assert process_dep('npm(a)', '~1.2')    == '(npm(a) >= 1.2 with npm(a) < 1.3)'
    assert process_dep('npm(a)', '~1.x')    == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '~1')      == '(npm(a) >= 1 with npm(a) < 2)'

    # Caret ranges
    assert process_dep('npm(a)', '^1.2.3')  == '(npm(a) >= 1.2.3 with npm(a) < 2)'
    assert process_dep('npm(a)', '^0.2.3')  == '(npm(a) >= 0.2.3 with npm(a) < 0.3)'
    assert process_dep('npm(a)', '^0.0.3')  == '(npm(a) >= 0.0.3 with npm(a) < 0.0.4)'
    assert process_dep('npm(a)', '^1.2.x')  == '(npm(a) >= 1.2 with npm(a) < 2)'
    assert process_dep('npm(a)', '^1.2')    == '(npm(a) >= 1.2 with npm(a) < 2)'
    assert process_dep('npm(a)', '^0.1.x')  == '(npm(a) >= 0.1 with npm(a) < 0.2)'
    assert process_dep('npm(a)', '^0.1')    == '(npm(a) >= 0.1 with npm(a) < 0.2)'
    assert process_dep('npm(a)', '^1.x')    == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '^1')      == '(npm(a) >= 1 with npm(a) < 2)'
    assert process_dep('npm(a)', '^0.0.x')  == 'npm(a) < 0.1'
    assert process_dep('npm(a)', '^0.0')    == 'npm(a) < 0.1'
    assert process_dep('npm(a)', '^0.x')    == 'npm(a) < 1'
    assert process_dep('npm(a)', '^0')      == 'npm(a) < 1'

    # More than two comparators in a set
    # (no reason for this to ever appear, but it is permitted)
    assert process_dep('npm(a)', '>1.2 <2.0 <1.9') == '(npm(a) > 1.2 with npm(a) < 1.9)'

    # The following cases are not implemented currently...

    # Multiple comparator sets separated by ||
    assert process_dep('npm(a)', '^1.2 || ^2.2') == 'npm(a)'

    # The whole pre-release stuff: https://docs.npmjs.com/misc/semver#prerelease-tags
    # which is not even enumerated here because it is so complex.
