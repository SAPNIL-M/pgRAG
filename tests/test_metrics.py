from eval.metrics import hit_rate_at_k, mrr_at_k


def test_rank_1_hit():
    retrieved = [10, 20, 30]
    targets = [10]
    assert hit_rate_at_k(retrieved, targets, k=3) == 1.0
    assert mrr_at_k(retrieved, targets, k=3) == 1.0


def test_rank_2_hit():
    retrieved = [20, 10, 30]
    targets = [10]
    assert hit_rate_at_k(retrieved, targets, k=3) == 1.0
    assert mrr_at_k(retrieved, targets, k=3) == 0.5


def test_hit_beyond_k():
    retrieved = [20, 30, 10]
    targets = [10]
    assert hit_rate_at_k(retrieved, targets, k=2) == 0.0
    assert mrr_at_k(retrieved, targets, k=2) == 0.0


def test_complete_miss():
    retrieved = [20, 30, 40]
    targets = [10]
    assert hit_rate_at_k(retrieved, targets, k=3) == 0.0
    assert mrr_at_k(retrieved, targets, k=3) == 0.0


def test_multiple_targets_first_hit_counts():
    retrieved = [50, 10, 20]
    targets = [20, 10]
    assert hit_rate_at_k(retrieved, targets, k=3) == 1.0
    assert mrr_at_k(retrieved, targets, k=3) == 0.5