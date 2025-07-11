# Generated from E:/python/minecraft-datapack-language/antlr/McFuncDSL.g4 by ANTLR 4.13.2
# encoding: utf-8
import sys

from antlr4 import *

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4, 1, 62, 463, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7,
        6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13,
        2, 14, 7, 14, 2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20,
        7, 20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26,
        2, 27, 7, 27, 2, 28, 7, 28, 2, 29, 7, 29, 2, 30, 7, 30, 2, 31, 7, 31, 2, 32, 7, 32, 1, 0,
        5, 0, 68, 8, 0, 10, 0, 12, 0, 71, 9, 0, 1, 0, 1, 0, 1, 0, 5, 0, 76, 8, 0, 10, 0, 12, 0, 79,
        9, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 3, 5, 3, 91, 8, 3, 10, 3, 12, 3,
        94, 9, 3, 1, 3, 1, 3, 1, 3, 1, 3, 3, 3, 100, 8, 3, 1, 3, 1, 3, 3, 3, 104, 8, 3, 1, 3, 1, 3, 1,
        3, 1, 3, 5, 3, 110, 8, 3, 10, 3, 12, 3, 113, 9, 3, 1, 3, 1, 3, 1, 4, 5, 4, 118, 8, 4, 10, 4,
        12, 4, 121, 9, 4, 1, 4, 1, 4, 1, 4, 1, 4, 3, 4, 127, 8, 4, 1, 4, 1, 4, 5, 4, 131, 8, 4, 10,
        4, 12, 4, 134, 9, 4, 1, 4, 1, 4, 1, 5, 5, 5, 139, 8, 5, 10, 5, 12, 5, 142, 9, 5, 1, 5, 1, 5,
        1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 6, 1, 6, 3, 6, 154, 8, 6, 1, 7, 1, 7, 1, 7, 5, 7, 159,
        8, 7, 10, 7, 12, 7, 162, 9, 7, 1, 8, 1, 8, 1, 9, 5, 9, 167, 8, 9, 10, 9, 12, 9, 170, 9, 9,
        1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 5, 9, 181, 8, 9, 10, 9, 12, 9, 184, 9,
        9, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 3, 9, 192, 8, 9, 1, 10, 5, 10, 195, 8, 10, 10, 10, 12,
        10, 198, 9, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 5, 10, 208, 8, 10,
        10, 10, 12, 10, 211, 9, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 3, 10, 219, 8, 10,
        1, 11, 1, 11, 1, 11, 1, 11, 5, 11, 225, 8, 11, 10, 11, 12, 11, 228, 9, 11, 1, 11, 1, 11,
        1, 11, 3, 11, 233, 8, 11, 1, 12, 1, 12, 1, 12, 1, 12, 1, 12, 1, 12, 3, 12, 241, 8, 12, 1,
        13, 1, 13, 5, 13, 245, 8, 13, 10, 13, 12, 13, 248, 9, 13, 1, 13, 1, 13, 1, 14, 1, 14, 1,
        14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1,
        14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 3, 14, 277, 8, 14, 1,
        15, 1, 15, 1, 16, 1, 16, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1,
        17, 1, 17, 1, 17, 1, 17, 1, 17, 3, 17, 297, 8, 17, 1, 18, 3, 18, 300, 8, 18, 1, 18, 1, 18,
        3, 18, 304, 8, 18, 1, 18, 1, 18, 3, 18, 308, 8, 18, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1,
        19, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1,
        20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 3, 20, 334, 8, 20, 1, 21, 1, 21, 1, 21, 1, 21, 1,
        21, 3, 21, 341, 8, 21, 1, 21, 1, 21, 3, 21, 345, 8, 21, 1, 21, 1, 21, 1, 21, 3, 21, 350,
        8, 21, 1, 21, 1, 21, 3, 21, 354, 8, 21, 3, 21, 356, 8, 21, 1, 22, 1, 22, 1, 22, 1, 22, 1,
        22, 1, 22, 1, 22, 3, 22, 365, 8, 22, 1, 23, 1, 23, 1, 23, 3, 23, 370, 8, 23, 1, 24, 1, 24,
        1, 24, 1, 24, 1, 25, 1, 25, 3, 25, 378, 8, 25, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26,
        1, 26, 3, 26, 387, 8, 26, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 3, 27,
        397, 8, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27,
        1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 5, 27, 421,
        8, 27, 10, 27, 12, 27, 424, 9, 27, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28,
        1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 3, 28, 440, 8, 28, 1, 29, 1, 29, 1, 29, 1, 30,
        1, 30, 3, 30, 447, 8, 30, 1, 30, 1, 30, 3, 30, 451, 8, 30, 1, 31, 1, 31, 1, 31, 5, 31, 456,
        8, 31, 10, 31, 12, 31, 459, 9, 31, 1, 32, 1, 32, 1, 32, 0, 1, 54, 33, 0, 2, 4, 6, 8, 10,
        12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54,
        56, 58, 60, 62, 64, 0, 6, 1, 0, 9, 12, 2, 0, 2, 2, 41, 41, 1, 0, 44, 45, 1, 0, 46, 47, 2,
        0, 7, 8, 48, 51, 2, 0, 34, 36, 55, 57, 498, 0, 69, 1, 0, 0, 0, 2, 82, 1, 0, 0, 0, 4, 86, 1,
        0, 0, 0, 6, 92, 1, 0, 0, 0, 8, 119, 1, 0, 0, 0, 10, 140, 1, 0, 0, 0, 12, 153, 1, 0, 0, 0, 14,
        155, 1, 0, 0, 0, 16, 163, 1, 0, 0, 0, 18, 191, 1, 0, 0, 0, 20, 218, 1, 0, 0, 0, 22, 232,
        1, 0, 0, 0, 24, 240, 1, 0, 0, 0, 26, 242, 1, 0, 0, 0, 28, 276, 1, 0, 0, 0, 30, 278, 1, 0,
        0, 0, 32, 280, 1, 0, 0, 0, 34, 296, 1, 0, 0, 0, 36, 299, 1, 0, 0, 0, 38, 309, 1, 0, 0, 0,
        40, 333, 1, 0, 0, 0, 42, 355, 1, 0, 0, 0, 44, 364, 1, 0, 0, 0, 46, 369, 1, 0, 0, 0, 48, 371,
        1, 0, 0, 0, 50, 375, 1, 0, 0, 0, 52, 379, 1, 0, 0, 0, 54, 396, 1, 0, 0, 0, 56, 439, 1, 0,
        0, 0, 58, 441, 1, 0, 0, 0, 60, 450, 1, 0, 0, 0, 62, 452, 1, 0, 0, 0, 64, 460, 1, 0, 0, 0,
        66, 68, 3, 2, 1, 0, 67, 66, 1, 0, 0, 0, 68, 71, 1, 0, 0, 0, 69, 67, 1, 0, 0, 0, 69, 70, 1,
        0, 0, 0, 70, 77, 1, 0, 0, 0, 71, 69, 1, 0, 0, 0, 72, 76, 3, 6, 3, 0, 73, 76, 3, 8, 4, 0, 74,
        76, 3, 28, 14, 0, 75, 72, 1, 0, 0, 0, 75, 73, 1, 0, 0, 0, 75, 74, 1, 0, 0, 0, 76, 79, 1, 0,
        0, 0, 77, 75, 1, 0, 0, 0, 77, 78, 1, 0, 0, 0, 78, 80, 1, 0, 0, 0, 79, 77, 1, 0, 0, 0, 80, 81,
        5, 0, 0, 1, 81, 1, 1, 0, 0, 0, 82, 83, 5, 20, 0, 0, 83, 84, 3, 64, 32, 0, 84, 85, 5, 18, 0,
        0, 85, 3, 1, 0, 0, 0, 86, 87, 5, 1, 0, 0, 87, 88, 5, 58, 0, 0, 88, 5, 1, 0, 0, 0, 89, 91, 3,
        4, 2, 0, 90, 89, 1, 0, 0, 0, 91, 94, 1, 0, 0, 0, 92, 90, 1, 0, 0, 0, 92, 93, 1, 0, 0, 0, 93,
        95, 1, 0, 0, 0, 94, 92, 1, 0, 0, 0, 95, 96, 5, 23, 0, 0, 96, 99, 5, 58, 0, 0, 97, 98, 5, 25,
        0, 0, 98, 100, 3, 12, 6, 0, 99, 97, 1, 0, 0, 0, 99, 100, 1, 0, 0, 0, 100, 103, 1, 0, 0, 0,
        101, 102, 5, 26, 0, 0, 102, 104, 3, 12, 6, 0, 103, 101, 1, 0, 0, 0, 103, 104, 1, 0, 0,
        0, 104, 105, 1, 0, 0, 0, 105, 111, 5, 16, 0, 0, 106, 110, 3, 44, 22, 0, 107, 110, 3, 40,
        20, 0, 108, 110, 3, 20, 10, 0, 109, 106, 1, 0, 0, 0, 109, 107, 1, 0, 0, 0, 109, 108, 1,
        0, 0, 0, 110, 113, 1, 0, 0, 0, 111, 109, 1, 0, 0, 0, 111, 112, 1, 0, 0, 0, 112, 114, 1,
        0, 0, 0, 113, 111, 1, 0, 0, 0, 114, 115, 5, 17, 0, 0, 115, 7, 1, 0, 0, 0, 116, 118, 3, 4,
        2, 0, 117, 116, 1, 0, 0, 0, 118, 121, 1, 0, 0, 0, 119, 117, 1, 0, 0, 0, 119, 120, 1, 0,
        0, 0, 120, 122, 1, 0, 0, 0, 121, 119, 1, 0, 0, 0, 122, 123, 5, 24, 0, 0, 123, 126, 5, 58,
        0, 0, 124, 125, 5, 25, 0, 0, 125, 127, 3, 12, 6, 0, 126, 124, 1, 0, 0, 0, 126, 127, 1,
        0, 0, 0, 127, 128, 1, 0, 0, 0, 128, 132, 5, 16, 0, 0, 129, 131, 3, 10, 5, 0, 130, 129,
        1, 0, 0, 0, 131, 134, 1, 0, 0, 0, 132, 130, 1, 0, 0, 0, 132, 133, 1, 0, 0, 0, 133, 135,
        1, 0, 0, 0, 134, 132, 1, 0, 0, 0, 135, 136, 5, 17, 0, 0, 136, 9, 1, 0, 0, 0, 137, 139, 3,
        4, 2, 0, 138, 137, 1, 0, 0, 0, 139, 142, 1, 0, 0, 0, 140, 138, 1, 0, 0, 0, 140, 141, 1,
        0, 0, 0, 141, 143, 1, 0, 0, 0, 142, 140, 1, 0, 0, 0, 143, 144, 5, 22, 0, 0, 144, 145, 5,
        58, 0, 0, 145, 146, 3, 22, 11, 0, 146, 147, 5, 2, 0, 0, 147, 148, 3, 12, 6, 0, 148, 149,
        1, 0, 0, 0, 149, 150, 5, 18, 0, 0, 150, 11, 1, 0, 0, 0, 151, 154, 5, 58, 0, 0, 152, 154,
        3, 16, 8, 0, 153, 151, 1, 0, 0, 0, 153, 152, 1, 0, 0, 0, 154, 13, 1, 0, 0, 0, 155, 160,
        3, 12, 6, 0, 156, 157, 5, 19, 0, 0, 157, 159, 3, 12, 6, 0, 158, 156, 1, 0, 0, 0, 159, 162,
        1, 0, 0, 0, 160, 158, 1, 0, 0, 0, 160, 161, 1, 0, 0, 0, 161, 15, 1, 0, 0, 0, 162, 160, 1,
        0, 0, 0, 163, 164, 7, 0, 0, 0, 164, 17, 1, 0, 0, 0, 165, 167, 3, 4, 2, 0, 166, 165, 1, 0,
        0, 0, 167, 170, 1, 0, 0, 0, 168, 166, 1, 0, 0, 0, 168, 169, 1, 0, 0, 0, 169, 171, 1, 0,
        0, 0, 170, 168, 1, 0, 0, 0, 171, 172, 5, 21, 0, 0, 172, 173, 5, 58, 0, 0, 173, 174, 3,
        22, 11, 0, 174, 175, 7, 1, 0, 0, 175, 176, 3, 12, 6, 0, 176, 177, 1, 0, 0, 0, 177, 178,
        3, 26, 13, 0, 178, 192, 1, 0, 0, 0, 179, 181, 3, 4, 2, 0, 180, 179, 1, 0, 0, 0, 181, 184,
        1, 0, 0, 0, 182, 180, 1, 0, 0, 0, 182, 183, 1, 0, 0, 0, 183, 185, 1, 0, 0, 0, 184, 182,
        1, 0, 0, 0, 185, 186, 5, 21, 0, 0, 186, 187, 3, 12, 6, 0, 187, 188, 5, 58, 0, 0, 188, 189,
        3, 22, 11, 0, 189, 190, 3, 26, 13, 0, 190, 192, 1, 0, 0, 0, 191, 168, 1, 0, 0, 0, 191,
        182, 1, 0, 0, 0, 192, 19, 1, 0, 0, 0, 193, 195, 3, 4, 2, 0, 194, 193, 1, 0, 0, 0, 195, 198,
        1, 0, 0, 0, 196, 194, 1, 0, 0, 0, 196, 197, 1, 0, 0, 0, 197, 199, 1, 0, 0, 0, 198, 196,
        1, 0, 0, 0, 199, 200, 5, 22, 0, 0, 200, 201, 5, 58, 0, 0, 201, 202, 3, 22, 11, 0, 202,
        203, 7, 1, 0, 0, 203, 204, 3, 12, 6, 0, 204, 205, 3, 26, 13, 0, 205, 219, 1, 0, 0, 0, 206,
        208, 3, 4, 2, 0, 207, 206, 1, 0, 0, 0, 208, 211, 1, 0, 0, 0, 209, 207, 1, 0, 0, 0, 209,
        210, 1, 0, 0, 0, 210, 212, 1, 0, 0, 0, 211, 209, 1, 0, 0, 0, 212, 213, 5, 22, 0, 0, 213,
        214, 3, 12, 6, 0, 214, 215, 5, 58, 0, 0, 215, 216, 3, 22, 11, 0, 216, 217, 3, 26, 13,
        0, 217, 219, 1, 0, 0, 0, 218, 196, 1, 0, 0, 0, 218, 209, 1, 0, 0, 0, 219, 21, 1, 0, 0, 0,
        220, 221, 5, 14, 0, 0, 221, 226, 3, 24, 12, 0, 222, 223, 5, 19, 0, 0, 223, 225, 3, 24,
        12, 0, 224, 222, 1, 0, 0, 0, 225, 228, 1, 0, 0, 0, 226, 224, 1, 0, 0, 0, 226, 227, 1, 0,
        0, 0, 227, 229, 1, 0, 0, 0, 228, 226, 1, 0, 0, 0, 229, 230, 5, 15, 0, 0, 230, 233, 1, 0,
        0, 0, 231, 233, 5, 3, 0, 0, 232, 220, 1, 0, 0, 0, 232, 231, 1, 0, 0, 0, 233, 23, 1, 0, 0,
        0, 234, 235, 5, 58, 0, 0, 235, 236, 5, 2, 0, 0, 236, 241, 3, 12, 6, 0, 237, 238, 3, 12,
        6, 0, 238, 239, 5, 58, 0, 0, 239, 241, 1, 0, 0, 0, 240, 234, 1, 0, 0, 0, 240, 237, 1, 0,
        0, 0, 241, 25, 1, 0, 0, 0, 242, 246, 5, 16, 0, 0, 243, 245, 3, 28, 14, 0, 244, 243, 1,
        0, 0, 0, 245, 248, 1, 0, 0, 0, 246, 244, 1, 0, 0, 0, 246, 247, 1, 0, 0, 0, 247, 249, 1,
        0, 0, 0, 248, 246, 1, 0, 0, 0, 249, 250, 5, 17, 0, 0, 250, 27, 1, 0, 0, 0, 251, 252, 3,
        58, 29, 0, 252, 253, 5, 18, 0, 0, 253, 277, 1, 0, 0, 0, 254, 277, 3, 44, 22, 0, 255, 277,
        3, 40, 20, 0, 256, 277, 3, 34, 17, 0, 257, 277, 3, 38, 19, 0, 258, 259, 3, 48, 24, 0,
        259, 260, 5, 18, 0, 0, 260, 277, 1, 0, 0, 0, 261, 262, 3, 54, 27, 0, 262, 263, 5, 18,
        0, 0, 263, 277, 1, 0, 0, 0, 264, 265, 3, 50, 25, 0, 265, 266, 5, 18, 0, 0, 266, 277, 1,
        0, 0, 0, 267, 277, 3, 26, 13, 0, 268, 277, 3, 52, 26, 0, 269, 270, 3, 30, 15, 0, 270,
        271, 5, 18, 0, 0, 271, 277, 1, 0, 0, 0, 272, 273, 3, 32, 16, 0, 273, 274, 5, 18, 0, 0,
        274, 277, 1, 0, 0, 0, 275, 277, 3, 18, 9, 0, 276, 251, 1, 0, 0, 0, 276, 254, 1, 0, 0, 0,
        276, 255, 1, 0, 0, 0, 276, 256, 1, 0, 0, 0, 276, 257, 1, 0, 0, 0, 276, 258, 1, 0, 0, 0,
        276, 261, 1, 0, 0, 0, 276, 264, 1, 0, 0, 0, 276, 267, 1, 0, 0, 0, 276, 268, 1, 0, 0, 0,
        276, 269, 1, 0, 0, 0, 276, 272, 1, 0, 0, 0, 276, 275, 1, 0, 0, 0, 277, 29, 1, 0, 0, 0, 278,
        279, 5, 38, 0, 0, 279, 31, 1, 0, 0, 0, 280, 281, 5, 39, 0, 0, 281, 33, 1, 0, 0, 0, 282,
        283, 5, 29, 0, 0, 283, 284, 5, 14, 0, 0, 284, 285, 3, 36, 18, 0, 285, 286, 5, 15, 0, 0,
        286, 287, 3, 26, 13, 0, 287, 297, 1, 0, 0, 0, 288, 289, 5, 29, 0, 0, 289, 290, 5, 14,
        0, 0, 290, 291, 5, 58, 0, 0, 291, 292, 5, 2, 0, 0, 292, 293, 3, 54, 27, 0, 293, 294, 5,
        15, 0, 0, 294, 295, 3, 26, 13, 0, 295, 297, 1, 0, 0, 0, 296, 282, 1, 0, 0, 0, 296, 288,
        1, 0, 0, 0, 297, 35, 1, 0, 0, 0, 298, 300, 3, 46, 23, 0, 299, 298, 1, 0, 0, 0, 299, 300,
        1, 0, 0, 0, 300, 301, 1, 0, 0, 0, 301, 303, 5, 18, 0, 0, 302, 304, 3, 54, 27, 0, 303, 302,
        1, 0, 0, 0, 303, 304, 1, 0, 0, 0, 304, 305, 1, 0, 0, 0, 305, 307, 5, 18, 0, 0, 306, 308,
        3, 48, 24, 0, 307, 306, 1, 0, 0, 0, 307, 308, 1, 0, 0, 0, 308, 37, 1, 0, 0, 0, 309, 310,
        5, 30, 0, 0, 310, 311, 5, 14, 0, 0, 311, 312, 3, 54, 27, 0, 312, 313, 5, 15, 0, 0, 313,
        314, 3, 26, 13, 0, 314, 39, 1, 0, 0, 0, 315, 316, 5, 4, 0, 0, 316, 317, 5, 58, 0, 0, 317,
        318, 5, 2, 0, 0, 318, 319, 3, 12, 6, 0, 319, 320, 1, 0, 0, 0, 320, 321, 5, 54, 0, 0, 321,
        322, 3, 54, 27, 0, 322, 323, 1, 0, 0, 0, 323, 324, 5, 18, 0, 0, 324, 334, 1, 0, 0, 0, 325,
        326, 5, 4, 0, 0, 326, 327, 3, 12, 6, 0, 327, 328, 5, 58, 0, 0, 328, 329, 5, 54, 0, 0, 329,
        330, 3, 54, 27, 0, 330, 331, 1, 0, 0, 0, 331, 332, 5, 18, 0, 0, 332, 334, 1, 0, 0, 0, 333,
        315, 1, 0, 0, 0, 333, 325, 1, 0, 0, 0, 334, 41, 1, 0, 0, 0, 335, 336, 5, 58, 0, 0, 336,
        337, 5, 2, 0, 0, 337, 338, 3, 12, 6, 0, 338, 340, 1, 0, 0, 0, 339, 341, 5, 5, 0, 0, 340,
        339, 1, 0, 0, 0, 340, 341, 1, 0, 0, 0, 341, 344, 1, 0, 0, 0, 342, 343, 5, 54, 0, 0, 343,
        345, 3, 54, 27, 0, 344, 342, 1, 0, 0, 0, 344, 345, 1, 0, 0, 0, 345, 356, 1, 0, 0, 0, 346,
        347, 3, 12, 6, 0, 347, 349, 5, 58, 0, 0, 348, 350, 5, 5, 0, 0, 349, 348, 1, 0, 0, 0, 349,
        350, 1, 0, 0, 0, 350, 353, 1, 0, 0, 0, 351, 352, 5, 54, 0, 0, 352, 354, 3, 54, 27, 0, 353,
        351, 1, 0, 0, 0, 353, 354, 1, 0, 0, 0, 354, 356, 1, 0, 0, 0, 355, 335, 1, 0, 0, 0, 355,
        346, 1, 0, 0, 0, 356, 43, 1, 0, 0, 0, 357, 358, 5, 27, 0, 0, 358, 359, 3, 42, 21, 0, 359,
        360, 5, 18, 0, 0, 360, 365, 1, 0, 0, 0, 361, 362, 3, 42, 21, 0, 362, 363, 5, 18, 0, 0,
        363, 365, 1, 0, 0, 0, 364, 357, 1, 0, 0, 0, 364, 361, 1, 0, 0, 0, 365, 45, 1, 0, 0, 0, 366,
        367, 5, 27, 0, 0, 367, 370, 3, 42, 21, 0, 368, 370, 3, 42, 21, 0, 369, 366, 1, 0, 0, 0,
        369, 368, 1, 0, 0, 0, 370, 47, 1, 0, 0, 0, 371, 372, 5, 58, 0, 0, 372, 373, 5, 54, 0, 0,
        373, 374, 3, 54, 27, 0, 374, 49, 1, 0, 0, 0, 375, 377, 5, 28, 0, 0, 376, 378, 3, 54, 27,
        0, 377, 376, 1, 0, 0, 0, 377, 378, 1, 0, 0, 0, 378, 51, 1, 0, 0, 0, 379, 380, 5, 31, 0,
        0, 380, 381, 5, 14, 0, 0, 381, 382, 3, 54, 27, 0, 382, 383, 5, 15, 0, 0, 383, 386, 3,
        26, 13, 0, 384, 385, 5, 32, 0, 0, 385, 387, 3, 26, 13, 0, 386, 384, 1, 0, 0, 0, 386, 387,
        1, 0, 0, 0, 387, 53, 1, 0, 0, 0, 388, 389, 6, 27, -1, 0, 389, 390, 5, 58, 0, 0, 390, 397,
        3, 60, 30, 0, 391, 397, 3, 56, 28, 0, 392, 393, 5, 47, 0, 0, 393, 397, 3, 54, 27, 7, 394,
        395, 5, 43, 0, 0, 395, 397, 3, 54, 27, 6, 396, 388, 1, 0, 0, 0, 396, 391, 1, 0, 0, 0, 396,
        392, 1, 0, 0, 0, 396, 394, 1, 0, 0, 0, 397, 422, 1, 0, 0, 0, 398, 399, 10, 5, 0, 0, 399,
        400, 7, 2, 0, 0, 400, 421, 3, 54, 27, 6, 401, 402, 10, 4, 0, 0, 402, 403, 7, 3, 0, 0, 403,
        421, 3, 54, 27, 5, 404, 405, 10, 3, 0, 0, 405, 406, 7, 4, 0, 0, 406, 421, 3, 54, 27, 4,
        407, 408, 10, 2, 0, 0, 408, 409, 5, 52, 0, 0, 409, 421, 3, 54, 27, 3, 410, 411, 10, 1,
        0, 0, 411, 412, 5, 53, 0, 0, 412, 421, 3, 54, 27, 2, 413, 414, 10, 11, 0, 0, 414, 415,
        5, 6, 0, 0, 415, 416, 5, 58, 0, 0, 416, 421, 3, 60, 30, 0, 417, 418, 10, 10, 0, 0, 418,
        419, 5, 6, 0, 0, 419, 421, 5, 58, 0, 0, 420, 398, 1, 0, 0, 0, 420, 401, 1, 0, 0, 0, 420,
        404, 1, 0, 0, 0, 420, 407, 1, 0, 0, 0, 420, 410, 1, 0, 0, 0, 420, 413, 1, 0, 0, 0, 420,
        417, 1, 0, 0, 0, 421, 424, 1, 0, 0, 0, 422, 420, 1, 0, 0, 0, 422, 423, 1, 0, 0, 0, 423,
        55, 1, 0, 0, 0, 424, 422, 1, 0, 0, 0, 425, 440, 5, 58, 0, 0, 426, 440, 3, 64, 32, 0, 427,
        428, 5, 14, 0, 0, 428, 429, 3, 54, 27, 0, 429, 430, 5, 15, 0, 0, 430, 440, 1, 0, 0, 0,
        431, 432, 5, 33, 0, 0, 432, 433, 5, 58, 0, 0, 433, 440, 3, 60, 30, 0, 434, 435, 5, 14,
        0, 0, 435, 436, 3, 12, 6, 0, 436, 437, 5, 15, 0, 0, 437, 438, 3, 54, 27, 0, 438, 440,
        1, 0, 0, 0, 439, 425, 1, 0, 0, 0, 439, 426, 1, 0, 0, 0, 439, 427, 1, 0, 0, 0, 439, 431,
        1, 0, 0, 0, 439, 434, 1, 0, 0, 0, 440, 57, 1, 0, 0, 0, 441, 442, 5, 40, 0, 0, 442, 443,
        3, 60, 30, 0, 443, 59, 1, 0, 0, 0, 444, 446, 5, 14, 0, 0, 445, 447, 3, 62, 31, 0, 446,
        445, 1, 0, 0, 0, 446, 447, 1, 0, 0, 0, 447, 448, 1, 0, 0, 0, 448, 451, 5, 15, 0, 0, 449,
        451, 5, 3, 0, 0, 450, 444, 1, 0, 0, 0, 450, 449, 1, 0, 0, 0, 451, 61, 1, 0, 0, 0, 452, 457,
        3, 54, 27, 0, 453, 454, 5, 19, 0, 0, 454, 456, 3, 54, 27, 0, 455, 453, 1, 0, 0, 0, 456,
        459, 1, 0, 0, 0, 457, 455, 1, 0, 0, 0, 457, 458, 1, 0, 0, 0, 458, 63, 1, 0, 0, 0, 459, 457,
        1, 0, 0, 0, 460, 461, 7, 5, 0, 0, 461, 65, 1, 0, 0, 0, 46, 69, 75, 77, 92, 99, 103, 109,
        111, 119, 126, 132, 140, 153, 160, 168, 182, 191, 196, 209, 218, 226, 232, 240,
        246, 276, 296, 299, 303, 307, 333, 340, 344, 349, 353, 355, 364, 369, 377, 386,
        396, 420, 422, 439, 446, 450, 457
    ]


