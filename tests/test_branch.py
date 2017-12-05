# Sample Test passing with nose and pytest
# https://stackoverflow.com/questions/35851323/pytest-how-to-test-a-function-with-input-call
import branched_story as bs

def test_path_following(mocker, capfd):
    mocker.patch('branched_story.story_module.get_user_input', lambda: "a_o")
    mocker.patch('emb_text.embellish_parse.colored',
                 lambda text, *args, **kwargs: text)
    mocker.patch('branched_story.story_module.colored',
                 lambda text, *args, **kwargs: text)
    __test__ = bs.Book("Test Book", "Jon Doe")
    __test__.add_story("start", "Story Text 1", "dec")
    __test__.add_decision("dec", "Decision: A or B", {
        'A_OPTION': 'sA', 'B_OPTION': 'sB'})
    __test__.add_story(
        "sA", "End Story Text 2A", False)
    __test__.add_story(
        'sB', "End Story Text 2B", False)
    __test__.set_start_point("start")
    __test__()
    out, err = capfd.readouterr()
    assert out == "===TEST BOOK===\nby Jon Doe.\nStory Text 1\nDecision: A or B\nEnd Story Text 2A\n====END====\n"