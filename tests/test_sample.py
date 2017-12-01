# Sample Test passing with nose and pytest
# https://stackoverflow.com/questions/35851323/pytest-how-to-test-a-function-with-input-call
import branched_story as bs
import emb_text as et


def test_example():
    assert 1 == 1


def test_path_following(mocker, capfd):
    mocker.patch('branched_story.story_module.my_input', lambda: "a_o")
    __test__ = bs.Book("Test Book", "Jon Doe")
    __test__.add_story("start", "Story Text 1", "dec")
    __test__.add_decision("dec", "Decision: A or B", {
        'A_OPTION': 'sA', 'A_OPTION': 'sB'})
    __test__.add_story(
        "sA", "End Story Text 2A", False)
    __test__.add_story(
        'sB', "End Story Text 2B", False)
    __test__.set_start_point("start")
    __test__.tell()
    out, err = capfd.readouterr()
    print(out, err)
    