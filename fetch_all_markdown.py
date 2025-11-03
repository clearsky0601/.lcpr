#!/usr/bin/env python3
import os
import sys
import json
import time
import argparse
from typing import Dict, Any, List, Optional

import requests


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def load_auth(user_json_path: str) -> Dict[str, str]:
    if not os.path.isfile(user_json_path):
        return {}
    with open(user_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    session = data.get("sessionId") or ""
    csrf = data.get("sessionCSRF") or data.get("loginCSRF") or ""
    return {"LEETCODE_SESSION": session, "csrftoken": csrf}


def build_session(cookies: Dict[str, str]) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
        "Referer": "https://leetcode.cn",
        "Origin": "https://leetcode.cn",
        "Content-Type": "application/json",
    })
    if cookies.get("csrftoken"):
        s.headers["x-csrftoken"] = cookies["csrftoken"]
    if cookies:
        s.cookies.update(cookies)
    return s


GRAPHQL_ENDPOINT = "https://leetcode.cn/graphql"


def gql(session: requests.Session, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    resp = session.post(GRAPHQL_ENDPOINT, json={"query": query, "variables": variables}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


Q_LIST = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total
    questions {
      acRate
      difficulty
      freqBar
      frontendQuestionId
      isFavor
      paidOnly
      status
      title
      titleCn
      titleSlug
      topicTags { name slug }
      hasSolution
      hasVideoSolution
    }
  }
}
"""


Q_ONE = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    translatedTitle
    title
    titleSlug
    difficulty
    content
    translatedContent
    similarQuestions
    topicTags { name slug }
    companyTagStats
    codeSnippets { lang langSlug code }
    mysqlSchemas
  }
}
"""


def iter_all_slugs(session: requests.Session, limit: int = 100) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    skip = 0
    total = None
    while True:
        data = gql(session, Q_LIST, {
            "categorySlug": "all-code-essentials",
            "limit": limit,
            "skip": skip,
            "filters": {},
        })
        lst = data["problemsetQuestionList"]["questions"]
        if total is None:
            total = data["problemsetQuestionList"]["total"]
        results.extend(lst)
        skip += len(lst)
        if not lst or (total is not None and skip >= total):
            break
        # polite delay to avoid rate limit
        time.sleep(0.2)
    return results


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_markdown(md_dir: str, q: Dict[str, Any]) -> str:
    from export_lcpr_markdown import html_to_markdown  # reuse converter

    qid = q.get("questionFrontendId") or q.get("questionId") or ""
    slug = q.get("titleSlug") or ""
    cn_name = q.get("translatedTitle") or q.get("title") or ""
    en_name = q.get("title") or ""
    link = f"https://leetcode.cn/problems/{slug}/description/" if slug else ""
    level = q.get("difficulty") or ""
    category = "algorithms"
    desc_html = q.get("translatedContent") or q.get("content") or ""

    title_line = f"# {qid}. {cn_name}"
    if en_name:
        title_line += f" ({en_name})"

    header_lines = [title_line, ""]
    if link:
        header_lines.append(f"- 链接: [{link}]({link})")
    if level:
        header_lines.append(f"- 难度: {level}")
    if category:
        header_lines.append(f"- 分类: {category}")
    header = "\n".join(header_lines).rstrip() + "\n\n---\n\n"

    body_md = html_to_markdown(desc_html)

    ensure_dir(md_dir)
    out_name = f"{qid}.{slug}.md" if qid and slug else (slug or str(qid) or "problem") + ".md"
    out_path = os.path.join(md_dir, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(body_md)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Fetch ALL LeetCode problems from leetcode.cn and export Markdown")
    parser.add_argument("--user-json", default=os.path.expanduser("~/.lcpr/leetcode/user.json"))
    parser.add_argument("--out-dir", default=os.path.expanduser("~/.lcpr/problems_markdown_all"))
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    cookies = load_auth(args.user_json)
    session = build_session(cookies)

    print("Listing all problems...")
    problems = iter_all_slugs(session, limit=args.limit)
    print(f"Found {len(problems)} problems")

    exported = 0
    for i, item in enumerate(problems, 1):
        slug = item.get("titleSlug")
        if not slug:
            continue
        try:
            data = gql(session, Q_ONE, {"titleSlug": slug})
            q = data["question"]
            save_markdown(args.out_dir, q)
            exported += 1
        except Exception as e:
            print(f"Failed {slug}: {e}")
        if i % 20 == 0:
            print(f"Progress: {i}/{len(problems)} (exported {exported})")
            # mild delay to avoid throttling
            time.sleep(0.3)

    print(f"Done. Exported {exported} markdown files to {args.out_dir}")


if __name__ == "__main__":
    # Ensure local import works
    sys.path.insert(0, THIS_DIR)
    main()


