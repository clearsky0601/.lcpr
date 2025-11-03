#!/bin/bash
# 修复 LeetCode Problem Rating 扩展的 HOME 目录问题
# 当扩展更新后，如果问题再次出现，运行此脚本即可

EXTENSION_DIR="$HOME/.cursor/extensions/ccagml.vscode-leetcode-problem-rating-*"
STORAGE_UTILS_FILE="out/src/rpc/utils/storageUtils.js"

echo "🔧 正在修复 LeetCode Problem Rating 扩展..."

# 查找扩展目录
EXT_PATH=$(ls -d $EXTENSION_DIR 2>/dev/null | head -1)

if [ -z "$EXT_PATH" ]; then
    echo "❌ 未找到扩展目录: $EXTENSION_DIR"
    exit 1
fi

echo "✅ 找到扩展目录: $EXT_PATH"

FILE_PATH="$EXT_PATH/$STORAGE_UTILS_FILE"

if [ ! -f "$FILE_PATH" ]; then
    echo "❌ 未找到文件: $FILE_PATH"
    exit 1
fi

# 检查是否已经修复过
if grep -q "os.homedir()" "$FILE_PATH"; then
    echo "✅ 扩展已经修复过，无需再次修复"
    exit 0
fi

# 备份原文件
BACKUP_FILE="${FILE_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$FILE_PATH" "$BACKUP_FILE"
echo "📦 已创建备份: $BACKUP_FILE"

# 修复代码
sed -i '' 's/return process\.env\.HOME || process\.env\.USERPROFILE;/return process.env.HOME || process.env.USERPROFILE || os.homedir();/' "$FILE_PATH"

if grep -q "os.homedir()" "$FILE_PATH"; then
    echo "✅ 修复成功！"
    echo ""
    echo "⚠️  注意：如果扩展更新，可能需要重新运行此脚本"
else
    echo "❌ 修复失败，正在恢复备份..."
    mv "$BACKUP_FILE" "$FILE_PATH"
    exit 1
fi


