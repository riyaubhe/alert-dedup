from dedup import clean_url, clean_title, dedupe


def test_url_ignores_www_and_caps():
    assert clean_url("https://WWW.News.com/story") == "news.com/story"


def test_url_ignores_trailing_slash():
    assert clean_url("https://news.com/story/") == "news.com/story"


def test_url_drops_tracking_params():
    assert clean_url("https://news.com/story?utm_source=google") == "news.com/story"


def test_url_keeps_real_params():
    assert clean_url("https://news.com/article?id=5") == "news.com/article?id=5"


def test_title_cleaning():
    assert clean_title("  Breaking: Big News!! ") == "breaking big news"


def test_same_url_merges_topics():
    alerts = [
        {"title": "Story A", "url": "https://news.com/a", "topic": "Uganda"},
        {"title": "Story A", "url": "https://news.com/a?utm_source=x", "topic": "Human Rights"},
    ]
    result = dedupe(alerts)
    assert len(result) == 1
    assert result[0]["topics"] == ["Uganda", "Human Rights"]


def test_same_title_is_duplicate():
    alerts = [
        {"title": "Big Event Today", "url": "https://site1.com/x", "topic": "Peace"},
        {"title": "big event today!", "url": "https://site2.com/y", "topic": "Africa"},
    ]
    assert len(dedupe(alerts)) == 1


def test_different_stories_stay_separate():
    alerts = [
        {"title": "Story A", "url": "https://news.com/a", "topic": "Uganda"},
        {"title": "Story B", "url": "https://news.com/b", "topic": "Uganda"},
    ]
    assert len(dedupe(alerts)) == 2


def test_topic_not_repeated():
    alerts = [
        {"title": "Story A", "url": "https://news.com/a", "topic": "Uganda"},
        {"title": "Story A", "url": "https://news.com/a", "topic": "Uganda"},
    ]
    assert dedupe(alerts)[0]["topics"] == ["Uganda"]


def test_empty_input():
    assert dedupe([]) == []

def test_similar_titles_are_duplicates():
    alerts = [
        {"title": "Flooding hits city", "url": "https://site1.com/a", "topic": "Weather"},
        {"title": "Flooding hits the city", "url": "https://site2.com/b", "topic": "Disasters"},
    ]
    assert len(dedupe(alerts)) == 1


def test_different_meaning_titles_stay_separate():
    alerts = [
        {"title": "City council approves budget", "url": "https://site1.com/a", "topic": "Politics"},
        {"title": "City council rejects budget", "url": "https://site2.com/b", "topic": "Politics"},
    ]
    assert len(dedupe(alerts)) == 2