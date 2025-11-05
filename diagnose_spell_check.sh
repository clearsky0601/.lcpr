#!/bin/bash
# 诊断拼写检查问题的脚本

echo "🔍 诊断 Cursor 拼写检查问题..."
echo ""

echo "1. 检查已安装的拼写检查相关扩展："
echo "-----------------------------------"
code --list-extensions | grep -i spell
echo ""

echo "2. 检查配置文件："
echo "-----------------------------------"
if [ -f ".vscode/settings.json" ]; then
    echo "✅ .vscode/settings.json 存在"
    echo "拼写检查相关配置："
    grep -i "spell\|cSpell" .vscode/settings.json || echo "  未找到相关配置"
else
    echo "❌ .vscode/settings.json 不存在"
fi
echo ""

if [ -f ".cspell.json" ]; then
    echo "✅ .cspell.json 存在"
else
    echo "❌ .cspell.json 不存在"
fi
echo ""

echo "3. 建议的解决方案："
echo "-----------------------------------"
echo "请按照以下步骤操作："
echo ""
echo "方法1: 禁用所有拼写检查扩展"
echo "  1. 按 Cmd+Shift+X 打开扩展面板"
echo "  2. 搜索 'spell' 或 '拼写'"
echo "  3. 禁用所有拼写检查相关的扩展"
echo ""
echo "方法2: 检查 Cursor 设置"
echo "  1. 按 Cmd+, 打开设置"
echo "  2. 搜索 'spell'"
echo "  3. 禁用所有拼写检查相关的选项"
echo ""
echo "方法3: 重新加载窗口"
echo "  1. 按 Cmd+Shift+P"
echo "  2. 输入 'Reload Window'"
echo "  3. 选择 'Developer: Reload Window'"
echo ""
echo "如果问题仍然存在，请告诉我具体的错误信息或截图。"









