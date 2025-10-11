import Gen_Content.extract_title_markdown as extract_title_markdown
import unittest

class TestExtractTitleMarkdown(unittest.TestCase):
    def test_extract_title():
        md = """# My Title"""
        title = extract_title_markdown.extract_title(md)
        assert title == "My Title"

    def test_ignores_non_h1_and_whitespace():
        md = """### slslkdi\n # This is my title\n ## someother bs"""
        title = extract_title_markdown.extract_title(md)
        assert title == "This is my title"
        
    def test_no_title():
        md ="""### slslkdi\n ## someother bs"""
        try:
            extract_title_markdown.extract_title(md)
        except ValueError as e:
            assert str(e) == "No title found in markdown"


if __name__ == "__main__":
    unittest.main()