#!/usr/bin/env python3
import os
import sys
import json
import time
import re
import argparse
from typing import Dict, Any, List

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
    if cookies:
        s.cookies.update(cookies)
    # If no csrftoken provided, fetch homepage to obtain one
    if not s.cookies.get("csrftoken"):
        try:
            r = s.get("https://leetcode.cn", timeout=15)
            r.raise_for_status()
        except Exception:
            pass
    # Set x-csrftoken header if present
    if s.cookies.get("csrftoken") and not s.headers.get("x-csrftoken"):
        s.headers["x-csrftoken"] = s.cookies.get("csrftoken")
    return s


GRAPHQL_ENDPOINT = "https://leetcode.cn/graphql"
API_PROBLEMS_ALL = "https://leetcode.cn/api/problems/all/"


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
      frontendQuestionId
      title
      titleCn
      titleSlug
      paidOnly
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
    codeSnippets { lang langSlug code }
  }
}
"""


def iter_all(session: requests.Session, limit: int = 100) -> List[Dict[str, Any]]:
    """Return a list of problem list items with keys: titleSlug, frontendQuestionId, titleCn, difficulty, acRate, paidOnly.

    Prefer public problems API (no auth). Fallback to GraphQL if needed.
    """
    # Try public API first (no auth required)
    try:
        r = session.get(API_PROBLEMS_ALL, timeout=30)
        r.raise_for_status()
        payload = r.json()
        stat_status_pairs = payload.get("stat_status_pairs") or []
        results: List[Dict[str, Any]] = []
        for it in stat_status_pairs:
            stat = it.get("stat") or {}
            difficulty_level = (it.get("difficulty") or {}).get("level")
            diff_map = {1: "Easy", 2: "Medium", 3: "Hard"}
            results.append({
                "acRate": it.get("acRate"),
                "difficulty": diff_map.get(difficulty_level, ""),
                "frontendQuestionId": str(stat.get("frontend_question_id") or ""),
                "title": stat.get("question__title") or "",
                "titleCn": stat.get("question__title") or "",
                "titleSlug": stat.get("question__title_slug") or "",
                "paidOnly": bool(it.get("paid_only")),
            })
        return results
    except Exception:
        pass

    # Fallback to GraphQL (may require auth)
    results: List[Dict[str, Any]] = []
    skip = 0
    total = None
    while True:
        variables = {
            "categorySlug": "all-code-essentials",
            "limit": limit,
            "skip": skip,
            "filters": {},
        }
        try:
            data = gql(session, Q_LIST, variables)
        except Exception:
            variables["categorySlug"] = "algorithms"
            data = gql(session, Q_LIST, variables)
        page = data["problemsetQuestionList"]["questions"]
        if total is None:
            total = data["problemsetQuestionList"]["total"]
        results.extend(page)
        skip += len(page)
        if not page or (total is not None and skip >= total):
            break
        time.sleep(0.2)
    return results

def fetch_detail_via_page(session: requests.Session, slug: str) -> Dict[str, Any]:
    """Fetch problem detail without GraphQL by parsing __NEXT_DATA__ from HTML page."""
    url = f"https://leetcode.cn/problems/{slug}/description/"
    r = session.get(url, timeout=30)
    r.raise_for_status()
    html = r.text
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        raise RuntimeError("__NEXT_DATA__ not found")
    data = json.loads(m.group(1))
    # Try several known paths for question data
    # 1) dehydrated React Query state
    queries = (((data.get("props") or {}).get("pageProps") or {}).get("dehydratedState") or {}).get("queries") or []
    for it in queries:
        st = it.get("state") or {}
        if isinstance(st, dict):
            for v in st.values():
                if isinstance(v, dict) and (v.get("questionId") or v.get("questionFrontendId") or v.get("titleSlug")):
                    return v
    # 2) legacy questionData path
    legacy = (((data.get("props") or {}).get("pageProps") or {}).get("questionData"))
    if legacy:
        return legacy
    raise RuntimeError("question detail not found in __NEXT_DATA__")


def to_cache_json(list_item: Dict[str, Any], detail: Dict[str, Any]) -> Dict[str, Any]:
    # Map fields to mimic *.algorithms.json in ~/.lcpr/leetcode/cache
    fid = str(detail.get("questionFrontendId") or list_item.get("frontendQuestionId") or "")
    slug = detail.get("titleSlug") or list_item.get("titleSlug") or ""
    cn_name = detail.get("translatedTitle") or list_item.get("titleCn") or ""
    en_name = detail.get("title") or list_item.get("title") or ""
    difficulty = detail.get("difficulty") or list_item.get("difficulty") or ""
    desc_html = detail.get("translatedContent") or detail.get("content") or ""
    ac_rate = list_item.get("acRate")

    obj = {
        "id": int(fid) if fid.isdigit() else fid,
        "fid": fid,
        "name": cn_name or en_name,
        "slug": slug,
        "link": f"https://leetcode.cn/problems/{slug}/description/" if slug else "",
        "percent": ac_rate if ac_rate is not None else 0,
        "level": difficulty,
        "category": "algorithms",
        "en_name": en_name,
        "cn_name": cn_name or en_name,
        "desc": desc_html,
    }

    # Templates from codeSnippets (best effort)
    snippets = (detail.get("codeSnippets") or [])
    templates = []
    for sn in snippets:
        lang_slug = (sn.get("langSlug") or "").lower()
        lang_text = sn.get("lang") or lang_slug
        templates.append({
            "value": lang_slug,
            "text": lang_text,
            "defaultCode": sn.get("code") or "",
        })
    if templates:
        obj["templates"] = templates

    return obj


def main():
    parser = argparse.ArgumentParser(description="Fetch ALL LeetCode problems to ~/.lcpr/leetcode/cache JSON")
    parser.add_argument("--user-json", default=os.path.expanduser("~/.lcpr/leetcode/user.json"))
    parser.add_argument("--cache-dir", default=os.path.expanduser("~/.lcpr/leetcode/cache"))
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    os.makedirs(args.cache_dir, exist_ok=True)

    cookies = load_auth(args.user_json)
    session = build_session(cookies)

    print("Listing all problems...")
    problems = iter_all(session, limit=args.limit)
    print(f"Found {len(problems)} problems")

    # Save/refresh problems.json (raw list from GraphQL list)
    problems_json_path = os.path.join(args.cache_dir, "problems.json")
    with open(problems_json_path, "w", encoding="utf-8") as f:
        json.dump({"problems": problems}, f, ensure_ascii=False)
    print(f"Updated {problems_json_path}")

    exported = 0
    for i, item in enumerate(problems, 1):
        slug = item.get("titleSlug")
        if not slug:
            continue
        # 跳过付费题（未登录获取不到完整描述）
        if item.get("paidOnly"):
            continue
        try:
            # 先尝试页面解析（无需登录）
            # 先构造目标文件名，便于跳过已存在文件
            tentative_fid = str(item.get("frontendQuestionId") or "").strip()
            tentative_slug = slug
            tentative_name = f"{tentative_fid}.{tentative_slug}.algorithms.json" if tentative_fid and tentative_slug else f"{tentative_slug or tentative_fid}.algorithms.json"
            out_path = os.path.join(args.cache_dir, tentative_name)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                # 已存在则跳过，加快续跑
                continue

            retries = 3
            q = None
            for attempt in range(1, retries + 1):
                try:
                    q = fetch_detail_via_page(session, slug)
                    break
                except Exception:
                    # 回退到 GraphQL，并设置 Referer
                    old_ref = session.headers.get("Referer")
                    session.headers["Referer"] = f"https://leetcode.cn/problems/{slug}/description/"
                    try:
                        data = gql(session, Q_ONE, {"titleSlug": slug})
                        q = data["question"]
                        break
                    except Exception:
                        if attempt == retries:
                            raise
                        time.sleep(0.5 * attempt)
                    finally:
                        if old_ref is not None:
                            session.headers["Referer"] = old_ref
                        else:
                            session.headers.pop("Referer", None)

            cache_obj = to_cache_json(item, q)
            fid = str(cache_obj.get("fid") or cache_obj.get("id") or "").strip()
            file_slug = cache_obj.get("slug") or slug
            name = f"{fid}.{file_slug}.algorithms.json" if fid and file_slug else f"{file_slug or fid}.algorithms.json"
            out_path = os.path.join(args.cache_dir, name)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(cache_obj, f, ensure_ascii=False)
            exported += 1
        except Exception as e:
            print(f"Failed {slug}: {e}")
        if i % 20 == 0:
            print(f"Progress: {i}/{len(problems)} (exported {exported})")
            time.sleep(0.3)

    print(f"Done. Exported {exported} cache files to {args.cache_dir}")


if __name__ == "__main__":
    sys.path.insert(0, THIS_DIR)
    main()


