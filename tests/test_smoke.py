def test_site_is_up(browser):
    """Проверяем, что сайт открывается"""
    browser.get("https://www.demoblaze.com/")
    assert "STORE" in browser.title
