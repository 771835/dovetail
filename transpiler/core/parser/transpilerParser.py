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
        4, 1, 57, 525, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7,
        6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13,
        2, 14, 7, 14, 2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20,
        7, 20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26,
        2, 27, 7, 27, 2, 28, 7, 28, 2, 29, 7, 29, 1, 0, 5, 0, 62, 8, 0, 10, 0, 12, 0, 65, 9, 0, 1,
        0, 1, 0, 1, 0, 1, 0, 1, 0, 3, 0, 72, 8, 0, 1, 0, 1, 0, 3, 0, 76, 8, 0, 5, 0, 78, 8, 0, 10, 0,
        12, 0, 81, 9, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 1, 88, 8, 1, 1, 2, 1, 2, 1, 2, 1, 3, 5, 3, 94,
        8, 3, 10, 3, 12, 3, 97, 9, 3, 1, 3, 1, 3, 1, 3, 1, 3, 3, 3, 103, 8, 3, 1, 3, 1, 3, 3, 3, 107,
        8, 3, 1, 3, 1, 3, 1, 3, 3, 3, 112, 8, 3, 1, 3, 5, 3, 115, 8, 3, 10, 3, 12, 3, 118, 9, 3, 1,
        3, 1, 3, 1, 4, 5, 4, 123, 8, 4, 10, 4, 12, 4, 126, 9, 4, 1, 4, 1, 4, 1, 4, 1, 4, 3, 4, 132,
        8, 4, 1, 4, 1, 4, 1, 4, 3, 4, 137, 8, 4, 1, 4, 5, 4, 140, 8, 4, 10, 4, 12, 4, 143, 9, 4, 1,
        4, 1, 4, 1, 5, 1, 5, 1, 5, 3, 5, 150, 8, 5, 1, 5, 1, 5, 1, 5, 3, 5, 155, 8, 5, 1, 5, 1, 5, 3,
        5, 159, 8, 5, 1, 6, 1, 6, 1, 7, 5, 7, 164, 8, 7, 10, 7, 12, 7, 167, 9, 7, 1, 7, 1, 7, 1, 7,
        1, 7, 1, 7, 1, 7, 5, 7, 175, 8, 7, 10, 7, 12, 7, 178, 9, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1,
        7, 1, 7, 1, 7, 1, 7, 5, 7, 189, 8, 7, 10, 7, 12, 7, 192, 9, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7,
        1, 7, 3, 7, 200, 8, 7, 1, 8, 5, 8, 203, 8, 8, 10, 8, 12, 8, 206, 9, 8, 1, 8, 1, 8, 1, 8, 1,
        8, 1, 8, 1, 8, 5, 8, 214, 8, 8, 10, 8, 12, 8, 217, 9, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8,
        1, 8, 1, 8, 1, 8, 5, 8, 228, 8, 8, 10, 8, 12, 8, 231, 9, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1,
        8, 3, 8, 239, 8, 8, 1, 9, 1, 9, 1, 9, 1, 9, 5, 9, 245, 8, 9, 10, 9, 12, 9, 248, 9, 9, 3, 9,
        250, 8, 9, 1, 9, 1, 9, 3, 9, 254, 8, 9, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 3, 10, 261, 8,
        10, 1, 10, 1, 10, 1, 10, 1, 10, 3, 10, 267, 8, 10, 3, 10, 269, 8, 10, 1, 11, 1, 11, 1, 11,
        5, 11, 274, 8, 11, 10, 11, 12, 11, 277, 9, 11, 1, 11, 1, 11, 3, 11, 281, 8, 11, 1, 12,
        1, 12, 1, 12, 3, 12, 286, 8, 12, 1, 12, 1, 12, 3, 12, 290, 8, 12, 1, 12, 1, 12, 1, 12, 1,
        12, 3, 12, 296, 8, 12, 1, 12, 1, 12, 3, 12, 300, 8, 12, 1, 12, 1, 12, 1, 12, 3, 12, 305,
        8, 12, 1, 12, 1, 12, 3, 12, 309, 8, 12, 1, 12, 3, 12, 312, 8, 12, 1, 13, 1, 13, 1, 14, 1,
        14, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1, 15, 1,
        15, 1, 15, 1, 15, 3, 15, 333, 8, 15, 1, 16, 3, 16, 336, 8, 16, 1, 16, 1, 16, 3, 16, 340,
        8, 16, 1, 16, 1, 16, 3, 16, 344, 8, 16, 1, 17, 1, 17, 3, 17, 348, 8, 17, 1, 18, 1, 18, 1,
        19, 1, 19, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 21, 1, 21, 1, 21, 1, 21, 3, 21, 364,
        8, 21, 1, 21, 3, 21, 367, 8, 21, 1, 21, 1, 21, 1, 21, 1, 21, 1, 21, 1, 21, 1, 21, 1, 21,
        3, 21, 377, 8, 21, 1, 22, 1, 22, 1, 22, 3, 22, 382, 8, 22, 1, 22, 1, 22, 1, 22, 1, 22, 1,
        22, 1, 22, 3, 22, 390, 8, 22, 1, 22, 1, 22, 3, 22, 394, 8, 22, 1, 22, 1, 22, 1, 22, 3, 22,
        399, 8, 22, 1, 22, 1, 22, 3, 22, 403, 8, 22, 1, 22, 1, 22, 1, 22, 3, 22, 408, 8, 22, 1,
        22, 1, 22, 1, 22, 1, 22, 1, 22, 3, 22, 415, 8, 22, 1, 23, 1, 23, 3, 23, 419, 8, 23, 1, 24,
        1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 3, 24, 428, 8, 24, 1, 25, 1, 25, 1, 25, 1, 25,
        1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 3, 25, 439, 8, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25,
        1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25,
        1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25,
        1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25,
        1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 5, 25, 494, 8, 25, 10, 25,
        12, 25, 497, 9, 25, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 3, 26, 505, 8, 26, 1, 27,
        1, 27, 3, 27, 509, 8, 27, 1, 27, 1, 27, 3, 27, 513, 8, 27, 1, 28, 1, 28, 1, 28, 5, 28, 518,
        8, 28, 10, 28, 12, 28, 521, 9, 28, 1, 29, 1, 29, 1, 29, 0, 1, 50, 30, 0, 2, 4, 6, 8, 10,
        12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54,
        56, 58, 0, 6, 1, 0, 13, 14, 2, 0, 32, 32, 53, 53, 1, 0, 36, 38, 1, 0, 39, 40, 1, 0, 41, 46,
        2, 0, 30, 32, 50, 52, 592, 0, 63, 1, 0, 0, 0, 2, 84, 1, 0, 0, 0, 4, 89, 1, 0, 0, 0, 6, 95,
        1, 0, 0, 0, 8, 124, 1, 0, 0, 0, 10, 158, 1, 0, 0, 0, 12, 160, 1, 0, 0, 0, 14, 199, 1, 0, 0,
        0, 16, 238, 1, 0, 0, 0, 18, 253, 1, 0, 0, 0, 20, 268, 1, 0, 0, 0, 22, 280, 1, 0, 0, 0, 24,
        311, 1, 0, 0, 0, 26, 313, 1, 0, 0, 0, 28, 315, 1, 0, 0, 0, 30, 332, 1, 0, 0, 0, 32, 335,
        1, 0, 0, 0, 34, 347, 1, 0, 0, 0, 36, 349, 1, 0, 0, 0, 38, 351, 1, 0, 0, 0, 40, 353, 1, 0,
        0, 0, 42, 376, 1, 0, 0, 0, 44, 414, 1, 0, 0, 0, 46, 416, 1, 0, 0, 0, 48, 420, 1, 0, 0, 0,
        50, 438, 1, 0, 0, 0, 52, 504, 1, 0, 0, 0, 54, 512, 1, 0, 0, 0, 56, 514, 1, 0, 0, 0, 58, 522,
        1, 0, 0, 0, 60, 62, 3, 2, 1, 0, 61, 60, 1, 0, 0, 0, 62, 65, 1, 0, 0, 0, 63, 61, 1, 0, 0, 0,
        63, 64, 1, 0, 0, 0, 64, 79, 1, 0, 0, 0, 65, 63, 1, 0, 0, 0, 66, 78, 3, 6, 3, 0, 67, 78, 3,
        8, 4, 0, 68, 78, 3, 14, 7, 0, 69, 71, 3, 44, 22, 0, 70, 72, 5, 10, 0, 0, 71, 70, 1, 0, 0,
        0, 71, 72, 1, 0, 0, 0, 72, 78, 1, 0, 0, 0, 73, 75, 3, 42, 21, 0, 74, 76, 5, 10, 0, 0, 75,
        74, 1, 0, 0, 0, 75, 76, 1, 0, 0, 0, 76, 78, 1, 0, 0, 0, 77, 66, 1, 0, 0, 0, 77, 67, 1, 0, 0,
        0, 77, 68, 1, 0, 0, 0, 77, 69, 1, 0, 0, 0, 77, 73, 1, 0, 0, 0, 78, 81, 1, 0, 0, 0, 79, 77,
        1, 0, 0, 0, 79, 80, 1, 0, 0, 0, 80, 82, 1, 0, 0, 0, 81, 79, 1, 0, 0, 0, 82, 83, 5, 0, 0, 1,
        83, 1, 1, 0, 0, 0, 84, 85, 5, 16, 0, 0, 85, 87, 3, 58, 29, 0, 86, 88, 5, 10, 0, 0, 87, 86,
        1, 0, 0, 0, 87, 88, 1, 0, 0, 0, 88, 3, 1, 0, 0, 0, 89, 90, 5, 1, 0, 0, 90, 91, 5, 53, 0, 0,
        91, 5, 1, 0, 0, 0, 92, 94, 3, 4, 2, 0, 93, 92, 1, 0, 0, 0, 94, 97, 1, 0, 0, 0, 95, 93, 1, 0,
        0, 0, 95, 96, 1, 0, 0, 0, 96, 98, 1, 0, 0, 0, 97, 95, 1, 0, 0, 0, 98, 99, 5, 19, 0, 0, 99,
        102, 5, 53, 0, 0, 100, 101, 5, 21, 0, 0, 101, 103, 3, 12, 6, 0, 102, 100, 1, 0, 0, 0, 102,
        103, 1, 0, 0, 0, 103, 106, 1, 0, 0, 0, 104, 105, 5, 22, 0, 0, 105, 107, 3, 12, 6, 0, 106,
        104, 1, 0, 0, 0, 106, 107, 1, 0, 0, 0, 107, 108, 1, 0, 0, 0, 108, 116, 5, 8, 0, 0, 109,
        111, 3, 10, 5, 0, 110, 112, 5, 10, 0, 0, 111, 110, 1, 0, 0, 0, 111, 112, 1, 0, 0, 0, 112,
        115, 1, 0, 0, 0, 113, 115, 3, 16, 8, 0, 114, 109, 1, 0, 0, 0, 114, 113, 1, 0, 0, 0, 115,
        118, 1, 0, 0, 0, 116, 114, 1, 0, 0, 0, 116, 117, 1, 0, 0, 0, 117, 119, 1, 0, 0, 0, 118,
        116, 1, 0, 0, 0, 119, 120, 5, 9, 0, 0, 120, 7, 1, 0, 0, 0, 121, 123, 3, 4, 2, 0, 122, 121,
        1, 0, 0, 0, 123, 126, 1, 0, 0, 0, 124, 122, 1, 0, 0, 0, 124, 125, 1, 0, 0, 0, 125, 127,
        1, 0, 0, 0, 126, 124, 1, 0, 0, 0, 127, 128, 5, 20, 0, 0, 128, 131, 5, 53, 0, 0, 129, 130,
        5, 21, 0, 0, 130, 132, 3, 12, 6, 0, 131, 129, 1, 0, 0, 0, 131, 132, 1, 0, 0, 0, 132, 133,
        1, 0, 0, 0, 133, 141, 5, 8, 0, 0, 134, 136, 3, 10, 5, 0, 135, 137, 5, 10, 0, 0, 136, 135,
        1, 0, 0, 0, 136, 137, 1, 0, 0, 0, 137, 140, 1, 0, 0, 0, 138, 140, 3, 16, 8, 0, 139, 134,
        1, 0, 0, 0, 139, 138, 1, 0, 0, 0, 140, 143, 1, 0, 0, 0, 141, 139, 1, 0, 0, 0, 141, 142,
        1, 0, 0, 0, 142, 144, 1, 0, 0, 0, 143, 141, 1, 0, 0, 0, 144, 145, 5, 9, 0, 0, 145, 9, 1,
        0, 0, 0, 146, 147, 3, 12, 6, 0, 147, 149, 5, 53, 0, 0, 148, 150, 5, 12, 0, 0, 149, 148,
        1, 0, 0, 0, 149, 150, 1, 0, 0, 0, 150, 159, 1, 0, 0, 0, 151, 152, 5, 24, 0, 0, 152, 154,
        5, 53, 0, 0, 153, 155, 5, 12, 0, 0, 154, 153, 1, 0, 0, 0, 154, 155, 1, 0, 0, 0, 155, 156,
        1, 0, 0, 0, 156, 157, 7, 0, 0, 0, 157, 159, 3, 12, 6, 0, 158, 146, 1, 0, 0, 0, 158, 151,
        1, 0, 0, 0, 159, 11, 1, 0, 0, 0, 160, 161, 7, 1, 0, 0, 161, 13, 1, 0, 0, 0, 162, 164, 3,
        4, 2, 0, 163, 162, 1, 0, 0, 0, 164, 167, 1, 0, 0, 0, 165, 163, 1, 0, 0, 0, 165, 166, 1,
        0, 0, 0, 166, 168, 1, 0, 0, 0, 167, 165, 1, 0, 0, 0, 168, 169, 5, 17, 0, 0, 169, 170, 5,
        53, 0, 0, 170, 171, 3, 18, 9, 0, 171, 172, 3, 22, 11, 0, 172, 200, 1, 0, 0, 0, 173, 175,
        3, 4, 2, 0, 174, 173, 1, 0, 0, 0, 175, 178, 1, 0, 0, 0, 176, 174, 1, 0, 0, 0, 176, 177,
        1, 0, 0, 0, 177, 179, 1, 0, 0, 0, 178, 176, 1, 0, 0, 0, 179, 180, 5, 17, 0, 0, 180, 181,
        5, 53, 0, 0, 181, 182, 3, 18, 9, 0, 182, 183, 7, 0, 0, 0, 183, 184, 3, 12, 6, 0, 184, 185,
        1, 0, 0, 0, 185, 186, 3, 22, 11, 0, 186, 200, 1, 0, 0, 0, 187, 189, 3, 4, 2, 0, 188, 187,
        1, 0, 0, 0, 189, 192, 1, 0, 0, 0, 190, 188, 1, 0, 0, 0, 190, 191, 1, 0, 0, 0, 191, 193,
        1, 0, 0, 0, 192, 190, 1, 0, 0, 0, 193, 194, 5, 17, 0, 0, 194, 195, 3, 12, 6, 0, 195, 196,
        5, 53, 0, 0, 196, 197, 3, 18, 9, 0, 197, 198, 3, 22, 11, 0, 198, 200, 1, 0, 0, 0, 199,
        165, 1, 0, 0, 0, 199, 176, 1, 0, 0, 0, 199, 190, 1, 0, 0, 0, 200, 15, 1, 0, 0, 0, 201, 203,
        3, 4, 2, 0, 202, 201, 1, 0, 0, 0, 203, 206, 1, 0, 0, 0, 204, 202, 1, 0, 0, 0, 204, 205,
        1, 0, 0, 0, 205, 207, 1, 0, 0, 0, 206, 204, 1, 0, 0, 0, 207, 208, 5, 18, 0, 0, 208, 209,
        5, 53, 0, 0, 209, 210, 3, 18, 9, 0, 210, 211, 3, 22, 11, 0, 211, 239, 1, 0, 0, 0, 212,
        214, 3, 4, 2, 0, 213, 212, 1, 0, 0, 0, 214, 217, 1, 0, 0, 0, 215, 213, 1, 0, 0, 0, 215,
        216, 1, 0, 0, 0, 216, 218, 1, 0, 0, 0, 217, 215, 1, 0, 0, 0, 218, 219, 5, 18, 0, 0, 219,
        220, 5, 53, 0, 0, 220, 221, 3, 18, 9, 0, 221, 222, 7, 0, 0, 0, 222, 223, 3, 12, 6, 0, 223,
        224, 1, 0, 0, 0, 224, 225, 3, 22, 11, 0, 225, 239, 1, 0, 0, 0, 226, 228, 3, 4, 2, 0, 227,
        226, 1, 0, 0, 0, 228, 231, 1, 0, 0, 0, 229, 227, 1, 0, 0, 0, 229, 230, 1, 0, 0, 0, 230,
        232, 1, 0, 0, 0, 231, 229, 1, 0, 0, 0, 232, 233, 5, 18, 0, 0, 233, 234, 3, 12, 6, 0, 234,
        235, 5, 53, 0, 0, 235, 236, 3, 18, 9, 0, 236, 237, 3, 22, 11, 0, 237, 239, 1, 0, 0, 0,
        238, 204, 1, 0, 0, 0, 238, 215, 1, 0, 0, 0, 238, 229, 1, 0, 0, 0, 239, 17, 1, 0, 0, 0, 240,
        249, 5, 4, 0, 0, 241, 246, 3, 20, 10, 0, 242, 243, 5, 11, 0, 0, 243, 245, 3, 20, 10, 0,
        244, 242, 1, 0, 0, 0, 245, 248, 1, 0, 0, 0, 246, 244, 1, 0, 0, 0, 246, 247, 1, 0, 0, 0,
        247, 250, 1, 0, 0, 0, 248, 246, 1, 0, 0, 0, 249, 241, 1, 0, 0, 0, 249, 250, 1, 0, 0, 0,
        250, 251, 1, 0, 0, 0, 251, 254, 5, 5, 0, 0, 252, 254, 5, 3, 0, 0, 253, 240, 1, 0, 0, 0,
        253, 252, 1, 0, 0, 0, 254, 19, 1, 0, 0, 0, 255, 256, 5, 53, 0, 0, 256, 257, 7, 0, 0, 0,
        257, 260, 3, 12, 6, 0, 258, 259, 5, 49, 0, 0, 259, 261, 3, 50, 25, 0, 260, 258, 1, 0,
        0, 0, 260, 261, 1, 0, 0, 0, 261, 269, 1, 0, 0, 0, 262, 263, 3, 12, 6, 0, 263, 266, 5, 53,
        0, 0, 264, 265, 5, 49, 0, 0, 265, 267, 3, 50, 25, 0, 266, 264, 1, 0, 0, 0, 266, 267, 1,
        0, 0, 0, 267, 269, 1, 0, 0, 0, 268, 255, 1, 0, 0, 0, 268, 262, 1, 0, 0, 0, 269, 21, 1, 0,
        0, 0, 270, 281, 3, 24, 12, 0, 271, 275, 5, 8, 0, 0, 272, 274, 3, 24, 12, 0, 273, 272,
        1, 0, 0, 0, 274, 277, 1, 0, 0, 0, 275, 273, 1, 0, 0, 0, 275, 276, 1, 0, 0, 0, 276, 278,
        1, 0, 0, 0, 277, 275, 1, 0, 0, 0, 278, 281, 5, 9, 0, 0, 279, 281, 5, 10, 0, 0, 280, 270,
        1, 0, 0, 0, 280, 271, 1, 0, 0, 0, 280, 279, 1, 0, 0, 0, 281, 23, 1, 0, 0, 0, 282, 312, 3,
        14, 7, 0, 283, 285, 3, 44, 22, 0, 284, 286, 5, 10, 0, 0, 285, 284, 1, 0, 0, 0, 285, 286,
        1, 0, 0, 0, 286, 312, 1, 0, 0, 0, 287, 289, 3, 42, 21, 0, 288, 290, 5, 10, 0, 0, 289, 288,
        1, 0, 0, 0, 289, 290, 1, 0, 0, 0, 290, 312, 1, 0, 0, 0, 291, 312, 3, 30, 15, 0, 292, 312,
        3, 40, 20, 0, 293, 295, 3, 50, 25, 0, 294, 296, 5, 10, 0, 0, 295, 294, 1, 0, 0, 0, 295,
        296, 1, 0, 0, 0, 296, 312, 1, 0, 0, 0, 297, 299, 3, 46, 23, 0, 298, 300, 5, 10, 0, 0, 299,
        298, 1, 0, 0, 0, 299, 300, 1, 0, 0, 0, 300, 312, 1, 0, 0, 0, 301, 312, 3, 48, 24, 0, 302,
        304, 3, 26, 13, 0, 303, 305, 5, 10, 0, 0, 304, 303, 1, 0, 0, 0, 304, 305, 1, 0, 0, 0, 305,
        312, 1, 0, 0, 0, 306, 308, 3, 28, 14, 0, 307, 309, 5, 10, 0, 0, 308, 307, 1, 0, 0, 0, 308,
        309, 1, 0, 0, 0, 309, 312, 1, 0, 0, 0, 310, 312, 5, 10, 0, 0, 311, 282, 1, 0, 0, 0, 311,
        283, 1, 0, 0, 0, 311, 287, 1, 0, 0, 0, 311, 291, 1, 0, 0, 0, 311, 292, 1, 0, 0, 0, 311,
        293, 1, 0, 0, 0, 311, 297, 1, 0, 0, 0, 311, 301, 1, 0, 0, 0, 311, 302, 1, 0, 0, 0, 311,
        306, 1, 0, 0, 0, 311, 310, 1, 0, 0, 0, 312, 25, 1, 0, 0, 0, 313, 314, 5, 33, 0, 0, 314,
        27, 1, 0, 0, 0, 315, 316, 5, 34, 0, 0, 316, 29, 1, 0, 0, 0, 317, 318, 5, 26, 0, 0, 318,
        319, 5, 4, 0, 0, 319, 320, 3, 32, 16, 0, 320, 321, 5, 5, 0, 0, 321, 322, 3, 22, 11, 0,
        322, 333, 1, 0, 0, 0, 323, 324, 5, 26, 0, 0, 324, 325, 5, 4, 0, 0, 325, 326, 3, 12, 6,
        0, 326, 327, 5, 53, 0, 0, 327, 328, 5, 14, 0, 0, 328, 329, 3, 50, 25, 0, 329, 330, 5,
        5, 0, 0, 330, 331, 3, 22, 11, 0, 331, 333, 1, 0, 0, 0, 332, 317, 1, 0, 0, 0, 332, 323,
        1, 0, 0, 0, 333, 31, 1, 0, 0, 0, 334, 336, 3, 34, 17, 0, 335, 334, 1, 0, 0, 0, 335, 336,
        1, 0, 0, 0, 336, 337, 1, 0, 0, 0, 337, 339, 5, 10, 0, 0, 338, 340, 3, 36, 18, 0, 339, 338,
        1, 0, 0, 0, 339, 340, 1, 0, 0, 0, 340, 341, 1, 0, 0, 0, 341, 343, 5, 10, 0, 0, 342, 344,
        3, 38, 19, 0, 343, 342, 1, 0, 0, 0, 343, 344, 1, 0, 0, 0, 344, 33, 1, 0, 0, 0, 345, 348,
        3, 44, 22, 0, 346, 348, 3, 50, 25, 0, 347, 345, 1, 0, 0, 0, 347, 346, 1, 0, 0, 0, 348,
        35, 1, 0, 0, 0, 349, 350, 3, 50, 25, 0, 350, 37, 1, 0, 0, 0, 351, 352, 3, 50, 25, 0, 352,
        39, 1, 0, 0, 0, 353, 354, 5, 27, 0, 0, 354, 355, 5, 4, 0, 0, 355, 356, 3, 36, 18, 0, 356,
        357, 5, 5, 0, 0, 357, 358, 3, 22, 11, 0, 358, 41, 1, 0, 0, 0, 359, 360, 5, 23, 0, 0, 360,
        363, 5, 53, 0, 0, 361, 362, 7, 0, 0, 0, 362, 364, 3, 12, 6, 0, 363, 361, 1, 0, 0, 0, 363,
        364, 1, 0, 0, 0, 364, 366, 1, 0, 0, 0, 365, 367, 5, 12, 0, 0, 366, 365, 1, 0, 0, 0, 366,
        367, 1, 0, 0, 0, 367, 368, 1, 0, 0, 0, 368, 369, 5, 49, 0, 0, 369, 377, 3, 50, 25, 0, 370,
        371, 5, 23, 0, 0, 371, 372, 3, 12, 6, 0, 372, 373, 5, 53, 0, 0, 373, 374, 5, 49, 0, 0,
        374, 375, 3, 50, 25, 0, 375, 377, 1, 0, 0, 0, 376, 359, 1, 0, 0, 0, 376, 370, 1, 0, 0,
        0, 377, 43, 1, 0, 0, 0, 378, 379, 5, 24, 0, 0, 379, 381, 5, 53, 0, 0, 380, 382, 5, 12,
        0, 0, 381, 380, 1, 0, 0, 0, 381, 382, 1, 0, 0, 0, 382, 383, 1, 0, 0, 0, 383, 384, 5, 49,
        0, 0, 384, 415, 3, 50, 25, 0, 385, 386, 5, 53, 0, 0, 386, 387, 7, 0, 0, 0, 387, 389, 3,
        12, 6, 0, 388, 390, 5, 12, 0, 0, 389, 388, 1, 0, 0, 0, 389, 390, 1, 0, 0, 0, 390, 393,
        1, 0, 0, 0, 391, 392, 5, 49, 0, 0, 392, 394, 3, 50, 25, 0, 393, 391, 1, 0, 0, 0, 393, 394,
        1, 0, 0, 0, 394, 415, 1, 0, 0, 0, 395, 396, 3, 12, 6, 0, 396, 398, 5, 53, 0, 0, 397, 399,
        5, 12, 0, 0, 398, 397, 1, 0, 0, 0, 398, 399, 1, 0, 0, 0, 399, 402, 1, 0, 0, 0, 400, 401,
        5, 49, 0, 0, 401, 403, 3, 50, 25, 0, 402, 400, 1, 0, 0, 0, 402, 403, 1, 0, 0, 0, 403, 415,
        1, 0, 0, 0, 404, 405, 5, 24, 0, 0, 405, 407, 5, 53, 0, 0, 406, 408, 5, 12, 0, 0, 407, 406,
        1, 0, 0, 0, 407, 408, 1, 0, 0, 0, 408, 409, 1, 0, 0, 0, 409, 410, 7, 0, 0, 0, 410, 411,
        3, 12, 6, 0, 411, 412, 5, 49, 0, 0, 412, 413, 3, 50, 25, 0, 413, 415, 1, 0, 0, 0, 414,
        378, 1, 0, 0, 0, 414, 385, 1, 0, 0, 0, 414, 395, 1, 0, 0, 0, 414, 404, 1, 0, 0, 0, 415,
        45, 1, 0, 0, 0, 416, 418, 5, 25, 0, 0, 417, 419, 3, 50, 25, 0, 418, 417, 1, 0, 0, 0, 418,
        419, 1, 0, 0, 0, 419, 47, 1, 0, 0, 0, 420, 421, 5, 28, 0, 0, 421, 422, 5, 4, 0, 0, 422,
        423, 3, 36, 18, 0, 423, 424, 5, 5, 0, 0, 424, 427, 3, 22, 11, 0, 425, 426, 5, 29, 0, 0,
        426, 428, 3, 22, 11, 0, 427, 425, 1, 0, 0, 0, 427, 428, 1, 0, 0, 0, 428, 49, 1, 0, 0, 0,
        429, 430, 6, 25, -1, 0, 430, 439, 3, 52, 26, 0, 431, 432, 5, 40, 0, 0, 432, 439, 3, 50,
        25, 12, 433, 434, 5, 35, 0, 0, 434, 439, 3, 50, 25, 11, 435, 436, 5, 53, 0, 0, 436, 437,
        5, 49, 0, 0, 437, 439, 3, 50, 25, 1, 438, 429, 1, 0, 0, 0, 438, 431, 1, 0, 0, 0, 438, 433,
        1, 0, 0, 0, 438, 435, 1, 0, 0, 0, 439, 495, 1, 0, 0, 0, 440, 441, 10, 10, 0, 0, 441, 442,
        7, 2, 0, 0, 442, 494, 3, 50, 25, 11, 443, 444, 10, 9, 0, 0, 444, 445, 7, 3, 0, 0, 445,
        494, 3, 50, 25, 10, 446, 447, 10, 8, 0, 0, 447, 448, 7, 4, 0, 0, 448, 494, 3, 50, 25,
        9, 449, 450, 10, 7, 0, 0, 450, 451, 5, 47, 0, 0, 451, 494, 3, 50, 25, 8, 452, 453, 10,
        6, 0, 0, 453, 454, 5, 48, 0, 0, 454, 494, 3, 50, 25, 7, 455, 456, 10, 5, 0, 0, 456, 457,
        5, 12, 0, 0, 457, 458, 3, 50, 25, 0, 458, 459, 5, 14, 0, 0, 459, 460, 3, 50, 25, 5, 460,
        494, 1, 0, 0, 0, 461, 462, 10, 4, 0, 0, 462, 463, 5, 28, 0, 0, 463, 464, 3, 50, 25, 0,
        464, 465, 5, 29, 0, 0, 465, 466, 3, 50, 25, 4, 466, 494, 1, 0, 0, 0, 467, 468, 10, 3,
        0, 0, 468, 469, 5, 6, 0, 0, 469, 470, 3, 50, 25, 0, 470, 471, 5, 7, 0, 0, 471, 472, 5,
        49, 0, 0, 472, 473, 3, 50, 25, 4, 473, 494, 1, 0, 0, 0, 474, 475, 10, 2, 0, 0, 475, 476,
        5, 2, 0, 0, 476, 477, 5, 53, 0, 0, 477, 478, 5, 49, 0, 0, 478, 494, 3, 50, 25, 3, 479,
        480, 10, 16, 0, 0, 480, 481, 5, 2, 0, 0, 481, 482, 5, 53, 0, 0, 482, 494, 3, 54, 27, 0,
        483, 484, 10, 15, 0, 0, 484, 485, 5, 2, 0, 0, 485, 494, 5, 53, 0, 0, 486, 487, 10, 14,
        0, 0, 487, 488, 5, 6, 0, 0, 488, 489, 3, 50, 25, 0, 489, 490, 5, 7, 0, 0, 490, 494, 1,
        0, 0, 0, 491, 492, 10, 13, 0, 0, 492, 494, 3, 54, 27, 0, 493, 440, 1, 0, 0, 0, 493, 443,
        1, 0, 0, 0, 493, 446, 1, 0, 0, 0, 493, 449, 1, 0, 0, 0, 493, 452, 1, 0, 0, 0, 493, 455,
        1, 0, 0, 0, 493, 461, 1, 0, 0, 0, 493, 467, 1, 0, 0, 0, 493, 474, 1, 0, 0, 0, 493, 479,
        1, 0, 0, 0, 493, 483, 1, 0, 0, 0, 493, 486, 1, 0, 0, 0, 493, 491, 1, 0, 0, 0, 494, 497,
        1, 0, 0, 0, 495, 493, 1, 0, 0, 0, 495, 496, 1, 0, 0, 0, 496, 51, 1, 0, 0, 0, 497, 495, 1,
        0, 0, 0, 498, 505, 5, 53, 0, 0, 499, 505, 3, 58, 29, 0, 500, 501, 5, 4, 0, 0, 501, 502,
        3, 50, 25, 0, 502, 503, 5, 5, 0, 0, 503, 505, 1, 0, 0, 0, 504, 498, 1, 0, 0, 0, 504, 499,
        1, 0, 0, 0, 504, 500, 1, 0, 0, 0, 505, 53, 1, 0, 0, 0, 506, 508, 5, 4, 0, 0, 507, 509, 3,
        56, 28, 0, 508, 507, 1, 0, 0, 0, 508, 509, 1, 0, 0, 0, 509, 510, 1, 0, 0, 0, 510, 513,
        5, 5, 0, 0, 511, 513, 5, 3, 0, 0, 512, 506, 1, 0, 0, 0, 512, 511, 1, 0, 0, 0, 513, 55, 1,
        0, 0, 0, 514, 519, 3, 50, 25, 0, 515, 516, 5, 11, 0, 0, 516, 518, 3, 50, 25, 0, 517, 515,
        1, 0, 0, 0, 518, 521, 1, 0, 0, 0, 519, 517, 1, 0, 0, 0, 519, 520, 1, 0, 0, 0, 520, 57, 1,
        0, 0, 0, 521, 519, 1, 0, 0, 0, 522, 523, 7, 5, 0, 0, 523, 59, 1, 0, 0, 0, 67, 63, 71, 75,
        77, 79, 87, 95, 102, 106, 111, 114, 116, 124, 131, 136, 139, 141, 149, 154, 158,
        165, 176, 190, 199, 204, 215, 229, 238, 246, 249, 253, 260, 266, 268, 275, 280,
        285, 289, 295, 299, 304, 308, 311, 332, 335, 339, 343, 347, 363, 366, 376, 381,
        389, 393, 398, 402, 407, 414, 418, 427, 438, 493, 495, 504, 508, 512, 519
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
                    "<INVALID>", "'*'", "'/'", "'%'", "'+'", "'-'", "'>'",
                    "'<'", "'=='", "'!='", "'>='", "'<='", "<INVALID>",
                    "<INVALID>", "'='"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "PAREN", "LPAREN",
                     "RPAREN", "LBRACK", "RBRACK", "LBRACE", "RBRACE",
                     "SEMI", "COMMA", "QUESTION", "ARROW", "COLON", "DOUBLE_COLON",
                     "INCLUDE", "FUNC", "METHOD", "CLASS", "INTERFACE",
                     "EXTENDS", "IMPLEMENTS", "CONST", "LET", "RETURN",
                     "FOR", "WHILE", "IF", "ELSE", "TRUE", "FALSE", "NULL",
                     "BREAK", "CONTINUE", "NOT", "MUL", "DIV", "MOD", "ADD",
                     "SUB", "GT", "LT", "EQ", "NEQ", "GTE", "LTE", "AND",
                     "OR", "ASSIGN", "NUMBER", "STRING", "FSTRING", "ID",
                     "WS", "LINE_COMMENT", "LINE_COMMENT2", "BLOCK_COMMENT"]

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
    RULE_expr = 25
    RULE_primary = 26
    RULE_argumentList = 27
    RULE_exprList = 28
    RULE_literal = 29

    ruleNames = ["program", "includeStmt", "annotation", "classDecl",
                 "interfaceDecl", "classPropertyDecl", "type", "functionDecl",
                 "methodDecl", "paramList", "paramDecl", "block", "statement",
                 "breakStmt", "continueStmt", "forStmt", "forControl",
                 "forInit", "condition", "forUpdate", "whileStmt", "constDecl",
                 "varDecl", "returnStmt", "ifStmt", "expr", "primary",
                 "argumentList", "exprList", "literal"]

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
    NOT = 35
    MUL = 36
    DIV = 37
    MOD = 38
    ADD = 39
    SUB = 40
    GT = 41
    LT = 42
    EQ = 43
    NEQ = 44
    GTE = 45
    LTE = 46
    AND = 47
    OR = 48
    ASSIGN = 49
    NUMBER = 50
    STRING = 51
    FSTRING = 52
    ID = 53
    WS = 54
    LINE_COMMENT = 55
    LINE_COMMENT2 = 56
    BLOCK_COMMENT = 57

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
            self.state = 63
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 16:
                self.state = 60
                self.includeStmt()
                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 79
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 9007203576578050) != 0):
                self.state = 77
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 3, self._ctx)
                if la_ == 1:
                    self.state = 66
                    self.classDecl()
                    pass

                elif la_ == 2:
                    self.state = 67
                    self.interfaceDecl()
                    pass

                elif la_ == 3:
                    self.state = 68
                    self.functionDecl()
                    pass

                elif la_ == 4:
                    self.state = 69
                    self.varDecl()
                    self.state = 71
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == 10:
                        self.state = 70
                        self.match(transpilerParser.SEMI)

                    pass

                elif la_ == 5:
                    self.state = 73
                    self.constDecl()
                    self.state = 75
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == 10:
                        self.state = 74
                        self.match(transpilerParser.SEMI)

                    pass

                self.state = 81
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 82
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
            self.state = 84
            self.match(transpilerParser.INCLUDE)
            self.state = 85
            self.literal()
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 10:
                self.state = 86
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
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(transpilerParser.T__0)
            self.state = 90
            self.match(transpilerParser.ID)
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
            self.state = 95
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 92
                self.annotation()
                self.state = 97
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 98
            self.match(transpilerParser.CLASS)
            self.state = 99
            self.match(transpilerParser.ID)
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 21:
                self.state = 100
                self.match(transpilerParser.EXTENDS)
                self.state = 101
                self.type_()

            self.state = 106
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 22:
                self.state = 104
                self.match(transpilerParser.IMPLEMENTS)
                self.state = 105
                self.type_()

            self.state = 108
            self.match(transpilerParser.LBRACE)
            self.state = 116
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 9007203566747650) != 0):
                self.state = 114
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [24, 32, 53]:
                    self.state = 109
                    self.classPropertyDecl()
                    self.state = 111
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == 10:
                        self.state = 110
                        self.match(transpilerParser.SEMI)

                    pass
                elif token in [1, 18]:
                    self.state = 113
                    self.methodDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 118
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 119
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
            self.state = 124
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 121
                self.annotation()
                self.state = 126
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 127
            self.match(transpilerParser.INTERFACE)
            self.state = 128
            self.match(transpilerParser.ID)
            self.state = 131
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 21:
                self.state = 129
                self.match(transpilerParser.EXTENDS)
                self.state = 130
                self.type_()

            self.state = 133
            self.match(transpilerParser.LBRACE)
            self.state = 141
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 9007203566747650) != 0):
                self.state = 139
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [24, 32, 53]:
                    self.state = 134
                    self.classPropertyDecl()
                    self.state = 136
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la == 10:
                        self.state = 135
                        self.match(transpilerParser.SEMI)

                    pass
                elif token in [1, 18]:
                    self.state = 138
                    self.methodDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 144
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
            self.state = 158
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [32, 53]:
                self.enterOuterAlt(localctx, 1)
                self.state = 146
                self.type_()
                self.state = 147
                self.match(transpilerParser.ID)
                self.state = 149
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 148
                    self.match(transpilerParser.QUESTION)

                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 2)
                self.state = 151
                self.match(transpilerParser.LET)
                self.state = 152
                self.match(transpilerParser.ID)
                self.state = 154
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 153
                    self.match(transpilerParser.QUESTION)

                self.state = 156
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 157
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
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            _la = self._input.LA(1)
            if not (_la == 32 or _la == 53):
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
            self.state = 199
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 23, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 165
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 162
                    self.annotation()
                    self.state = 167
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 168
                self.match(transpilerParser.FUNC)
                self.state = 169
                self.match(transpilerParser.ID)
                self.state = 170
                self.paramList()
                self.state = 171
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 176
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 173
                    self.annotation()
                    self.state = 178
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 179
                self.match(transpilerParser.FUNC)
                self.state = 180
                self.match(transpilerParser.ID)
                self.state = 181
                self.paramList()

                self.state = 182
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 183
                self.type_()
                self.state = 185
                self.block()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 187
                    self.annotation()
                    self.state = 192
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 193
                self.match(transpilerParser.FUNC)
                self.state = 194
                self.type_()
                self.state = 195
                self.match(transpilerParser.ID)
                self.state = 196
                self.paramList()
                self.state = 197
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
            self.state = 238
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 27, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 204
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 201
                    self.annotation()
                    self.state = 206
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 207
                self.match(transpilerParser.METHOD)
                self.state = 208
                self.match(transpilerParser.ID)
                self.state = 209
                self.paramList()
                self.state = 210
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 215
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 212
                    self.annotation()
                    self.state = 217
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 218
                self.match(transpilerParser.METHOD)
                self.state = 219
                self.match(transpilerParser.ID)
                self.state = 220
                self.paramList()

                self.state = 221
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 222
                self.type_()
                self.state = 224
                self.block()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 229
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 226
                    self.annotation()
                    self.state = 231
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 232
                self.match(transpilerParser.METHOD)
                self.state = 233
                self.type_()
                self.state = 234
                self.match(transpilerParser.ID)
                self.state = 235
                self.paramList()
                self.state = 236
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
            self.state = 253
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 240
                self.match(transpilerParser.LPAREN)
                self.state = 249
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 32 or _la == 53:
                    self.state = 241
                    self.paramDecl()
                    self.state = 246
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == 11:
                        self.state = 242
                        self.match(transpilerParser.COMMA)
                        self.state = 243
                        self.paramDecl()
                        self.state = 248
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                self.state = 251
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 252
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
            self.state = 268
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 33, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 255
                self.match(transpilerParser.ID)
                self.state = 256
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 257
                self.type_()
                self.state = 260
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 49:
                    self.state = 258
                    self.match(transpilerParser.ASSIGN)
                    self.state = 259
                    self.expr(0)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 262
                self.type_()
                self.state = 263
                self.match(transpilerParser.ID)
                self.state = 266
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 49:
                    self.state = 264
                    self.match(transpilerParser.ASSIGN)
                    self.state = 265
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

        def statement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.StatementContext)
            else:
                return self.getTypedRuleContext(transpilerParser.StatementContext, i)

        def LBRACE(self):
            return self.getToken(transpilerParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(transpilerParser.RBRACE, 0)

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
            self.state = 280
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 35, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 270
                self.statement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 271
                self.match(transpilerParser.LBRACE)
                self.state = 275
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 16889666288616466) != 0):
                    self.state = 272
                    self.statement()
                    self.state = 277
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 278
                self.match(transpilerParser.RBRACE)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 279
                self.match(transpilerParser.SEMI)
                pass


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
            self.state = 311
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 42, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 282
                self.functionDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 283
                self.varDecl()
                self.state = 285
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 36, self._ctx)
                if la_ == 1:
                    self.state = 284
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 287
                self.constDecl()
                self.state = 289
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 37, self._ctx)
                if la_ == 1:
                    self.state = 288
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 291
                self.forStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 292
                self.whileStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 293
                self.expr(0)
                self.state = 295
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 38, self._ctx)
                if la_ == 1:
                    self.state = 294
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 297
                self.returnStmt()
                self.state = 299
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 39, self._ctx)
                if la_ == 1:
                    self.state = 298
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 301
                self.ifStmt()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 302
                self.breakStmt()
                self.state = 304
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 40, self._ctx)
                if la_ == 1:
                    self.state = 303
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 306
                self.continueStmt()
                self.state = 308
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 41, self._ctx)
                if la_ == 1:
                    self.state = 307
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 310
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
            self.state = 313
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
            self.state = 315
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

        def block(self):
            return self.getTypedRuleContext(transpilerParser.BlockContext, 0)

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
            self.state = 332
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 43, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 317
                self.match(transpilerParser.FOR)
                self.state = 318
                self.match(transpilerParser.LPAREN)
                self.state = 319
                self.forControl()
                self.state = 320
                self.match(transpilerParser.RPAREN)
                self.state = 321
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 323
                self.match(transpilerParser.FOR)
                self.state = 324
                self.match(transpilerParser.LPAREN)
                self.state = 325
                self.type_()
                self.state = 326
                self.match(transpilerParser.ID)
                self.state = 327
                self.match(transpilerParser.COLON)
                self.state = 328
                self.expr(0)
                self.state = 329
                self.match(transpilerParser.RPAREN)
                self.state = 330
                self.block()
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
            self.state = 335
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16889640006975504) != 0):
                self.state = 334
                self.forInit()

            self.state = 337
            self.match(transpilerParser.SEMI)
            self.state = 339
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16889639990198288) != 0):
                self.state = 338
                self.condition()

            self.state = 341
            self.match(transpilerParser.SEMI)
            self.state = 343
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16889639990198288) != 0):
                self.state = 342
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
            self.state = 347
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 47, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 345
                self.varDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 346
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
            self.state = 349
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
            self.state = 351
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

        def block(self):
            return self.getTypedRuleContext(transpilerParser.BlockContext, 0)

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
            self.state = 353
            self.match(transpilerParser.WHILE)
            self.state = 354
            self.match(transpilerParser.LPAREN)
            self.state = 355
            self.condition()
            self.state = 356
            self.match(transpilerParser.RPAREN)
            self.state = 357
            self.block()
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
            self.state = 376
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 50, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 359
                self.match(transpilerParser.CONST)
                self.state = 360
                self.match(transpilerParser.ID)
                self.state = 363
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13 or _la == 14:
                    self.state = 361
                    _la = self._input.LA(1)
                    if not (_la == 13 or _la == 14):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 362
                    self.type_()

                self.state = 366
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 365
                    self.match(transpilerParser.QUESTION)

                self.state = 368
                self.match(transpilerParser.ASSIGN)
                self.state = 369
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 370
                self.match(transpilerParser.CONST)
                self.state = 371
                self.type_()
                self.state = 372
                self.match(transpilerParser.ID)

                self.state = 373
                self.match(transpilerParser.ASSIGN)
                self.state = 374
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
            self.state = 414
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 57, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 378
                self.match(transpilerParser.LET)
                self.state = 379
                self.match(transpilerParser.ID)
                self.state = 381
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 380
                    self.match(transpilerParser.QUESTION)

                self.state = 383
                self.match(transpilerParser.ASSIGN)
                self.state = 384
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 385
                self.match(transpilerParser.ID)
                self.state = 386
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 387
                self.type_()
                self.state = 389
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 388
                    self.match(transpilerParser.QUESTION)

                self.state = 393
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 49:
                    self.state = 391
                    self.match(transpilerParser.ASSIGN)
                    self.state = 392
                    self.expr(0)

                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 395
                self.type_()
                self.state = 396
                self.match(transpilerParser.ID)
                self.state = 398
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 397
                    self.match(transpilerParser.QUESTION)

                self.state = 402
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 49:
                    self.state = 400
                    self.match(transpilerParser.ASSIGN)
                    self.state = 401
                    self.expr(0)

                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 404
                self.match(transpilerParser.LET)
                self.state = 405
                self.match(transpilerParser.ID)
                self.state = 407
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 12:
                    self.state = 406
                    self.match(transpilerParser.QUESTION)

                self.state = 409
                _la = self._input.LA(1)
                if not (_la == 13 or _la == 14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 410
                self.type_()
                self.state = 411
                self.match(transpilerParser.ASSIGN)
                self.state = 412
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
            self.state = 416
            self.match(transpilerParser.RETURN)
            self.state = 418
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 58, self._ctx)
            if la_ == 1:
                self.state = 417
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

        def block(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.BlockContext)
            else:
                return self.getTypedRuleContext(transpilerParser.BlockContext, i)

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
            self.state = 420
            self.match(transpilerParser.IF)
            self.state = 421
            self.match(transpilerParser.LPAREN)
            self.state = 422
            self.condition()
            self.state = 423
            self.match(transpilerParser.RPAREN)
            self.state = 424
            self.block()
            self.state = 427
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 59, self._ctx)
            if la_ == 1:
                self.state = 425
                self.match(transpilerParser.ELSE)
                self.state = 426
                self.block()


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
        _startState = 50
        self.enterRecursionRule(localctx, 50, self.RULE_expr, _p)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 438
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 60, self._ctx)
            if la_ == 1:
                localctx = transpilerParser.PrimaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 430
                self.primary()
                pass

            elif la_ == 2:
                localctx = transpilerParser.NegExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 431
                self.match(transpilerParser.SUB)
                self.state = 432
                self.expr(12)
                pass

            elif la_ == 3:
                localctx = transpilerParser.LogicalNotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 433
                self.match(transpilerParser.NOT)
                self.state = 434
                self.expr(11)
                pass

            elif la_ == 4:
                localctx = transpilerParser.LocalAssignmentExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 435
                self.match(transpilerParser.ID)
                self.state = 436
                self.match(transpilerParser.ASSIGN)
                self.state = 437
                self.expr(1)
                pass

            self._ctx.stop = self._input.LT(-1)
            self.state = 495
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 62, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 493
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 61, self._ctx)
                    if la_ == 1:
                        localctx = transpilerParser.FactorExprContext(self,
                                                                      transpilerParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 440
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 441
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 481036337152) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 442
                        self.expr(11)
                        pass

                    elif la_ == 2:
                        localctx = transpilerParser.TermExprContext(self, transpilerParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 443
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 444
                        _la = self._input.LA(1)
                        if not (_la == 39 or _la == 40):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 445
                        self.expr(10)
                        pass

                    elif la_ == 3:
                        localctx = transpilerParser.CompareExprContext(self,
                                                                       transpilerParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 446
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 447
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 138538465099776) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 448
                        self.expr(9)
                        pass

                    elif la_ == 4:
                        localctx = transpilerParser.LogicalAndExprContext(self,
                                                                          transpilerParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 449
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 450
                        self.match(transpilerParser.AND)
                        self.state = 451
                        self.expr(8)
                        pass

                    elif la_ == 5:
                        localctx = transpilerParser.LogicalOrExprContext(self,
                                                                         transpilerParser.ExprContext(self, _parentctx,
                                                                                                      _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 452
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 453
                        self.match(transpilerParser.OR)
                        self.state = 454
                        self.expr(7)
                        pass

                    elif la_ == 6:
                        localctx = transpilerParser.TernaryTraditionalExprContext(self,
                                                                                  transpilerParser.ExprContext(self,
                                                                                                               _parentctx,
                                                                                                               _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 455
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 456
                        self.match(transpilerParser.QUESTION)
                        self.state = 457
                        self.expr(0)
                        self.state = 458
                        self.match(transpilerParser.COLON)
                        self.state = 459
                        self.expr(5)
                        pass

                    elif la_ == 7:
                        localctx = transpilerParser.TernaryPythonicExprContext(self, transpilerParser.ExprContext(self,
                                                                                                                  _parentctx,
                                                                                                                  _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 461
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 462
                        self.match(transpilerParser.IF)
                        self.state = 463
                        self.expr(0)
                        self.state = 464
                        self.match(transpilerParser.ELSE)
                        self.state = 465
                        self.expr(4)
                        pass

                    elif la_ == 8:
                        localctx = transpilerParser.ArrayAssignmentExprContext(self, transpilerParser.ExprContext(self,
                                                                                                                  _parentctx,
                                                                                                                  _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 467
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 468
                        self.match(transpilerParser.LBRACK)
                        self.state = 469
                        self.expr(0)
                        self.state = 470
                        self.match(transpilerParser.RBRACK)
                        self.state = 471
                        self.match(transpilerParser.ASSIGN)
                        self.state = 472
                        self.expr(4)
                        pass

                    elif la_ == 9:
                        localctx = transpilerParser.MemberAssignmentExprContext(self, transpilerParser.ExprContext(self,
                                                                                                                   _parentctx,
                                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 474
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 475
                        self.match(transpilerParser.T__1)
                        self.state = 476
                        self.match(transpilerParser.ID)
                        self.state = 477
                        self.match(transpilerParser.ASSIGN)
                        self.state = 478
                        self.expr(3)
                        pass

                    elif la_ == 10:
                        localctx = transpilerParser.MethodCallContext(self,
                                                                      transpilerParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 479
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 480
                        self.match(transpilerParser.T__1)
                        self.state = 481
                        self.match(transpilerParser.ID)
                        self.state = 482
                        self.argumentList()
                        pass

                    elif la_ == 11:
                        localctx = transpilerParser.MemberAccessContext(self,
                                                                        transpilerParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 483
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 484
                        self.match(transpilerParser.T__1)
                        self.state = 485
                        self.match(transpilerParser.ID)
                        pass

                    elif la_ == 12:
                        localctx = transpilerParser.ArrayAccessContext(self,
                                                                       transpilerParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 486
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 487
                        self.match(transpilerParser.LBRACK)
                        self.state = 488
                        self.expr(0)
                        self.state = 489
                        self.match(transpilerParser.RBRACK)
                        pass

                    elif la_ == 13:
                        localctx = transpilerParser.FunctionCallContext(self,
                                                                        transpilerParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 491
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 492
                        self.argumentList()
                        pass

                self.state = 497
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 62, self._ctx)

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
        self.enterRule(localctx, 52, self.RULE_primary)
        try:
            self.state = 504
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [53]:
                localctx = transpilerParser.IdentifierExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 498
                self.match(transpilerParser.ID)
                pass
            elif token in [30, 31, 32, 50, 51, 52]:
                localctx = transpilerParser.LiteralExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 499
                self.literal()
                pass
            elif token in [4]:
                localctx = transpilerParser.ParenExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 500
                self.match(transpilerParser.LPAREN)
                self.state = 501
                self.expr(0)
                self.state = 502
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
        self.enterRule(localctx, 54, self.RULE_argumentList)
        self._la = 0  # Token type
        try:
            self.state = 512
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 506
                self.match(transpilerParser.LPAREN)
                self.state = 508
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 16889639990198288) != 0):
                    self.state = 507
                    self.exprList()

                self.state = 510
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 511
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
        self.enterRule(localctx, 56, self.RULE_exprList)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 514
            self.expr(0)
            self.state = 519
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 11:
                self.state = 515
                self.match(transpilerParser.COMMA)
                self.state = 516
                self.expr(0)
                self.state = 521
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
        self.enterRule(localctx, 58, self.RULE_literal)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 522
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 7881306864091136) != 0)):
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
        self._predicates[25] = self.expr_sempred
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
