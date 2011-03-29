def test_cuter():
    from opal.TestProblemCollections import CUTEr
    assert CUTEr['HS100'].name == 'HS100'
    assert CUTEr['HS100'] is CUTEr.HS['HS100']
    return
