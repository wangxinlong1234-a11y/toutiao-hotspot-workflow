#!/usr/bin/env python3
"""选题评分脚本：对公开采集的候选选题按多维度打分并输出排名。

各维度取值 1-5：
  timeliness          时效性
  heat_signal         热度信号（榜单/可见指标，非单篇阅读量）
  reader_interest     读者兴趣
  source_reliability  资料可靠性
  original_space      原创发挥空间
"""
import csv
import sys
from pathlib import Path

WEIGHTS = {
    "timeliness": 0.25,
    "heat_signal": 0.25,
    "reader_interest": 0.20,
    "source_reliability": 0.15,
    "original_space": 0.15,
}

DIMENSIONS = list(WEIGHTS.keys())


def score_row(row, weights=WEIGHTS):
    """根据各维度 1-5 分计算加权总分（最高 5.0）。"""
    total = 0.0
    for key, w in weights.items():
        try:
            val = float(row.get(key, 0) or 0)
        except (ValueError, TypeError):
            val = 0.0
        total += w * max(0.0, min(5.0, val))
    return round(total, 3)


def load_candidates(path):
    # 使用 utf-8-sig 兼容带 BOM 的 CSV（Windows 记事本常用）
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def rank(candidates, weights=WEIGHTS, top_n=3):
    scored = []
    for row in candidates:
        item = dict(row)
        item["_score"] = score_row(row, weights)
        scored.append(item)
    scored.sort(key=lambda x: x["_score"], reverse=True)
    return scored[:top_n]


def write_ranked_csv(candidates, out_path, weights=WEIGHTS):
    """将全部候选按评分排序后写出 CSV（含 _score 列）。"""
    scored = []
    for row in candidates:
        item = dict(row)
        item["_score"] = score_row(row, weights)
        scored.append(item)
    scored.sort(key=lambda x: x["_score"], reverse=True)
    fields = list(scored[0].keys()) if scored else list(DIMENSIONS) + ["_score"]
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(scored)
    return out_path


def main(argv):
    if len(argv) < 2:
        print("用法: python score_topics.py <candidates.csv> [top_n] [ranked_out.csv]")
        return 1
    path = Path(argv[1])
    if not path.exists():
        print(f"找不到文件: {path}")
        return 1
    top_n = int(argv[2]) if len(argv) > 2 else 3
    ranked_out = argv[3] if len(argv) > 3 else None
    candidates = load_candidates(path)
    if not candidates:
        print("候选列表为空，请先采集数据。")
        return 1
    if ranked_out:
        out = write_ranked_csv(candidates, ranked_out)
        print(f"已写出排名 CSV: {out}（共 {len(candidates)} 条）\n")
    top = rank(candidates, top_n=top_n)
    print(f"共 {len(candidates)} 条候选，推荐前 {len(top)} 名：\n")
    for i, item in enumerate(top, 1):
        print(f"{i}. {item.get('title', '(无标题)')}")
        print(f"   评分: {item['_score']}  来源: {item.get('source', '')}  排名: {item.get('rank', '')}")
        print(f"   链接: {item.get('url', '')}")
        if item.get("rationale"):
            print(f"   理由: {item['rationale']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
