#!/bin/bash
# dream-check.sh - 做梦记忆机制检测

STATE_FILE="/root/.openclaw/workspace/.dream/state.json"
TASK_FILE="/root/.openclaw/workspace/.dream/task-state.json"
TOPIC_FILE="/root/.openclaw/workspace/.dream/topic-state.json"
FRAG_FILE="/tmp/.dream-trigger"
mkdir -p "$(dirname "$STATE_FILE")"

# 检查碎片化指标
check_fragmentation() {
    local tasks=0
    local topics=0
    local stale=0
    
    if [ -f "$TASK_FILE" ]; then
        local t=$(grep -c '"status"' "$TASK_FILE" 2>/dev/null)
        [ -n "$t" ] && tasks=$t
        local s=$(grep -c 'stale' "$TASK_FILE" 2>/dev/null)
        [ -n "$s" ] && stale=$s
    fi
    
    if [ -f "$TOPIC_FILE" ]; then
        local m=$(grep -c '"status"' "$TOPIC_FILE" 2>/dev/null)
        [ -n "$m" ] && topics=$m
    fi
    
    echo "$tasks|$topics|$stale"
}

# 检查触发标志
check_trigger() {
    if [ -f "$FRAG_FILE" ]; then
        echo "triggered"
    else
        echo "idle"
    fi
}

# 检查token估算
check_token_usage() {
    local today_file="/root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md"
    if [ -f "$today_file" ]; then
        local chars=$(wc -c < "$today_file" 2>/dev/null || echo 0)
        echo $((chars / 2))  # 粗略估算
    else
        echo 0
    fi
}

# 评估做梦需求
eval_dream_need() {
    local tasks=$1
    local topics=$2
    local stale=$3
    local tokens=$4
    local trigger=$5
    
    local score=0
    [ $tasks -gt 3 ] && ((score++))
    [ $topics -gt 3 ] && ((score++))
    [ $stale -gt 2 ] && ((score++))
    [ $tokens -gt 30000 ] && ((score++))
    [ "$trigger" = "triggered" ] && ((score++))
    
    echo $score
}

# 主函数
main() {
    local frag_info=$(check_fragmentation)
    local tasks=$(echo "$frag_info" | cut -d'|' -f1)
    local topics=$(echo "$frag_info" | cut -d'|' -f2)
    local stale=$(echo "$frag_info" | cut -d'|' -f3)
    local trigger=$(check_trigger)
    local tokens=$(check_token_usage)
    local score=$(eval_dream_need $tasks $topics $stale $tokens "$trigger")
    
    echo "🌙 [apollo-dream] 做梦状态报告"
    echo ""
    echo "记忆状态："
    echo "  - 进行中任务：${tasks}个"
    echo "  - 活跃话题：${topics}个"
    echo "  - 停滞任务：${stale}个"
    echo "  - Token估算：$tokens"
    echo "  - 触发标志：$trigger"
    echo ""
    
    if [ $score -ge 4 ]; then
        echo "🔴 需要深度做梦"
    elif [ $score -ge 2 ]; then
        echo "🟡 建议轻量整理"
    else
        echo "🟢 记忆状态正常"
    fi
    
    # 保存状态
    cat > "$STATE_FILE" << EOF
{
    "tasks": $tasks,
    "topics": $topics,
    "stale": $stale,
    "tokens": $tokens,
    "trigger": "$trigger",
    "dream_need_score": $score,
    "needs_dream": $([ $score -ge 2 ] && echo "true" || echo "false"),
    "checked_at": "$(date -Iseconds)"
}
EOF
}

main
