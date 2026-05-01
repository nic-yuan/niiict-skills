# niiict.art - AI Skills Portfolio

AI 技能包作品集，自动同步更新。

## 品牌

- **Apollo OS** — AI 个人操作系统（11个模块）
- **Inter-Control** — 企业内控系列（7个模块）
- **Local** — 社区团购系列（10个模块）
- **Vertical** — 垂直工具

## 自动更新机制

每次 push 到 `brands/` 目录，GitHub Actions 自动：
1. 运行 `scripts/generate-index.py` 生成 `index.html`
2. 提交并推送到 `gh-pages` 分支
3. niict.art 自动展示最新内容

## 本地调试

```bash
python3 scripts/generate-index.py
```

## 发布新 Skill

```bash
# 把新 skill 放到对应品牌目录
cp -r /path/to/new-skill brands/apollo/

# 提交推送，自动更新网页
git add brands/ && git commit -m "Add new Apollo skill" && git push
```