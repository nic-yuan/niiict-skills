#!/usr/bin/env python3
"""
density-detector.py - 信息密度检测
"""
import re

HIGH = [r'决定|决策|结论', r'任务|下一步', r'\d+[./年]']
LOW = [r'^哈+|^嗯', r'对|好的']

def calculate_density(text):
    if not text:
        return 0.0
    high = sum(len(re.findall(p, text)) for p in HIGH)
    low = sum(len(re.findall(p, text)) for p in LOW)
    return min(1.0, high * 2 / max(len(text), 100))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        d = calculate_density(sys.argv[1])
        print(f"密度: {d:.3f}")
