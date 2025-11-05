#!/usr/bin/env python3
"""
更新README文件中的题目链接，使用正确的slug
"""

import os
import re
from pathlib import Path

def get_slug_from_cache(problem_id: str) -> str:
    """从缓存文件中获取slug"""
    cache_file = Path(f"leetcode/cache/{problem_id}.two-sum.algorithms.json")
    if cache_file.exists():
        import json
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('slug', '')
    
    # 尝试其他可能的文件名
    cache_dir = Path("leetcode/cache")
    for f in cache_dir.glob(f"{problem_id}.*.algorithms.json"):
        import json
        with open(f, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('slug', '')
    return ''

def update_readme_slug(readme_path: Path):
    """更新README中的slug"""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取题目编号
        match = re.search(r'^# (\d+)\.', content)
        if not match:
            return False
        
        problem_id = match.group(1)
        
        # 从缓存获取slug
        slug = get_slug_from_cache(problem_id)
        if not slug:
            # 尝试从文件夹名提取
            folder_name = readme_path.parent.name
            if '.' in folder_name:
                slug = folder_name.split('.', 1)[1]
        
        # 更新链接
        old_pattern = r'https://leetcode\.cn/problems/[^/]+/'
        new_link = f'https://leetcode.cn/problems/{slug}/'
        
        if re.search(old_pattern, content):
            content = re.sub(old_pattern, new_link, content)
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"错误处理 {readme_path}: {e}")
    return False

def main():
    base_dir = Path('.')
    updated = 0
    
    for readme in base_dir.rglob('**/README.md'):
        if 'leetcode' in str(readme) or '.lcpr_data' in str(readme):
            continue
        if update_readme_slug(readme):
            updated += 1
            print(f"✅ 更新: {readme}")
    
    print(f"\n共更新 {updated} 个README文件")

if __name__ == '__main__':
    main()

