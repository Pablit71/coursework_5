from dataclasses import dataclass, field
from typing import List
from random import uniform

import marshmallow
import marshmallow_dataclass
import json


@dataclass
class Armor:
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


ArmorSchema = marshmallow_dataclass.class_schema(Armor)


@dataclass
class Weapon:
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    class Meta:
        unknown = marshmallow.EXCLUDE

    def calculate_damage(self):
        return uniform(self.min_damage, self.max_damage)


WeaponSchema = marshmallow_dataclass.class_schema(Weapon)


@dataclass
class EquipmentData:
    weapons: list = field(default_factory=list)
    armor: list = field(default_factory=list)


class Equipment:
    def __init__(self, filename: str):
        self.filename = filename
        self.equipment: EquipmentData = self._create_equipment()

    def _create_equipment(self) -> EquipmentData:
        with open(self.filename, encoding='utf-8') as file:
            data = json.load(file)

            return EquipmentData(
                weapons=WeaponSchema(many=True).load(data['weapons']),
                armor=ArmorSchema(many=True).load(data['armors']))

    def get_weapon(self, weapon_name: str) -> Weapon:
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                weapon_to_equip = weapon
        return weapon_to_equip

    def get_weapon_names(self) -> List[Weapon]:
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armor(self, armor_name: str) -> Armor:
        for armor in self.equipment.armor:
            if armor.name == armor_name:
                armor_to_equip = armor
        return armor_to_equip

    def get_armor_names(self) -> List[Armor]:
        return [armor.name for armor in self.equipment.armor]
