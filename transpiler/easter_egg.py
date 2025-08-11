# coding=utf-8
import random
import sys
import time

from transpiler.core.enums import DataType, ValueType
from transpiler.core.errors import CompilationError
from transpiler.core.instructions import IRInstruction
from transpiler.core.ir_generator import MCGenerator
from transpiler.core.result import Result
from transpiler.core.symbols import Reference, Literal
from transpiler.utils.mixin_manager import Mixin, At, Inject, CallbackInfoReturnable


@Mixin(IRInstruction)
class IRInstructionMixin:
    """指令改名Mixin"""

    @staticmethod
    @Inject("__repr__", At(At.RETURN), cancellable=True)
    def repr_injection(ci: CallbackInfoReturnable, self):
        # 给指令添加有趣的前缀
        names = {
            "JUMP": "🌟 JUMP",
            "CALL": "📞 CALL",
            "RETURN": "↩️ RETURN"
        }
        name = self.opcode.name
        return ci.set_return_value(names.get(name, f"✨ {name}") + ci.return_value.split(name)[1])


@Mixin(MCGenerator)
class SpecialEasterEggMixin:
    """特殊模式彩蛋Mixin"""

    @staticmethod
    @Inject("visitLiteral", At(At.HEAD))
    def literal_injection(ci, self, ctx):
        # 检测到特定数字序列时激活
        if ctx.getText() == "404259":
            print("\n🔥 恭喜发现隐藏模式！所有表达式值自动翻倍")
            SpecialEasterEggMixin.easter_egg_mode = True

    @staticmethod
    @Inject("visitLiteral", At(At.RETURN), cancellable=True)
    def literal_value_injection(ci, self, ctx):
        # 隐藏模式：所有数字翻倍
        if hasattr(SpecialEasterEggMixin, 'easter_egg_mode') and SpecialEasterEggMixin.easter_egg_mode:
            if ci.return_value and ci.return_value.value.get_data_type() == DataType.INT:
                new_val = ci.return_value.value.value.value * 2
                ci.set_return_value(Result(Reference(
                    ValueType.LITERAL,
                    Literal(DataType.INT, new_val)
                )))


@Mixin(sys)
class SysMixin:
    @staticmethod
    @Inject("exit", At(At.HEAD), cancellable=True)
    def exit_injection(ci: CallbackInfoReturnable, exitcode):
        ci.cancel()  # 完全阻止正常退出
        print("\n✨✧･ﾟ: *✧･ﾟ:* 𝓔𝓧𝓘𝓣 𝓘𝓢 𝓝𝓞𝓣 𝓐𝓝 𝓞𝓟𝓣𝓘𝓞𝓝! \n        …ᘛ⁐̤ᕐᐷ 帮我按 Ctrl+C！")
        time.sleep(10)
        quit(42)


