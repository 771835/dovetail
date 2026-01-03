# coding=utf-8

class ReturnBuilder:
    @staticmethod
    def return_null():
        return "return"

    @staticmethod
    def return_value(value):
        return f"return {value}"

    @staticmethod
    def return_fail():
        return "return fail"

    @staticmethod
    def return_run(command):
        return f"return {command}"
