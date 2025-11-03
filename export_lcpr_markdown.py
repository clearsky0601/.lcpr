#!/usr/bin/env python3
import os
import re
import json
import argparse
from html import unescape


def html_to_markdown(html: str) -> str:
    """A lightweight HTML -> Markdown converter tailored for LeetCode desc.

    Handles common tags: p, br, strong/b, em/i, code, pre, ul/ol/li, a, h1-h6.
    Keeps code blocks and inline code, converts HTML entities.
    This avoids external deps to run out-of-the-box.
    """
    if not html:
        return ""

    text = html

    # Normalize newlines for block-level tags
    text = re.sub(r"\r\n?", "\n", text)

    # Convert <pre><code>...</code></pre> first to fenced blocks
    def _pre_block(m):
        inner = m.group(1)
        # Remove outer <code> if present
        inner = re.sub(r"^\s*<code[^>]*>|</code>\s*$", "", inner, flags=re.IGNORECASE)
        inner = unescape(inner)
        # Replace <br> inside code with newlines
        inner = re.sub(r"<br\s*/?>", "\n", inner, flags=re.IGNORECASE)
        # Strip any remaining HTML tags inside code conservatively
        inner = re.sub(r"<[^>]+>", "", inner)
        return "\n```\n" + inner.strip("\n") + "\n```\n"

    text = re.sub(r"<pre[^>]*>([\s\S]*?)</pre>", _pre_block, text, flags=re.IGNORECASE)

    # Headings
    for i in range(6, 0, -1):
        text = re.sub(rf"<h{i}[^>]*>([\s\S]*?)</h{i}>", lambda m: "\n" + ("#" * i) + " " + unescape(_inline_html_to_text(m.group(1))).strip() + "\n", text, flags=re.IGNORECASE)

    # Lists: convert <li> to markdown list items; handle ul/ol wrappers by newlines
    text = re.sub(r"</?(ul|ol)[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li[^>]*>([\s\S]*?)</li>", lambda m: "- " + _inline_html_to_text(m.group(1)).strip() + "\n", text, flags=re.IGNORECASE)

    # Paragraphs and line breaks
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<p[^>]*>", "", text, flags=re.IGNORECASE)

    # Inline code and strong/emphasis and links
    text = re.sub(r"<code[^>]*>([\s\S]*?)</code>", lambda m: "`" + _clean_inline(unescape(m.group(1))) + "`", text, flags=re.IGNORECASE)
    text = re.sub(r"<(strong|b)[^>]*>([\s\S]*?)</\1>", lambda m: "**" + _inline_html_to_text(m.group(2)).strip() + "**", text, flags=re.IGNORECASE)
    text = re.sub(r"<(em|i)[^>]*>([\s\S]*?)</\1>", lambda m: "*" + _inline_html_to_text(m.group(2)).strip() + "*", text, flags=re.IGNORECASE)
    text = re.sub(r"<a[^>]*href=\"([^\"]+)\"[^>]*>([\s\S]*?)</a>", lambda m: f"[{_inline_html_to_text(m.group(2)).strip()}]({m.group(1)})", text, flags=re.IGNORECASE)

    # Remove any remaining tags
    text = re.sub(r"<[^>]+>", "", text)

    # Unescape HTML entities and normalize blank lines
    text = unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


def _inline_html_to_text(s: str) -> str:
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<\/?(span|div)[^>]*>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<code[^>]*>([\s\S]*?)</code>", lambda m: "`" + _clean_inline(unescape(m.group(1))) + "`", s, flags=re.IGNORECASE)
    s = re.sub(r"<(strong|b)[^>]*>([\s\S]*?)</\1>", lambda m: "**" + _inline_html_to_text(m.group(2)) + "**", s, flags=re.IGNORECASE)
    s = re.sub(r"<(em|i)[^>]*>([\s\S]*?)</\1>", lambda m: "*" + _inline_html_to_text(m.group(2)) + "*", s, flags=re.IGNORECASE)
    s = re.sub(r"<a[^>]*href=\"([^\"]+)\"[^>]*>([\s\S]*?)</a>", lambda m: f"[{_inline_html_to_text(m.group(2)).strip()}]({m.group(1)})", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    return unescape(s)


def _clean_inline(s: str) -> str:
    s = s.replace("`", "\u200b`\u200b")  # avoid breaking backticks
    return s


def export_one(json_path: str, out_dir: str) -> str:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    problem_id = str(data.get("id") or data.get("fid") or "")
    slug = data.get("slug") or ""
    cn_name = data.get("name") or data.get("cn_name") or ""
    en_name = data.get("en_name") or ""
    link = data.get("link") or ""
    level = data.get("level") or ""
    category = data.get("category") or ""
    desc_html = data.get("desc") or ""

    title_line = f"# {problem_id}. {cn_name}"
    if en_name:
        title_line += f" ({en_name})"

    header_lines = [
        title_line,
        "",
    ]
    if link:
        header_lines.append(f"- 链接: [{link}]({link})")
    if level:
        header_lines.append(f"- 难度: {level}")
    if category:
        header_lines.append(f"- 分类: {category}")

    header = "\n".join(header_lines).rstrip() + "\n\n---\n\n"

    body_md = html_to_markdown(desc_html)

    os.makedirs(out_dir, exist_ok=True)
    out_name = f"{problem_id}.{slug}.md" if problem_id and slug else (slug or problem_id or "problem") + ".md"
    out_path = os.path.join(out_dir, out_name)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(body_md)

    return out_path


def main():
    parser = argparse.ArgumentParser(description="Export LCPR/LeetCode problem descriptions to Markdown")
    parser.add_argument("--cache-dir", default=os.path.expanduser("~/.lcpr/leetcode/cache"), help="Path to leetcode/cache directory")
    parser.add_argument("--out-dir", default=os.path.expanduser("~/.lcpr/problems_markdown"), help="Directory to write Markdown files")
    parser.add_argument("--filter", default="", help="Filter by id or slug (substring match). Empty = all")
    args = parser.parse_args()

    cache_dir = args.cache_dir
    out_dir = args.out_dir
    flt = args.filter.strip()

    if not os.path.isdir(cache_dir):
        raise SystemExit(f"Cache dir not found: {cache_dir}")

    exported = []
    for name in sorted(os.listdir(cache_dir)):
        if not name.endswith(".algorithms.json"):
            continue
        if flt and flt not in name:
            continue
        json_path = os.path.join(cache_dir, name)
        try:
            out_path = export_one(json_path, out_dir)
            exported.append(out_path)
        except Exception as e:
            print(f"Failed to export {name}: {e}")

    print(f"Exported {len(exported)} file(s).")
    for p in exported:
        print(p)


if __name__ == "__main__":
    main()


