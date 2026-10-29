#!/usr/bin/env python3
"""选题评分逻辑的单元测试。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from score_topics import score_row, rank, WEIGHTS, DIMENSIONS  # noqa: E402


def test_score_range():
    high = {k: 5 for k in DIMENSIONS}
    low = {k: 1 for k in DIMENSIONS}
    assert score_row(high) > score_row(low)
    assert 0.0 <= score_row(high) <= 5.0


def test_missing_dimension_treated_as_zero():
    partial = {"timeliness": 5}
    val = score_row(partial)
    assert val == round(WEIGHTS["timeliness"] * 5, 3)


def test_rank_returns_top_n():
    cands = [
        {"title": "低分", **{k: 1 for k in DIMENSIONS}},
        {"title": "高分", **{k: 5 for k in DIMENSIONS}},
        {"title": "中分", **{k: 3 for k in DIMENSIONS}},
    ]
    top = rank(cands, top_n=1)
    assert top[0]["title"] == "高分"
    assert len(rank(cands, top_n=2)) == 2


if __name__ == "__main__":
    test_score_range()
    test_missing_dimension_treated_as_zero()
    test_rank_returns_top_n()
    print("全部测试通过")
