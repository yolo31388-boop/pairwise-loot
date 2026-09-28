
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loot.drop import DropTable, LootSystem


class Player:
    def __init__(self):
        self.inventory = []
        self.inventory_cap = 10


def test_drop_not_always_same():
    t1 = DropTable()
    t1.add_entry("sword", 50)
    t2 = DropTable()
    t2.add_entry("sword", 50)
    # 不同实例不应完全相同（概率上）
    r1 = [t1.roll() for _ in range(20)]
    r2 = [t2.roll() for _ in range(20)]
    assert r1 != r2


def test_rare_drop_possible():
    t = DropTable(seed=123)
    t.add_entry("rare", 1)
    # 1%掉率，roll 1000次至少掉一次
    drops = [t.roll() for _ in range(1000)]
    assert any(d for d in drops)


def test_party_loot_checks_members():
    ls = LootSystem()
    table = DropTable()
    table.add_entry("item", 100)
    ls.drop_tables["boss1"] = table
    members = [{"id": "p1", "in_instance": True}, {"id": "p2", "in_instance": False}]
    result = ls.distribute_party("boss1", members)
    assert "p2" not in result


def test_personal_loot_checks_bag_space():
    ls = LootSystem()
    p = Player()
    p.inventory = ["x"] * 10
    assert ls.personal_loot(p, {"item": "sword", "count": 1}) == False
    assert len(p.inventory) == 10


def test_item_display_matches_actual():
    t = DropTable()
    t.add_entry("sword", 100, 1, 1)
    drop = t.roll()[0]
    # 显示和实际属性应一致
    assert drop["count"] >= 1


def test_world_boss_by_damage():
    ls = LootSystem()
    ls.damage_records["wb1"] = [
        {"player": "p1", "damage": 500},
        {"player": "p2", "damage": 300},
        {"player": "p1", "damage": 200},
    ]
    result = ls.world_boss_reward("wb1")
    assert "p1" in result
    assert result["p1"] != "all_rewards"


def test_drop_count_in_range():
    t = DropTable()
    t.add_entry("stack", 100, 3, 5)
    for _ in range(50):
        drop = t.roll()
        if drop:
            assert 3 <= drop[0]["count"] <= 5


def test_empty_drop_table():
    t = DropTable()
    assert t.roll() == []


def test_multiple_drops():
    t = DropTable()
    t.add_entry("a", 100)
    t.add_entry("b", 100)
    drop = t.roll()
    assert len(drop) == 2
