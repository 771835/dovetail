# Generated from E:/python/minecraft-datapack-language/antlr/transpiler.g4 by ANTLR 4.13.2
# encoding: utf-8
import sys

from antlr4 import *

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4, 1, 62, 558, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7,
        6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13,
        2, 14, 7, 14, 2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20,
        7, 20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26,
        2, 27, 7, 27, 2, 28, 7, 28, 2, 29, 7, 29, 2, 30, 7, 30, 1, 0, 5, 0, 64, 8, 0, 10, 0, 12, 0,
        67, 9, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 3, 0, 74, 8, 0, 1, 0, 1, 0, 3, 0, 78, 8, 0, 5, 0, 80,
        8, 0, 10, 0, 12, 0, 83, 9, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 1, 90, 8, 1, 1, 2, 1, 2, 1, 2,
        1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 5, 2, 100, 8, 2, 10, 2, 12, 2, 103, 9, 2, 1, 2, 1, 2, 3, 2, 107,
        8, 2, 1, 3, 5, 3, 110, 8, 3, 10, 3, 12, 3, 113, 9, 3, 1, 3, 1, 3, 1, 3, 1, 3, 3, 3, 119, 8,
        3, 1, 3, 1, 3, 3, 3, 123, 8, 3, 1, 3, 1, 3, 1, 3, 3, 3, 128, 8, 3, 1, 3, 5, 3, 131, 8, 3, 10,
        3, 12, 3, 134, 9, 3, 1, 3, 1, 3, 1, 4, 5, 4, 139, 8, 4, 10, 4, 12, 4, 142, 9, 4, 1, 4, 1, 4,
        1, 4, 1, 4, 3, 4, 148, 8, 4, 1, 4, 1, 4, 1, 4, 3, 4, 153, 8, 4, 1, 4, 5, 4, 156, 8, 4, 10, 4,
        12, 4, 159, 9, 4, 1, 4, 1, 4, 1, 5, 1, 5, 1, 5, 3, 5, 166, 8, 5, 1, 5, 1, 5, 1, 5, 3, 5, 171,
        8, 5, 1, 5, 1, 5, 3, 5, 175, 8, 5, 1, 6, 1, 6, 1, 6, 1, 6, 3, 6, 181, 8, 6, 1, 6, 3, 6, 184,
        8, 6, 1, 7, 5, 7, 187, 8, 7, 10, 7, 12, 7, 190, 9, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 5,
        7, 198, 8, 7, 10, 7, 12, 7, 201, 9, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7,
        5, 7, 212, 8, 7, 10, 7, 12, 7, 215, 9, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 3, 7, 223, 8,
        7, 1, 8, 5, 8, 226, 8, 8, 10, 8, 12, 8, 229, 9, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 5, 8,
        237, 8, 8, 10, 8, 12, 8, 240, 9, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 5,
        8, 251, 8, 8, 10, 8, 12, 8, 254, 9, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 3, 8, 262, 8, 8,
        1, 9, 1, 9, 1, 9, 1, 9, 5, 9, 268, 8, 9, 10, 9, 12, 9, 271, 9, 9, 3, 9, 273, 8, 9, 1, 9, 1,
        9, 3, 9, 277, 8, 9, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 3, 10, 284, 8, 10, 1, 10, 1, 10, 1,
        10, 1, 10, 3, 10, 290, 8, 10, 3, 10, 292, 8, 10, 1, 11, 1, 11, 5, 11, 296, 8, 11, 10, 11,
        12, 11, 299, 9, 11, 1, 11, 1, 11, 3, 11, 303, 8, 11, 1, 12, 1, 12, 1, 12, 3, 12, 308, 8,
        12, 1, 12, 1, 12, 3, 12, 312, 8, 12, 1, 12, 1, 12, 1, 12, 1, 12, 3, 12, 318, 8, 12, 1, 12,
        1, 12, 3, 12, 322, 8, 12, 1, 12, 1, 12, 1, 12, 3, 12, 327, 8, 12, 1, 12, 1, 12, 3, 12, 331,
        8, 12, 1, 12, 3, 12, 334, 8, 12, 1, 13, 1, 13, 1, 14, 1, 14, 1, 15, 1, 15, 1, 15, 1, 15,
        1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 3, 15, 355,
        8, 15, 1, 16, 3, 16, 358, 8, 16, 1, 16, 1, 16, 3, 16, 362, 8, 16, 1, 16, 1, 16, 3, 16, 366,
        8, 16, 1, 17, 1, 17, 3, 17, 370, 8, 17, 1, 18, 1, 18, 1, 19, 1, 19, 1, 20, 1, 20, 1, 20,
        1, 20, 1, 20, 1, 20, 1, 21, 1, 21, 1, 21, 1, 21, 3, 21, 386, 8, 21, 1, 21, 3, 21, 389, 8,
        21, 1, 21, 1, 21, 1, 21, 1, 21, 1, 21, 1, 21, 1, 21, 1, 21, 3, 21, 399, 8, 21, 1, 22, 1,
        22, 1, 22, 3, 22, 404, 8, 22, 1, 22, 1, 22, 1, 22, 1, 22, 1, 22, 1, 22, 3, 22, 412, 8, 22,
        1, 22, 1, 22, 3, 22, 416, 8, 22, 1, 22, 1, 22, 1, 22, 3, 22, 421, 8, 22, 1, 22, 1, 22, 3,
        22, 425, 8, 22, 1, 22, 1, 22, 1, 22, 3, 22, 430, 8, 22, 1, 22, 1, 22, 1, 22, 1, 22, 1, 22,
        3, 22, 437, 8, 22, 1, 22, 1, 22, 1, 22, 1, 22, 1, 22, 3, 22, 444, 8, 22, 1, 23, 1, 23, 3,
        23, 448, 8, 23, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 3, 24, 457, 8, 24, 1, 25,
        1, 25, 3, 25, 461, 8, 25, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26,
        3, 26, 472, 8, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26,
        1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26,
        1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26,
        1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26,
        1, 26, 1, 26, 1, 26, 1, 26, 5, 26, 527, 8, 26, 10, 26, 12, 26, 530, 9, 26, 1, 27, 1, 27,
        1, 27, 1, 27, 1, 27, 1, 27, 3, 27, 538, 8, 27, 1, 28, 1, 28, 3, 28, 542, 8, 28, 1, 28, 1,
        28, 3, 28, 546, 8, 28, 1, 29, 1, 29, 1, 29, 5, 29, 551, 8, 29, 10, 29, 12, 29, 554, 9,
        29, 1, 30, 1, 30, 1, 30, 0, 1, 52, 31, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26,
        28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 0, 5, 1, 0, 13, 14,
        1, 0, 42, 44, 1, 0, 45, 46, 1, 0, 47, 52, 2, 0, 30, 32, 55, 57, 630, 0, 65, 1, 0, 0, 0, 2,
        86, 1, 0, 0, 0, 4, 106, 1, 0, 0, 0, 6, 111, 1, 0, 0, 0, 8, 140, 1, 0, 0, 0, 10, 174, 1, 0,
        0, 0, 12, 183, 1, 0, 0, 0, 14, 222, 1, 0, 0, 0, 16, 261, 1, 0, 0, 0, 18, 276, 1, 0, 0, 0,
        20, 291, 1, 0, 0, 0, 22, 302, 1, 0, 0, 0, 24, 333, 1, 0, 0, 0, 26, 335, 1, 0, 0, 0, 28, 337,
        1, 0, 0, 0, 30, 354, 1, 0, 0, 0, 32, 357, 1, 0, 0, 0, 34, 369, 1, 0, 0, 0, 36, 371, 1, 0,
        0, 0, 38, 373, 1, 0, 0, 0, 40, 375, 1, 0, 0, 0, 42, 398, 1, 0, 0, 0, 44, 443, 1, 0, 0, 0,
        46, 445, 1, 0, 0, 0, 48, 449, 1, 0, 0, 0, 50, 460, 1, 0, 0, 0, 52, 471, 1, 0, 0, 0, 54, 537,
        1, 0, 0, 0, 56, 545, 1, 0, 0, 0, 58, 547, 1, 0, 0, 0, 60, 555, 1, 0, 0, 0, 62, 64, 3, 2, 1,
        0, 63, 62, 1, 0, 0, 0, 64, 67, 1, 0, 0, 0, 65, 63, 1, 0, 0, 0, 65, 66, 1, 0, 0, 0, 66, 81,
        1, 0, 0, 0, 67, 65, 1, 0, 0, 0, 68, 80, 3, 6, 3, 0, 69, 80, 3, 8, 4, 0, 70, 80, 3, 14, 7, 0,
        71, 73, 3, 44, 22, 0, 72, 74, 5, 10, 0, 0, 73, 72, 1, 0, 0, 0, 73, 74, 1, 0, 0, 0, 74, 80,
        1, 0, 0, 0, 75, 77, 3, 42, 21, 0, 76, 78, 5, 10, 0, 0, 77, 76, 1, 0, 0, 0, 77, 78, 1, 0, 0,
        0, 78, 80, 1, 0, 0, 0, 79, 68, 1, 0, 0, 0, 79, 69, 1, 0, 0, 0, 79, 70, 1, 0, 0, 0, 79, 71,
        1, 0, 0, 0, 79, 75, 1, 0, 0, 0, 80, 83, 1, 0, 0, 0, 81, 79, 1, 0, 0, 0, 81, 82, 1, 0, 0, 0,
        82, 84, 1, 0, 0, 0, 83, 81, 1, 0, 0, 0, 84, 85, 5, 0, 0, 1, 85, 1, 1, 0, 0, 0, 86, 87, 5, 16,
        0, 0, 87, 89, 3, 60, 30, 0, 88, 90, 5, 10, 0, 0, 89, 88, 1, 0, 0, 0, 89, 90, 1, 0, 0, 0, 90,
        3, 1, 0, 0, 0, 91, 92, 5, 1, 0, 0, 92, 107, 5, 58, 0, 0, 93, 94, 5, 1, 0, 0, 94, 95, 5, 58,
        0, 0, 95, 96, 5, 4, 0, 0, 96, 101, 3, 60, 30, 0, 97, 98, 5, 11, 0, 0, 98, 100, 3, 60, 30,
        0, 99, 97, 1, 0, 0, 0, 100, 103, 1, 0, 0, 0, 101, 99, 1, 0, 0, 0, 101, 102, 1, 0, 0, 0, 102,
        104, 1, 0, 0, 0, 103, 101, 1, 0, 0, 0, 104, 105, 5, 5, 0, 0, 105, 107, 1, 0, 0, 0, 106,
        91, 1, 0, 0, 0, 106, 93, 1, 0, 0, 0, 107, 5, 1, 0, 0, 0, 108, 110, 3, 4, 2, 0, 109, 108,
        1, 0, 0, 0, 110, 113, 1, 0, 0, 0, 111, 109, 1, 0, 0, 0, 111, 112, 1, 0, 0, 0, 112, 114,
        1, 0, 0, 0, 113, 111, 1, 0, 0, 0, 114, 115, 5, 19, 0, 0, 115, 118, 5, 58, 0, 0, 116, 117,
        5, 21, 0, 0, 117, 119, 3, 12, 6, 0, 118, 116, 1, 0, 0, 0, 118, 119, 1, 0, 0, 0, 119, 122,
        1, 0, 0, 0, 120, 121, 5, 22, 0, 0, 121, 123, 3, 12, 6, 0, 122, 120, 1, 0, 0, 0, 122, 123,
        1, 0, 0, 0, 123, 124, 1, 0, 0, 0, 124, 132, 5, 8, 0, 0, 125, 127, 3, 10, 5, 0, 126, 128,
        5, 10, 0, 0, 127, 126, 1, 0, 0, 0, 127, 128, 1, 0, 0, 0, 128, 131, 1, 0, 0, 0, 129, 131,
        3, 16, 8, 0, 130, 125, 1, 0, 0, 0, 130, 129, 1, 0, 0, 0, 131, 134, 1, 0, 0, 0, 132, 130,
        1, 0, 0, 0, 132, 133, 1, 0, 0, 0, 133, 135, 1, 0, 0, 0, 134, 132, 1, 0, 0, 0, 135, 136,
        5, 9, 0, 0, 136, 7, 1, 0, 0, 0, 137, 139, 3, 4, 2, 0, 138, 137, 1, 0, 0, 0, 139, 142, 1,
        0, 0, 0, 140, 138, 1, 0, 0, 0, 140, 141, 1, 0, 0, 0, 141, 143, 1, 0, 0, 0, 142, 140, 1,
        0, 0, 0, 143, 144, 5, 20, 0, 0, 144, 147, 5, 58, 0, 0, 145, 146, 5, 21, 0, 0, 146, 148,
        3, 12, 6, 0, 147, 145, 1, 0, 0, 0, 147, 148, 1, 0, 0, 0, 148, 149, 1, 0, 0, 0, 149, 157,
        5, 8, 0, 0, 150, 152, 3, 10, 5, 0, 151, 153, 5, 10, 0, 0, 152, 151, 1, 0, 0, 0, 152, 153,
        1, 0, 0, 0, 153, 156, 1, 0, 0, 0, 154, 156, 3, 16, 8, 0, 155, 150, 1, 0, 0, 0, 155, 154,
        1, 0, 0, 0, 156, 159, 1, 0, 0, 0, 157, 155, 1, 0, 0, 0, 157, 158, 1, 0, 0, 0, 158, 160,
        1, 0, 0, 0, 159, 157, 1, 0, 0, 0, 160, 161, 5, 9, 0, 0, 161, 9, 1, 0, 0, 0, 162, 163, 3,
        12, 6, 0, 163, 165, 5, 58, 0, 0, 164, 166, 5, 12, 0, 0, 165, 164, 1, 0, 0, 0, 165, 166,
        1, 0, 0, 0, 166, 175, 1, 0, 0, 0, 167, 168, 5, 24, 0, 0, 168, 170, 5, 58, 0, 0, 169, 171,
        5, 12, 0, 0, 170, 169, 1, 0, 0, 0, 170, 171, 1, 0, 0, 0, 171, 172, 1, 0, 0, 0, 172, 173,
        7, 0, 0, 0, 173, 175, 3, 12, 6, 0, 174, 162, 1, 0, 0, 0, 174, 167, 1, 0, 0, 0, 175, 11,
        1, 0, 0, 0, 176, 180, 5, 58, 0, 0, 177, 178, 5, 6, 0, 0, 178, 179, 5, 55, 0, 0, 179, 181,
        5, 7, 0, 0, 180, 177, 1, 0, 0, 0, 180, 181, 1, 0, 0, 0, 181, 184, 1, 0, 0, 0, 182, 184,
        5, 32, 0, 0, 183, 176, 1, 0, 0, 0, 183, 182, 1, 0, 0, 0, 184, 13, 1, 0, 0, 0, 185, 187,
        3, 4, 2, 0, 186, 185, 1, 0, 0, 0, 187, 190, 1, 0, 0, 0, 188, 186, 1, 0, 0, 0, 188, 189,
        1, 0, 0, 0, 189, 191, 1, 0, 0, 0, 190, 188, 1, 0, 0, 0, 191, 192, 5, 17, 0, 0, 192, 193,
        5, 58, 0, 0, 193, 194, 3, 18, 9, 0, 194, 195, 3, 22, 11, 0, 195, 223, 1, 0, 0, 0, 196,
        198, 3, 4, 2, 0, 197, 196, 1, 0, 0, 0, 198, 201, 1, 0, 0, 0, 199, 197, 1, 0, 0, 0, 199,
        200, 1, 0, 0, 0, 200, 202, 1, 0, 0, 0, 201, 199, 1, 0, 0, 0, 202, 203, 5, 17, 0, 0, 203,
        204, 5, 58, 0, 0, 204, 205, 3, 18, 9, 0, 205, 206, 7, 0, 0, 0, 206, 207, 3, 12, 6, 0, 207,
        208, 1, 0, 0, 0, 208, 209, 3, 22, 11, 0, 209, 223, 1, 0, 0, 0, 210, 212, 3, 4, 2, 0, 211,
        210, 1, 0, 0, 0, 212, 215, 1, 0, 0, 0, 213, 211, 1, 0, 0, 0, 213, 214, 1, 0, 0, 0, 214,
        216, 1, 0, 0, 0, 215, 213, 1, 0, 0, 0, 216, 217, 5, 17, 0, 0, 217, 218, 3, 12, 6, 0, 218,
        219, 5, 58, 0, 0, 219, 220, 3, 18, 9, 0, 220, 221, 3, 22, 11, 0, 221, 223, 1, 0, 0, 0,
        222, 188, 1, 0, 0, 0, 222, 199, 1, 0, 0, 0, 222, 213, 1, 0, 0, 0, 223, 15, 1, 0, 0, 0, 224,
        226, 3, 4, 2, 0, 225, 224, 1, 0, 0, 0, 226, 229, 1, 0, 0, 0, 227, 225, 1, 0, 0, 0, 227,
        228, 1, 0, 0, 0, 228, 230, 1, 0, 0, 0, 229, 227, 1, 0, 0, 0, 230, 231, 5, 18, 0, 0, 231,
        232, 5, 58, 0, 0, 232, 233, 3, 18, 9, 0, 233, 234, 3, 22, 11, 0, 234, 262, 1, 0, 0, 0,
        235, 237, 3, 4, 2, 0, 236, 235, 1, 0, 0, 0, 237, 240, 1, 0, 0, 0, 238, 236, 1, 0, 0, 0,
        238, 239, 1, 0, 0, 0, 239, 241, 1, 0, 0, 0, 240, 238, 1, 0, 0, 0, 241, 242, 5, 18, 0, 0,
        242, 243, 5, 58, 0, 0, 243, 244, 3, 18, 9, 0, 244, 245, 7, 0, 0, 0, 245, 246, 3, 12, 6,
        0, 246, 247, 1, 0, 0, 0, 247, 248, 3, 22, 11, 0, 248, 262, 1, 0, 0, 0, 249, 251, 3, 4,
        2, 0, 250, 249, 1, 0, 0, 0, 251, 254, 1, 0, 0, 0, 252, 250, 1, 0, 0, 0, 252, 253, 1, 0,
        0, 0, 253, 255, 1, 0, 0, 0, 254, 252, 1, 0, 0, 0, 255, 256, 5, 18, 0, 0, 256, 257, 3, 12,
        6, 0, 257, 258, 5, 58, 0, 0, 258, 259, 3, 18, 9, 0, 259, 260, 3, 22, 11, 0, 260, 262,
        1, 0, 0, 0, 261, 227, 1, 0, 0, 0, 261, 238, 1, 0, 0, 0, 261, 252, 1, 0, 0, 0, 262, 17, 1,
        0, 0, 0, 263, 272, 5, 4, 0, 0, 264, 269, 3, 20, 10, 0, 265, 266, 5, 11, 0, 0, 266, 268,
        3, 20, 10, 0, 267, 265, 1, 0, 0, 0, 268, 271, 1, 0, 0, 0, 269, 267, 1, 0, 0, 0, 269, 270,
        1, 0, 0, 0, 270, 273, 1, 0, 0, 0, 271, 269, 1, 0, 0, 0, 272, 264, 1, 0, 0, 0, 272, 273,
        1, 0, 0, 0, 273, 274, 1, 0, 0, 0, 274, 277, 5, 5, 0, 0, 275, 277, 5, 3, 0, 0, 276, 263,
        1, 0, 0, 0, 276, 275, 1, 0, 0, 0, 277, 19, 1, 0, 0, 0, 278, 279, 5, 58, 0, 0, 279, 280,
        7, 0, 0, 0, 280, 283, 3, 12, 6, 0, 281, 282, 5, 35, 0, 0, 282, 284, 3, 52, 26, 0, 283,
        281, 1, 0, 0, 0, 283, 284, 1, 0, 0, 0, 284, 292, 1, 0, 0, 0, 285, 286, 3, 12, 6, 0, 286,
        289, 5, 58, 0, 0, 287, 288, 5, 35, 0, 0, 288, 290, 3, 52, 26, 0, 289, 287, 1, 0, 0, 0,
        289, 290, 1, 0, 0, 0, 290, 292, 1, 0, 0, 0, 291, 278, 1, 0, 0, 0, 291, 285, 1, 0, 0, 0,
        292, 21, 1, 0, 0, 0, 293, 297, 5, 8, 0, 0, 294, 296, 3, 24, 12, 0, 295, 294, 1, 0, 0, 0,
        296, 299, 1, 0, 0, 0, 297, 295, 1, 0, 0, 0, 297, 298, 1, 0, 0, 0, 298, 300, 1, 0, 0, 0,
        299, 297, 1, 0, 0, 0, 300, 303, 5, 9, 0, 0, 301, 303, 5, 10, 0, 0, 302, 293, 1, 0, 0, 0,
        302, 301, 1, 0, 0, 0, 303, 23, 1, 0, 0, 0, 304, 334, 3, 14, 7, 0, 305, 307, 3, 44, 22,
        0, 306, 308, 5, 10, 0, 0, 307, 306, 1, 0, 0, 0, 307, 308, 1, 0, 0, 0, 308, 334, 1, 0, 0,
        0, 309, 311, 3, 42, 21, 0, 310, 312, 5, 10, 0, 0, 311, 310, 1, 0, 0, 0, 311, 312, 1, 0,
        0, 0, 312, 334, 1, 0, 0, 0, 313, 334, 3, 30, 15, 0, 314, 334, 3, 40, 20, 0, 315, 317,
        3, 52, 26, 0, 316, 318, 5, 10, 0, 0, 317, 316, 1, 0, 0, 0, 317, 318, 1, 0, 0, 0, 318, 334,
        1, 0, 0, 0, 319, 321, 3, 46, 23, 0, 320, 322, 5, 10, 0, 0, 321, 320, 1, 0, 0, 0, 321, 322,
        1, 0, 0, 0, 322, 334, 1, 0, 0, 0, 323, 334, 3, 48, 24, 0, 324, 326, 3, 26, 13, 0, 325,
        327, 5, 10, 0, 0, 326, 325, 1, 0, 0, 0, 326, 327, 1, 0, 0, 0, 327, 334, 1, 0, 0, 0, 328,
        330, 3, 28, 14, 0, 329, 331, 5, 10, 0, 0, 330, 329, 1, 0, 0, 0, 330, 331, 1, 0, 0, 0, 331,
        334, 1, 0, 0, 0, 332, 334, 5, 10, 0, 0, 333, 304, 1, 0, 0, 0, 333, 305, 1, 0, 0, 0, 333,
        309, 1, 0, 0, 0, 333, 313, 1, 0, 0, 0, 333, 314, 1, 0, 0, 0, 333, 315, 1, 0, 0, 0, 333,
        319, 1, 0, 0, 0, 333, 323, 1, 0, 0, 0, 333, 324, 1, 0, 0, 0, 333, 328, 1, 0, 0, 0, 333,
        332, 1, 0, 0, 0, 334, 25, 1, 0, 0, 0, 335, 336, 5, 33, 0, 0, 336, 27, 1, 0, 0, 0, 337, 338,
        5, 34, 0, 0, 338, 29, 1, 0, 0, 0, 339, 340, 5, 26, 0, 0, 340, 341, 5, 4, 0, 0, 341, 342,
        3, 32, 16, 0, 342, 343, 5, 5, 0, 0, 343, 344, 3, 50, 25, 0, 344, 355, 1, 0, 0, 0, 345,
        346, 5, 26, 0, 0, 346, 347, 5, 4, 0, 0, 347, 348, 3, 12, 6, 0, 348, 349, 5, 58, 0, 0, 349,
        350, 5, 14, 0, 0, 350, 351, 3, 52, 26, 0, 351, 352, 5, 5, 0, 0, 352, 353, 3, 50, 25, 0,
        353, 355, 1, 0, 0, 0, 354, 339, 1, 0, 0, 0, 354, 345, 1, 0, 0, 0, 355, 31, 1, 0, 0, 0, 356,
        358, 3, 34, 17, 0, 357, 356, 1, 0, 0, 0, 357, 358, 1, 0, 0, 0, 358, 359, 1, 0, 0, 0, 359,
        361, 5, 10, 0, 0, 360, 362, 3, 36, 18, 0, 361, 360, 1, 0, 0, 0, 361, 362, 1, 0, 0, 0, 362,
        363, 1, 0, 0, 0, 363, 365, 5, 10, 0, 0, 364, 366, 3, 38, 19, 0, 365, 364, 1, 0, 0, 0, 365,
        366, 1, 0, 0, 0, 366, 33, 1, 0, 0, 0, 367, 370, 3, 44, 22, 0, 368, 370, 3, 52, 26, 0, 369,
        367, 1, 0, 0, 0, 369, 368, 1, 0, 0, 0, 370, 35, 1, 0, 0, 0, 371, 372, 3, 52, 26, 0, 372,
        37, 1, 0, 0, 0, 373, 374, 3, 52, 26, 0, 374, 39, 1, 0, 0, 0, 375, 376, 5, 27, 0, 0, 376,
        377, 5, 4, 0, 0, 377, 378, 3, 36, 18, 0, 378, 379, 5, 5, 0, 0, 379, 380, 3, 50, 25, 0,
        380, 41, 1, 0, 0, 0, 381, 382, 5, 23, 0, 0, 382, 385, 5, 58, 0, 0, 383, 384, 7, 0, 0, 0,
        384, 386, 3, 12, 6, 0, 385, 383, 1, 0, 0, 0, 385, 386, 1, 0, 0, 0, 386, 388, 1, 0, 0, 0,
        387, 389, 5, 12, 0, 0, 388, 387, 1, 0, 0, 0, 388, 389, 1, 0, 0, 0, 389, 390, 1, 0, 0, 0,
        390, 391, 5, 35, 0, 0, 391, 399, 3, 52, 26, 0, 392, 393, 5, 23, 0, 0, 393, 394, 3, 12,
        6, 0, 394, 395, 5, 58, 0, 0, 395, 396, 5, 35, 0, 0, 396, 397, 3, 52, 26, 0, 397, 399,
        1, 0, 0, 0, 398, 381, 1, 0, 0, 0, 398, 392, 1, 0, 0, 0, 399, 43, 1, 0, 0, 0, 400, 401, 5,
        24, 0, 0, 401, 403, 5, 58, 0, 0, 402, 404, 5, 12, 0, 0, 403, 402, 1, 0, 0, 0, 403, 404,
        1, 0, 0, 0, 404, 405, 1, 0, 0, 0, 405, 406, 5, 35, 0, 0, 406, 444, 3, 52, 26, 0, 407, 408,
        5, 58, 0, 0, 408, 409, 7, 0, 0, 0, 409, 411, 3, 12, 6, 0, 410, 412, 5, 12, 0, 0, 411, 410,
        1, 0, 0, 0, 411, 412, 1, 0, 0, 0, 412, 415, 1, 0, 0, 0, 413, 414, 5, 35, 0, 0, 414, 416,
        3, 52, 26, 0, 415, 413, 1, 0, 0, 0, 415, 416, 1, 0, 0, 0, 416, 444, 1, 0, 0, 0, 417, 418,
        3, 12, 6, 0, 418, 420, 5, 58, 0, 0, 419, 421, 5, 12, 0, 0, 420, 419, 1, 0, 0, 0, 420, 421,
        1, 0, 0, 0, 421, 424, 1, 0, 0, 0, 422, 423, 5, 35, 0, 0, 423, 425, 3, 52, 26, 0, 424, 422,
        1, 0, 0, 0, 424, 425, 1, 0, 0, 0, 425, 444, 1, 0, 0, 0, 426, 427, 5, 24, 0, 0, 427, 429,
        5, 58, 0, 0, 428, 430, 5, 12, 0, 0, 429, 428, 1, 0, 0, 0, 429, 430, 1, 0, 0, 0, 430, 431,
        1, 0, 0, 0, 431, 432, 7, 0, 0, 0, 432, 444, 3, 12, 6, 0, 433, 434, 5, 24, 0, 0, 434, 436,
        5, 58, 0, 0, 435, 437, 5, 12, 0, 0, 436, 435, 1, 0, 0, 0, 436, 437, 1, 0, 0, 0, 437, 438,
        1, 0, 0, 0, 438, 439, 7, 0, 0, 0, 439, 440, 3, 12, 6, 0, 440, 441, 5, 35, 0, 0, 441, 442,
        3, 52, 26, 0, 442, 444, 1, 0, 0, 0, 443, 400, 1, 0, 0, 0, 443, 407, 1, 0, 0, 0, 443, 417,
        1, 0, 0, 0, 443, 426, 1, 0, 0, 0, 443, 433, 1, 0, 0, 0, 444, 45, 1, 0, 0, 0, 445, 447, 5,
        25, 0, 0, 446, 448, 3, 52, 26, 0, 447, 446, 1, 0, 0, 0, 447, 448, 1, 0, 0, 0, 448, 47,
        1, 0, 0, 0, 449, 450, 5, 28, 0, 0, 450, 451, 5, 4, 0, 0, 451, 452, 3, 36, 18, 0, 452, 453,
        5, 5, 0, 0, 453, 456, 3, 50, 25, 0, 454, 455, 5, 29, 0, 0, 455, 457, 3, 50, 25, 0, 456,
        454, 1, 0, 0, 0, 456, 457, 1, 0, 0, 0, 457, 49, 1, 0, 0, 0, 458, 461, 3, 24, 12, 0, 459,
        461, 3, 22, 11, 0, 460, 458, 1, 0, 0, 0, 460, 459, 1, 0, 0, 0, 461, 51, 1, 0, 0, 0, 462,
        463, 6, 26, -1, 0, 463, 472, 3, 54, 27, 0, 464, 465, 5, 46, 0, 0, 465, 472, 3, 52, 26,
        12, 466, 467, 5, 41, 0, 0, 467, 472, 3, 52, 26, 11, 468, 469, 5, 58, 0, 0, 469, 470,
        5, 35, 0, 0, 470, 472, 3, 52, 26, 1, 471, 462, 1, 0, 0, 0, 471, 464, 1, 0, 0, 0, 471, 466,
        1, 0, 0, 0, 471, 468, 1, 0, 0, 0, 472, 528, 1, 0, 0, 0, 473, 474, 10, 10, 0, 0, 474, 475,
        7, 1, 0, 0, 475, 527, 3, 52, 26, 11, 476, 477, 10, 9, 0, 0, 477, 478, 7, 2, 0, 0, 478,
        527, 3, 52, 26, 10, 479, 480, 10, 8, 0, 0, 480, 481, 7, 3, 0, 0, 481, 527, 3, 52, 26,
        9, 482, 483, 10, 7, 0, 0, 483, 484, 5, 53, 0, 0, 484, 527, 3, 52, 26, 8, 485, 486, 10,
        6, 0, 0, 486, 487, 5, 54, 0, 0, 487, 527, 3, 52, 26, 7, 488, 489, 10, 5, 0, 0, 489, 490,
        5, 12, 0, 0, 490, 491, 3, 52, 26, 0, 491, 492, 5, 14, 0, 0, 492, 493, 3, 52, 26, 5, 493,
        527, 1, 0, 0, 0, 494, 495, 10, 4, 0, 0, 495, 496, 5, 28, 0, 0, 496, 497, 3, 52, 26, 0,
        497, 498, 5, 29, 0, 0, 498, 499, 3, 52, 26, 4, 499, 527, 1, 0, 0, 0, 500, 501, 10, 3,
        0, 0, 501, 502, 5, 6, 0, 0, 502, 503, 3, 52, 26, 0, 503, 504, 5, 7, 0, 0, 504, 505, 5,
        35, 0, 0, 505, 506, 3, 52, 26, 4, 506, 527, 1, 0, 0, 0, 507, 508, 10, 2, 0, 0, 508, 509,
        5, 2, 0, 0, 509, 510, 5, 58, 0, 0, 510, 511, 5, 35, 0, 0, 511, 527, 3, 52, 26, 3, 512,
        513, 10, 16, 0, 0, 513, 514, 5, 2, 0, 0, 514, 515, 5, 58, 0, 0, 515, 527, 3, 56, 28, 0,
        516, 517, 10, 15, 0, 0, 517, 518, 5, 2, 0, 0, 518, 527, 5, 58, 0, 0, 519, 520, 10, 14,
        0, 0, 520, 521, 5, 6, 0, 0, 521, 522, 3, 52, 26, 0, 522, 523, 5, 7, 0, 0, 523, 527, 1,
        0, 0, 0, 524, 525, 10, 13, 0, 0, 525, 527, 3, 56, 28, 0, 526, 473, 1, 0, 0, 0, 526, 476,
        1, 0, 0, 0, 526, 479, 1, 0, 0, 0, 526, 482, 1, 0, 0, 0, 526, 485, 1, 0, 0, 0, 526, 488,
        1, 0, 0, 0, 526, 494, 1, 0, 0, 0, 526, 500, 1, 0, 0, 0, 526, 507, 1, 0, 0, 0, 526, 512,
        1, 0, 0, 0, 526, 516, 1, 0, 0, 0, 526, 519, 1, 0, 0, 0, 526, 524, 1, 0, 0, 0, 527, 530,
        1, 0, 0, 0, 528, 526, 1, 0, 0, 0, 528, 529, 1, 0, 0, 0, 529, 53, 1, 0, 0, 0, 530, 528, 1,
        0, 0, 0, 531, 538, 5, 58, 0, 0, 532, 538, 3, 60, 30, 0, 533, 534, 5, 4, 0, 0, 534, 535,
        3, 52, 26, 0, 535, 536, 5, 5, 0, 0, 536, 538, 1, 0, 0, 0, 537, 531, 1, 0, 0, 0, 537, 532,
        1, 0, 0, 0, 537, 533, 1, 0, 0, 0, 538, 55, 1, 0, 0, 0, 539, 541, 5, 4, 0, 0, 540, 542, 3,
        58, 29, 0, 541, 540, 1, 0, 0, 0, 541, 542, 1, 0, 0, 0, 542, 543, 1, 0, 0, 0, 543, 546,
        5, 5, 0, 0, 544, 546, 5, 3, 0, 0, 545, 539, 1, 0, 0, 0, 545, 544, 1, 0, 0, 0, 546, 57, 1,
        0, 0, 0, 547, 552, 3, 52, 26, 0, 548, 549, 5, 11, 0, 0, 549, 551, 3, 52, 26, 0, 550, 548,
        1, 0, 0, 0, 551, 554, 1, 0, 0, 0, 552, 550, 1, 0, 0, 0, 552, 553, 1, 0, 0, 0, 553, 59, 1,
        0, 0, 0, 554, 552, 1, 0, 0, 0, 555, 556, 7, 4, 0, 0, 556, 61, 1, 0, 0, 0, 73, 65, 73, 77,
        79, 81, 89, 101, 106, 111, 118, 122, 127, 130, 132, 140, 147, 152, 155, 157, 165,
        170, 174, 180, 183, 188, 199, 213, 222, 227, 238, 252, 261, 269, 272, 276, 283,
        289, 291, 297, 302, 307, 311, 317, 321, 326, 330, 333, 354, 357, 361, 365, 369,
        385, 388, 398, 403, 411, 415, 420, 424, 429, 436, 443, 447, 456, 460, 471, 526,
        528, 537, 541, 545, 552
    ]


