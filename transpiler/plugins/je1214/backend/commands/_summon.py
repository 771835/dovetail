# coding=utf-8

class SummonBuilder:
    @staticmethod
    def summon(entity: str, x: float | int, y: float | int, z: float | int, nbt: str):
        return f"summon {entity} {x} {y} {z} {nbt}"
