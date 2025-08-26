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
        4, 1, 58, 469, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7,
        6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13,
        2, 14, 7, 14, 2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20,
        7, 20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26,
        2, 27, 7, 27, 2, 28, 7, 28, 1, 0, 5, 0, 60, 8, 0, 10, 0, 12, 0, 63, 9, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 5, 0, 70, 8, 0, 10, 0, 12, 0, 73, 9, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 3, 1, 80, 8,
        1, 1, 2, 1, 2, 1, 2, 1, 3, 5, 3, 86, 8, 3, 10, 3, 12, 3, 89, 9, 3, 1, 3, 1, 3, 1, 3, 1, 3, 3,
        3, 95, 8, 3, 1, 3, 1, 3, 3, 3, 99, 8, 3, 1, 3, 1, 3, 1, 3, 1, 3, 5, 3, 105, 8, 3, 10, 3, 12,
        3, 108, 9, 3, 1, 3, 1, 3, 1, 4, 5, 4, 113, 8, 4, 10, 4, 12, 4, 116, 9, 4, 1, 4, 1, 4, 1, 4,
        1, 4, 3, 4, 122, 8, 4, 1, 4, 1, 4, 5, 4, 126, 8, 4, 10, 4, 12, 4, 129, 9, 4, 1, 4, 1, 4, 1,
        5, 1, 5, 1, 5, 1, 5, 1, 5, 5, 5, 138, 8, 5, 10, 5, 12, 5, 141, 9, 5, 1, 5, 3, 5, 144, 8, 5,
        1, 5, 3, 5, 147, 8, 5, 1, 6, 5, 6, 150, 8, 6, 10, 6, 12, 6, 153, 9, 6, 1, 6, 1, 6, 1, 6, 1,
        6, 1, 6, 3, 6, 160, 8, 6, 1, 6, 1, 6, 1, 6, 5, 6, 165, 8, 6, 10, 6, 12, 6, 168, 9, 6, 1, 6,
        1, 6, 3, 6, 172, 8, 6, 1, 6, 1, 6, 1, 6, 1, 6, 3, 6, 178, 8, 6, 1, 7, 5, 7, 181, 8, 7, 10, 7,
        12, 7, 184, 9, 7, 1, 7, 1, 7, 1, 7, 1, 7, 1, 7, 3, 7, 191, 8, 7, 1, 7, 1, 7, 1, 7, 5, 7, 196,
        8, 7, 10, 7, 12, 7, 199, 9, 7, 1, 7, 1, 7, 3, 7, 203, 8, 7, 1, 7, 1, 7, 1, 7, 1, 7, 3, 7, 209,
        8, 7, 1, 8, 1, 8, 1, 8, 1, 8, 5, 8, 215, 8, 8, 10, 8, 12, 8, 218, 9, 8, 3, 8, 220, 8, 8, 1,
        8, 1, 8, 3, 8, 224, 8, 8, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 3, 9, 232, 8, 9, 1, 10, 1, 10,
        5, 10, 236, 8, 10, 10, 10, 12, 10, 239, 9, 10, 1, 10, 1, 10, 3, 10, 243, 8, 10, 1, 11,
        1, 11, 1, 11, 1, 11, 1, 11, 1, 11, 1, 11, 3, 11, 252, 8, 11, 1, 11, 1, 11, 3, 11, 256, 8,
        11, 1, 11, 1, 11, 3, 11, 260, 8, 11, 1, 11, 1, 11, 1, 11, 1, 11, 3, 11, 266, 8, 11, 1, 11,
        1, 11, 3, 11, 270, 8, 11, 3, 11, 272, 8, 11, 1, 12, 1, 12, 1, 13, 1, 13, 1, 14, 1, 14, 1,
        14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 3,
        14, 293, 8, 14, 1, 15, 3, 15, 296, 8, 15, 1, 15, 1, 15, 3, 15, 300, 8, 15, 1, 15, 1, 15,
        3, 15, 304, 8, 15, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 17, 1, 17, 1, 17, 1, 17,
        3, 17, 316, 8, 17, 1, 17, 3, 17, 319, 8, 17, 1, 17, 1, 17, 1, 17, 1, 17, 3, 17, 325, 8,
        17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 3, 17, 334, 8, 17, 3, 17, 336, 8, 17,
        1, 18, 1, 18, 1, 18, 3, 18, 341, 8, 18, 1, 18, 1, 18, 1, 18, 1, 18, 1, 18, 1, 18, 1, 18,
        3, 18, 350, 8, 18, 1, 18, 1, 18, 3, 18, 354, 8, 18, 1, 18, 1, 18, 1, 18, 3, 18, 359, 8,
        18, 1, 18, 1, 18, 3, 18, 363, 8, 18, 1, 18, 1, 18, 1, 18, 3, 18, 368, 8, 18, 1, 18, 1, 18,
        1, 18, 1, 18, 1, 18, 1, 18, 3, 18, 376, 8, 18, 1, 19, 1, 19, 3, 19, 380, 8, 19, 1, 20, 1,
        20, 1, 21, 1, 21, 1, 21, 1, 21, 1, 22, 1, 22, 3, 22, 390, 8, 22, 1, 23, 1, 23, 1, 23, 1,
        23, 1, 23, 1, 23, 1, 23, 3, 23, 399, 8, 23, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 3,
        24, 407, 8, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1,
        24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 1,
        24, 1, 24, 1, 24, 1, 24, 1, 24, 1, 24, 5, 24, 438, 8, 24, 10, 24, 12, 24, 441, 9, 24, 1,
        25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 3, 25, 449, 8, 25, 1, 26, 1, 26, 3, 26, 453, 8, 26,
        1, 26, 1, 26, 3, 26, 457, 8, 26, 1, 27, 1, 27, 1, 27, 5, 27, 462, 8, 27, 10, 27, 12, 27,
        465, 9, 27, 1, 28, 1, 28, 1, 28, 0, 1, 48, 29, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22,
        24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 0, 4, 1, 0, 37, 39,
        1, 0, 40, 41, 1, 0, 42, 47, 2, 0, 30, 32, 51, 53, 527, 0, 61, 1, 0, 0, 0, 2, 76, 1, 0, 0,
        0, 4, 81, 1, 0, 0, 0, 6, 87, 1, 0, 0, 0, 8, 114, 1, 0, 0, 0, 10, 146, 1, 0, 0, 0, 12, 177,
        1, 0, 0, 0, 14, 208, 1, 0, 0, 0, 16, 223, 1, 0, 0, 0, 18, 231, 1, 0, 0, 0, 20, 242, 1, 0,
        0, 0, 22, 271, 1, 0, 0, 0, 24, 273, 1, 0, 0, 0, 26, 275, 1, 0, 0, 0, 28, 292, 1, 0, 0, 0,
        30, 295, 1, 0, 0, 0, 32, 305, 1, 0, 0, 0, 34, 335, 1, 0, 0, 0, 36, 375, 1, 0, 0, 0, 38, 377,
        1, 0, 0, 0, 40, 381, 1, 0, 0, 0, 42, 383, 1, 0, 0, 0, 44, 387, 1, 0, 0, 0, 46, 391, 1, 0,
        0, 0, 48, 406, 1, 0, 0, 0, 50, 448, 1, 0, 0, 0, 52, 456, 1, 0, 0, 0, 54, 458, 1, 0, 0, 0,
        56, 466, 1, 0, 0, 0, 58, 60, 3, 2, 1, 0, 59, 58, 1, 0, 0, 0, 60, 63, 1, 0, 0, 0, 61, 59, 1,
        0, 0, 0, 61, 62, 1, 0, 0, 0, 62, 71, 1, 0, 0, 0, 63, 61, 1, 0, 0, 0, 64, 70, 3, 6, 3, 0, 65,
        70, 3, 8, 4, 0, 66, 70, 3, 12, 6, 0, 67, 70, 3, 38, 19, 0, 68, 70, 3, 34, 17, 0, 69, 64,
        1, 0, 0, 0, 69, 65, 1, 0, 0, 0, 69, 66, 1, 0, 0, 0, 69, 67, 1, 0, 0, 0, 69, 68, 1, 0, 0, 0,
        70, 73, 1, 0, 0, 0, 71, 69, 1, 0, 0, 0, 71, 72, 1, 0, 0, 0, 72, 74, 1, 0, 0, 0, 73, 71, 1,
        0, 0, 0, 74, 75, 5, 0, 0, 1, 75, 1, 1, 0, 0, 0, 76, 77, 5, 15, 0, 0, 77, 79, 3, 56, 28, 0,
        78, 80, 5, 11, 0, 0, 79, 78, 1, 0, 0, 0, 79, 80, 1, 0, 0, 0, 80, 3, 1, 0, 0, 0, 81, 82, 5,
        1, 0, 0, 82, 83, 5, 54, 0, 0, 83, 5, 1, 0, 0, 0, 84, 86, 3, 4, 2, 0, 85, 84, 1, 0, 0, 0, 86,
        89, 1, 0, 0, 0, 87, 85, 1, 0, 0, 0, 87, 88, 1, 0, 0, 0, 88, 90, 1, 0, 0, 0, 89, 87, 1, 0, 0,
        0, 90, 91, 5, 18, 0, 0, 91, 94, 5, 54, 0, 0, 92, 93, 5, 20, 0, 0, 93, 95, 3, 10, 5, 0, 94,
        92, 1, 0, 0, 0, 94, 95, 1, 0, 0, 0, 95, 98, 1, 0, 0, 0, 96, 97, 5, 21, 0, 0, 97, 99, 3, 10,
        5, 0, 98, 96, 1, 0, 0, 0, 98, 99, 1, 0, 0, 0, 99, 100, 1, 0, 0, 0, 100, 106, 5, 9, 0, 0, 101,
        105, 3, 38, 19, 0, 102, 105, 3, 34, 17, 0, 103, 105, 3, 14, 7, 0, 104, 101, 1, 0, 0, 0,
        104, 102, 1, 0, 0, 0, 104, 103, 1, 0, 0, 0, 105, 108, 1, 0, 0, 0, 106, 104, 1, 0, 0, 0,
        106, 107, 1, 0, 0, 0, 107, 109, 1, 0, 0, 0, 108, 106, 1, 0, 0, 0, 109, 110, 5, 10, 0, 0,
        110, 7, 1, 0, 0, 0, 111, 113, 3, 4, 2, 0, 112, 111, 1, 0, 0, 0, 113, 116, 1, 0, 0, 0, 114,
        112, 1, 0, 0, 0, 114, 115, 1, 0, 0, 0, 115, 117, 1, 0, 0, 0, 116, 114, 1, 0, 0, 0, 117,
        118, 5, 19, 0, 0, 118, 121, 5, 54, 0, 0, 119, 120, 5, 20, 0, 0, 120, 122, 3, 10, 5, 0,
        121, 119, 1, 0, 0, 0, 121, 122, 1, 0, 0, 0, 122, 123, 1, 0, 0, 0, 123, 127, 5, 9, 0, 0,
        124, 126, 3, 14, 7, 0, 125, 124, 1, 0, 0, 0, 126, 129, 1, 0, 0, 0, 127, 125, 1, 0, 0, 0,
        127, 128, 1, 0, 0, 0, 128, 130, 1, 0, 0, 0, 129, 127, 1, 0, 0, 0, 130, 131, 5, 10, 0, 0,
        131, 9, 1, 0, 0, 0, 132, 143, 5, 54, 0, 0, 133, 139, 5, 2, 0, 0, 134, 135, 3, 10, 5, 0,
        135, 136, 5, 12, 0, 0, 136, 138, 1, 0, 0, 0, 137, 134, 1, 0, 0, 0, 138, 141, 1, 0, 0, 0,
        139, 137, 1, 0, 0, 0, 139, 140, 1, 0, 0, 0, 140, 142, 1, 0, 0, 0, 141, 139, 1, 0, 0, 0,
        142, 144, 5, 3, 0, 0, 143, 133, 1, 0, 0, 0, 143, 144, 1, 0, 0, 0, 144, 147, 1, 0, 0, 0,
        145, 147, 5, 32, 0, 0, 146, 132, 1, 0, 0, 0, 146, 145, 1, 0, 0, 0, 147, 11, 1, 0, 0, 0,
        148, 150, 3, 4, 2, 0, 149, 148, 1, 0, 0, 0, 150, 153, 1, 0, 0, 0, 151, 149, 1, 0, 0, 0,
        151, 152, 1, 0, 0, 0, 152, 154, 1, 0, 0, 0, 153, 151, 1, 0, 0, 0, 154, 155, 5, 16, 0, 0,
        155, 156, 5, 54, 0, 0, 156, 159, 3, 16, 8, 0, 157, 158, 5, 13, 0, 0, 158, 160, 3, 10,
        5, 0, 159, 157, 1, 0, 0, 0, 159, 160, 1, 0, 0, 0, 160, 161, 1, 0, 0, 0, 161, 162, 3, 20,
        10, 0, 162, 178, 1, 0, 0, 0, 163, 165, 3, 4, 2, 0, 164, 163, 1, 0, 0, 0, 165, 168, 1, 0,
        0, 0, 166, 164, 1, 0, 0, 0, 166, 167, 1, 0, 0, 0, 167, 169, 1, 0, 0, 0, 168, 166, 1, 0,
        0, 0, 169, 171, 5, 16, 0, 0, 170, 172, 3, 10, 5, 0, 171, 170, 1, 0, 0, 0, 171, 172, 1,
        0, 0, 0, 172, 173, 1, 0, 0, 0, 173, 174, 5, 54, 0, 0, 174, 175, 3, 16, 8, 0, 175, 176,
        3, 20, 10, 0, 176, 178, 1, 0, 0, 0, 177, 151, 1, 0, 0, 0, 177, 166, 1, 0, 0, 0, 178, 13,
        1, 0, 0, 0, 179, 181, 3, 4, 2, 0, 180, 179, 1, 0, 0, 0, 181, 184, 1, 0, 0, 0, 182, 180,
        1, 0, 0, 0, 182, 183, 1, 0, 0, 0, 183, 185, 1, 0, 0, 0, 184, 182, 1, 0, 0, 0, 185, 186,
        5, 17, 0, 0, 186, 187, 5, 54, 0, 0, 187, 190, 3, 16, 8, 0, 188, 189, 5, 13, 0, 0, 189,
        191, 3, 10, 5, 0, 190, 188, 1, 0, 0, 0, 190, 191, 1, 0, 0, 0, 191, 192, 1, 0, 0, 0, 192,
        193, 3, 20, 10, 0, 193, 209, 1, 0, 0, 0, 194, 196, 3, 4, 2, 0, 195, 194, 1, 0, 0, 0, 196,
        199, 1, 0, 0, 0, 197, 195, 1, 0, 0, 0, 197, 198, 1, 0, 0, 0, 198, 200, 1, 0, 0, 0, 199,
        197, 1, 0, 0, 0, 200, 202, 5, 17, 0, 0, 201, 203, 3, 10, 5, 0, 202, 201, 1, 0, 0, 0, 202,
        203, 1, 0, 0, 0, 203, 204, 1, 0, 0, 0, 204, 205, 5, 54, 0, 0, 205, 206, 3, 16, 8, 0, 206,
        207, 3, 20, 10, 0, 207, 209, 1, 0, 0, 0, 208, 182, 1, 0, 0, 0, 208, 197, 1, 0, 0, 0, 209,
        15, 1, 0, 0, 0, 210, 219, 5, 7, 0, 0, 211, 216, 3, 18, 9, 0, 212, 213, 5, 12, 0, 0, 213,
        215, 3, 18, 9, 0, 214, 212, 1, 0, 0, 0, 215, 218, 1, 0, 0, 0, 216, 214, 1, 0, 0, 0, 216,
        217, 1, 0, 0, 0, 217, 220, 1, 0, 0, 0, 218, 216, 1, 0, 0, 0, 219, 211, 1, 0, 0, 0, 219,
        220, 1, 0, 0, 0, 220, 221, 1, 0, 0, 0, 221, 224, 5, 8, 0, 0, 222, 224, 5, 6, 0, 0, 223,
        210, 1, 0, 0, 0, 223, 222, 1, 0, 0, 0, 224, 17, 1, 0, 0, 0, 225, 226, 5, 54, 0, 0, 226,
        227, 5, 13, 0, 0, 227, 232, 3, 10, 5, 0, 228, 229, 3, 10, 5, 0, 229, 230, 5, 54, 0, 0,
        230, 232, 1, 0, 0, 0, 231, 225, 1, 0, 0, 0, 231, 228, 1, 0, 0, 0, 232, 19, 1, 0, 0, 0, 233,
        237, 5, 9, 0, 0, 234, 236, 3, 22, 11, 0, 235, 234, 1, 0, 0, 0, 236, 239, 1, 0, 0, 0, 237,
        235, 1, 0, 0, 0, 237, 238, 1, 0, 0, 0, 238, 240, 1, 0, 0, 0, 239, 237, 1, 0, 0, 0, 240,
        243, 5, 10, 0, 0, 241, 243, 5, 11, 0, 0, 242, 233, 1, 0, 0, 0, 242, 241, 1, 0, 0, 0, 243,
        21, 1, 0, 0, 0, 244, 272, 3, 12, 6, 0, 245, 272, 3, 38, 19, 0, 246, 272, 3, 34, 17, 0,
        247, 272, 3, 28, 14, 0, 248, 272, 3, 32, 16, 0, 249, 251, 3, 42, 21, 0, 250, 252, 5,
        11, 0, 0, 251, 250, 1, 0, 0, 0, 251, 252, 1, 0, 0, 0, 252, 272, 1, 0, 0, 0, 253, 255, 3,
        48, 24, 0, 254, 256, 5, 11, 0, 0, 255, 254, 1, 0, 0, 0, 255, 256, 1, 0, 0, 0, 256, 272,
        1, 0, 0, 0, 257, 259, 3, 44, 22, 0, 258, 260, 5, 11, 0, 0, 259, 258, 1, 0, 0, 0, 259, 260,
        1, 0, 0, 0, 260, 272, 1, 0, 0, 0, 261, 272, 3, 20, 10, 0, 262, 272, 3, 46, 23, 0, 263,
        265, 3, 24, 12, 0, 264, 266, 5, 11, 0, 0, 265, 264, 1, 0, 0, 0, 265, 266, 1, 0, 0, 0, 266,
        272, 1, 0, 0, 0, 267, 269, 3, 26, 13, 0, 268, 270, 5, 11, 0, 0, 269, 268, 1, 0, 0, 0, 269,
        270, 1, 0, 0, 0, 270, 272, 1, 0, 0, 0, 271, 244, 1, 0, 0, 0, 271, 245, 1, 0, 0, 0, 271,
        246, 1, 0, 0, 0, 271, 247, 1, 0, 0, 0, 271, 248, 1, 0, 0, 0, 271, 249, 1, 0, 0, 0, 271,
        253, 1, 0, 0, 0, 271, 257, 1, 0, 0, 0, 271, 261, 1, 0, 0, 0, 271, 262, 1, 0, 0, 0, 271,
        263, 1, 0, 0, 0, 271, 267, 1, 0, 0, 0, 272, 23, 1, 0, 0, 0, 273, 274, 5, 34, 0, 0, 274,
        25, 1, 0, 0, 0, 275, 276, 5, 35, 0, 0, 276, 27, 1, 0, 0, 0, 277, 278, 5, 25, 0, 0, 278,
        279, 5, 7, 0, 0, 279, 280, 3, 30, 15, 0, 280, 281, 5, 8, 0, 0, 281, 282, 3, 20, 10, 0,
        282, 293, 1, 0, 0, 0, 283, 284, 5, 25, 0, 0, 284, 285, 5, 7, 0, 0, 285, 286, 3, 10, 5,
        0, 286, 287, 5, 54, 0, 0, 287, 288, 5, 13, 0, 0, 288, 289, 3, 48, 24, 0, 289, 290, 5,
        8, 0, 0, 290, 291, 3, 20, 10, 0, 291, 293, 1, 0, 0, 0, 292, 277, 1, 0, 0, 0, 292, 283,
        1, 0, 0, 0, 293, 29, 1, 0, 0, 0, 294, 296, 3, 40, 20, 0, 295, 294, 1, 0, 0, 0, 295, 296,
        1, 0, 0, 0, 296, 297, 1, 0, 0, 0, 297, 299, 5, 11, 0, 0, 298, 300, 3, 48, 24, 0, 299, 298,
        1, 0, 0, 0, 299, 300, 1, 0, 0, 0, 300, 301, 1, 0, 0, 0, 301, 303, 5, 11, 0, 0, 302, 304,
        3, 42, 21, 0, 303, 302, 1, 0, 0, 0, 303, 304, 1, 0, 0, 0, 304, 31, 1, 0, 0, 0, 305, 306,
        5, 26, 0, 0, 306, 307, 5, 7, 0, 0, 307, 308, 3, 48, 24, 0, 308, 309, 5, 8, 0, 0, 309, 310,
        3, 20, 10, 0, 310, 33, 1, 0, 0, 0, 311, 312, 5, 22, 0, 0, 312, 315, 5, 54, 0, 0, 313, 314,
        5, 13, 0, 0, 314, 316, 3, 10, 5, 0, 315, 313, 1, 0, 0, 0, 315, 316, 1, 0, 0, 0, 316, 318,
        1, 0, 0, 0, 317, 319, 5, 4, 0, 0, 318, 317, 1, 0, 0, 0, 318, 319, 1, 0, 0, 0, 319, 320,
        1, 0, 0, 0, 320, 321, 5, 50, 0, 0, 321, 322, 3, 48, 24, 0, 322, 324, 1, 0, 0, 0, 323, 325,
        5, 11, 0, 0, 324, 323, 1, 0, 0, 0, 324, 325, 1, 0, 0, 0, 325, 336, 1, 0, 0, 0, 326, 327,
        5, 22, 0, 0, 327, 328, 3, 10, 5, 0, 328, 329, 5, 54, 0, 0, 329, 330, 5, 50, 0, 0, 330,
        331, 3, 48, 24, 0, 331, 333, 1, 0, 0, 0, 332, 334, 5, 11, 0, 0, 333, 332, 1, 0, 0, 0, 333,
        334, 1, 0, 0, 0, 334, 336, 1, 0, 0, 0, 335, 311, 1, 0, 0, 0, 335, 326, 1, 0, 0, 0, 336,
        35, 1, 0, 0, 0, 337, 338, 5, 23, 0, 0, 338, 340, 5, 54, 0, 0, 339, 341, 5, 4, 0, 0, 340,
        339, 1, 0, 0, 0, 340, 341, 1, 0, 0, 0, 341, 342, 1, 0, 0, 0, 342, 343, 5, 50, 0, 0, 343,
        376, 3, 48, 24, 0, 344, 345, 5, 54, 0, 0, 345, 346, 5, 13, 0, 0, 346, 347, 3, 10, 5, 0,
        347, 349, 1, 0, 0, 0, 348, 350, 5, 4, 0, 0, 349, 348, 1, 0, 0, 0, 349, 350, 1, 0, 0, 0,
        350, 353, 1, 0, 0, 0, 351, 352, 5, 50, 0, 0, 352, 354, 3, 48, 24, 0, 353, 351, 1, 0, 0,
        0, 353, 354, 1, 0, 0, 0, 354, 376, 1, 0, 0, 0, 355, 356, 3, 10, 5, 0, 356, 358, 5, 54,
        0, 0, 357, 359, 5, 4, 0, 0, 358, 357, 1, 0, 0, 0, 358, 359, 1, 0, 0, 0, 359, 362, 1, 0,
        0, 0, 360, 361, 5, 50, 0, 0, 361, 363, 3, 48, 24, 0, 362, 360, 1, 0, 0, 0, 362, 363, 1,
        0, 0, 0, 363, 376, 1, 0, 0, 0, 364, 365, 5, 23, 0, 0, 365, 367, 5, 54, 0, 0, 366, 368,
        5, 4, 0, 0, 367, 366, 1, 0, 0, 0, 367, 368, 1, 0, 0, 0, 368, 369, 1, 0, 0, 0, 369, 370,
        5, 13, 0, 0, 370, 371, 3, 10, 5, 0, 371, 372, 1, 0, 0, 0, 372, 373, 5, 50, 0, 0, 373, 374,
        3, 48, 24, 0, 374, 376, 1, 0, 0, 0, 375, 337, 1, 0, 0, 0, 375, 344, 1, 0, 0, 0, 375, 355,
        1, 0, 0, 0, 375, 364, 1, 0, 0, 0, 376, 37, 1, 0, 0, 0, 377, 379, 3, 36, 18, 0, 378, 380,
        5, 11, 0, 0, 379, 378, 1, 0, 0, 0, 379, 380, 1, 0, 0, 0, 380, 39, 1, 0, 0, 0, 381, 382,
        3, 36, 18, 0, 382, 41, 1, 0, 0, 0, 383, 384, 5, 54, 0, 0, 384, 385, 5, 50, 0, 0, 385, 386,
        3, 48, 24, 0, 386, 43, 1, 0, 0, 0, 387, 389, 5, 24, 0, 0, 388, 390, 3, 48, 24, 0, 389,
        388, 1, 0, 0, 0, 389, 390, 1, 0, 0, 0, 390, 45, 1, 0, 0, 0, 391, 392, 5, 27, 0, 0, 392,
        393, 5, 7, 0, 0, 393, 394, 3, 48, 24, 0, 394, 395, 5, 8, 0, 0, 395, 398, 3, 20, 10, 0,
        396, 397, 5, 28, 0, 0, 397, 399, 3, 20, 10, 0, 398, 396, 1, 0, 0, 0, 398, 399, 1, 0, 0,
        0, 399, 47, 1, 0, 0, 0, 400, 401, 6, 24, -1, 0, 401, 407, 3, 50, 25, 0, 402, 403, 5, 41,
        0, 0, 403, 407, 3, 48, 24, 7, 404, 405, 5, 36, 0, 0, 405, 407, 3, 48, 24, 6, 406, 400,
        1, 0, 0, 0, 406, 402, 1, 0, 0, 0, 406, 404, 1, 0, 0, 0, 407, 439, 1, 0, 0, 0, 408, 409,
        10, 5, 0, 0, 409, 410, 7, 0, 0, 0, 410, 438, 3, 48, 24, 6, 411, 412, 10, 4, 0, 0, 412,
        413, 7, 1, 0, 0, 413, 438, 3, 48, 24, 5, 414, 415, 10, 3, 0, 0, 415, 416, 7, 2, 0, 0, 416,
        438, 3, 48, 24, 4, 417, 418, 10, 2, 0, 0, 418, 419, 5, 48, 0, 0, 419, 438, 3, 48, 24,
        3, 420, 421, 10, 1, 0, 0, 421, 422, 5, 49, 0, 0, 422, 438, 3, 48, 24, 2, 423, 424, 10,
        12, 0, 0, 424, 425, 5, 5, 0, 0, 425, 426, 5, 54, 0, 0, 426, 438, 3, 52, 26, 0, 427, 428,
        10, 11, 0, 0, 428, 429, 5, 5, 0, 0, 429, 438, 5, 54, 0, 0, 430, 431, 10, 10, 0, 0, 431,
        432, 5, 2, 0, 0, 432, 433, 3, 48, 24, 0, 433, 434, 5, 3, 0, 0, 434, 438, 1, 0, 0, 0, 435,
        436, 10, 9, 0, 0, 436, 438, 3, 52, 26, 0, 437, 408, 1, 0, 0, 0, 437, 411, 1, 0, 0, 0, 437,
        414, 1, 0, 0, 0, 437, 417, 1, 0, 0, 0, 437, 420, 1, 0, 0, 0, 437, 423, 1, 0, 0, 0, 437,
        427, 1, 0, 0, 0, 437, 430, 1, 0, 0, 0, 437, 435, 1, 0, 0, 0, 438, 441, 1, 0, 0, 0, 439,
        437, 1, 0, 0, 0, 439, 440, 1, 0, 0, 0, 440, 49, 1, 0, 0, 0, 441, 439, 1, 0, 0, 0, 442, 449,
        5, 54, 0, 0, 443, 449, 3, 56, 28, 0, 444, 445, 5, 7, 0, 0, 445, 446, 3, 48, 24, 0, 446,
        447, 5, 8, 0, 0, 447, 449, 1, 0, 0, 0, 448, 442, 1, 0, 0, 0, 448, 443, 1, 0, 0, 0, 448,
        444, 1, 0, 0, 0, 449, 51, 1, 0, 0, 0, 450, 452, 5, 7, 0, 0, 451, 453, 3, 54, 27, 0, 452,
        451, 1, 0, 0, 0, 452, 453, 1, 0, 0, 0, 453, 454, 1, 0, 0, 0, 454, 457, 5, 8, 0, 0, 455,
        457, 5, 6, 0, 0, 456, 450, 1, 0, 0, 0, 456, 455, 1, 0, 0, 0, 457, 53, 1, 0, 0, 0, 458, 463,
        3, 48, 24, 0, 459, 460, 5, 12, 0, 0, 460, 462, 3, 48, 24, 0, 461, 459, 1, 0, 0, 0, 462,
        465, 1, 0, 0, 0, 463, 461, 1, 0, 0, 0, 463, 464, 1, 0, 0, 0, 464, 55, 1, 0, 0, 0, 465, 463,
        1, 0, 0, 0, 466, 467, 7, 3, 0, 0, 467, 57, 1, 0, 0, 0, 63, 61, 69, 71, 79, 87, 94, 98, 104,
        106, 114, 121, 127, 139, 143, 146, 151, 159, 166, 171, 177, 182, 190, 197, 202,
        208, 216, 219, 223, 231, 237, 242, 251, 255, 259, 265, 269, 271, 292, 295, 299,
        303, 315, 318, 324, 333, 335, 340, 349, 353, 358, 362, 367, 375, 379, 389, 398,
        406, 437, 439, 448, 452, 456, 463
    ]


