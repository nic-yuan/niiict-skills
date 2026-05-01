#!/usr/bin/env python3
"""compressor.py - 三层做梦压缩"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def compress(text, layer=None):
    if not text:
        return text, 0
    tokens = len(text) // 4  # rough estimate
    if layer is None:
        layer = 1 if tokens > 50000 else 0
    if layer == 1:
        return "[Microcompact] " + text[:100], 1
    return text, layer

if __name__ == '__main__':
    test = "测试压缩功能" * 10
    result, layer = compress(test)
    print(f"Layer {layer}: {result[:50]}")