class transpilerParser(Parser):
    grammarFileName = "transpiler.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'@'", "'.'", "'()'", "'('", "')'", "'['",
                    "']'", "'{'", "'}'", "';'", "','", "'?'", "<INVALID>",
                    "':'", "'::'", "'include'", "'func'", "'method'", "'class'",
                    "'interface'", "'extends'", "'implements'", "'const'",
                    "'let'", "'return'", "'for'", "'while'", "'if'", "'else'",
                    "'true'", "'false'", "'null'", "'break'", "'continue'",
                    "'='", "'+='", "'-='", "'*='", "'/='", "'%='", "<INVALID>",
                    "'*'", "'/'", "'%'", "'+'", "'-'", "'>'", "'<'", "'=='",
                    "'!='", "'>='", "'<='"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "PAREN", "LPAREN",
                     "RPAREN", "LBRACK", "RBRACK", "LBRACE", "RBRACE",
                     "SEMI", "COMMA", "QUESTION", "ARROW", "COLON", "DOUBLE_COLON",
                     "INCLUDE", "FUNC", "METHOD", "CLASS", "INTERFACE",
                     "EXTENDS", "IMPLEMENTS", "CONST", "LET", "RETURN",
                     "FOR", "WHILE", "IF", "ELSE", "TRUE", "FALSE", "NULL",
                     "BREAK", "CONTINUE", "ASSIGN", "ADD_ASSIGN", "SUB_ASSIGN",
                     "MUL_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", "NOT", "MUL",
                     "DIV", "MOD", "ADD", "SUB", "GT", "LT", "EQ", "NEQ",
                     "GTE", "LTE", "AND", "OR", "NUMBER", "STRING", "FSTRING",
                     "ID", "WS", "LINE_COMMENT", "LINE_COMMENT2", "BLOCK_COMMENT"]

    RULE_program = 0
    RULE_includeStmt = 1
    RULE_annotation = 2
    RULE_classDecl = 3
    RULE_interfaceDecl = 4
    RULE_classPropertyDecl = 5
    RULE_type = 6
    RULE_functionDecl = 7
    RULE_methodDecl = 8
    RULE_paramList = 9
    RULE_paramDecl = 10
    RULE_block = 11
    RULE_statement = 12
    RULE_breakStmt = 13
    RULE_continueStmt = 14
    RULE_forStmt = 15
    RULE_forControl = 16
    RULE_forInit = 17
    RULE_condition = 18
    RULE_forUpdate = 19
    RULE_whileStmt = 20
    RULE_constDecl = 21
    RULE_varDecl = 22
    RULE_returnStmt = 23
    RULE_ifStmt = 24
    RULE_statementBlock = 25
    RULE_expr = 26
    RULE_primary = 27
    RULE_argumentList = 28
    RULE_exprList = 29
    RULE_literal = 30

    ruleNames = ["program", "includeStmt", "annotation", "classDecl",
                 "interfaceDecl", "classPropertyDecl", "type", "functionDecl",
                 "methodDecl", "paramList", "paramDecl", "block", "statement",
                 "breakStmt", "continueStmt", "forStmt", "forControl",
                 "forInit", "condition", "forUpdate", "whileStmt", "constDecl",
                 "varDecl", "returnStmt", "ifStmt", "statementBlock",
                 "expr", "primary", "argumentList", "exprList", "literal"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    PAREN = 3
    LPAREN = 4
    RPAREN = 5
    LBRACK = 6
    RBRACK = 7
    LBRACE = 8
    RBRACE = 9
    SEMI = 10
    COMMA = 11
    QUESTION = 12
    ARROW = 13
    COLON = 14
    DOUBLE_COLON = 15
    INCLUDE = 16
    FUNC = 17
    METHOD = 18
    CLASS = 19
    INTERFACE = 20
    EXTENDS = 21
    IMPLEMENTS = 22
    CONST = 23
    LET = 24
    RETURN = 25
    FOR = 26
    WHILE = 27
    IF = 28
    ELSE = 29
    TRUE = 30
    FALSE = 31
    NULL = 32
    BREAK = 33
    CONTINUE = 34
    ASSIGN = 35
    ADD_ASSIGN = 36
    SUB_ASSIGN = 37
    MUL_ASSIGN = 38
    DIV_ASSIGN = 39
    MOD_ASSIGN = 40
    NOT = 41
    MUL = 42
    DIV = 43
    MOD = 44
    ADD = 45
    SUB = 46
    GT = 47
    LT = 48
    EQ = 49
    NEQ = 50
    GTE = 51
    LTE = 52
    AND = 53
    OR = 54
    NUMBER = 55
    STRING = 56
    FSTRING = 57
    ID = 58
    WS = 59
    LINE_COMMENT = 60
    LINE_COMMENT2 = 61
    BLOCK_COMMENT = 62

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None

    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(transpilerParser.EOF, 0)

        def includeStmt(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.IncludeStmtContext)
            else:
                return self.getTypedRuleContext(transpilerParser.IncludeStmtContext, i)

        def classDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ClassDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ClassDeclContext, i)

        def interfaceDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.InterfaceDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.InterfaceDeclContext, i)

        def functionDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.FunctionDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.FunctionDeclContext, i)

        def varDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.VarDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.VarDeclContext, i)

        def constDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ConstDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ConstDeclContext, i)

        def SEMI(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.SEMI)
            else:
                return self.getToken(transpilerParser.SEMI, i)

        def getRuleIndex(self):
            return transpilerParser.RULE_program

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterProgram"):
                listener.enterProgram(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitProgram"):
                listener.exitProgram(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitProgram"):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)

    def program(self):

        localctx = transpilerParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 16:
                self.state = 62
                self.includeStmt()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230380473548802) != 0):
                self.state = 79
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 3, self._ctx)
                if la_ == 1:
                    self.state = 68
                    self.classDecl()
                    pass

                elif la_ == 2:
                    self.state = 69
                    self.interfaceDecl()
                    pass

                elif la_ == 3:
                    self.state = 70
                    self.functionDecl()
                    pass

                elif la_ == 4:
                    self.state = 71
                    self.varDecl()
                    self.state = 73
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == 10:
                        self.state = 72
                        self.match(transpilerParser.SEMI)

                    pass

                elif la_ == 5:
                    self.state = 75
                    self.constDecl()
                    self.state = 77
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == 10:
                        self.state = 76
                        self.match(transpilerParser.SEMI)

                    pass

                self.state = 83
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 84
            self.match(transpilerParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IncludeStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INCLUDE(self):
            return self.getToken(transpilerParser.INCLUDE, 0)

        def literal(self):
            return self.getTypedRuleContext(transpilerParser.LiteralContext, 0)

        def SEMI(self):
            return self.getToken(transpilerParser.SEMI, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_includeStmt

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterIncludeStmt"):
                listener.enterIncludeStmt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitIncludeStmt"):
                listener.exitIncludeStmt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIncludeStmt"):
                return visitor.visitIncludeStmt(self)
            else:
                return visitor.visitChildren(self)

    def includeStmt(self):

        localctx = transpilerParser.IncludeStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_includeStmt)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(transpilerParser.INCLUDE)
            self.state = 87
            self.literal()
            self.state = 89
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 10:
                self.state = 88
                self.match(transpilerParser.SEMI)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AnnotationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def LPAREN(self):
            return self.getToken(transpilerParser.LPAREN, 0)

        def literal(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.LiteralContext)
            else:
                return self.getTypedRuleContext(transpilerParser.LiteralContext, i)

        def RPAREN(self):
            return self.getToken(transpilerParser.RPAREN, 0)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.COMMA)
            else:
                return self.getToken(transpilerParser.COMMA, i)

        def getRuleIndex(self):
            return transpilerParser.RULE_annotation

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAnnotation"):
                listener.enterAnnotation(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAnnotation"):
                listener.exitAnnotation(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAnnotation"):
                return visitor.visitAnnotation(self)
            else:
                return visitor.visitChildren(self)

    def annotation(self):

        localctx = transpilerParser.AnnotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_annotation)
        self._la = 0  # Token type
        try:
            self.state = 106
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 7, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 91
                self.match(transpilerParser.T__0)
                self.state = 92
                self.match(transpilerParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 93
                self.match(transpilerParser.T__0)
                self.state = 94
                self.match(transpilerParser.ID)
                self.state = 95
                self.match(transpilerParser.LPAREN)
                self.state = 96
                self.literal()
                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 11:
                    self.state = 97
                    self.match(transpilerParser.COMMA)
                    self.state = 98
                    self.literal()
                    self.state = 103
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 104
                self.match(transpilerParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ClassDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CLASS(self):
            return self.getToken(transpilerParser.CLASS, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def LBRACE(self):
            return self.getToken(transpilerParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(transpilerParser.RBRACE, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(transpilerParser.AnnotationContext, i)

        def EXTENDS(self):
            return self.getToken(transpilerParser.EXTENDS, 0)

        def type_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.TypeContext)
            else:
                return self.getTypedRuleContext(transpilerParser.TypeContext, i)

        def IMPLEMENTS(self):
            return self.getToken(transpilerParser.IMPLEMENTS, 0)

        def classPropertyDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ClassPropertyDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ClassPropertyDeclContext, i)

        def methodDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.MethodDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.MethodDeclContext, i)

        def SEMI(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.SEMI)
            else:
                return self.getToken(transpilerParser.SEMI, i)

        def getRuleIndex(self):
            return transpilerParser.RULE_classDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterClassDecl"):
                listener.enterClassDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitClassDecl"):
                listener.exitClassDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitClassDecl"):
                return visitor.visitClassDecl(self)
            else:
                return visitor.visitChildren(self)

    def classDecl(self):

        localctx = transpilerParser.ClassDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_classDecl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 108
                self.annotation()
                self.state = 113
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 114
            self.match(transpilerParser.CLASS)
            self.state = 115
            self.match(transpilerParser.ID)
            self.state = 118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 21:
                self.state = 116
                self.match(transpilerParser.EXTENDS)
                self.state = 117
                self.type_()

            self.state = 122
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 22:
                self.state = 120
                self.match(transpilerParser.IMPLEMENTS)
                self.state = 121
                self.type_()

            self.state = 124
            self.match(transpilerParser.LBRACE)
            self.state = 132
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230380463718402) != 0):
                self.state = 130
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [24, 32, 58]:
                    self.state = 125
                    self.classPropertyDecl()
                    self.state = 127
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == 10:
                        self.state = 126
                        self.match(transpilerParser.SEMI)

                    pass
                elif token in [1, 18]:
                    self.state = 129
                    self.methodDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 134
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 135
            self.match(transpilerParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class InterfaceDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTERFACE(self):
            return self.getToken(transpilerParser.INTERFACE, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def LBRACE(self):
            return self.getToken(transpilerParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(transpilerParser.RBRACE, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(transpilerParser.AnnotationContext, i)

        def EXTENDS(self):
            return self.getToken(transpilerParser.EXTENDS, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def classPropertyDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ClassPropertyDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ClassPropertyDeclContext, i)

        def methodDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.MethodDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.MethodDeclContext, i)

        def SEMI(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.SEMI)
            else:
                return self.getToken(transpilerParser.SEMI, i)

        def getRuleIndex(self):
            return transpilerParser.RULE_interfaceDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterInterfaceDecl"):
                listener.enterInterfaceDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitInterfaceDecl"):
                listener.exitInterfaceDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitInterfaceDecl"):
                return visitor.visitInterfaceDecl(self)
            else:
                return visitor.visitChildren(self)

    def interfaceDecl(self):

        localctx = transpilerParser.InterfaceDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_interfaceDecl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 137
                self.annotation()
                self.state = 142
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 143
            self.match(transpilerParser.INTERFACE)
            self.state = 144
            self.match(transpilerParser.ID)
            self.state = 147
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 21:
                self.state = 145
                self.match(transpilerParser.EXTENDS)
                self.state = 146
                self.type_()

            self.state = 149
            self.match(transpilerParser.LBRACE)
            self.state = 157
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230380463718402) != 0):
                self.state = 155
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [24, 32, 58]:
                    self.state = 150
                    self.classPropertyDecl()
                    self.state = 152
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == 10:
                        self.state = 151
                        self.match(transpilerParser.SEMI)

                    pass
                elif token in [1, 18]:
                    self.state = 154
                    self.methodDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 159
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 160
            self.match(transpilerParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ClassPropertyDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def QUESTION(self):
            return self.getToken(transpilerParser.QUESTION, 0)

        def LET(self):
            return self.getToken(transpilerParser.LET, 0)

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def COLON(self):
            return self.getToken(transpilerParser.COLON, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_classPropertyDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterClassPropertyDecl"):
                listener.enterClassPropertyDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitClassPropertyDecl"):
                listener.exitClassPropertyDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitClassPropertyDecl"):
                return visitor.visitClassPropertyDecl(self)
            else:
                return visitor.visitChildren(self)

    def classPropertyDecl(self):

        localctx = transpilerParser.ClassPropertyDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_classPropertyDecl)
        self._la = 0  # Token type
        try:
            self.state = 174
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32, 58]:
                self.enterOuterAlt(localctx, 1)
                self.state = 162
                self.type_()
                self.state = 163
                self.match(transpilerParser.ID)
                self.state = 165
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 164
                    self.match(transpilerParser.QUESTION)

                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 2)
                self.state = 167
                self.match(transpilerParser.LET)
                self.state = 168
                self.match(transpilerParser.ID)
                self.state = 170
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 169
                    self.match(transpilerParser.QUESTION)

                self.state = 172
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 173
                self.type_()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def LBRACK(self):
            return self.getToken(transpilerParser.LBRACK, 0)

        def NUMBER(self):
            return self.getToken(transpilerParser.NUMBER, 0)

        def RBRACK(self):
            return self.getToken(transpilerParser.RBRACK, 0)

        def NULL(self):
            return self.getToken(transpilerParser.NULL, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_type

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterType"):
                listener.enterType(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitType"):
                listener.exitType(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitType"):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)

    def type_(self):

        localctx = transpilerParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_type)
        self._la = 0  # Token type
        try:
            self.state = 183
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [58]:
                self.enterOuterAlt(localctx, 1)
                self.state = 176
                self.match(transpilerParser.ID)
                self.state = 180
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 6:
                    self.state = 177
                    self.match(transpilerParser.LBRACK)
                    self.state = 178
                    self.match(transpilerParser.NUMBER)
                    self.state = 179
                    self.match(transpilerParser.RBRACK)

                pass
            elif token in [32]:
                self.enterOuterAlt(localctx, 2)
                self.state = 182
                self.match(transpilerParser.NULL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FunctionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNC(self):
            return self.getToken(transpilerParser.FUNC, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def paramList(self):
            return self.getTypedRuleContext(transpilerParser.ParamListContext, 0)

        def block(self):
            return self.getTypedRuleContext(transpilerParser.BlockContext, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(transpilerParser.AnnotationContext, i)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def COLON(self):
            return self.getToken(transpilerParser.COLON, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_functionDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFunctionDecl"):
                listener.enterFunctionDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFunctionDecl"):
                listener.exitFunctionDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFunctionDecl"):
                return visitor.visitFunctionDecl(self)
            else:
                return visitor.visitChildren(self)

    def functionDecl(self):

        localctx = transpilerParser.FunctionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_functionDecl)
        self._la = 0  # Token type
        try:
            self.state = 222
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 27, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 188
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 185
                    self.annotation()
                    self.state = 190
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 191
                self.match(transpilerParser.FUNC)
                self.state = 192
                self.match(transpilerParser.ID)
                self.state = 193
                self.paramList()
                self.state = 194
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 199
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 196
                    self.annotation()
                    self.state = 201
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 202
                self.match(transpilerParser.FUNC)
                self.state = 203
                self.match(transpilerParser.ID)
                self.state = 204
                self.paramList()

                self.state = 205
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 206
                self.type_()
                self.state = 208
                self.block()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 213
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 210
                    self.annotation()
                    self.state = 215
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 216
                self.match(transpilerParser.FUNC)
                self.state = 217
                self.type_()
                self.state = 218
                self.match(transpilerParser.ID)
                self.state = 219
                self.paramList()
                self.state = 220
                self.block()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class MethodDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def METHOD(self):
            return self.getToken(transpilerParser.METHOD, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def paramList(self):
            return self.getTypedRuleContext(transpilerParser.ParamListContext, 0)

        def block(self):
            return self.getTypedRuleContext(transpilerParser.BlockContext, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(transpilerParser.AnnotationContext, i)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def COLON(self):
            return self.getToken(transpilerParser.COLON, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_methodDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterMethodDecl"):
                listener.enterMethodDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitMethodDecl"):
                listener.exitMethodDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMethodDecl"):
                return visitor.visitMethodDecl(self)
            else:
                return visitor.visitChildren(self)

    def methodDecl(self):

        localctx = transpilerParser.MethodDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_methodDecl)
        self._la = 0  # Token type
        try:
            self.state = 261
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 31, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 227
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 224
                    self.annotation()
                    self.state = 229
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 230
                self.match(transpilerParser.METHOD)
                self.state = 231
                self.match(transpilerParser.ID)
                self.state = 232
                self.paramList()
                self.state = 233
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 238
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 235
                    self.annotation()
                    self.state = 240
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 241
                self.match(transpilerParser.METHOD)
                self.state = 242
                self.match(transpilerParser.ID)
                self.state = 243
                self.paramList()

                self.state = 244
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 245
                self.type_()
                self.state = 247
                self.block()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 252
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 249
                    self.annotation()
                    self.state = 254
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 255
                self.match(transpilerParser.METHOD)
                self.state = 256
                self.type_()
                self.state = 257
                self.match(transpilerParser.ID)
                self.state = 258
                self.paramList()
                self.state = 259
                self.block()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(transpilerParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(transpilerParser.RPAREN, 0)

        def paramDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ParamDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ParamDeclContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.COMMA)
            else:
                return self.getToken(transpilerParser.COMMA, i)

        def PAREN(self):
            return self.getToken(transpilerParser.PAREN, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_paramList

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterParamList"):
                listener.enterParamList(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitParamList"):
                listener.exitParamList(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitParamList"):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)

    def paramList(self):

        localctx = transpilerParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_paramList)
        self._la = 0  # Token type
        try:
            self.state = 276
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 263
                self.match(transpilerParser.LPAREN)
                self.state = 272
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 32 or _la == 58:
                    self.state = 264
                    self.paramDecl()
                    self.state = 269
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == 11:
                        self.state = 265
                        self.match(transpilerParser.COMMA)
                        self.state = 266
                        self.paramDecl()
                        self.state = 271
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                self.state = 274
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 275
                self.match(transpilerParser.PAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ParamDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def COLON(self):
            return self.getToken(transpilerParser.COLON, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_paramDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterParamDecl"):
                listener.enterParamDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitParamDecl"):
                listener.exitParamDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitParamDecl"):
                return visitor.visitParamDecl(self)
            else:
                return visitor.visitChildren(self)

    def paramDecl(self):

        localctx = transpilerParser.ParamDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_paramDecl)
        self._la = 0  # Token type
        try:
            self.state = 291
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 37, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 278
                self.match(transpilerParser.ID)
                self.state = 279
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 280
                self.type_()
                self.state = 283
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 35:
                    self.state = 281
                    self.match(transpilerParser.ASSIGN)
                    self.state = 282
                    self.expr(0)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 285
                self.type_()
                self.state = 286
                self.match(transpilerParser.ID)
                self.state = 289
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 35:
                    self.state = 287
                    self.match(transpilerParser.ASSIGN)
                    self.state = 288
                    self.expr(0)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(transpilerParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(transpilerParser.RBRACE, 0)

        def statement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.StatementContext)
            else:
                return self.getTypedRuleContext(transpilerParser.StatementContext, i)

        def SEMI(self):
            return self.getToken(transpilerParser.SEMI, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_block

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterBlock"):
                listener.enterBlock(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitBlock"):
                listener.exitBlock(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBlock"):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)

    def block(self):

        localctx = transpilerParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_block)
        self._la = 0  # Token type
        try:
            self.state = 302
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 293
                self.match(transpilerParser.LBRACE)
                self.state = 297
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 540504556866503698) != 0):
                    self.state = 294
                    self.statement()
                    self.state = 299
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 300
                self.match(transpilerParser.RBRACE)
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 2)
                self.state = 301
                self.match(transpilerParser.SEMI)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionDecl(self):
            return self.getTypedRuleContext(transpilerParser.FunctionDeclContext, 0)

        def varDecl(self):
            return self.getTypedRuleContext(transpilerParser.VarDeclContext, 0)

        def SEMI(self):
            return self.getToken(transpilerParser.SEMI, 0)

        def constDecl(self):
            return self.getTypedRuleContext(transpilerParser.ConstDeclContext, 0)

        def forStmt(self):
            return self.getTypedRuleContext(transpilerParser.ForStmtContext, 0)

        def whileStmt(self):
            return self.getTypedRuleContext(transpilerParser.WhileStmtContext, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def returnStmt(self):
            return self.getTypedRuleContext(transpilerParser.ReturnStmtContext, 0)

        def ifStmt(self):
            return self.getTypedRuleContext(transpilerParser.IfStmtContext, 0)

        def breakStmt(self):
            return self.getTypedRuleContext(transpilerParser.BreakStmtContext, 0)

        def continueStmt(self):
            return self.getTypedRuleContext(transpilerParser.ContinueStmtContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_statement

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterStatement"):
                listener.enterStatement(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitStatement"):
                listener.exitStatement(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitStatement"):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)

    def statement(self):

        localctx = transpilerParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_statement)
        try:
            self.state = 333
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 46, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 304
                self.functionDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 305
                self.varDecl()
                self.state = 307
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 40, self._ctx)
                if la_ == 1:
                    self.state = 306
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 309
                self.constDecl()
                self.state = 311
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 41, self._ctx)
                if la_ == 1:
                    self.state = 310
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 313
                self.forStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 314
                self.whileStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 315
                self.expr(0)
                self.state = 317
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 42, self._ctx)
                if la_ == 1:
                    self.state = 316
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 319
                self.returnStmt()
                self.state = 321
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 43, self._ctx)
                if la_ == 1:
                    self.state = 320
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 323
                self.ifStmt()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 324
                self.breakStmt()
                self.state = 326
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 44, self._ctx)
                if la_ == 1:
                    self.state = 325
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 328
                self.continueStmt()
                self.state = 330
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 45, self._ctx)
                if la_ == 1:
                    self.state = 329
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 332
                self.match(transpilerParser.SEMI)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BreakStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(transpilerParser.BREAK, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_breakStmt

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterBreakStmt"):
                listener.enterBreakStmt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitBreakStmt"):
                listener.exitBreakStmt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitBreakStmt"):
                return visitor.visitBreakStmt(self)
            else:
                return visitor.visitChildren(self)

    def breakStmt(self):

        localctx = transpilerParser.BreakStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_breakStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 335
            self.match(transpilerParser.BREAK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ContinueStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTINUE(self):
            return self.getToken(transpilerParser.CONTINUE, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_continueStmt

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterContinueStmt"):
                listener.enterContinueStmt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitContinueStmt"):
                listener.exitContinueStmt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitContinueStmt"):
                return visitor.visitContinueStmt(self)
            else:
                return visitor.visitChildren(self)

    def continueStmt(self):

        localctx = transpilerParser.ContinueStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_continueStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 337
            self.match(transpilerParser.CONTINUE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ForStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(transpilerParser.FOR, 0)

        def LPAREN(self):
            return self.getToken(transpilerParser.LPAREN, 0)

        def forControl(self):
            return self.getTypedRuleContext(transpilerParser.ForControlContext, 0)

        def RPAREN(self):
            return self.getToken(transpilerParser.RPAREN, 0)

        def statementBlock(self):
            return self.getTypedRuleContext(transpilerParser.StatementBlockContext, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def COLON(self):
            return self.getToken(transpilerParser.COLON, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_forStmt

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterForStmt"):
                listener.enterForStmt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitForStmt"):
                listener.exitForStmt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitForStmt"):
                return visitor.visitForStmt(self)
            else:
                return visitor.visitChildren(self)

    def forStmt(self):

        localctx = transpilerParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_forStmt)
        try:
            self.state = 354
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 47, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 339
                self.match(transpilerParser.FOR)
                self.state = 340
                self.match(transpilerParser.LPAREN)
                self.state = 341
                self.forControl()
                self.state = 342
                self.match(transpilerParser.RPAREN)
                self.state = 343
                self.statementBlock()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 345
                self.match(transpilerParser.FOR)
                self.state = 346
                self.match(transpilerParser.LPAREN)
                self.state = 347
                self.type_()
                self.state = 348
                self.match(transpilerParser.ID)
                self.state = 349
                self.match(transpilerParser.COLON)
                self.state = 350
                self.expr(0)
                self.state = 351
                self.match(transpilerParser.RPAREN)
                self.state = 352
                self.statementBlock()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ForControlContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEMI(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.SEMI)
            else:
                return self.getToken(transpilerParser.SEMI, i)

        def forInit(self):
            return self.getTypedRuleContext(transpilerParser.ForInitContext, 0)

        def condition(self):
            return self.getTypedRuleContext(transpilerParser.ConditionContext, 0)

        def forUpdate(self):
            return self.getTypedRuleContext(transpilerParser.ForUpdateContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_forControl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterForControl"):
                listener.enterForControl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitForControl"):
                listener.exitForControl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitForControl"):
                return visitor.visitForControl(self)
            else:
                return visitor.visitChildren(self)

    def forControl(self):

        localctx = transpilerParser.ForControlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_forControl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 357
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540504530584862736) != 0):
                self.state = 356
                self.forInit()

            self.state = 359
            self.match(transpilerParser.SEMI)
            self.state = 361
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540504530568085520) != 0):
                self.state = 360
                self.condition()

            self.state = 363
            self.match(transpilerParser.SEMI)
            self.state = 365
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540504530568085520) != 0):
                self.state = 364
                self.forUpdate()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ForInitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varDecl(self):
            return self.getTypedRuleContext(transpilerParser.VarDeclContext, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_forInit

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterForInit"):
                listener.enterForInit(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitForInit"):
                listener.exitForInit(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitForInit"):
                return visitor.visitForInit(self)
            else:
                return visitor.visitChildren(self)

    def forInit(self):

        localctx = transpilerParser.ForInitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_forInit)
        try:
            self.state = 369
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 51, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 367
                self.varDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 368
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_condition

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCondition"):
                listener.enterCondition(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCondition"):
                listener.exitCondition(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCondition"):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)

    def condition(self):

        localctx = transpilerParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 371
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ForUpdateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_forUpdate

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterForUpdate"):
                listener.enterForUpdate(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitForUpdate"):
                listener.exitForUpdate(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitForUpdate"):
                return visitor.visitForUpdate(self)
            else:
                return visitor.visitChildren(self)

    def forUpdate(self):

        localctx = transpilerParser.ForUpdateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_forUpdate)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 373
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(transpilerParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(transpilerParser.LPAREN, 0)

        def condition(self):
            return self.getTypedRuleContext(transpilerParser.ConditionContext, 0)

        def RPAREN(self):
            return self.getToken(transpilerParser.RPAREN, 0)

        def statementBlock(self):
            return self.getTypedRuleContext(transpilerParser.StatementBlockContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_whileStmt

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterWhileStmt"):
                listener.enterWhileStmt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitWhileStmt"):
                listener.exitWhileStmt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitWhileStmt"):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)

    def whileStmt(self):

        localctx = transpilerParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 375
            self.match(transpilerParser.WHILE)
            self.state = 376
            self.match(transpilerParser.LPAREN)
            self.state = 377
            self.condition()
            self.state = 378
            self.match(transpilerParser.RPAREN)
            self.state = 379
            self.statementBlock()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConstDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONST(self):
            return self.getToken(transpilerParser.CONST, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def QUESTION(self):
            return self.getToken(transpilerParser.QUESTION, 0)

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def COLON(self):
            return self.getToken(transpilerParser.COLON, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_constDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterConstDecl"):
                listener.enterConstDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitConstDecl"):
                listener.exitConstDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitConstDecl"):
                return visitor.visitConstDecl(self)
            else:
                return visitor.visitChildren(self)

    def constDecl(self):

        localctx = transpilerParser.ConstDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_constDecl)
        self._la = 0  # Token type
        try:
            self.state = 398
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 54, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 381
                self.match(transpilerParser.CONST)
                self.state = 382
                self.match(transpilerParser.ID)
                self.state = 385
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13 or _la == 14:
                    self.state = 383
                    _la = self._input.LA(1)
                    if not (_la == 13 or _la == 14):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 384
                    self.type_()

                self.state = 388
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 387
                    self.match(transpilerParser.QUESTION)

                self.state = 390
                self.match(transpilerParser.ASSIGN)
                self.state = 391
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 392
                self.match(transpilerParser.CONST)
                self.state = 393
                self.type_()
                self.state = 394
                self.match(transpilerParser.ID)

                self.state = 395
                self.match(transpilerParser.ASSIGN)
                self.state = 396
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class VarDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LET(self):
            return self.getToken(transpilerParser.LET, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def QUESTION(self):
            return self.getToken(transpilerParser.QUESTION, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def COLON(self):
            return self.getToken(transpilerParser.COLON, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_varDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterVarDecl"):
                listener.enterVarDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitVarDecl"):
                listener.exitVarDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitVarDecl"):
                return visitor.visitVarDecl(self)
            else:
                return visitor.visitChildren(self)

    def varDecl(self):

        localctx = transpilerParser.VarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_varDecl)
        self._la = 0  # Token type
        try:
            self.state = 443
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 62, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 400
                self.match(transpilerParser.LET)
                self.state = 401
                self.match(transpilerParser.ID)
                self.state = 403
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 402
                    self.match(transpilerParser.QUESTION)

                self.state = 405
                self.match(transpilerParser.ASSIGN)
                self.state = 406
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 407
                self.match(transpilerParser.ID)
                self.state = 408
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 409
                self.type_()
                self.state = 411
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 410
                    self.match(transpilerParser.QUESTION)

                self.state = 415
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 35:
                    self.state = 413
                    self.match(transpilerParser.ASSIGN)
                    self.state = 414
                    self.expr(0)

                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 417
                self.type_()
                self.state = 418
                self.match(transpilerParser.ID)
                self.state = 420
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 419
                    self.match(transpilerParser.QUESTION)

                self.state = 424
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 35:
                    self.state = 422
                    self.match(transpilerParser.ASSIGN)
                    self.state = 423
                    self.expr(0)

                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 426
                self.match(transpilerParser.LET)
                self.state = 427
                self.match(transpilerParser.ID)
                self.state = 429
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 428
                    self.match(transpilerParser.QUESTION)

                self.state = 431
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 432
                self.type_()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 433
                self.match(transpilerParser.LET)
                self.state = 434
                self.match(transpilerParser.ID)
                self.state = 436
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 435
                    self.match(transpilerParser.QUESTION)

                self.state = 438
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 439
                self.type_()
                self.state = 440
                self.match(transpilerParser.ASSIGN)
                self.state = 441
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(transpilerParser.RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_returnStmt

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterReturnStmt"):
                listener.enterReturnStmt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitReturnStmt"):
                listener.exitReturnStmt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitReturnStmt"):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)

    def returnStmt(self):

        localctx = transpilerParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_returnStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 445
            self.match(transpilerParser.RETURN)
            self.state = 447
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 63, self._ctx)
            if la_ == 1:
                self.state = 446
                self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(transpilerParser.IF, 0)

        def LPAREN(self):
            return self.getToken(transpilerParser.LPAREN, 0)

        def condition(self):
            return self.getTypedRuleContext(transpilerParser.ConditionContext, 0)

        def RPAREN(self):
            return self.getToken(transpilerParser.RPAREN, 0)

        def statementBlock(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.StatementBlockContext)
            else:
                return self.getTypedRuleContext(transpilerParser.StatementBlockContext, i)

        def ELSE(self):
            return self.getToken(transpilerParser.ELSE, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_ifStmt

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterIfStmt"):
                listener.enterIfStmt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitIfStmt"):
                listener.exitIfStmt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIfStmt"):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)

    def ifStmt(self):

        localctx = transpilerParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_ifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 449
            self.match(transpilerParser.IF)
            self.state = 450
            self.match(transpilerParser.LPAREN)
            self.state = 451
            self.condition()
            self.state = 452
            self.match(transpilerParser.RPAREN)
            self.state = 453
            self.statementBlock()
            self.state = 456
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 64, self._ctx)
            if la_ == 1:
                self.state = 454
                self.match(transpilerParser.ELSE)
                self.state = 455
                self.statementBlock()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StatementBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self):
            return self.getTypedRuleContext(transpilerParser.StatementContext, 0)

        def block(self):
            return self.getTypedRuleContext(transpilerParser.BlockContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_statementBlock

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterStatementBlock"):
                listener.enterStatementBlock(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitStatementBlock"):
                listener.exitStatementBlock(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitStatementBlock"):
                return visitor.visitStatementBlock(self)
            else:
                return visitor.visitChildren(self)

    def statementBlock(self):

        localctx = transpilerParser.StatementBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_statementBlock)
        try:
            self.state = 460
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 65, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 458
                self.statement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 459
                self.block()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return transpilerParser.RULE_expr

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class TermExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def ADD(self):
            return self.getToken(transpilerParser.ADD, 0)

        def SUB(self):
            return self.getToken(transpilerParser.SUB, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterTermExpr"):
                listener.enterTermExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitTermExpr"):
                listener.exitTermExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTermExpr"):
                return visitor.visitTermExpr(self)
            else:
                return visitor.visitChildren(self)

    class NegExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SUB(self):
            return self.getToken(transpilerParser.SUB, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNegExpr"):
                listener.enterNegExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNegExpr"):
                listener.exitNegExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNegExpr"):
                return visitor.visitNegExpr(self)
            else:
                return visitor.visitChildren(self)

    class LogicalNotExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(transpilerParser.NOT, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLogicalNotExpr"):
                listener.enterLogicalNotExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLogicalNotExpr"):
                listener.exitLogicalNotExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLogicalNotExpr"):
                return visitor.visitLogicalNotExpr(self)
            else:
                return visitor.visitChildren(self)

    class MemberAssignmentExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterMemberAssignmentExpr"):
                listener.enterMemberAssignmentExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitMemberAssignmentExpr"):
                listener.exitMemberAssignmentExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMemberAssignmentExpr"):
                return visitor.visitMemberAssignmentExpr(self)
            else:
                return visitor.visitChildren(self)

    class LocalAssignmentExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLocalAssignmentExpr"):
                listener.enterLocalAssignmentExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLocalAssignmentExpr"):
                listener.exitLocalAssignmentExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLocalAssignmentExpr"):
                return visitor.visitLocalAssignmentExpr(self)
            else:
                return visitor.visitChildren(self)

    class LogicalAndExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def AND(self):
            return self.getToken(transpilerParser.AND, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLogicalAndExpr"):
                listener.enterLogicalAndExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLogicalAndExpr"):
                listener.exitLogicalAndExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLogicalAndExpr"):
                return visitor.visitLogicalAndExpr(self)
            else:
                return visitor.visitChildren(self)

    class MethodCallContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def argumentList(self):
            return self.getTypedRuleContext(transpilerParser.ArgumentListContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterMethodCall"):
                listener.enterMethodCall(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitMethodCall"):
                listener.exitMethodCall(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMethodCall"):
                return visitor.visitMethodCall(self)
            else:
                return visitor.visitChildren(self)

    class LogicalOrExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def OR(self):
            return self.getToken(transpilerParser.OR, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLogicalOrExpr"):
                listener.enterLogicalOrExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLogicalOrExpr"):
                listener.exitLogicalOrExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLogicalOrExpr"):
                return visitor.visitLogicalOrExpr(self)
            else:
                return visitor.visitChildren(self)

    class ArrayAccessContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def LBRACK(self):
            return self.getToken(transpilerParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(transpilerParser.RBRACK, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterArrayAccess"):
                listener.enterArrayAccess(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitArrayAccess"):
                listener.exitArrayAccess(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitArrayAccess"):
                return visitor.visitArrayAccess(self)
            else:
                return visitor.visitChildren(self)

    class MemberAccessContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterMemberAccess"):
                listener.enterMemberAccess(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitMemberAccess"):
                listener.exitMemberAccess(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMemberAccess"):
                return visitor.visitMemberAccess(self)
            else:
                return visitor.visitChildren(self)

    class CompareExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def GT(self):
            return self.getToken(transpilerParser.GT, 0)

        def LT(self):
            return self.getToken(transpilerParser.LT, 0)

        def EQ(self):
            return self.getToken(transpilerParser.EQ, 0)

        def NEQ(self):
            return self.getToken(transpilerParser.NEQ, 0)

        def LTE(self):
            return self.getToken(transpilerParser.LTE, 0)

        def GTE(self):
            return self.getToken(transpilerParser.GTE, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCompareExpr"):
                listener.enterCompareExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCompareExpr"):
                listener.exitCompareExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCompareExpr"):
                return visitor.visitCompareExpr(self)
            else:
                return visitor.visitChildren(self)

    class TernaryPythonicExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def IF(self):
            return self.getToken(transpilerParser.IF, 0)

        def ELSE(self):
            return self.getToken(transpilerParser.ELSE, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterTernaryPythonicExpr"):
                listener.enterTernaryPythonicExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitTernaryPythonicExpr"):
                listener.exitTernaryPythonicExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTernaryPythonicExpr"):
                return visitor.visitTernaryPythonicExpr(self)
            else:
                return visitor.visitChildren(self)

    class PrimaryExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def primary(self):
            return self.getTypedRuleContext(transpilerParser.PrimaryContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterPrimaryExpr"):
                listener.enterPrimaryExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitPrimaryExpr"):
                listener.exitPrimaryExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitPrimaryExpr"):
                return visitor.visitPrimaryExpr(self)
            else:
                return visitor.visitChildren(self)

    class ArrayAssignmentExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def LBRACK(self):
            return self.getToken(transpilerParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(transpilerParser.RBRACK, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterArrayAssignmentExpr"):
                listener.enterArrayAssignmentExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitArrayAssignmentExpr"):
                listener.exitArrayAssignmentExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitArrayAssignmentExpr"):
                return visitor.visitArrayAssignmentExpr(self)
            else:
                return visitor.visitChildren(self)

    class TernaryTraditionalExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def QUESTION(self):
            return self.getToken(transpilerParser.QUESTION, 0)

        def COLON(self):
            return self.getToken(transpilerParser.COLON, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterTernaryTraditionalExpr"):
                listener.enterTernaryTraditionalExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitTernaryTraditionalExpr"):
                listener.exitTernaryTraditionalExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTernaryTraditionalExpr"):
                return visitor.visitTernaryTraditionalExpr(self)
            else:
                return visitor.visitChildren(self)

    class FunctionCallContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def argumentList(self):
            return self.getTypedRuleContext(transpilerParser.ArgumentListContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFunctionCall"):
                listener.enterFunctionCall(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFunctionCall"):
                listener.exitFunctionCall(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFunctionCall"):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)

    class FactorExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def MUL(self):
            return self.getToken(transpilerParser.MUL, 0)

        def DIV(self):
            return self.getToken(transpilerParser.DIV, 0)

        def MOD(self):
            return self.getToken(transpilerParser.MOD, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterFactorExpr"):
                listener.enterFactorExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitFactorExpr"):
                listener.exitFactorExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitFactorExpr"):
                return visitor.visitFactorExpr(self)
            else:
                return visitor.visitChildren(self)

    def expr(self, _p: int = 0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = transpilerParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 52
        self.enterRecursionRule(localctx, 52, self.RULE_expr, _p)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 471
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 66, self._ctx)
            if la_ == 1:
                localctx = transpilerParser.PrimaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 463
                self.primary()
                pass

            elif la_ == 2:
                localctx = transpilerParser.NegExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 464
                self.match(transpilerParser.SUB)
                self.state = 465
                self.expr(12)
                pass

            elif la_ == 3:
                localctx = transpilerParser.LogicalNotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 466
                self.match(transpilerParser.NOT)
                self.state = 467
                self.expr(11)
                pass

            elif la_ == 4:
                localctx = transpilerParser.LocalAssignmentExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 468
                self.match(transpilerParser.ID)
                self.state = 469
                self.match(transpilerParser.ASSIGN)
                self.state = 470
                self.expr(1)
                pass

            self._ctx.stop = self._input.LT(-1)
            self.state = 528
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 68, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 526
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 67, self._ctx)
                    if la_ == 1:
                        localctx = transpilerParser.FactorExprContext(self,
                                                                      transpilerParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 473
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 474
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 30786325577728) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 475
                        self.expr(11)
                        pass

                    elif la_ == 2:
                        localctx = transpilerParser.TermExprContext(self, transpilerParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 476
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 477
                        _la = self._input.LA(1)
                        if not (_la == 45 or _la == 46):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 478
                        self.expr(10)
                        pass

                    elif la_ == 3:
                        localctx = transpilerParser.CompareExprContext(self,
                                                                       transpilerParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 479
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 480
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 8866461766385664) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 481
                        self.expr(9)
                        pass

                    elif la_ == 4:
                        localctx = transpilerParser.LogicalAndExprContext(self,
                                                                          transpilerParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 482
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 483
                        self.match(transpilerParser.AND)
                        self.state = 484
                        self.expr(8)
                        pass

                    elif la_ == 5:
                        localctx = transpilerParser.LogicalOrExprContext(self,
                                                                         transpilerParser.ExprContext(self, _parentctx,
                                                                                                      _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 485
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 486
                        self.match(transpilerParser.OR)
                        self.state = 487
                        self.expr(7)
                        pass

                    elif la_ == 6:
                        localctx = transpilerParser.TernaryTraditionalExprContext(self,
                                                                                  transpilerParser.ExprContext(self,
                                                                                                               _parentctx,
                                                                                                               _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 488
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 489
                        self.match(transpilerParser.QUESTION)
                        self.state = 490
                        self.expr(0)
                        self.state = 491
                        self.match(transpilerParser.COLON)
                        self.state = 492
                        self.expr(5)
                        pass

                    elif la_ == 7:
                        localctx = transpilerParser.TernaryPythonicExprContext(self, transpilerParser.ExprContext(self,
                                                                                                                  _parentctx,
                                                                                                                  _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 494
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 495
                        self.match(transpilerParser.IF)
                        self.state = 496
                        self.expr(0)
                        self.state = 497
                        self.match(transpilerParser.ELSE)
                        self.state = 498
                        self.expr(4)
                        pass

                    elif la_ == 8:
                        localctx = transpilerParser.ArrayAssignmentExprContext(self, transpilerParser.ExprContext(self,
                                                                                                                  _parentctx,
                                                                                                                  _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 500
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 501
                        self.match(transpilerParser.LBRACK)
                        self.state = 502
                        self.expr(0)
                        self.state = 503
                        self.match(transpilerParser.RBRACK)
                        self.state = 504
                        self.match(transpilerParser.ASSIGN)
                        self.state = 505
                        self.expr(4)
                        pass

                    elif la_ == 9:
                        localctx = transpilerParser.MemberAssignmentExprContext(self, transpilerParser.ExprContext(self,
                                                                                                                   _parentctx,
                                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 507
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 508
                        self.match(transpilerParser.T__1)
                        self.state = 509
                        self.match(transpilerParser.ID)
                        self.state = 510
                        self.match(transpilerParser.ASSIGN)
                        self.state = 511
                        self.expr(3)
                        pass

                    elif la_ == 10:
                        localctx = transpilerParser.MethodCallContext(self,
                                                                      transpilerParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 512
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 513
                        self.match(transpilerParser.T__1)
                        self.state = 514
                        self.match(transpilerParser.ID)
                        self.state = 515
                        self.argumentList()
                        pass

                    elif la_ == 11:
                        localctx = transpilerParser.MemberAccessContext(self,
                                                                        transpilerParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 516
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 517
                        self.match(transpilerParser.T__1)
                        self.state = 518
                        self.match(transpilerParser.ID)
                        pass

                    elif la_ == 12:
                        localctx = transpilerParser.ArrayAccessContext(self,
                                                                       transpilerParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 519
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 520
                        self.match(transpilerParser.LBRACK)
                        self.state = 521
                        self.expr(0)
                        self.state = 522
                        self.match(transpilerParser.RBRACK)
                        pass

                    elif la_ == 13:
                        localctx = transpilerParser.FunctionCallContext(self,
                                                                        transpilerParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 524
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 525
                        self.argumentList()
                        pass

                self.state = 530
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 68, self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return transpilerParser.RULE_primary

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class IdentifierExprContext(PrimaryContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterIdentifierExpr"):
                listener.enterIdentifierExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitIdentifierExpr"):
                listener.exitIdentifierExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitIdentifierExpr"):
                return visitor.visitIdentifierExpr(self)
            else:
                return visitor.visitChildren(self)

    class LiteralExprContext(PrimaryContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(transpilerParser.LiteralContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLiteralExpr"):
                listener.enterLiteralExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLiteralExpr"):
                listener.exitLiteralExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLiteralExpr"):
                return visitor.visitLiteralExpr(self)
            else:
                return visitor.visitChildren(self)

    class ParenExprContext(PrimaryContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(transpilerParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def RPAREN(self):
            return self.getToken(transpilerParser.RPAREN, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterParenExpr"):
                listener.enterParenExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitParenExpr"):
                listener.exitParenExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitParenExpr"):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)

    def primary(self):

        localctx = transpilerParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_primary)
        try:
            self.state = 537
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [58]:
                localctx = transpilerParser.IdentifierExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 531
                self.match(transpilerParser.ID)
                pass
            elif token in [30, 31, 32, 55, 56, 57]:
                localctx = transpilerParser.LiteralExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 532
                self.literal()
                pass
            elif token in [4]:
                localctx = transpilerParser.ParenExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 533
                self.match(transpilerParser.LPAREN)
                self.state = 534
                self.expr(0)
                self.state = 535
                self.match(transpilerParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArgumentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(transpilerParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(transpilerParser.RPAREN, 0)

        def exprList(self):
            return self.getTypedRuleContext(transpilerParser.ExprListContext, 0)

        def PAREN(self):
            return self.getToken(transpilerParser.PAREN, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_argumentList

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterArgumentList"):
                listener.enterArgumentList(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitArgumentList"):
                listener.exitArgumentList(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitArgumentList"):
                return visitor.visitArgumentList(self)
            else:
                return visitor.visitChildren(self)

    def argumentList(self):

        localctx = transpilerParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_argumentList)
        self._la = 0  # Token type
        try:
            self.state = 545
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 539
                self.match(transpilerParser.LPAREN)
                self.state = 541
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540504530568085520) != 0):
                    self.state = 540
                    self.exprList()

                self.state = 543
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 544
                self.match(transpilerParser.PAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.ExprContext)
            else:
                return self.getTypedRuleContext(transpilerParser.ExprContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.COMMA)
            else:
                return self.getToken(transpilerParser.COMMA, i)

        def getRuleIndex(self):
            return transpilerParser.RULE_exprList

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterExprList"):
                listener.enterExprList(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitExprList"):
                listener.exitExprList(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitExprList"):
                return visitor.visitExprList(self)
            else:
                return visitor.visitChildren(self)

    def exprList(self):

        localctx = transpilerParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_exprList)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 547
            self.expr(0)
            self.state = 552
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 11:
                self.state = 548
                self.match(transpilerParser.COMMA)
                self.state = 549
                self.expr(0)
                self.state = 554
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(transpilerParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(transpilerParser.STRING, 0)

        def FSTRING(self):
            return self.getToken(transpilerParser.FSTRING, 0)

        def TRUE(self):
            return self.getToken(transpilerParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(transpilerParser.FALSE, 0)

        def NULL(self):
            return self.getToken(transpilerParser.NULL, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_literal

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterLiteral"):
                listener.enterLiteral(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitLiteral"):
                listener.exitLiteral(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitLiteral"):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)

    def literal(self):

        localctx = transpilerParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_literal)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 555
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 252201586648940544) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    def sempred(self, localctx: RuleContext, ruleIndex: int, predIndex: int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[26] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx: ExprContext, predIndex: int):
        if predIndex == 0:
            return self.precpred(self._ctx, 10)

        if predIndex == 1:
            return self.precpred(self._ctx, 9)

        if predIndex == 2:
            return self.precpred(self._ctx, 8)

        if predIndex == 3:
            return self.precpred(self._ctx, 7)

        if predIndex == 4:
            return self.precpred(self._ctx, 6)

        if predIndex == 5:
            return self.precpred(self._ctx, 5)

        if predIndex == 6:
            return self.precpred(self._ctx, 4)

        if predIndex == 7:
            return self.precpred(self._ctx, 3)

        if predIndex == 8:
            return self.precpred(self._ctx, 2)

        if predIndex == 9:
            return self.precpred(self._ctx, 16)

        if predIndex == 10:
            return self.precpred(self._ctx, 15)

        if predIndex == 11:
            return self.precpred(self._ctx, 14)

        if predIndex == 12:
            return self.precpred(self._ctx, 13)
