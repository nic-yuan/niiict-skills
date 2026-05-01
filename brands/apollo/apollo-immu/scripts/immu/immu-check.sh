#!/bin/bash
# immu-check.sh - 免疫防御检测

STATE_FILE="/root/.openclaw/workspace/.immu/state.json"
TRUST_FILE="/root/.openclaw/workspace/.immu/trust-state.json"
mkdir -p "$(dirname "$STATE_FILE")"

# 检查最近的风险拦截
check_recent_blocks() {
    local log_file="/root/.openclaw/workspace/logs/immu.log"
    if [ -f "$log_file" ]; then
        tail -20 "$log_file" 2>/dev/null | grep -c "BLOCK\|ALLOW" || echo 0
    else
        echo 0
    fi
}

# 检查信任计数
check_trust_count() {
    if [ -f "$TRUST_FILE" ]; then
        python3 -c "import json; d=json.load(open('$TRUST_FILE')); print(len(d.get('trusted', [])))" 2>/dev/null || echo 0
    else
        echo 0
    fi
}

# 检查危险操作日志
check_dangerous_ops() {
    local log_file="/root/.openclaw/workspace/logs/immu.log"
    if [ -f "$log_file" ]; then
        tail -50 "$log_file" 2>/dev/null | grep -cE "delete|rm |sudo|exec.*rm" || echo 0
    else
        echo 0
    fi
}

# 检查白名单
check_whitelist() {
    local whitelist_file="/root/.openclaw/workspace/.immu/whitelist.json"
    if [ -f "$whitelist_file" ]; then
        python3 -c "import json; d=json.load(open('$whitelist_file')); print(len(d.get('commands', [])))" 2>/dev/null || echo 0
    else
        echo 0
    fi
}

# 评估免疫状态
eval_immu_status() {
    local blocks=$1
    local trust=$2
    local dangerous=$3
    local whitelist=$4
    
    local score=3
    [ $blocks -gt 10 ] && ((score--))
    [ $trust -lt 3 ] && ((score--))
    [ $dangerous -gt 5 ] && ((score--))
    [ $whitelist -eq 0 ] && ((score--))
    
    [ $score -lt 0 ] && score=0
    echo $score
}

# 主函数
main() {
    local blocks=$(check_recent_blocks)
    local trust=$(check_trust_count)
    local dangerous=$(check_dangerous_ops)
    local whitelist=$(check_whitelist)
    local score=$(eval_immu_status $blocks $trust $dangerous $whitelist)
    
    echo "🛡️ [apollo-immu] 免疫状态报告"
    echo ""
    echo "防御状态："
    echo "  - 最近拦截/放行：${blocks}次"
    echo "  - 信任实体数：${trust}个"
    echo "  - 危险操作日志：${dangerous}次"
    echo "  - 白名单规则：${whitelist}条"
    echo ""
    
    if [ $score -ge 3 ]; then
        echo "🟢 免疫状态正常"
    elif [ $score -ge 1 ]; then
        echo "🟡 免疫需要关注"
    else
        echo "🔴 免疫状态异常"
    fi
    
    # 保存状态
    cat > "$STATE_FILE" << EOF
{
    "recent_blocks": $blocks,
    "trust_count": $trust,
    "dangerous_ops": $dangerous,
    "whitelist_rules": $whitelist,
    "immu_score": $score,
    "checked_at": "$(date -Iseconds)"
}
EOF
}

main
