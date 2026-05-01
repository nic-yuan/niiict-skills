#!/usr/bin/env python3
"""
token-estimator.py - 快速Token估算
"""
import re

def count_tokens(text):
    if not text:
        return 0
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    other_chars = len(re.findall(r'[^\w\s]', text))
    return int(chinese_chars * 1.5 + english_words * 0.75 + other_chars / 4)

def estimate_tokens_from_text(text):
    return count_tokens(text)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(f"Token数: {count_tokens(sys.argv[1])}")