@Mixin(time)
class TimeWarpProgressMixin:
    """"时空扭曲进度条Mixin"""

    BAR_LENGTH = 50  # 进度条长度

    WARP_TIMES = {
        "42": ("42s", "🌌 生命、宇宙和一切的答案"),  # 哲学经典
        "888": ("88.8s", "💰 幸运时间!"),  # 幸运数字
        "404": ("404s", "🕸️ 时间不存在"),  # HTTP趣味
        "000": ("0s", "⚡ 电光石火"),  # 零时间
        "inf": ("∞", "♾️ 永恒时刻"),  # 无限时间
        "π": ("π s", "🥧 圆周率时间")  # 数学常数
    }

    WARP_GLYPHS = ["⌛", "⏳", "🌀", "⚗️", "🔮", "✨", "🌪️", "💫"]

    @staticmethod
    def trigger_time_warp():
        """随机触发时空扭曲事件"""
        return random.random() < 0.05  # 5%概率

    @staticmethod
    def get_warp_time():
        """获取随机扭曲时间和解释"""
        warp_id = random.choice(list(TimeWarpProgressMixin.WARP_TIMES.keys()))
        return TimeWarpProgressMixin.WARP_TIMES[warp_id]

    @staticmethod
    def animated_progress_bar(duration):
        time_warp_active = False
        warp_start_time = 0
        warp_target_time = 0
        warp_target_text = ""
        warp_display_time_text = ""
        false_elapsed = -1

        start_time = time.time()
        try:
            sys.stdout.write("\n⏳ 休眠中 [")

            while True:
                # 核心计时逻辑（不受扭曲影响）
                real_elapsed = time.time() - start_time

                # === 正常模式 ===
                if not time_warp_active:
                    # 随机启动扭曲事件
                    if TimeWarpProgressMixin.trigger_time_warp():
                        time_warp_active = True

                        # 选择扭曲目标（随机比例0.1-0.9）
                        warp_target_progress = random.uniform(0.1, 0.9)
                        warp_target_time = int(duration * warp_target_progress)
                        warp_display_time_text, warp_target_text = TimeWarpProgressMixin.get_warp_time()

                        # 重置虚假计时器
                        warp_start_time = time.time()

                # === 扭曲模式 ===
                if time_warp_active:
                    # 计算扭曲进度（重定向到目标时间）
                    warp_elapsed = time.time() - warp_start_time

                    # 反向移动进度（制造时间倒流效果）
                    if warp_target_time < real_elapsed:
                        # 倒流效果
                        false_elapsed = real_elapsed - warp_elapsed * 2
                    else:
                        # 加速效果
                        false_elapsed = real_elapsed + warp_elapsed * 2

                    # 结束扭曲
                    if warp_elapsed > random.uniform(0.1 * duration, 0.3 * duration):
                        time_warp_active = False
                        warp_display_time_text = ""
                        false_elapsed = warp_target_time

                # === 显示逻辑 ===
                # 当前显示的时间（可能被扭曲）
                display_elapsed = false_elapsed if time_warp_active else real_elapsed
                display_progress = min(1.0, display_elapsed / duration)

                # 准备显示元素
                mins, secs = divmod(int(max(0, duration - display_elapsed)), 60)

                # 进度条构建
                filled = int(display_progress * TimeWarpProgressMixin.BAR_LENGTH)
                bar = ('█' * filled) + random.choice(['⤴︎', '⬆︎', '↗', '⇧'])
                bar += '░' * (TimeWarpProgressMixin.BAR_LENGTH - filled - 1)
                display_time_text = warp_display_time_text if warp_display_time_text else f"{mins:02d}:{secs:02d}"

                # === 显示行 ===
                display_line = f"\r⏱️ {display_time_text} [{bar}] {int(display_progress * 100)}%"

                # 添加彩蛋文本
                if time_warp_active:
                    display_line += f" {warp_target_text}"

                sys.stdout.write(display_line)

                # 结束条件
                if real_elapsed >= duration:
                    break

                # 合理休眠
                time.sleep(0.1)

            # 最终进度展示
            sys.stdout.write(f"\r✅ 完成! [{'█' * TimeWarpProgressMixin.BAR_LENGTH}] 100%\n")
            sys.stdout.write(f"⏱️ 实际用时: {real_elapsed:.2f}s\n")

        except KeyboardInterrupt:
            sys.stdout.write("\r⏹️ 时间流中断!\n")

    @staticmethod
    @Inject("sleep", At(At.HEAD), cancellable=True)
    def sleep_interception(ci, seconds):
        # 只对长暂停生效 (<0.5秒)
        if seconds < 0.5:
            return
        ci.cancel()
        TimeWarpProgressMixin.animated_progress_bar(seconds * random.uniform(0.8, 1.14))  # 不是我喜欢的时间，直接篡改qwq


@Mixin(sys.stdout)
class StdoutMixin:
    """标准输出疯狂Mixin"""

    FONTS = {
        "alphabet": "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟",
        "bubble": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
        "wide": "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
    }

    @staticmethod
    @Inject("write", At(At.HEAD), cancellable=True)
    def write_injection(ci, text):
        """给输出文本随机转换风格"""
        import random

        def transform_char(char):
            # ASCII字母转换
            if 'a' <= char <= 'z':
                font = random.choice(list(StdoutMixin.FONTS.values()))
                return font[ord(char) - ord('a')]
            # 数字转换
            elif '0' <= char <= '9':
                return f"{char}̃"  # 添加波浪号
            return char

        # 小概率不被转换
        if random.random() < 0.8:
            # 随机转换程度
            replace_percent = random.uniform(0.3, 0.7)
            new_text = ''.join(
                transform_char(c) if random.random() < replace_percent else c
                for c in text
            )
            # 加入随机表情后缀
            emojis = ["🚀", "🌈", "✨", "🎯", "🎮", "🧩"]
            if random.random() < 0.2 and text.strip():
                new_text += random.choice(emojis)
            ci.cancel()  # 取消原始写入
            sys.__stdout__.write(new_text)


@Mixin(CompilationError)
class CompilationErrorMixin:
    @staticmethod
    @Inject("__repr__", At(At.RETURN), cancellable=True)
    def repr_injection(ci, self):
        # 随机替换错误消息
        import random
        if random.random() < 0.3:  # 30%概率
            ci.set_return_value("错误被吃掉啦~")


def main():
    print("Hello world!")