class transpilerParser(Parser):
    grammarFileName = "transpiler.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'@'", "'['", "']'", "'?'", "'.'", "'()'",
                    "'('", "')'", "'{'", "'}'", "';'", "','", "<INVALID>",
                    "'::'", "'include'", "'func'", "'method'", "'class'",
                    "'interface'", "'extends'", "'implements'", "'const'",
                    "'let'", "'return'", "'for'", "'while'", "'if'", "'else'",
                    "'new'", "'true'", "'false'", "'null'", "'in'", "'break'",
                    "'continue'", "'!'", "'*'", "'/'", "'%'", "'+'", "'-'",
                    "'>'", "'<'", "'=='", "'!='", "'>='", "'<='", "<INVALID>",
                    "<INVALID>", "'='"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "PAREN", "LPAREN", "RPAREN",
                     "LBRACE", "RBRACE", "SEMI", "COMMA", "ARROW", "DOUBLE_COLON",
                     "INCLUDE", "FUNC", "METHOD", "CLASS", "INTERFACE",
                     "EXTENDS", "IMPLEMENTS", "CONST", "LET", "RETURN",
                     "FOR", "WHILE", "IF", "ELSE", "NEW", "TRUE", "FALSE",
                     "NULL", "IN", "BREAK", "CONTINUE", "NOT", "MUL", "DIV",
                     "MOD", "ADD", "SUB", "GT", "LT", "EQ", "NEQ", "GTE",
                     "LTE", "AND", "OR", "ASSIGN", "NUMBER", "STRING",
                     "FSTRING", "ID", "WS", "LINE_COMMENT", "LINE_COMMENT2",
                     "BLOCK_COMMENT"]

    RULE_program = 0
    RULE_includeStmt = 1
    RULE_annotation = 2
    RULE_classDecl = 3
    RULE_interfaceDecl = 4
    RULE_type = 5
    RULE_functionDecl = 6
    RULE_methodDecl = 7
    RULE_paramList = 8
    RULE_paramDecl = 9
    RULE_block = 10
    RULE_statement = 11
    RULE_breakStmt = 12
    RULE_continueStmt = 13
    RULE_forStmt = 14
    RULE_forControl = 15
    RULE_whileStmt = 16
    RULE_constDecl = 17
    RULE_varDeclaration = 18
    RULE_varDecl = 19
    RULE_forLoopVarDecl = 20
    RULE_assignment = 21
    RULE_returnStmt = 22
    RULE_ifStmt = 23
    RULE_expr = 24
    RULE_primary = 25
    RULE_argumentList = 26
    RULE_exprList = 27
    RULE_literal = 28

    ruleNames = ["program", "includeStmt", "annotation", "classDecl",
                 "interfaceDecl", "type", "functionDecl", "methodDecl",
                 "paramList", "paramDecl", "block", "statement", "breakStmt",
                 "continueStmt", "forStmt", "forControl", "whileStmt",
                 "constDecl", "varDeclaration", "varDecl", "forLoopVarDecl",
                 "assignment", "returnStmt", "ifStmt", "expr", "primary",
                 "argumentList", "exprList", "literal"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    PAREN = 6
    LPAREN = 7
    RPAREN = 8
    LBRACE = 9
    RBRACE = 10
    SEMI = 11
    COMMA = 12
    ARROW = 13
    DOUBLE_COLON = 14
    INCLUDE = 15
    FUNC = 16
    METHOD = 17
    CLASS = 18
    INTERFACE = 19
    EXTENDS = 20
    IMPLEMENTS = 21
    CONST = 22
    LET = 23
    RETURN = 24
    FOR = 25
    WHILE = 26
    IF = 27
    ELSE = 28
    NEW = 29
    TRUE = 30
    FALSE = 31
    NULL = 32
    IN = 33
    BREAK = 34
    CONTINUE = 35
    NOT = 36
    MUL = 37
    DIV = 38
    MOD = 39
    ADD = 40
    SUB = 41
    GT = 42
    LT = 43
    EQ = 44
    NEQ = 45
    GTE = 46
    LTE = 47
    AND = 48
    OR = 49
    ASSIGN = 50
    NUMBER = 51
    STRING = 52
    FSTRING = 53
    ID = 54
    WS = 55
    LINE_COMMENT = 56
    LINE_COMMENT2 = 57
    BLOCK_COMMENT = 58

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
            self.state = 61
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 15:
                self.state = 58
                self.includeStmt()
                self.state = 63
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18014402817884162) != 0):
                self.state = 69
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 1, self._ctx)
                if la_ == 1:
                    self.state = 64
                    self.classDecl()
                    pass

                elif la_ == 2:
                    self.state = 65
                    self.interfaceDecl()
                    pass

                elif la_ == 3:
                    self.state = 66
                    self.functionDecl()
                    pass

                elif la_ == 4:
                    self.state = 67
                    self.varDecl()
                    pass

                elif la_ == 5:
                    self.state = 68
                    self.constDecl()
                    pass

                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 74
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
            self.state = 76
            self.match(transpilerParser.INCLUDE)
            self.state = 77
            self.literal()
            self.state = 79
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 11:
                self.state = 78
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
            self.state = 81
            self.match(transpilerParser.T__0)
            self.state = 82
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

        def methodDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.MethodDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.MethodDeclContext, i)

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
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 84
                self.annotation()
                self.state = 89
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 90
            self.match(transpilerParser.CLASS)
            self.state = 91
            self.match(transpilerParser.ID)
            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 20:
                self.state = 92
                self.match(transpilerParser.EXTENDS)
                self.state = 93
                self.type_()

            self.state = 98
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 21:
                self.state = 96
                self.match(transpilerParser.IMPLEMENTS)
                self.state = 97
                self.type_()

            self.state = 100
            self.match(transpilerParser.LBRACE)
            self.state = 106
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18014402817163266) != 0):
                self.state = 104
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [23, 32, 54]:
                    self.state = 101
                    self.varDecl()
                    pass
                elif token in [22]:
                    self.state = 102
                    self.constDecl()
                    pass
                elif token in [1, 17]:
                    self.state = 103
                    self.methodDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 108
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 109
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

        def methodDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.MethodDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.MethodDeclContext, i)

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
            self.state = 114
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 111
                self.annotation()
                self.state = 116
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 117
            self.match(transpilerParser.INTERFACE)
            self.state = 118
            self.match(transpilerParser.ID)
            self.state = 121
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 20:
                self.state = 119
                self.match(transpilerParser.EXTENDS)
                self.state = 120
                self.type_()

            self.state = 123
            self.match(transpilerParser.LBRACE)
            self.state = 127
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1 or _la == 17:
                self.state = 124
                self.methodDecl()
                self.state = 129
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 130
            self.match(transpilerParser.RBRACE)
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

        def type_(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.TypeContext)
            else:
                return self.getTypedRuleContext(transpilerParser.TypeContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.COMMA)
            else:
                return self.getToken(transpilerParser.COMMA, i)

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
        self.enterRule(localctx, 10, self.RULE_type)
        self._la = 0  # Token type
        try:
            self.state = 146
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [54]:
                self.enterOuterAlt(localctx, 1)
                self.state = 132
                self.match(transpilerParser.ID)
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 2:
                    self.state = 133
                    self.match(transpilerParser.T__1)
                    self.state = 139
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == 32 or _la == 54:
                        self.state = 134
                        self.type_()
                        self.state = 135
                        self.match(transpilerParser.COMMA)
                        self.state = 141
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 142
                    self.match(transpilerParser.T__2)

                pass
            elif token in [32]:
                self.enterOuterAlt(localctx, 2)
                self.state = 145
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

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

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
        self.enterRule(localctx, 12, self.RULE_functionDecl)
        self._la = 0  # Token type
        try:
            self.state = 177
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 19, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 151
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 148
                    self.annotation()
                    self.state = 153
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 154
                self.match(transpilerParser.FUNC)
                self.state = 155
                self.match(transpilerParser.ID)
                self.state = 156
                self.paramList()
                self.state = 159
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 157
                    self.match(transpilerParser.ARROW)
                    self.state = 158
                    self.type_()

                self.state = 161
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 166
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 163
                    self.annotation()
                    self.state = 168
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 169
                self.match(transpilerParser.FUNC)
                self.state = 171
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 18, self._ctx)
                if la_ == 1:
                    self.state = 170
                    self.type_()

                self.state = 173
                self.match(transpilerParser.ID)
                self.state = 174
                self.paramList()
                self.state = 175
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

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

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
        self.enterRule(localctx, 14, self.RULE_methodDecl)
        self._la = 0  # Token type
        try:
            self.state = 208
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 24, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
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
                self.match(transpilerParser.METHOD)
                self.state = 186
                self.match(transpilerParser.ID)
                self.state = 187
                self.paramList()
                self.state = 190
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 188
                    self.match(transpilerParser.ARROW)
                    self.state = 189
                    self.type_()

                self.state = 192
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 197
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 194
                    self.annotation()
                    self.state = 199
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 200
                self.match(transpilerParser.METHOD)
                self.state = 202
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 23, self._ctx)
                if la_ == 1:
                    self.state = 201
                    self.type_()

                self.state = 204
                self.match(transpilerParser.ID)
                self.state = 205
                self.paramList()
                self.state = 206
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
        self.enterRule(localctx, 16, self.RULE_paramList)
        self._la = 0  # Token type
        try:
            self.state = 223
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                self.enterOuterAlt(localctx, 1)
                self.state = 210
                self.match(transpilerParser.LPAREN)
                self.state = 219
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 32 or _la == 54:
                    self.state = 211
                    self.paramDecl()
                    self.state = 216
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la == 12:
                        self.state = 212
                        self.match(transpilerParser.COMMA)
                        self.state = 213
                        self.paramDecl()
                        self.state = 218
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                self.state = 221
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 222
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

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

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
        self.enterRule(localctx, 18, self.RULE_paramDecl)
        try:
            self.state = 231
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 28, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 225
                self.match(transpilerParser.ID)

                self.state = 226
                self.match(transpilerParser.ARROW)
                self.state = 227
                self.type_()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 228
                self.type_()
                self.state = 229
                self.match(transpilerParser.ID)
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
        self.enterRule(localctx, 20, self.RULE_block)
        self._la = 0  # Token type
        try:
            self.state = 242
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 233
                self.match(transpilerParser.LBRACE)
                self.state = 237
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 33779324268120706) != 0):
                    self.state = 234
                    self.statement()
                    self.state = 239
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 240
                self.match(transpilerParser.RBRACE)
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 2)
                self.state = 241
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

        def constDecl(self):
            return self.getTypedRuleContext(transpilerParser.ConstDeclContext, 0)

        def forStmt(self):
            return self.getTypedRuleContext(transpilerParser.ForStmtContext, 0)

        def whileStmt(self):
            return self.getTypedRuleContext(transpilerParser.WhileStmtContext, 0)

        def assignment(self):
            return self.getTypedRuleContext(transpilerParser.AssignmentContext, 0)

        def SEMI(self):
            return self.getToken(transpilerParser.SEMI, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def returnStmt(self):
            return self.getTypedRuleContext(transpilerParser.ReturnStmtContext, 0)

        def block(self):
            return self.getTypedRuleContext(transpilerParser.BlockContext, 0)

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
        self.enterRule(localctx, 22, self.RULE_statement)
        try:
            self.state = 271
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 36, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 244
                self.functionDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 245
                self.varDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 246
                self.constDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 247
                self.forStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 248
                self.whileStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 249
                self.assignment()
                self.state = 251
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 31, self._ctx)
                if la_ == 1:
                    self.state = 250
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 253
                self.expr(0)
                self.state = 255
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 32, self._ctx)
                if la_ == 1:
                    self.state = 254
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 257
                self.returnStmt()
                self.state = 259
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 33, self._ctx)
                if la_ == 1:
                    self.state = 258
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 261
                self.block()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 262
                self.ifStmt()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 263
                self.breakStmt()
                self.state = 265
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 34, self._ctx)
                if la_ == 1:
                    self.state = 264
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 267
                self.continueStmt()
                self.state = 269
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 35, self._ctx)
                if la_ == 1:
                    self.state = 268
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
        self.enterRule(localctx, 24, self.RULE_breakStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 273
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
        self.enterRule(localctx, 26, self.RULE_continueStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 275
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

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

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
        self.enterRule(localctx, 28, self.RULE_forStmt)
        try:
            self.state = 292
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 37, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 277
                self.match(transpilerParser.FOR)
                self.state = 278
                self.match(transpilerParser.LPAREN)
                self.state = 279
                self.forControl()
                self.state = 280
                self.match(transpilerParser.RPAREN)
                self.state = 281
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 283
                self.match(transpilerParser.FOR)
                self.state = 284
                self.match(transpilerParser.LPAREN)
                self.state = 285
                self.type_()
                self.state = 286
                self.match(transpilerParser.ID)
                self.state = 287
                self.match(transpilerParser.ARROW)
                self.state = 288
                self.expr(0)
                self.state = 289
                self.match(transpilerParser.RPAREN)
                self.state = 290
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

        def forLoopVarDecl(self):
            return self.getTypedRuleContext(transpilerParser.ForLoopVarDeclContext, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def assignment(self):
            return self.getTypedRuleContext(transpilerParser.AssignmentContext, 0)

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
        self.enterRule(localctx, 30, self.RULE_forControl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 295
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 18014402812837888) != 0):
                self.state = 294
                self.forLoopVarDecl()

            self.state = 297
            self.match(transpilerParser.SEMI)
            self.state = 299
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 33779272464203904) != 0):
                self.state = 298
                self.expr(0)

            self.state = 301
            self.match(transpilerParser.SEMI)
            self.state = 303
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 54:
                self.state = 302
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
            return self.getToken(transpilerParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(transpilerParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

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
        self.enterRule(localctx, 32, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 305
            self.match(transpilerParser.WHILE)
            self.state = 306
            self.match(transpilerParser.LPAREN)
            self.state = 307
            self.expr(0)
            self.state = 308
            self.match(transpilerParser.RPAREN)
            self.state = 309
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

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def SEMI(self):
            return self.getToken(transpilerParser.SEMI, 0)

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
        self.enterRule(localctx, 34, self.RULE_constDecl)
        self._la = 0  # Token type
        try:
            self.state = 335
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 45, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 311
                self.match(transpilerParser.CONST)
                self.state = 312
                self.match(transpilerParser.ID)
                self.state = 315
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 313
                    self.match(transpilerParser.ARROW)
                    self.state = 314
                    self.type_()

                self.state = 318
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 4:
                    self.state = 317
                    self.match(transpilerParser.T__3)

                self.state = 320
                self.match(transpilerParser.ASSIGN)
                self.state = 321
                self.expr(0)
                self.state = 324
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 43, self._ctx)
                if la_ == 1:
                    self.state = 323
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 326
                self.match(transpilerParser.CONST)
                self.state = 327
                self.type_()
                self.state = 328
                self.match(transpilerParser.ID)

                self.state = 329
                self.match(transpilerParser.ASSIGN)
                self.state = 330
                self.expr(0)
                self.state = 333
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 44, self._ctx)
                if la_ == 1:
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

    class VarDeclarationContext(ParserRuleContext):
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

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_varDeclaration

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

        localctx = transpilerParser.VarDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_varDeclaration)
        self._la = 0  # Token type
        try:
            self.state = 375
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 52, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 337
                self.match(transpilerParser.LET)
                self.state = 338
                self.match(transpilerParser.ID)
                self.state = 340
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 4:
                    self.state = 339
                    self.match(transpilerParser.T__3)

                self.state = 342
                self.match(transpilerParser.ASSIGN)
                self.state = 343
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 344
                self.match(transpilerParser.ID)

                self.state = 345
                self.match(transpilerParser.ARROW)
                self.state = 346
                self.type_()
                self.state = 349
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 4:
                    self.state = 348
                    self.match(transpilerParser.T__3)

                self.state = 353
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 50:
                    self.state = 351
                    self.match(transpilerParser.ASSIGN)
                    self.state = 352
                    self.expr(0)

                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 355
                self.type_()
                self.state = 356
                self.match(transpilerParser.ID)
                self.state = 358
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 4:
                    self.state = 357
                    self.match(transpilerParser.T__3)

                self.state = 362
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 50:
                    self.state = 360
                    self.match(transpilerParser.ASSIGN)
                    self.state = 361
                    self.expr(0)

                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 364
                self.match(transpilerParser.LET)
                self.state = 365
                self.match(transpilerParser.ID)
                self.state = 367
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 4:
                    self.state = 366
                    self.match(transpilerParser.T__3)

                self.state = 369
                self.match(transpilerParser.ARROW)
                self.state = 370
                self.type_()

                self.state = 372
                self.match(transpilerParser.ASSIGN)
                self.state = 373
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

        def varDeclaration(self):
            return self.getTypedRuleContext(transpilerParser.VarDeclarationContext, 0)

        def SEMI(self):
            return self.getToken(transpilerParser.SEMI, 0)

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
        self.enterRule(localctx, 38, self.RULE_varDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 377
            self.varDeclaration()
            self.state = 379
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 53, self._ctx)
            if la_ == 1:
                self.state = 378
                self.match(transpilerParser.SEMI)


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

        def varDeclaration(self):
            return self.getTypedRuleContext(transpilerParser.VarDeclarationContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_forLoopVarDecl

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

        localctx = transpilerParser.ForLoopVarDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_forLoopVarDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
            self.varDeclaration()
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
            return self.getToken(transpilerParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_assignment

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

        localctx = transpilerParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 383
            self.match(transpilerParser.ID)
            self.state = 384
            self.match(transpilerParser.ASSIGN)
            self.state = 385
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
        self.enterRule(localctx, 44, self.RULE_returnStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 387
            self.match(transpilerParser.RETURN)
            self.state = 389
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 54, self._ctx)
            if la_ == 1:
                self.state = 388
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

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

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
        self.enterRule(localctx, 46, self.RULE_ifStmt)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 391
            self.match(transpilerParser.IF)
            self.state = 392
            self.match(transpilerParser.LPAREN)
            self.state = 393
            self.expr(0)
            self.state = 394
            self.match(transpilerParser.RPAREN)
            self.state = 395
            self.block()
            self.state = 398
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 28:
                self.state = 396
                self.match(transpilerParser.ELSE)
                self.state = 397
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
        _startState = 48
        self.enterRecursionRule(localctx, 48, self.RULE_expr, _p)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 406
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7, 30, 31, 32, 51, 52, 53, 54]:
                localctx = transpilerParser.PrimaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 401
                self.primary()
                pass
            elif token in [41]:
                localctx = transpilerParser.NegExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 402
                self.match(transpilerParser.SUB)
                self.state = 403
                self.expr(7)
                pass
            elif token in [36]:
                localctx = transpilerParser.LogicalNotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 404
                self.match(transpilerParser.NOT)
                self.state = 405
                self.expr(6)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 439
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 58, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 437
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 57, self._ctx)
                    if la_ == 1:
                        localctx = transpilerParser.FactorExprContext(self,
                                                                      transpilerParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 408
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 409
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 962072674304) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 410
                        self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = transpilerParser.TermExprContext(self, transpilerParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 411
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 412
                        _la = self._input.LA(1)
                        if not (_la == 40 or _la == 41):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 413
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = transpilerParser.CompareExprContext(self,
                                                                       transpilerParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 414
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 415
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 277076930199552) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 416
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = transpilerParser.LogicalAndExprContext(self,
                                                                          transpilerParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 417
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 418
                        self.match(transpilerParser.AND)
                        self.state = 419
                        self.expr(3)
                        pass

                    elif la_ == 5:
                        localctx = transpilerParser.LogicalOrExprContext(self,
                                                                         transpilerParser.ExprContext(self, _parentctx,
                                                                                                      _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 420
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 421
                        self.match(transpilerParser.OR)
                        self.state = 422
                        self.expr(2)
                        pass

                    elif la_ == 6:
                        localctx = transpilerParser.MethodCallContext(self,
                                                                      transpilerParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 423
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 424
                        self.match(transpilerParser.T__4)
                        self.state = 425
                        self.match(transpilerParser.ID)
                        self.state = 426
                        self.argumentList()
                        pass

                    elif la_ == 7:
                        localctx = transpilerParser.MemberAccessContext(self,
                                                                        transpilerParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 427
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 428
                        self.match(transpilerParser.T__4)
                        self.state = 429
                        self.match(transpilerParser.ID)
                        pass

                    elif la_ == 8:
                        localctx = transpilerParser.ArrayAccessContext(self,
                                                                       transpilerParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 430
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 431
                        self.match(transpilerParser.T__1)
                        self.state = 432
                        self.expr(0)
                        self.state = 433
                        self.match(transpilerParser.T__2)
                        pass

                    elif la_ == 9:
                        localctx = transpilerParser.FunctionCallContext(self,
                                                                        transpilerParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 435
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 436
                        self.argumentList()
                        pass

                self.state = 441
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 58, self._ctx)

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
        self.enterRule(localctx, 50, self.RULE_primary)
        try:
            self.state = 448
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [54]:
                localctx = transpilerParser.IdentifierExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 442
                self.match(transpilerParser.ID)
                pass
            elif token in [30, 31, 32, 51, 52, 53]:
                localctx = transpilerParser.LiteralExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 443
                self.literal()
                pass
            elif token in [7]:
                localctx = transpilerParser.ParenExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 444
                self.match(transpilerParser.LPAREN)
                self.state = 445
                self.expr(0)
                self.state = 446
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
        self.enterRule(localctx, 52, self.RULE_argumentList)
        self._la = 0  # Token type
        try:
            self.state = 456
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                self.enterOuterAlt(localctx, 1)
                self.state = 450
                self.match(transpilerParser.LPAREN)
                self.state = 452
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 33779272464203904) != 0):
                    self.state = 451
                    self.exprList()

                self.state = 454
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 455
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
        self.enterRule(localctx, 54, self.RULE_exprList)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 458
            self.expr(0)
            self.state = 463
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 12:
                self.state = 459
                self.match(transpilerParser.COMMA)
                self.state = 460
                self.expr(0)
                self.state = 465
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
        self.enterRule(localctx, 56, self.RULE_literal)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 466
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 15762606211989504) != 0)):
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
        self._predicates[24] = self.expr_sempred
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
            return self.precpred(self._ctx, 12)

        if predIndex == 6:
            return self.precpred(self._ctx, 11)

        if predIndex == 7:
            return self.precpred(self._ctx, 10)

        if predIndex == 8:
            return self.precpred(self._ctx, 9)
