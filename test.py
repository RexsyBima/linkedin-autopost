from markdown import markdown
from bs4 import BeautifulSoup


def html_to_text_with_lists(html):
    soup = BeautifulSoup(html, "html.parser")
    lines = []

    def walk(node, indent=0, ol_level=0):
        if node.name == "ul":
            for li in node.find_all("li", recursive=False):
                lines.append("  " * indent + "* " + walk(li, indent + 1))
        elif node.name == "ol":
            i = 1
            for li in node.find_all("li", recursive=False):
                lines.append("  " * indent + f"{i}. " + walk(li, indent + 1))
                i += 1
        elif node.name == "li":
            # If li has nested ul/ol, handle separately
            text = node.get_text(" ", strip=True)
            sublists = node.find_all(["ul", "ol"], recursive=False)
            return text if not sublists else text
        else:
            # For headings, paragraphs, etc.
            if node.string:
                return node.string.strip()
            else:
                return " ".join(
                    child.get_text(" ", strip=True) for child in node.children if child
                )

    for child in soup.children:
        txt = walk(child)
        if txt:
            if isinstance(txt, str):
                lines.append(txt)

    return "\n".join(lines)


# Load your markdown file
with open("sample.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert markdown → HTML
html_content = markdown(md_content)

# Convert HTML → styled plain text
text_content = html_to_text_with_lists(html_content)

# Save to .txt file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text_content)
