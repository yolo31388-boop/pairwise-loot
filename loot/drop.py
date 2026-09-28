
import random

class DropTable:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.entries = []

    def add_entry(self, item_id, chance, min_count=1, max_count=1):
        self.entries.append({"item": item_id, "chance": chance, "min": min_count, "max": max_count})

    def roll(self):
        # BUG: 固定种子，每次一样
        results = []
        for e in self.entries:
            # BUG: 整数除法，1%算成0
            if self.rng.randint(1, 100) <= int(e["chance"]):
                count = self.rng.randint(e["min"], e["max"])
                results.append({"item": e["item"], "count": count})
        return results


class LootSystem:
    def __init__(self):
        self.drop_tables = {}
        self.damage_records = {}

    def distribute_party(self, boss_id, members):
        table = self.drop_tables.get(boss_id)
        if not table:
            return []
        drops = table.roll()
        # BUG: 不检查是否在副本内
       分配 = {}
        for i, drop in enumerate(drops):
            member = members[i % len(members)]
            分配[member] = drop
        return 分配

    def personal_loot(self, player, drop):
        # BUG: 不检查背包空间
        player.inventory.append(drop)
        return True

    def world_boss_reward(self, boss_id):
        # BUG: 最后一刀拿全部
        if self.damage_records.get(boss_id):
            last = self.damage_records[boss_id][-1]
            return {last["player"]: "all_rewards"}
        return {}