class McFuncDSLParser(Parser):
    grammarFileName = "McFuncDSL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'@'", "':'", "'()'", "'const'", "'?'",
                    "'.'", "'<='", "'>='", "'int'", "'string'", "'boolean'",
                    "'void'", "'any'", "'('", "')'", "'{'", "'}'", "';'",
                    "','", "'include'", "'func'", "'method'", "'class'",
                    "'interface'", "'extends'", "'implements'", "'var'",
                    "'return'", "'for'", "'while'", "'if'", "'else'", "'new'",
                    "'true'", "'false'", "'null'", "'in'", "'break'", "'continue'",
                    "<INVALID>", "'->'", "'::'", "'!'", "'*'", "'/'", "'+'",
                    "'-'", "'>'", "'<'", "'=='", "'!='", "<INVALID>", "<INVALID>",
                    "'='"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "TYPE_INT", "TYPE_STRING", "TYPE_BOOLEAN",
                     "TYPE_VOID", "TYPE_ANY", "LPAREN", "RPAREN", "LBRACE",
                     "RBRACE", "SEMI", "COMMA", "INCULDE", "FUNC", "METHOD",
                     "CLASS", "INTERFACE", "EXTENDS", "IMPLEMENTS", "VAR",
                     "RETURN", "FOR", "WHILE", "IF", "ELSE", "NEW", "TRUE",
                     "FALSE", "NULL", "IN", "BREAK", "CONTINUE", "CMD",
                     "ARROW", "DOUBLE_COLON", "NOT", "MUL", "DIV", "ADD",
                     "SUB", "GT", "LT", "EQ", "NEQ", "AND", "OR", "ASSIGN",
                     "NUMBER", "STRING", "FSTRING", "ID", "WS", "LINE_COMMENT",
                     "LINE_COMMENT2", "BLOCK_COMMENT"]

    RULE_program = 0
    RULE_includeStmt = 1
    RULE_annotation = 2
    RULE_classDecl = 3
    RULE_interfaceDecl = 4
    RULE_interfaceMethodDecl = 5
    RULE_type = 6
    RULE_typeList = 7
    RULE_primitiveType = 8
    RULE_functionDecl = 9
    RULE_methodDecl = 10
    RULE_paramList = 11
    RULE_paramDecl = 12
    RULE_block = 13
    RULE_statement = 14
    RULE_breakStmt = 15
    RULE_continueStmt = 16
    RULE_forStmt = 17
    RULE_forControl = 18
    RULE_whileStmt = 19
    RULE_constDecl = 20
    RULE_varDeclaration = 21
    RULE_varDecl = 22
    RULE_forLoopVarDecl = 23
    RULE_assignment = 24
    RULE_returnStmt = 25
    RULE_ifStmt = 26
    RULE_expr = 27
    RULE_primary = 28
    RULE_commandExpr = 29
    RULE_argumentList = 30
    RULE_exprList = 31
    RULE_literal = 32

    ruleNames = ["program", "includeStmt", "annotation", "classDecl",
                 "interfaceDecl", "interfaceMethodDecl", "type", "typeList",
                 "primitiveType", "functionDecl", "methodDecl", "paramList",
                 "paramDecl", "block", "statement", "breakStmt", "continueStmt",
                 "forStmt", "forControl", "whileStmt", "constDecl", "varDeclaration",
                 "varDecl", "forLoopVarDecl", "assignment", "returnStmt",
                 "ifStmt", "expr", "primary", "commandExpr", "argumentList",
                 "exprList", "literal"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    TYPE_INT = 9
    TYPE_STRING = 10
    TYPE_BOOLEAN = 11
    TYPE_VOID = 12
    TYPE_ANY = 13
    LPAREN = 14
    RPAREN = 15
    LBRACE = 16
    RBRACE = 17
    SEMI = 18
    COMMA = 19
    INCULDE = 20
    FUNC = 21
    METHOD = 22
    CLASS = 23
    INTERFACE = 24
    EXTENDS = 25
    IMPLEMENTS = 26
    VAR = 27
    RETURN = 28
    FOR = 29
    WHILE = 30
    IF = 31
    ELSE = 32
    NEW = 33
    TRUE = 34
    FALSE = 35
    NULL = 36
    IN = 37
    BREAK = 38
    CONTINUE = 39
    CMD = 40
    ARROW = 41
    DOUBLE_COLON = 42
    NOT = 43
    MUL = 44
    DIV = 45
    ADD = 46
    SUB = 47
    GT = 48
    LT = 49
    EQ = 50
    NEQ = 51
    AND = 52
    OR = 53
    ASSIGN = 54
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
            return self.getToken(McFuncDSLParser.EOF, 0)

        def includeStmt(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.IncludeStmtContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.IncludeStmtContext, i)

        def classDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ClassDeclContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ClassDeclContext, i)

        def interfaceDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.InterfaceDeclContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.InterfaceDeclContext, i)

        def statement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.StatementContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.StatementContext, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_program

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

        localctx = McFuncDSLParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 20:
                self.state = 66
                self.includeStmt()
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 77
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 540583546048306706) != 0):
                self.state = 75
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 1, self._ctx)
                if la_ == 1:
                    self.state = 72
                    self.classDecl()
                    pass

                elif la_ == 2:
                    self.state = 73
                    self.interfaceDecl()
                    pass

                elif la_ == 3:
                    self.state = 74
                    self.statement()
                    pass

                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 80
            self.match(McFuncDSLParser.EOF)
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

        def INCULDE(self):
            return self.getToken(McFuncDSLParser.INCULDE, 0)

        def literal(self):
            return self.getTypedRuleContext(McFuncDSLParser.LiteralContext, 0)

        def SEMI(self):
            return self.getToken(McFuncDSLParser.SEMI, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_includeStmt

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

        localctx = McFuncDSLParser.IncludeStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_includeStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(McFuncDSLParser.INCULDE)
            self.state = 83
            self.literal()
            self.state = 84
            self.match(McFuncDSLParser.SEMI)
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
            return self.getToken(McFuncDSLParser.ID, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_annotation

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

        localctx = McFuncDSLParser.AnnotationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_annotation)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(McFuncDSLParser.T__0)
            self.state = 87
            self.match(McFuncDSLParser.ID)
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
            return self.getToken(McFuncDSLParser.CLASS, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def LBRACE(self):
            return self.getToken(McFuncDSLParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(McFuncDSLParser.RBRACE, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.AnnotationContext, i)

        def EXTENDS(self):
            return self.getToken(McFuncDSLParser.EXTENDS, 0)

        def type_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.TypeContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.TypeContext, i)

        def IMPLEMENTS(self):
            return self.getToken(McFuncDSLParser.IMPLEMENTS, 0)

        def varDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.VarDeclContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.VarDeclContext, i)

        def constDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ConstDeclContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ConstDeclContext, i)

        def methodDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.MethodDeclContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.MethodDeclContext, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_classDecl

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

        localctx = McFuncDSLParser.ClassDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_classDecl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 89
                self.annotation()
                self.state = 94
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 95
            self.match(McFuncDSLParser.CLASS)
            self.state = 96
            self.match(McFuncDSLParser.ID)
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 25:
                self.state = 97
                self.match(McFuncDSLParser.EXTENDS)
                self.state = 98
                self.type_()

            self.state = 103
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 26:
                self.state = 101
                self.match(McFuncDSLParser.IMPLEMENTS)
                self.state = 102
                self.type_()

            self.state = 105
            self.match(McFuncDSLParser.LBRACE)
            self.state = 111
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230376290131474) != 0):
                self.state = 109
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [9, 10, 11, 12, 27, 58]:
                    self.state = 106
                    self.varDecl()
                    pass
                elif token in [4]:
                    self.state = 107
                    self.constDecl()
                    pass
                elif token in [1, 22]:
                    self.state = 108
                    self.methodDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 113
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 114
            self.match(McFuncDSLParser.RBRACE)
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
            return self.getToken(McFuncDSLParser.INTERFACE, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def LBRACE(self):
            return self.getToken(McFuncDSLParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(McFuncDSLParser.RBRACE, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.AnnotationContext, i)

        def EXTENDS(self):
            return self.getToken(McFuncDSLParser.EXTENDS, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def interfaceMethodDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.InterfaceMethodDeclContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.InterfaceMethodDeclContext, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_interfaceDecl

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

        localctx = McFuncDSLParser.InterfaceDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_interfaceDecl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 116
                self.annotation()
                self.state = 121
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 122
            self.match(McFuncDSLParser.INTERFACE)
            self.state = 123
            self.match(McFuncDSLParser.ID)
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 25:
                self.state = 124
                self.match(McFuncDSLParser.EXTENDS)
                self.state = 125
                self.type_()

            self.state = 128
            self.match(McFuncDSLParser.LBRACE)
            self.state = 132
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1 or _la == 22:
                self.state = 129
                self.interfaceMethodDecl()
                self.state = 134
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 135
            self.match(McFuncDSLParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class InterfaceMethodDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def METHOD(self):
            return self.getToken(McFuncDSLParser.METHOD, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def paramList(self):
            return self.getTypedRuleContext(McFuncDSLParser.ParamListContext, 0)

        def SEMI(self):
            return self.getToken(McFuncDSLParser.SEMI, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.AnnotationContext, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_interfaceMethodDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterInterfaceMethodDecl"):
                listener.enterInterfaceMethodDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitInterfaceMethodDecl"):
                listener.exitInterfaceMethodDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitInterfaceMethodDecl"):
                return visitor.visitInterfaceMethodDecl(self)
            else:
                return visitor.visitChildren(self)

    def interfaceMethodDecl(self):

        localctx = McFuncDSLParser.InterfaceMethodDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_interfaceMethodDecl)
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
            self.match(McFuncDSLParser.METHOD)
            self.state = 144
            self.match(McFuncDSLParser.ID)
            self.state = 145
            self.paramList()

            self.state = 146
            self.match(McFuncDSLParser.T__1)
            self.state = 147
            self.type_()
            self.state = 149
            self.match(McFuncDSLParser.SEMI)
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
            return self.getToken(McFuncDSLParser.ID, 0)

        def primitiveType(self):
            return self.getTypedRuleContext(McFuncDSLParser.PrimitiveTypeContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_type

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

        localctx = McFuncDSLParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_type)
        try:
            self.state = 153
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [58]:
                self.enterOuterAlt(localctx, 1)
                self.state = 151
                self.match(McFuncDSLParser.ID)
                pass
            elif token in [9, 10, 11, 12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 152
                self.primitiveType()
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

    class TypeListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.TypeContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.TypeContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(McFuncDSLParser.COMMA)
            else:
                return self.getToken(McFuncDSLParser.COMMA, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_typeList

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterTypeList"):
                listener.enterTypeList(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitTypeList"):
                listener.exitTypeList(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTypeList"):
                return visitor.visitTypeList(self)
            else:
                return visitor.visitChildren(self)

    def typeList(self):

        localctx = McFuncDSLParser.TypeListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_typeList)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 155
            self.type_()
            self.state = 160
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 19:
                self.state = 156
                self.match(McFuncDSLParser.COMMA)
                self.state = 157
                self.type_()
                self.state = 162
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PrimitiveTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TYPE_INT(self):
            return self.getToken(McFuncDSLParser.TYPE_INT, 0)

        def TYPE_STRING(self):
            return self.getToken(McFuncDSLParser.TYPE_STRING, 0)

        def TYPE_BOOLEAN(self):
            return self.getToken(McFuncDSLParser.TYPE_BOOLEAN, 0)

        def TYPE_VOID(self):
            return self.getToken(McFuncDSLParser.TYPE_VOID, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_primitiveType

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterPrimitiveType"):
                listener.enterPrimitiveType(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitPrimitiveType"):
                listener.exitPrimitiveType(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitPrimitiveType"):
                return visitor.visitPrimitiveType(self)
            else:
                return visitor.visitChildren(self)

    def primitiveType(self):

        localctx = McFuncDSLParser.PrimitiveTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_primitiveType)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 163
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 7680) != 0)):
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
            return self.getToken(McFuncDSLParser.FUNC, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def block(self):
            return self.getTypedRuleContext(McFuncDSLParser.BlockContext, 0)

        def paramList(self):
            return self.getTypedRuleContext(McFuncDSLParser.ParamListContext, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.AnnotationContext, i)

        def ARROW(self):
            return self.getToken(McFuncDSLParser.ARROW, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_functionDecl

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

        localctx = McFuncDSLParser.FunctionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_functionDecl)
        self._la = 0  # Token type
        try:
            self.state = 191
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 16, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 168
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 165
                    self.annotation()
                    self.state = 170
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 171
                self.match(McFuncDSLParser.FUNC)
                self.state = 172
                self.match(McFuncDSLParser.ID)

                self.state = 173
                self.paramList()

                self.state = 174
                _la = self._input.LA(1)
                if not (_la == 2 or _la == 41):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 175
                self.type_()
                self.state = 177
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 182
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 179
                    self.annotation()
                    self.state = 184
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 185
                self.match(McFuncDSLParser.FUNC)
                self.state = 186
                self.type_()
                self.state = 187
                self.match(McFuncDSLParser.ID)

                self.state = 188
                self.paramList()
                self.state = 189
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
            return self.getToken(McFuncDSLParser.METHOD, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def paramList(self):
            return self.getTypedRuleContext(McFuncDSLParser.ParamListContext, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def block(self):
            return self.getTypedRuleContext(McFuncDSLParser.BlockContext, 0)

        def ARROW(self):
            return self.getToken(McFuncDSLParser.ARROW, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.AnnotationContext, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_methodDecl

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

        localctx = McFuncDSLParser.MethodDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_methodDecl)
        self._la = 0  # Token type
        try:
            self.state = 218
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 19, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 196
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 193
                    self.annotation()
                    self.state = 198
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 199
                self.match(McFuncDSLParser.METHOD)
                self.state = 200
                self.match(McFuncDSLParser.ID)
                self.state = 201
                self.paramList()
                self.state = 202
                _la = self._input.LA(1)
                if not (_la == 2 or _la == 41):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 203
                self.type_()
                self.state = 204
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 209
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 206
                    self.annotation()
                    self.state = 211
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 212
                self.match(McFuncDSLParser.METHOD)
                self.state = 213
                self.type_()
                self.state = 214
                self.match(McFuncDSLParser.ID)
                self.state = 215
                self.paramList()
                self.state = 216
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
            return self.getToken(McFuncDSLParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(McFuncDSLParser.RPAREN, 0)

        def paramDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ParamDeclContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ParamDeclContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(McFuncDSLParser.COMMA)
            else:
                return self.getToken(McFuncDSLParser.COMMA, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_paramList

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

        localctx = McFuncDSLParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_paramList)
        self._la = 0  # Token type
        try:
            self.state = 232
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [14]:
                self.enterOuterAlt(localctx, 1)
                self.state = 220
                self.match(McFuncDSLParser.LPAREN)

                self.state = 221
                self.paramDecl()
                self.state = 226
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 19:
                    self.state = 222
                    self.match(McFuncDSLParser.COMMA)
                    self.state = 223
                    self.paramDecl()
                    self.state = 228
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 229
                self.match(McFuncDSLParser.RPAREN)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 231
                self.match(McFuncDSLParser.T__2)
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
            return self.getToken(McFuncDSLParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_paramDecl

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

        localctx = McFuncDSLParser.ParamDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_paramDecl)
        try:
            self.state = 240
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 22, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 234
                self.match(McFuncDSLParser.ID)

                self.state = 235
                self.match(McFuncDSLParser.T__1)
                self.state = 236
                self.type_()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 237
                self.type_()
                self.state = 238
                self.match(McFuncDSLParser.ID)
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
            return self.getToken(McFuncDSLParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(McFuncDSLParser.RBRACE, 0)

        def statement(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.StatementContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.StatementContext, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_block

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

        localctx = McFuncDSLParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_block)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 242
            self.match(McFuncDSLParser.LBRACE)
            self.state = 246
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 540583546023140882) != 0):
                self.state = 243
                self.statement()
                self.state = 248
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 249
            self.match(McFuncDSLParser.RBRACE)
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

        def commandExpr(self):
            return self.getTypedRuleContext(McFuncDSLParser.CommandExprContext, 0)

        def SEMI(self):
            return self.getToken(McFuncDSLParser.SEMI, 0)

        def varDecl(self):
            return self.getTypedRuleContext(McFuncDSLParser.VarDeclContext, 0)

        def constDecl(self):
            return self.getTypedRuleContext(McFuncDSLParser.ConstDeclContext, 0)

        def forStmt(self):
            return self.getTypedRuleContext(McFuncDSLParser.ForStmtContext, 0)

        def whileStmt(self):
            return self.getTypedRuleContext(McFuncDSLParser.WhileStmtContext, 0)

        def assignment(self):
            return self.getTypedRuleContext(McFuncDSLParser.AssignmentContext, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def returnStmt(self):
            return self.getTypedRuleContext(McFuncDSLParser.ReturnStmtContext, 0)

        def block(self):
            return self.getTypedRuleContext(McFuncDSLParser.BlockContext, 0)

        def ifStmt(self):
            return self.getTypedRuleContext(McFuncDSLParser.IfStmtContext, 0)

        def breakStmt(self):
            return self.getTypedRuleContext(McFuncDSLParser.BreakStmtContext, 0)

        def continueStmt(self):
            return self.getTypedRuleContext(McFuncDSLParser.ContinueStmtContext, 0)

        def functionDecl(self):
            return self.getTypedRuleContext(McFuncDSLParser.FunctionDeclContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_statement

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

        localctx = McFuncDSLParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_statement)
        try:
            self.state = 276
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 24, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 251
                self.commandExpr()
                self.state = 252
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 254
                self.varDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 255
                self.constDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 256
                self.forStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 257
                self.whileStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 258
                self.assignment()
                self.state = 259
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 261
                self.expr(0)
                self.state = 262
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 264
                self.returnStmt()
                self.state = 265
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 267
                self.block()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 268
                self.ifStmt()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 269
                self.breakStmt()
                self.state = 270
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 272
                self.continueStmt()
                self.state = 273
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 275
                self.functionDecl()
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
            return self.getToken(McFuncDSLParser.BREAK, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_breakStmt

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

        localctx = McFuncDSLParser.BreakStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_breakStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 278
            self.match(McFuncDSLParser.BREAK)
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
            return self.getToken(McFuncDSLParser.CONTINUE, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_continueStmt

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

        localctx = McFuncDSLParser.ContinueStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_continueStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 280
            self.match(McFuncDSLParser.CONTINUE)
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
            return self.getToken(McFuncDSLParser.FOR, 0)

        def LPAREN(self):
            return self.getToken(McFuncDSLParser.LPAREN, 0)

        def forControl(self):
            return self.getTypedRuleContext(McFuncDSLParser.ForControlContext, 0)

        def RPAREN(self):
            return self.getToken(McFuncDSLParser.RPAREN, 0)

        def block(self):
            return self.getTypedRuleContext(McFuncDSLParser.BlockContext, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_forStmt

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

        localctx = McFuncDSLParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_forStmt)
        try:
            self.state = 296
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 25, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 282
                self.match(McFuncDSLParser.FOR)
                self.state = 283
                self.match(McFuncDSLParser.LPAREN)
                self.state = 284
                self.forControl()
                self.state = 285
                self.match(McFuncDSLParser.RPAREN)
                self.state = 286
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 288
                self.match(McFuncDSLParser.FOR)
                self.state = 289
                self.match(McFuncDSLParser.LPAREN)
                self.state = 290
                self.match(McFuncDSLParser.ID)
                self.state = 291
                self.match(McFuncDSLParser.T__1)
                self.state = 292
                self.expr(0)
                self.state = 293
                self.match(McFuncDSLParser.RPAREN)
                self.state = 294
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
                return self.getTokens(McFuncDSLParser.SEMI)
            else:
                return self.getToken(McFuncDSLParser.SEMI, i)

        def forLoopVarDecl(self):
            return self.getTypedRuleContext(McFuncDSLParser.ForLoopVarDeclContext, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def assignment(self):
            return self.getTypedRuleContext(McFuncDSLParser.AssignmentContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_forControl

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

        localctx = McFuncDSLParser.ForControlContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_forControl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 299
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230376285937152) != 0):
                self.state = 298
                self.forLoopVarDecl()

            self.state = 301
            self.match(McFuncDSLParser.SEMI)
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540581617714872320) != 0):
                self.state = 302
                self.expr(0)

            self.state = 305
            self.match(McFuncDSLParser.SEMI)
            self.state = 307
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 58:
                self.state = 306
                self.assignment()


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
            return self.getToken(McFuncDSLParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(McFuncDSLParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def RPAREN(self):
            return self.getToken(McFuncDSLParser.RPAREN, 0)

        def block(self):
            return self.getTypedRuleContext(McFuncDSLParser.BlockContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_whileStmt

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

        localctx = McFuncDSLParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 309
            self.match(McFuncDSLParser.WHILE)
            self.state = 310
            self.match(McFuncDSLParser.LPAREN)
            self.state = 311
            self.expr(0)
            self.state = 312
            self.match(McFuncDSLParser.RPAREN)
            self.state = 313
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

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def SEMI(self):
            return self.getToken(McFuncDSLParser.SEMI, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def ASSIGN(self):
            return self.getToken(McFuncDSLParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_constDecl

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

        localctx = McFuncDSLParser.ConstDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_constDecl)
        try:
            self.state = 333
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 29, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 315
                self.match(McFuncDSLParser.T__3)
                self.state = 316
                self.match(McFuncDSLParser.ID)

                self.state = 317
                self.match(McFuncDSLParser.T__1)
                self.state = 318
                self.type_()

                self.state = 320
                self.match(McFuncDSLParser.ASSIGN)
                self.state = 321
                self.expr(0)
                self.state = 323
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 325
                self.match(McFuncDSLParser.T__3)
                self.state = 326
                self.type_()
                self.state = 327
                self.match(McFuncDSLParser.ID)

                self.state = 328
                self.match(McFuncDSLParser.ASSIGN)
                self.state = 329
                self.expr(0)
                self.state = 331
                self.match(McFuncDSLParser.SEMI)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class VarDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def ASSIGN(self):
            return self.getToken(McFuncDSLParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_varDeclaration

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterVarDeclaration"):
                listener.enterVarDeclaration(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitVarDeclaration"):
                listener.exitVarDeclaration(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitVarDeclaration"):
                return visitor.visitVarDeclaration(self)
            else:
                return visitor.visitChildren(self)

    def varDeclaration(self):

        localctx = McFuncDSLParser.VarDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_varDeclaration)
        self._la = 0  # Token type
        try:
            self.state = 355
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 34, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 335
                self.match(McFuncDSLParser.ID)

                self.state = 336
                self.match(McFuncDSLParser.T__1)
                self.state = 337
                self.type_()
                self.state = 340
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 5:
                    self.state = 339
                    self.match(McFuncDSLParser.T__4)

                self.state = 344
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 54:
                    self.state = 342
                    self.match(McFuncDSLParser.ASSIGN)
                    self.state = 343
                    self.expr(0)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 346
                self.type_()
                self.state = 347
                self.match(McFuncDSLParser.ID)
                self.state = 349
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 5:
                    self.state = 348
                    self.match(McFuncDSLParser.T__4)

                self.state = 353
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 54:
                    self.state = 351
                    self.match(McFuncDSLParser.ASSIGN)
                    self.state = 352
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

        def VAR(self):
            return self.getToken(McFuncDSLParser.VAR, 0)

        def varDeclaration(self):
            return self.getTypedRuleContext(McFuncDSLParser.VarDeclarationContext, 0)

        def SEMI(self):
            return self.getToken(McFuncDSLParser.SEMI, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_varDecl

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

        localctx = McFuncDSLParser.VarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_varDecl)
        try:
            self.state = 364
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 357
                self.match(McFuncDSLParser.VAR)
                self.state = 358
                self.varDeclaration()
                self.state = 359
                self.match(McFuncDSLParser.SEMI)
                pass
            elif token in [9, 10, 11, 12, 58]:
                self.enterOuterAlt(localctx, 2)
                self.state = 361
                self.varDeclaration()
                self.state = 362
                self.match(McFuncDSLParser.SEMI)
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

    class ForLoopVarDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(McFuncDSLParser.VAR, 0)

        def varDeclaration(self):
            return self.getTypedRuleContext(McFuncDSLParser.VarDeclarationContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_forLoopVarDecl

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterForLoopVarDecl"):
                listener.enterForLoopVarDecl(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitForLoopVarDecl"):
                listener.exitForLoopVarDecl(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitForLoopVarDecl"):
                return visitor.visitForLoopVarDecl(self)
            else:
                return visitor.visitChildren(self)

    def forLoopVarDecl(self):

        localctx = McFuncDSLParser.ForLoopVarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_forLoopVarDecl)
        try:
            self.state = 369
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 366
                self.match(McFuncDSLParser.VAR)
                self.state = 367
                self.varDeclaration()
                pass
            elif token in [9, 10, 11, 12, 58]:
                self.enterOuterAlt(localctx, 2)
                self.state = 368
                self.varDeclaration()
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

    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(McFuncDSLParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_assignment

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAssignment"):
                listener.enterAssignment(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAssignment"):
                listener.exitAssignment(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAssignment"):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)

    def assignment(self):

        localctx = McFuncDSLParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 371
            self.match(McFuncDSLParser.ID)
            self.state = 372
            self.match(McFuncDSLParser.ASSIGN)
            self.state = 373
            self.expr(0)
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
            return self.getToken(McFuncDSLParser.RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_returnStmt

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

        localctx = McFuncDSLParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_returnStmt)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 375
            self.match(McFuncDSLParser.RETURN)
            self.state = 377
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540581617714872320) != 0):
                self.state = 376
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
            return self.getToken(McFuncDSLParser.IF, 0)

        def LPAREN(self):
            return self.getToken(McFuncDSLParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def RPAREN(self):
            return self.getToken(McFuncDSLParser.RPAREN, 0)

        def block(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.BlockContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.BlockContext, i)

        def ELSE(self):
            return self.getToken(McFuncDSLParser.ELSE, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_ifStmt

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

        localctx = McFuncDSLParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_ifStmt)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 379
            self.match(McFuncDSLParser.IF)
            self.state = 380
            self.match(McFuncDSLParser.LPAREN)
            self.state = 381
            self.expr(0)
            self.state = 382
            self.match(McFuncDSLParser.RPAREN)
            self.state = 383
            self.block()
            self.state = 386
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 32:
                self.state = 384
                self.match(McFuncDSLParser.ELSE)
                self.state = 385
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
            return McFuncDSLParser.RULE_expr

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class LogicalOrExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ExprContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ExprContext, i)

        def OR(self):
            return self.getToken(McFuncDSLParser.OR, 0)

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

    class DirectFuncCallContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def argumentList(self):
            return self.getTypedRuleContext(McFuncDSLParser.ArgumentListContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterDirectFuncCall"):
                listener.enterDirectFuncCall(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitDirectFuncCall"):
                listener.exitDirectFuncCall(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitDirectFuncCall"):
                return visitor.visitDirectFuncCall(self)
            else:
                return visitor.visitChildren(self)

    class MulDivExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ExprContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ExprContext, i)

        def MUL(self):
            return self.getToken(McFuncDSLParser.MUL, 0)

        def DIV(self):
            return self.getToken(McFuncDSLParser.DIV, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterMulDivExpr"):
                listener.enterMulDivExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitMulDivExpr"):
                listener.exitMulDivExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitMulDivExpr"):
                return visitor.visitMulDivExpr(self)
            else:
                return visitor.visitChildren(self)

    class MemberAccessContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

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

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ExprContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ExprContext, i)

        def GT(self):
            return self.getToken(McFuncDSLParser.GT, 0)

        def LT(self):
            return self.getToken(McFuncDSLParser.LT, 0)

        def EQ(self):
            return self.getToken(McFuncDSLParser.EQ, 0)

        def NEQ(self):
            return self.getToken(McFuncDSLParser.NEQ, 0)

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

    class NegExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SUB(self):
            return self.getToken(McFuncDSLParser.SUB, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

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

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(McFuncDSLParser.NOT, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

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

    class PrimaryExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def primary(self):
            return self.getTypedRuleContext(McFuncDSLParser.PrimaryContext, 0)

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

    class AddSubExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ExprContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ExprContext, i)

        def ADD(self):
            return self.getToken(McFuncDSLParser.ADD, 0)

        def SUB(self):
            return self.getToken(McFuncDSLParser.SUB, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAddSubExpr"):
                listener.enterAddSubExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAddSubExpr"):
                listener.exitAddSubExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitAddSubExpr"):
                return visitor.visitAddSubExpr(self)
            else:
                return visitor.visitChildren(self)

    class LogicalAndExprContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ExprContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ExprContext, i)

        def AND(self):
            return self.getToken(McFuncDSLParser.AND, 0)

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

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def argumentList(self):
            return self.getTypedRuleContext(McFuncDSLParser.ArgumentListContext, 0)

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

    def expr(self, _p: int = 0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = McFuncDSLParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 54
        self.enterRecursionRule(localctx, 54, self.RULE_expr, _p)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 396
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 39, self._ctx)
            if la_ == 1:
                localctx = McFuncDSLParser.DirectFuncCallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 389
                self.match(McFuncDSLParser.ID)
                self.state = 390
                self.argumentList()
                pass

            elif la_ == 2:
                localctx = McFuncDSLParser.PrimaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 391
                self.primary()
                pass

            elif la_ == 3:
                localctx = McFuncDSLParser.NegExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 392
                self.match(McFuncDSLParser.SUB)
                self.state = 393
                self.expr(7)
                pass

            elif la_ == 4:
                localctx = McFuncDSLParser.LogicalNotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 394
                self.match(McFuncDSLParser.NOT)
                self.state = 395
                self.expr(6)
                pass

            self._ctx.stop = self._input.LT(-1)
            self.state = 422
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 41, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 420
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 40, self._ctx)
                    if la_ == 1:
                        localctx = McFuncDSLParser.MulDivExprContext(self, McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 398
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 399
                        _la = self._input.LA(1)
                        if not (_la == 44 or _la == 45):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 400
                        self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = McFuncDSLParser.AddSubExprContext(self, McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 401
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 402
                        _la = self._input.LA(1)
                        if not (_la == 46 or _la == 47):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 403
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = McFuncDSLParser.CompareExprContext(self,
                                                                      McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                  _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 404
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 405
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 4222124650660224) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 406
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = McFuncDSLParser.LogicalAndExprContext(self,
                                                                         McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 407
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 408
                        self.match(McFuncDSLParser.AND)
                        self.state = 409
                        self.expr(3)
                        pass

                    elif la_ == 5:
                        localctx = McFuncDSLParser.LogicalOrExprContext(self,
                                                                        McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 410
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 411
                        self.match(McFuncDSLParser.OR)
                        self.state = 412
                        self.expr(2)
                        pass

                    elif la_ == 6:
                        localctx = McFuncDSLParser.MethodCallContext(self, McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 413
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 414
                        self.match(McFuncDSLParser.T__5)
                        self.state = 415
                        self.match(McFuncDSLParser.ID)
                        self.state = 416
                        self.argumentList()
                        pass

                    elif la_ == 7:
                        localctx = McFuncDSLParser.MemberAccessContext(self,
                                                                       McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 417
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 418
                        self.match(McFuncDSLParser.T__5)
                        self.state = 419
                        self.match(McFuncDSLParser.ID)
                        pass

                self.state = 424
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 41, self._ctx)

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
            return McFuncDSLParser.RULE_primary

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class NewObjectExprContext(PrimaryContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NEW(self):
            return self.getToken(McFuncDSLParser.NEW, 0)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def argumentList(self):
            return self.getTypedRuleContext(McFuncDSLParser.ArgumentListContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNewObjectExpr"):
                listener.enterNewObjectExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNewObjectExpr"):
                listener.exitNewObjectExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitNewObjectExpr"):
                return visitor.visitNewObjectExpr(self)
            else:
                return visitor.visitChildren(self)

    class VarExprContext(PrimaryContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(McFuncDSLParser.ID, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterVarExpr"):
                listener.enterVarExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitVarExpr"):
                listener.exitVarExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitVarExpr"):
                return visitor.visitVarExpr(self)
            else:
                return visitor.visitChildren(self)

    class LiteralExprContext(PrimaryContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(McFuncDSLParser.LiteralContext, 0)

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

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(McFuncDSLParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def RPAREN(self):
            return self.getToken(McFuncDSLParser.RPAREN, 0)

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

    class TypeCastExprContext(PrimaryContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a McFuncDSLParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(McFuncDSLParser.LPAREN, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def RPAREN(self):
            return self.getToken(McFuncDSLParser.RPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterTypeCastExpr"):
                listener.enterTypeCastExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitTypeCastExpr"):
                listener.exitTypeCastExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitTypeCastExpr"):
                return visitor.visitTypeCastExpr(self)
            else:
                return visitor.visitChildren(self)

    def primary(self):

        localctx = McFuncDSLParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_primary)
        try:
            self.state = 439
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 42, self._ctx)
            if la_ == 1:
                localctx = McFuncDSLParser.VarExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 425
                self.match(McFuncDSLParser.ID)
                pass

            elif la_ == 2:
                localctx = McFuncDSLParser.LiteralExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 426
                self.literal()
                pass

            elif la_ == 3:
                localctx = McFuncDSLParser.ParenExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 427
                self.match(McFuncDSLParser.LPAREN)
                self.state = 428
                self.expr(0)
                self.state = 429
                self.match(McFuncDSLParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = McFuncDSLParser.NewObjectExprContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 431
                self.match(McFuncDSLParser.NEW)
                self.state = 432
                self.match(McFuncDSLParser.ID)
                self.state = 433
                self.argumentList()
                pass

            elif la_ == 5:
                localctx = McFuncDSLParser.TypeCastExprContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 434
                self.match(McFuncDSLParser.LPAREN)
                self.state = 435
                self.type_()
                self.state = 436
                self.match(McFuncDSLParser.RPAREN)
                self.state = 437
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CommandExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CMD(self):
            return self.getToken(McFuncDSLParser.CMD, 0)

        def argumentList(self):
            return self.getTypedRuleContext(McFuncDSLParser.ArgumentListContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_commandExpr

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCommandExpr"):
                listener.enterCommandExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCommandExpr"):
                listener.exitCommandExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCommandExpr"):
                return visitor.visitCommandExpr(self)
            else:
                return visitor.visitChildren(self)

    def commandExpr(self):

        localctx = McFuncDSLParser.CommandExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_commandExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 441
            self.match(McFuncDSLParser.CMD)
            self.state = 442
            self.argumentList()
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
            return self.getToken(McFuncDSLParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(McFuncDSLParser.RPAREN, 0)

        def exprList(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprListContext, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_argumentList

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

        localctx = McFuncDSLParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_argumentList)
        self._la = 0  # Token type
        try:
            self.state = 450
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [14]:
                self.enterOuterAlt(localctx, 1)
                self.state = 444
                self.match(McFuncDSLParser.LPAREN)
                self.state = 446
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540581617714872320) != 0):
                    self.state = 445
                    self.exprList()

                self.state = 448
                self.match(McFuncDSLParser.RPAREN)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 449
                self.match(McFuncDSLParser.T__2)
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
                return self.getTypedRuleContexts(McFuncDSLParser.ExprContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ExprContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(McFuncDSLParser.COMMA)
            else:
                return self.getToken(McFuncDSLParser.COMMA, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_exprList

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

        localctx = McFuncDSLParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_exprList)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 452
            self.expr(0)
            self.state = 457
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 19:
                self.state = 453
                self.match(McFuncDSLParser.COMMA)
                self.state = 454
                self.expr(0)
                self.state = 459
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
            return self.getToken(McFuncDSLParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(McFuncDSLParser.STRING, 0)

        def FSTRING(self):
            return self.getToken(McFuncDSLParser.FSTRING, 0)

        def TRUE(self):
            return self.getToken(McFuncDSLParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(McFuncDSLParser.FALSE, 0)

        def NULL(self):
            return self.getToken(McFuncDSLParser.NULL, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_literal

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

        localctx = McFuncDSLParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_literal)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 460
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 252201699391832064) != 0)):
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
        self._predicates[27] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx: ExprContext, predIndex: int):
        if predIndex == 0:
            return self.precpred(self._ctx, 5)

        if predIndex == 1:
            return self.precpred(self._ctx, 4)

        if predIndex == 2:
            return self.precpred(self._ctx, 3)

        if predIndex == 3:
            return self.precpred(self._ctx, 2)

        if predIndex == 4:
            return self.precpred(self._ctx, 1)

        if predIndex == 5:
            return self.precpred(self._ctx, 11)

        if predIndex == 6:
            return self.precpred(self._ctx, 10)
