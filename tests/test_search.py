import baseapp.search as func

def test_search():
    assert func.search("Train", cat=['tech', 'food']) == 5