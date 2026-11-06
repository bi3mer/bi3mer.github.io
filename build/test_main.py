import unittest

from main import Document, parse_yaml, split_front_matter


def md(text):
    return Document().render(text)


class Blocks(unittest.TestCase):
    def test_heading_ids_are_unique(self):
        self.assertEqual(md("# A b\n\n# A b"), '<h1 id="a-b">A b</h1>\n<h1 id="a-b-1">A b</h1>')

    def test_fence_escapes_and_keeps_tabs(self):
        result = md("```go\n\tif i < n {\n```")
        self.assertIn('<span class="k">if</span>', result)
        self.assertIn("&lt;", result)
        self.assertIn("\t", result)

    def test_unknown_language_is_plain(self):
        self.assertEqual(md("```nope\na < b\n```"), '<pre><code class="language-nope">a &lt; b\n</code></pre>')

    def test_nested_list(self):
        self.assertEqual(md("- a\n  - b\n- c"), "<ul>\n<li>a\n<ul>\n<li>b</li>\n</ul></li>\n<li>c</li>\n</ul>")

    def test_code_in_list(self):
        self.assertIn("<li>a\n<pre><code>x\n</code></pre></li>", md("1. a\n   ```\n   x\n   ```"))

    def test_table_attribute_after_blank_line(self):
        self.assertIn('<table class="styled-table">', md("| a |\n| - |\n| b |\n\n{.styled-table}"))

    def test_setext_and_rule(self):
        self.assertEqual(md("T\n---\n\n---"), '<h2 id="t">T</h2>\n<hr>')

    def test_raw_script_is_untouched(self):
        self.assertEqual(md("<script>\nif (a < b) {}\n\nx *= 2 * 3\n</script>"),
                         "<script>\nif (a < b) {}\n\nx *= 2 * 3\n</script>")

    def test_display_math(self):
        doc = Document()
        self.assertEqual(doc.render("$$\na_1 < b_2\n$$"), '<div class="math">$$\na_1 &lt; b_2\n$$</div>')
        self.assertTrue(doc.has_math)


class Inline(unittest.TestCase):
    def test_emphasis(self):
        self.assertEqual(md("*a* **b** ***c***"), "<p><em>a</em> <strong>b</strong> <em><strong>c</strong></em></p>")

    def test_snake_case_stays(self):
        self.assertEqual(md("snake_case_name"), "<p>snake_case_name</p>")

    def test_math_survives_escapes_and_emphasis(self):
        self.assertEqual(md(r"\(a_1 * b_2 * c\)"), r"<p>\(a_1 * b_2 * c\)</p>")

    def test_math_in_heading(self):
        self.assertIn(r"\(\Delta t\)</h2>", md(r"## Increasing \(\Delta t\)"))

    def test_code_span(self):
        self.assertEqual(md("`a < *b*`"), "<p><code>a &lt; *b*</code></p>")

    def test_link_and_escape(self):
        self.assertEqual(md(r"[a *b*](/c) \*d"), '<p><a href="/c">a <em>b</em></a> *d</p>')

    def test_image_with_title_is_a_figure(self):
        self.assertEqual(md('![x](/a.png "Figure 1")'),
                         '<figure><img src="/a.png" alt="x" loading="lazy">\n<small>Figure 1</small></figure>')

    def test_footnote(self):
        result = md("a[^n]\n\n[^n]: note")
        self.assertIn('href="#fn:1"', result)
        self.assertIn('<li id="fn:1"><p>note', result)

    def test_bare_url(self):
        self.assertEqual(md("see https://a.b/c."), '<p>see <a href="https://a.b/c">https://a.b/c</a>.</p>')


class FrontMatter(unittest.TestCase):
    def test_toml(self):
        meta, body = split_front_matter("+++\ntitle = 'a'\n+++\n\nbody\n")
        self.assertEqual((meta["title"], body.strip()), ("a", "body"))

    def test_yaml_comment(self):
        self.assertEqual(parse_yaml('title: "S" # note\nshow: false # no'), {"title": "S", "show": False})


if __name__ == "__main__":
    unittest.main()
