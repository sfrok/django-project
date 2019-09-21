import baseapp.search as func


def test_search():
    f = func.search("Train", cat=['tech', 'food'])
    assert type(f) is list and len(f) > 0
