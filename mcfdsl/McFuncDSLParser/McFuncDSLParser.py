# Generated from E:/python/minecraft-datapack-language/antlr/McFuncDSL.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4, 1, 62, 478, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7,
        6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13,
        2, 14, 7, 14, 2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20,
        7, 20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26,
        2, 27, 7, 27, 2, 28, 7, 28, 2, 29, 7, 29, 2, 30, 7, 30, 2, 31, 7, 31, 2, 32, 7, 32, 2, 33,
        7, 33, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 5, 0, 74, 8, 0, 10, 0, 12, 0, 77, 9, 0, 1, 0, 1, 0, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 3, 5, 3, 89, 8, 3, 10, 3, 12, 3, 92, 9, 3, 1, 3, 1, 3,
        1, 3, 1, 3, 3, 3, 98, 8, 3, 1, 3, 1, 3, 3, 3, 102, 8, 3, 1, 3, 1, 3, 1, 3, 1, 3, 5, 3, 108, 8,
        3, 10, 3, 12, 3, 111, 9, 3, 1, 3, 1, 3, 1, 4, 5, 4, 116, 8, 4, 10, 4, 12, 4, 119, 9, 4, 1,
        4, 1, 4, 1, 4, 1, 4, 3, 4, 125, 8, 4, 1, 4, 1, 4, 5, 4, 129, 8, 4, 10, 4, 12, 4, 132, 9, 4,
        1, 4, 1, 4, 1, 5, 5, 5, 137, 8, 5, 10, 5, 12, 5, 140, 9, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1,
        5, 1, 5, 1, 5, 1, 6, 1, 6, 3, 6, 152, 8, 6, 1, 7, 1, 7, 1, 7, 5, 7, 157, 8, 7, 10, 7, 12, 7,
        160, 9, 7, 1, 8, 1, 8, 1, 9, 5, 9, 165, 8, 9, 10, 9, 12, 9, 168, 9, 9, 1, 9, 1, 9, 1, 9, 1,
        9, 1, 9, 1, 9, 1, 9, 1, 9, 1, 9, 5, 9, 179, 8, 9, 10, 9, 12, 9, 182, 9, 9, 1, 9, 1, 9, 1, 9,
        1, 9, 1, 9, 1, 9, 3, 9, 190, 8, 9, 1, 10, 5, 10, 193, 8, 10, 10, 10, 12, 10, 196, 9, 10,
        1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 5, 10, 206, 8, 10, 10, 10, 12, 10,
        209, 9, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 3, 10, 217, 8, 10, 1, 11, 1, 11, 1,
        11, 1, 11, 5, 11, 223, 8, 11, 10, 11, 12, 11, 226, 9, 11, 1, 11, 1, 11, 1, 11, 3, 11, 231,
        8, 11, 1, 12, 1, 12, 1, 12, 1, 12, 1, 12, 1, 12, 3, 12, 239, 8, 12, 1, 13, 1, 13, 5, 13,
        243, 8, 13, 10, 13, 12, 13, 246, 9, 13, 1, 13, 1, 13, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14,
        1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14,
        1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 1, 14, 3, 14, 275, 8, 14, 1, 15, 1, 15, 1, 16,
        1, 16, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17, 1, 17,
        1, 17, 1, 17, 3, 17, 295, 8, 17, 1, 18, 3, 18, 298, 8, 18, 1, 18, 1, 18, 3, 18, 302, 8,
        18, 1, 18, 1, 18, 1, 18, 3, 18, 307, 8, 18, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1,
        20, 1, 20, 1, 20, 1, 20, 3, 20, 319, 8, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1, 20, 1,
        20, 1, 20, 1, 20, 1, 20, 3, 20, 331, 8, 20, 1, 20, 1, 20, 3, 20, 335, 8, 20, 1, 21, 1, 21,
        1, 21, 1, 21, 1, 21, 3, 21, 342, 8, 21, 1, 21, 1, 21, 3, 21, 346, 8, 21, 1, 21, 1, 21, 1,
        21, 3, 21, 351, 8, 21, 1, 21, 1, 21, 3, 21, 355, 8, 21, 3, 21, 357, 8, 21, 1, 22, 1, 22,
        1, 22, 1, 22, 1, 22, 1, 22, 1, 22, 3, 22, 366, 8, 22, 1, 23, 1, 23, 1, 23, 3, 23, 371, 8,
        23, 1, 24, 1, 24, 1, 24, 1, 24, 1, 25, 1, 25, 3, 25, 379, 8, 25, 1, 26, 1, 26, 1, 26, 1,
        26, 1, 26, 1, 26, 1, 26, 3, 26, 388, 8, 26, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1,
        27, 1, 27, 3, 27, 398, 8, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1,
        27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 1,
        27, 5, 27, 422, 8, 27, 10, 27, 12, 27, 425, 9, 27, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 1,
        28, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 1, 28, 3, 28, 441, 8, 28, 1, 29, 1,
        29, 1, 29, 1, 30, 1, 30, 1, 30, 1, 30, 5, 30, 450, 8, 30, 10, 30, 12, 30, 453, 9, 30, 1,
        30, 1, 30, 1, 31, 1, 31, 3, 31, 459, 8, 31, 1, 31, 1, 31, 3, 31, 463, 8, 31, 1, 32, 1, 32,
        1, 32, 5, 32, 468, 8, 32, 10, 32, 12, 32, 471, 9, 32, 1, 32, 3, 32, 474, 8, 32, 1, 33,
        1, 33, 1, 33, 0, 1, 54, 34, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32,
        34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 0, 6, 1, 0, 10, 13,
        2, 0, 3, 3, 41, 41, 1, 0, 44, 45, 1, 0, 46, 47, 2, 0, 8, 9, 48, 51, 2, 0, 34, 36, 55, 57,
        518, 0, 75, 1, 0, 0, 0, 2, 80, 1, 0, 0, 0, 4, 84, 1, 0, 0, 0, 6, 90, 1, 0, 0, 0, 8, 117, 1,
        0, 0, 0, 10, 138, 1, 0, 0, 0, 12, 151, 1, 0, 0, 0, 14, 153, 1, 0, 0, 0, 16, 161, 1, 0, 0,
        0, 18, 189, 1, 0, 0, 0, 20, 216, 1, 0, 0, 0, 22, 230, 1, 0, 0, 0, 24, 238, 1, 0, 0, 0, 26,
        240, 1, 0, 0, 0, 28, 274, 1, 0, 0, 0, 30, 276, 1, 0, 0, 0, 32, 278, 1, 0, 0, 0, 34, 294,
        1, 0, 0, 0, 36, 297, 1, 0, 0, 0, 38, 308, 1, 0, 0, 0, 40, 334, 1, 0, 0, 0, 42, 356, 1, 0,
        0, 0, 44, 365, 1, 0, 0, 0, 46, 370, 1, 0, 0, 0, 48, 372, 1, 0, 0, 0, 50, 376, 1, 0, 0, 0,
        52, 380, 1, 0, 0, 0, 54, 397, 1, 0, 0, 0, 56, 440, 1, 0, 0, 0, 58, 442, 1, 0, 0, 0, 60, 445,
        1, 0, 0, 0, 62, 462, 1, 0, 0, 0, 64, 473, 1, 0, 0, 0, 66, 475, 1, 0, 0, 0, 68, 74, 3, 2, 1,
        0, 69, 74, 3, 18, 9, 0, 70, 74, 3, 6, 3, 0, 71, 74, 3, 8, 4, 0, 72, 74, 3, 28, 14, 0, 73,
        68, 1, 0, 0, 0, 73, 69, 1, 0, 0, 0, 73, 70, 1, 0, 0, 0, 73, 71, 1, 0, 0, 0, 73, 72, 1, 0, 0,
        0, 74, 77, 1, 0, 0, 0, 75, 73, 1, 0, 0, 0, 75, 76, 1, 0, 0, 0, 76, 78, 1, 0, 0, 0, 77, 75,
        1, 0, 0, 0, 78, 79, 5, 0, 0, 1, 79, 1, 1, 0, 0, 0, 80, 81, 5, 1, 0, 0, 81, 82, 5, 56, 0, 0,
        82, 83, 5, 19, 0, 0, 83, 3, 1, 0, 0, 0, 84, 85, 5, 2, 0, 0, 85, 86, 5, 58, 0, 0, 86, 5, 1,
        0, 0, 0, 87, 89, 3, 4, 2, 0, 88, 87, 1, 0, 0, 0, 89, 92, 1, 0, 0, 0, 90, 88, 1, 0, 0, 0, 90,
        91, 1, 0, 0, 0, 91, 93, 1, 0, 0, 0, 92, 90, 1, 0, 0, 0, 93, 94, 5, 23, 0, 0, 94, 97, 5, 58,
        0, 0, 95, 96, 5, 25, 0, 0, 96, 98, 3, 12, 6, 0, 97, 95, 1, 0, 0, 0, 97, 98, 1, 0, 0, 0, 98,
        101, 1, 0, 0, 0, 99, 100, 5, 26, 0, 0, 100, 102, 3, 14, 7, 0, 101, 99, 1, 0, 0, 0, 101,
        102, 1, 0, 0, 0, 102, 103, 1, 0, 0, 0, 103, 109, 5, 17, 0, 0, 104, 108, 3, 44, 22, 0, 105,
        108, 3, 40, 20, 0, 106, 108, 3, 20, 10, 0, 107, 104, 1, 0, 0, 0, 107, 105, 1, 0, 0, 0,
        107, 106, 1, 0, 0, 0, 108, 111, 1, 0, 0, 0, 109, 107, 1, 0, 0, 0, 109, 110, 1, 0, 0, 0,
        110, 112, 1, 0, 0, 0, 111, 109, 1, 0, 0, 0, 112, 113, 5, 18, 0, 0, 113, 7, 1, 0, 0, 0, 114,
        116, 3, 4, 2, 0, 115, 114, 1, 0, 0, 0, 116, 119, 1, 0, 0, 0, 117, 115, 1, 0, 0, 0, 117,
        118, 1, 0, 0, 0, 118, 120, 1, 0, 0, 0, 119, 117, 1, 0, 0, 0, 120, 121, 5, 24, 0, 0, 121,
        124, 5, 58, 0, 0, 122, 123, 5, 25, 0, 0, 123, 125, 3, 12, 6, 0, 124, 122, 1, 0, 0, 0, 124,
        125, 1, 0, 0, 0, 125, 126, 1, 0, 0, 0, 126, 130, 5, 17, 0, 0, 127, 129, 3, 10, 5, 0, 128,
        127, 1, 0, 0, 0, 129, 132, 1, 0, 0, 0, 130, 128, 1, 0, 0, 0, 130, 131, 1, 0, 0, 0, 131,
        133, 1, 0, 0, 0, 132, 130, 1, 0, 0, 0, 133, 134, 5, 18, 0, 0, 134, 9, 1, 0, 0, 0, 135, 137,
        3, 4, 2, 0, 136, 135, 1, 0, 0, 0, 137, 140, 1, 0, 0, 0, 138, 136, 1, 0, 0, 0, 138, 139,
        1, 0, 0, 0, 139, 141, 1, 0, 0, 0, 140, 138, 1, 0, 0, 0, 141, 142, 5, 22, 0, 0, 142, 143,
        5, 58, 0, 0, 143, 144, 3, 22, 11, 0, 144, 145, 5, 3, 0, 0, 145, 146, 3, 12, 6, 0, 146,
        147, 1, 0, 0, 0, 147, 148, 5, 19, 0, 0, 148, 11, 1, 0, 0, 0, 149, 152, 5, 58, 0, 0, 150,
        152, 3, 16, 8, 0, 151, 149, 1, 0, 0, 0, 151, 150, 1, 0, 0, 0, 152, 13, 1, 0, 0, 0, 153,
        158, 3, 12, 6, 0, 154, 155, 5, 20, 0, 0, 155, 157, 3, 12, 6, 0, 156, 154, 1, 0, 0, 0, 157,
        160, 1, 0, 0, 0, 158, 156, 1, 0, 0, 0, 158, 159, 1, 0, 0, 0, 159, 15, 1, 0, 0, 0, 160, 158,
        1, 0, 0, 0, 161, 162, 7, 0, 0, 0, 162, 17, 1, 0, 0, 0, 163, 165, 3, 4, 2, 0, 164, 163, 1,
        0, 0, 0, 165, 168, 1, 0, 0, 0, 166, 164, 1, 0, 0, 0, 166, 167, 1, 0, 0, 0, 167, 169, 1,
        0, 0, 0, 168, 166, 1, 0, 0, 0, 169, 170, 5, 21, 0, 0, 170, 171, 5, 58, 0, 0, 171, 172,
        3, 22, 11, 0, 172, 173, 7, 1, 0, 0, 173, 174, 3, 12, 6, 0, 174, 175, 1, 0, 0, 0, 175, 176,
        3, 26, 13, 0, 176, 190, 1, 0, 0, 0, 177, 179, 3, 4, 2, 0, 178, 177, 1, 0, 0, 0, 179, 182,
        1, 0, 0, 0, 180, 178, 1, 0, 0, 0, 180, 181, 1, 0, 0, 0, 181, 183, 1, 0, 0, 0, 182, 180,
        1, 0, 0, 0, 183, 184, 5, 21, 0, 0, 184, 185, 3, 12, 6, 0, 185, 186, 5, 58, 0, 0, 186, 187,
        3, 22, 11, 0, 187, 188, 3, 26, 13, 0, 188, 190, 1, 0, 0, 0, 189, 166, 1, 0, 0, 0, 189,
        180, 1, 0, 0, 0, 190, 19, 1, 0, 0, 0, 191, 193, 3, 4, 2, 0, 192, 191, 1, 0, 0, 0, 193, 196,
        1, 0, 0, 0, 194, 192, 1, 0, 0, 0, 194, 195, 1, 0, 0, 0, 195, 197, 1, 0, 0, 0, 196, 194,
        1, 0, 0, 0, 197, 198, 5, 22, 0, 0, 198, 199, 5, 58, 0, 0, 199, 200, 3, 22, 11, 0, 200,
        201, 7, 1, 0, 0, 201, 202, 3, 12, 6, 0, 202, 203, 3, 26, 13, 0, 203, 217, 1, 0, 0, 0, 204,
        206, 3, 4, 2, 0, 205, 204, 1, 0, 0, 0, 206, 209, 1, 0, 0, 0, 207, 205, 1, 0, 0, 0, 207,
        208, 1, 0, 0, 0, 208, 210, 1, 0, 0, 0, 209, 207, 1, 0, 0, 0, 210, 211, 5, 22, 0, 0, 211,
        212, 3, 12, 6, 0, 212, 213, 5, 58, 0, 0, 213, 214, 3, 22, 11, 0, 214, 215, 3, 26, 13,
        0, 215, 217, 1, 0, 0, 0, 216, 194, 1, 0, 0, 0, 216, 207, 1, 0, 0, 0, 217, 21, 1, 0, 0, 0,
        218, 219, 5, 15, 0, 0, 219, 224, 3, 24, 12, 0, 220, 221, 5, 20, 0, 0, 221, 223, 3, 24,
        12, 0, 222, 220, 1, 0, 0, 0, 223, 226, 1, 0, 0, 0, 224, 222, 1, 0, 0, 0, 224, 225, 1, 0,
        0, 0, 225, 227, 1, 0, 0, 0, 226, 224, 1, 0, 0, 0, 227, 228, 5, 16, 0, 0, 228, 231, 1, 0,
        0, 0, 229, 231, 5, 4, 0, 0, 230, 218, 1, 0, 0, 0, 230, 229, 1, 0, 0, 0, 231, 23, 1, 0, 0,
        0, 232, 233, 5, 58, 0, 0, 233, 234, 5, 3, 0, 0, 234, 239, 3, 12, 6, 0, 235, 236, 3, 12,
        6, 0, 236, 237, 5, 58, 0, 0, 237, 239, 1, 0, 0, 0, 238, 232, 1, 0, 0, 0, 238, 235, 1, 0,
        0, 0, 239, 25, 1, 0, 0, 0, 240, 244, 5, 17, 0, 0, 241, 243, 3, 28, 14, 0, 242, 241, 1,
        0, 0, 0, 243, 246, 1, 0, 0, 0, 244, 242, 1, 0, 0, 0, 244, 245, 1, 0, 0, 0, 245, 247, 1,
        0, 0, 0, 246, 244, 1, 0, 0, 0, 247, 248, 5, 18, 0, 0, 248, 27, 1, 0, 0, 0, 249, 250, 3,
        58, 29, 0, 250, 251, 5, 19, 0, 0, 251, 275, 1, 0, 0, 0, 252, 275, 3, 60, 30, 0, 253, 275,
        3, 44, 22, 0, 254, 275, 3, 40, 20, 0, 255, 275, 3, 34, 17, 0, 256, 275, 3, 38, 19, 0,
        257, 258, 3, 48, 24, 0, 258, 259, 5, 19, 0, 0, 259, 275, 1, 0, 0, 0, 260, 261, 3, 54,
        27, 0, 261, 262, 5, 19, 0, 0, 262, 275, 1, 0, 0, 0, 263, 264, 3, 50, 25, 0, 264, 265,
        5, 19, 0, 0, 265, 275, 1, 0, 0, 0, 266, 275, 3, 26, 13, 0, 267, 275, 3, 52, 26, 0, 268,
        269, 3, 30, 15, 0, 269, 270, 5, 19, 0, 0, 270, 275, 1, 0, 0, 0, 271, 272, 3, 32, 16, 0,
        272, 273, 5, 19, 0, 0, 273, 275, 1, 0, 0, 0, 274, 249, 1, 0, 0, 0, 274, 252, 1, 0, 0, 0,
        274, 253, 1, 0, 0, 0, 274, 254, 1, 0, 0, 0, 274, 255, 1, 0, 0, 0, 274, 256, 1, 0, 0, 0,
        274, 257, 1, 0, 0, 0, 274, 260, 1, 0, 0, 0, 274, 263, 1, 0, 0, 0, 274, 266, 1, 0, 0, 0,
        274, 267, 1, 0, 0, 0, 274, 268, 1, 0, 0, 0, 274, 271, 1, 0, 0, 0, 275, 29, 1, 0, 0, 0, 276,
        277, 5, 38, 0, 0, 277, 31, 1, 0, 0, 0, 278, 279, 5, 39, 0, 0, 279, 33, 1, 0, 0, 0, 280,
        281, 5, 29, 0, 0, 281, 282, 5, 15, 0, 0, 282, 283, 3, 36, 18, 0, 283, 284, 5, 16, 0, 0,
        284, 285, 3, 26, 13, 0, 285, 295, 1, 0, 0, 0, 286, 287, 5, 29, 0, 0, 287, 288, 5, 15,
        0, 0, 288, 289, 5, 58, 0, 0, 289, 290, 5, 3, 0, 0, 290, 291, 3, 54, 27, 0, 291, 292, 5,
        16, 0, 0, 292, 293, 3, 26, 13, 0, 293, 295, 1, 0, 0, 0, 294, 280, 1, 0, 0, 0, 294, 286,
        1, 0, 0, 0, 295, 35, 1, 0, 0, 0, 296, 298, 3, 46, 23, 0, 297, 296, 1, 0, 0, 0, 297, 298,
        1, 0, 0, 0, 298, 299, 1, 0, 0, 0, 299, 301, 5, 19, 0, 0, 300, 302, 3, 54, 27, 0, 301, 300,
        1, 0, 0, 0, 301, 302, 1, 0, 0, 0, 302, 303, 1, 0, 0, 0, 303, 306, 5, 19, 0, 0, 304, 307,
        3, 48, 24, 0, 305, 307, 3, 54, 27, 0, 306, 304, 1, 0, 0, 0, 306, 305, 1, 0, 0, 0, 306,
        307, 1, 0, 0, 0, 307, 37, 1, 0, 0, 0, 308, 309, 5, 30, 0, 0, 309, 310, 5, 15, 0, 0, 310,
        311, 3, 54, 27, 0, 311, 312, 5, 16, 0, 0, 312, 313, 3, 26, 13, 0, 313, 39, 1, 0, 0, 0,
        314, 315, 5, 5, 0, 0, 315, 318, 5, 58, 0, 0, 316, 317, 5, 3, 0, 0, 317, 319, 3, 12, 6,
        0, 318, 316, 1, 0, 0, 0, 318, 319, 1, 0, 0, 0, 319, 320, 1, 0, 0, 0, 320, 321, 5, 54, 0,
        0, 321, 322, 3, 54, 27, 0, 322, 323, 1, 0, 0, 0, 323, 324, 5, 19, 0, 0, 324, 335, 1, 0,
        0, 0, 325, 326, 5, 5, 0, 0, 326, 327, 3, 12, 6, 0, 327, 330, 5, 58, 0, 0, 328, 329, 5,
        54, 0, 0, 329, 331, 3, 54, 27, 0, 330, 328, 1, 0, 0, 0, 330, 331, 1, 0, 0, 0, 331, 332,
        1, 0, 0, 0, 332, 333, 5, 19, 0, 0, 333, 335, 1, 0, 0, 0, 334, 314, 1, 0, 0, 0, 334, 325,
        1, 0, 0, 0, 335, 41, 1, 0, 0, 0, 336, 337, 5, 58, 0, 0, 337, 338, 5, 3, 0, 0, 338, 339,
        3, 12, 6, 0, 339, 341, 1, 0, 0, 0, 340, 342, 5, 6, 0, 0, 341, 340, 1, 0, 0, 0, 341, 342,
        1, 0, 0, 0, 342, 345, 1, 0, 0, 0, 343, 344, 5, 54, 0, 0, 344, 346, 3, 54, 27, 0, 345, 343,
        1, 0, 0, 0, 345, 346, 1, 0, 0, 0, 346, 357, 1, 0, 0, 0, 347, 348, 3, 12, 6, 0, 348, 350,
        5, 58, 0, 0, 349, 351, 5, 6, 0, 0, 350, 349, 1, 0, 0, 0, 350, 351, 1, 0, 0, 0, 351, 354,
        1, 0, 0, 0, 352, 353, 5, 54, 0, 0, 353, 355, 3, 54, 27, 0, 354, 352, 1, 0, 0, 0, 354, 355,
        1, 0, 0, 0, 355, 357, 1, 0, 0, 0, 356, 336, 1, 0, 0, 0, 356, 347, 1, 0, 0, 0, 357, 43, 1,
        0, 0, 0, 358, 359, 5, 27, 0, 0, 359, 360, 3, 42, 21, 0, 360, 361, 5, 19, 0, 0, 361, 366,
        1, 0, 0, 0, 362, 363, 3, 42, 21, 0, 363, 364, 5, 19, 0, 0, 364, 366, 1, 0, 0, 0, 365, 358,
        1, 0, 0, 0, 365, 362, 1, 0, 0, 0, 366, 45, 1, 0, 0, 0, 367, 368, 5, 27, 0, 0, 368, 371,
        3, 42, 21, 0, 369, 371, 3, 42, 21, 0, 370, 367, 1, 0, 0, 0, 370, 369, 1, 0, 0, 0, 371,
        47, 1, 0, 0, 0, 372, 373, 5, 58, 0, 0, 373, 374, 5, 54, 0, 0, 374, 375, 3, 54, 27, 0, 375,
        49, 1, 0, 0, 0, 376, 378, 5, 28, 0, 0, 377, 379, 3, 54, 27, 0, 378, 377, 1, 0, 0, 0, 378,
        379, 1, 0, 0, 0, 379, 51, 1, 0, 0, 0, 380, 381, 5, 31, 0, 0, 381, 382, 5, 15, 0, 0, 382,
        383, 3, 54, 27, 0, 383, 384, 5, 16, 0, 0, 384, 387, 3, 26, 13, 0, 385, 386, 5, 32, 0,
        0, 386, 388, 3, 26, 13, 0, 387, 385, 1, 0, 0, 0, 387, 388, 1, 0, 0, 0, 388, 53, 1, 0, 0,
        0, 389, 390, 6, 27, -1, 0, 390, 391, 5, 58, 0, 0, 391, 398, 3, 62, 31, 0, 392, 398, 3,
        56, 28, 0, 393, 394, 5, 47, 0, 0, 394, 398, 3, 54, 27, 7, 395, 396, 5, 43, 0, 0, 396,
        398, 3, 54, 27, 6, 397, 389, 1, 0, 0, 0, 397, 392, 1, 0, 0, 0, 397, 393, 1, 0, 0, 0, 397,
        395, 1, 0, 0, 0, 398, 423, 1, 0, 0, 0, 399, 400, 10, 5, 0, 0, 400, 401, 7, 2, 0, 0, 401,
        422, 3, 54, 27, 6, 402, 403, 10, 4, 0, 0, 403, 404, 7, 3, 0, 0, 404, 422, 3, 54, 27, 5,
        405, 406, 10, 3, 0, 0, 406, 407, 7, 4, 0, 0, 407, 422, 3, 54, 27, 4, 408, 409, 10, 2,
        0, 0, 409, 410, 5, 52, 0, 0, 410, 422, 3, 54, 27, 3, 411, 412, 10, 1, 0, 0, 412, 413,
        5, 53, 0, 0, 413, 422, 3, 54, 27, 2, 414, 415, 10, 11, 0, 0, 415, 416, 5, 7, 0, 0, 416,
        417, 5, 58, 0, 0, 417, 422, 3, 62, 31, 0, 418, 419, 10, 10, 0, 0, 419, 420, 5, 7, 0, 0,
        420, 422, 5, 58, 0, 0, 421, 399, 1, 0, 0, 0, 421, 402, 1, 0, 0, 0, 421, 405, 1, 0, 0, 0,
        421, 408, 1, 0, 0, 0, 421, 411, 1, 0, 0, 0, 421, 414, 1, 0, 0, 0, 421, 418, 1, 0, 0, 0,
        422, 425, 1, 0, 0, 0, 423, 421, 1, 0, 0, 0, 423, 424, 1, 0, 0, 0, 424, 55, 1, 0, 0, 0, 425,
        423, 1, 0, 0, 0, 426, 441, 5, 58, 0, 0, 427, 441, 3, 66, 33, 0, 428, 429, 5, 15, 0, 0,
        429, 430, 3, 54, 27, 0, 430, 431, 5, 16, 0, 0, 431, 441, 1, 0, 0, 0, 432, 433, 5, 33,
        0, 0, 433, 434, 5, 58, 0, 0, 434, 441, 3, 62, 31, 0, 435, 436, 5, 15, 0, 0, 436, 437,
        3, 12, 6, 0, 437, 438, 5, 16, 0, 0, 438, 439, 3, 54, 27, 0, 439, 441, 1, 0, 0, 0, 440,
        426, 1, 0, 0, 0, 440, 427, 1, 0, 0, 0, 440, 428, 1, 0, 0, 0, 440, 432, 1, 0, 0, 0, 440,
        435, 1, 0, 0, 0, 441, 57, 1, 0, 0, 0, 442, 443, 5, 40, 0, 0, 443, 444, 5, 57, 0, 0, 444,
        59, 1, 0, 0, 0, 445, 446, 5, 40, 0, 0, 446, 451, 5, 17, 0, 0, 447, 448, 5, 57, 0, 0, 448,
        450, 5, 19, 0, 0, 449, 447, 1, 0, 0, 0, 450, 453, 1, 0, 0, 0, 451, 449, 1, 0, 0, 0, 451,
        452, 1, 0, 0, 0, 452, 454, 1, 0, 0, 0, 453, 451, 1, 0, 0, 0, 454, 455, 5, 18, 0, 0, 455,
        61, 1, 0, 0, 0, 456, 458, 5, 15, 0, 0, 457, 459, 3, 64, 32, 0, 458, 457, 1, 0, 0, 0, 458,
        459, 1, 0, 0, 0, 459, 460, 1, 0, 0, 0, 460, 463, 5, 16, 0, 0, 461, 463, 5, 4, 0, 0, 462,
        456, 1, 0, 0, 0, 462, 461, 1, 0, 0, 0, 463, 63, 1, 0, 0, 0, 464, 469, 3, 54, 27, 0, 465,
        466, 5, 20, 0, 0, 466, 468, 3, 54, 27, 0, 467, 465, 1, 0, 0, 0, 468, 471, 1, 0, 0, 0, 469,
        467, 1, 0, 0, 0, 469, 470, 1, 0, 0, 0, 470, 474, 1, 0, 0, 0, 471, 469, 1, 0, 0, 0, 472,
        474, 5, 4, 0, 0, 473, 464, 1, 0, 0, 0, 473, 472, 1, 0, 0, 0, 474, 65, 1, 0, 0, 0, 475, 476,
        7, 5, 0, 0, 476, 67, 1, 0, 0, 0, 49, 73, 75, 90, 97, 101, 107, 109, 117, 124, 130, 138,
        151, 158, 166, 180, 189, 194, 207, 216, 224, 230, 238, 244, 274, 294, 297, 301,
        306, 318, 330, 334, 341, 345, 350, 354, 356, 365, 370, 378, 387, 397, 421, 423,
        440, 451, 458, 462, 469, 473
    ]


class McFuncDSLParser(Parser):
    grammarFileName = "McFuncDSL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'import'", "'@'", "':'", "'()'", "'const'",
                    "'?'", "'.'", "'<='", "'>='", "'int'", "'string'",
                    "'boolean'", "'void'", "'any'", "'('", "')'", "'{'",
                    "'}'", "';'", "','", "'func'", "'method'", "'class'",
                    "'interface'", "'extends'", "'implements'", "'var'",
                    "'return'", "'for'", "'while'", "'if'", "'else'", "'new'",
                    "'true'", "'false'", "'null'", "'in'", "'break'", "'continue'",
                    "<INVALID>", "'->'", "'::'", "'!'", "'*'", "'/'", "'+'",
                    "'-'", "'>'", "'<'", "'=='", "'!='", "<INVALID>", "<INVALID>",
                    "'='"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "TYPE_INT", "TYPE_STRING",
                     "TYPE_BOOLEAN", "TYPE_VOID", "TYPE_ANY", "LPAREN",
                     "RPAREN", "LBRACE", "RBRACE", "SEMI", "COMMA", "FUNC",
                     "METHOD", "CLASS", "INTERFACE", "EXTENDS", "IMPLEMENTS",
                     "VAR", "RETURN", "FOR", "WHILE", "IF", "ELSE", "NEW",
                     "TRUE", "FALSE", "NULL", "IN", "BREAK", "CONTINUE",
                     "CMD", "ARROW", "DOUBLE_COLON", "NOT", "MUL", "DIV",
                     "ADD", "SUB", "GT", "LT", "EQ", "NEQ", "AND", "OR",
                     "ASSIGN", "NUMBER", "STRING", "FSTRING", "ID", "WS",
                     "LINE_COMMENT", "LINE_COMMENT2", "BLOCK_COMMENT"]

    RULE_program = 0
    RULE_importStmt = 1
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
    RULE_cmdExpr = 29
    RULE_cmdBlockExpr = 30
    RULE_argumentList = 31
    RULE_exprList = 32
    RULE_literal = 33

    ruleNames = ["program", "importStmt", "annotation", "classDecl", "interfaceDecl",
                 "interfaceMethodDecl", "type", "typeList", "primitiveType",
                 "functionDecl", "methodDecl", "paramList", "paramDecl",
                 "block", "statement", "breakStmt", "continueStmt", "forStmt",
                 "forControl", "whileStmt", "constDecl", "varDeclaration",
                 "varDecl", "forLoopVarDecl", "assignment", "returnStmt",
                 "ifStmt", "expr", "primary", "cmdExpr", "cmdBlockExpr",
                 "argumentList", "exprList", "literal"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    TYPE_INT = 10
    TYPE_STRING = 11
    TYPE_BOOLEAN = 12
    TYPE_VOID = 13
    TYPE_ANY = 14
    LPAREN = 15
    RPAREN = 16
    LBRACE = 17
    RBRACE = 18
    SEMI = 19
    COMMA = 20
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

        def importStmt(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ImportStmtContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ImportStmtContext, i)

        def functionDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.FunctionDeclContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.FunctionDeclContext, i)

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
            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 540583546048396326) != 0):
                self.state = 73
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 0, self._ctx)
                if la_ == 1:
                    self.state = 68
                    self.importStmt()
                    pass

                elif la_ == 2:
                    self.state = 69
                    self.functionDecl()
                    pass

                elif la_ == 3:
                    self.state = 70
                    self.classDecl()
                    pass

                elif la_ == 4:
                    self.state = 71
                    self.interfaceDecl()
                    pass

                elif la_ == 5:
                    self.state = 72
                    self.statement()
                    pass

                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 78
            self.match(McFuncDSLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ImportStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(McFuncDSLParser.STRING, 0)

        def SEMI(self):
            return self.getToken(McFuncDSLParser.SEMI, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_importStmt

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterImportStmt"):
                listener.enterImportStmt(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitImportStmt"):
                listener.exitImportStmt(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitImportStmt"):
                return visitor.visitImportStmt(self)
            else:
                return visitor.visitChildren(self)

    def importStmt(self):

        localctx = McFuncDSLParser.ImportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_importStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(McFuncDSLParser.T__0)
            self.state = 81
            self.match(McFuncDSLParser.STRING)
            self.state = 82
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
            self.state = 84
            self.match(McFuncDSLParser.T__1)
            self.state = 85
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

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

        def IMPLEMENTS(self):
            return self.getToken(McFuncDSLParser.IMPLEMENTS, 0)

        def typeList(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeListContext, 0)

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
            self.state = 90
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 2:
                self.state = 87
                self.annotation()
                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 93
            self.match(McFuncDSLParser.CLASS)
            self.state = 94
            self.match(McFuncDSLParser.ID)
            self.state = 97
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 25:
                self.state = 95
                self.match(McFuncDSLParser.EXTENDS)
                self.state = 96
                self.type_()

            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 26:
                self.state = 99
                self.match(McFuncDSLParser.IMPLEMENTS)
                self.state = 100
                self.typeList()

            self.state = 103
            self.match(McFuncDSLParser.LBRACE)
            self.state = 109
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230376290139172) != 0):
                self.state = 107
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [10, 11, 12, 13, 27, 58]:
                    self.state = 104
                    self.varDecl()
                    pass
                elif token in [5]:
                    self.state = 105
                    self.constDecl()
                    pass
                elif token in [2, 22]:
                    self.state = 106
                    self.methodDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 111
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 112
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
            self.state = 117
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 2:
                self.state = 114
                self.annotation()
                self.state = 119
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 120
            self.match(McFuncDSLParser.INTERFACE)
            self.state = 121
            self.match(McFuncDSLParser.ID)
            self.state = 124
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 25:
                self.state = 122
                self.match(McFuncDSLParser.EXTENDS)
                self.state = 123
                self.type_()

            self.state = 126
            self.match(McFuncDSLParser.LBRACE)
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 2 or _la == 22:
                self.state = 127
                self.interfaceMethodDecl()
                self.state = 132
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 133
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
            self.state = 138
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 2:
                self.state = 135
                self.annotation()
                self.state = 140
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 141
            self.match(McFuncDSLParser.METHOD)
            self.state = 142
            self.match(McFuncDSLParser.ID)
            self.state = 143
            self.paramList()

            self.state = 144
            self.match(McFuncDSLParser.T__2)
            self.state = 145
            self.type_()
            self.state = 147
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
            self.state = 151
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [58]:
                self.enterOuterAlt(localctx, 1)
                self.state = 149
                self.match(McFuncDSLParser.ID)
                pass
            elif token in [10, 11, 12, 13]:
                self.enterOuterAlt(localctx, 2)
                self.state = 150
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
            self.state = 153
            self.type_()
            self.state = 158
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 20:
                self.state = 154
                self.match(McFuncDSLParser.COMMA)
                self.state = 155
                self.type_()
                self.state = 160
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
            self.state = 161
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 15360) != 0)):
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
            self.state = 189
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 15, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 166
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 2:
                    self.state = 163
                    self.annotation()
                    self.state = 168
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 169
                self.match(McFuncDSLParser.FUNC)
                self.state = 170
                self.match(McFuncDSLParser.ID)

                self.state = 171
                self.paramList()

                self.state = 172
                _la = self._input.LA(1)
                if not (_la == 3 or _la == 41):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 173
                self.type_()
                self.state = 175
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 180
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 2:
                    self.state = 177
                    self.annotation()
                    self.state = 182
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 183
                self.match(McFuncDSLParser.FUNC)
                self.state = 184
                self.type_()
                self.state = 185
                self.match(McFuncDSLParser.ID)

                self.state = 186
                self.paramList()
                self.state = 187
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
            self.state = 216
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 18, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 194
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 2:
                    self.state = 191
                    self.annotation()
                    self.state = 196
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 197
                self.match(McFuncDSLParser.METHOD)
                self.state = 198
                self.match(McFuncDSLParser.ID)
                self.state = 199
                self.paramList()
                self.state = 200
                _la = self._input.LA(1)
                if not (_la == 3 or _la == 41):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 201
                self.type_()
                self.state = 202
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 207
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 2:
                    self.state = 204
                    self.annotation()
                    self.state = 209
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 210
                self.match(McFuncDSLParser.METHOD)
                self.state = 211
                self.type_()
                self.state = 212
                self.match(McFuncDSLParser.ID)
                self.state = 213
                self.paramList()
                self.state = 214
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
            self.state = 230
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15]:
                self.enterOuterAlt(localctx, 1)
                self.state = 218
                self.match(McFuncDSLParser.LPAREN)

                self.state = 219
                self.paramDecl()
                self.state = 224
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 20:
                    self.state = 220
                    self.match(McFuncDSLParser.COMMA)
                    self.state = 221
                    self.paramDecl()
                    self.state = 226
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 227
                self.match(McFuncDSLParser.RPAREN)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 229
                self.match(McFuncDSLParser.T__3)
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
            self.state = 238
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 21, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 232
                self.match(McFuncDSLParser.ID)

                self.state = 233
                self.match(McFuncDSLParser.T__2)
                self.state = 234
                self.type_()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 235
                self.type_()
                self.state = 236
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
            self.state = 240
            self.match(McFuncDSLParser.LBRACE)
            self.state = 244
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 540583546021133344) != 0):
                self.state = 241
                self.statement()
                self.state = 246
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 247
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

        def cmdExpr(self):
            return self.getTypedRuleContext(McFuncDSLParser.CmdExprContext, 0)

        def SEMI(self):
            return self.getToken(McFuncDSLParser.SEMI, 0)

        def cmdBlockExpr(self):
            return self.getTypedRuleContext(McFuncDSLParser.CmdBlockExprContext, 0)

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
            self.state = 274
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 23, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 249
                self.cmdExpr()
                self.state = 250
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 252
                self.cmdBlockExpr()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 253
                self.varDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 254
                self.constDecl()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 255
                self.forStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 256
                self.whileStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 257
                self.assignment()
                self.state = 258
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 260
                self.expr(0)
                self.state = 261
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 263
                self.returnStmt()
                self.state = 264
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 266
                self.block()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 267
                self.ifStmt()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 268
                self.breakStmt()
                self.state = 269
                self.match(McFuncDSLParser.SEMI)
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 271
                self.continueStmt()
                self.state = 272
                self.match(McFuncDSLParser.SEMI)
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
            self.state = 276
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
            self.state = 278
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
            self.state = 294
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 24, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 280
                self.match(McFuncDSLParser.FOR)
                self.state = 281
                self.match(McFuncDSLParser.LPAREN)
                self.state = 282
                self.forControl()
                self.state = 283
                self.match(McFuncDSLParser.RPAREN)
                self.state = 284
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 286
                self.match(McFuncDSLParser.FOR)
                self.state = 287
                self.match(McFuncDSLParser.LPAREN)
                self.state = 288
                self.match(McFuncDSLParser.ID)
                self.state = 289
                self.match(McFuncDSLParser.T__2)
                self.state = 290
                self.expr(0)
                self.state = 291
                self.match(McFuncDSLParser.RPAREN)
                self.state = 292
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

        def expr(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(McFuncDSLParser.ExprContext)
            else:
                return self.getTypedRuleContext(McFuncDSLParser.ExprContext, i)

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
            self.state = 297
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 288230376285944832) != 0):
                self.state = 296
                self.forLoopVarDecl()

            self.state = 299
            self.match(McFuncDSLParser.SEMI)
            self.state = 301
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540581617714888704) != 0):
                self.state = 300
                self.expr(0)

            self.state = 303
            self.match(McFuncDSLParser.SEMI)
            self.state = 306
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 27, self._ctx)
            if la_ == 1:
                self.state = 304
                self.assignment()

            elif la_ == 2:
                self.state = 305
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
            self.state = 308
            self.match(McFuncDSLParser.WHILE)
            self.state = 309
            self.match(McFuncDSLParser.LPAREN)
            self.state = 310
            self.expr(0)
            self.state = 311
            self.match(McFuncDSLParser.RPAREN)
            self.state = 312
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

        def ASSIGN(self):
            return self.getToken(McFuncDSLParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(McFuncDSLParser.ExprContext, 0)

        def type_(self):
            return self.getTypedRuleContext(McFuncDSLParser.TypeContext, 0)

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
        self._la = 0  # Token type
        try:
            self.state = 334
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 30, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 314
                self.match(McFuncDSLParser.T__4)
                self.state = 315
                self.match(McFuncDSLParser.ID)
                self.state = 318
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 3:
                    self.state = 316
                    self.match(McFuncDSLParser.T__2)
                    self.state = 317
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
                self.match(McFuncDSLParser.T__4)
                self.state = 326
                self.type_()
                self.state = 327
                self.match(McFuncDSLParser.ID)
                self.state = 330
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 54:
                    self.state = 328
                    self.match(McFuncDSLParser.ASSIGN)
                    self.state = 329
                    self.expr(0)

                self.state = 332
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
            self.state = 356
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 35, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 336
                self.match(McFuncDSLParser.ID)

                self.state = 337
                self.match(McFuncDSLParser.T__2)
                self.state = 338
                self.type_()
                self.state = 341
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 6:
                    self.state = 340
                    self.match(McFuncDSLParser.T__5)

                self.state = 345
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 54:
                    self.state = 343
                    self.match(McFuncDSLParser.ASSIGN)
                    self.state = 344
                    self.expr(0)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 347
                self.type_()
                self.state = 348
                self.match(McFuncDSLParser.ID)
                self.state = 350
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 6:
                    self.state = 349
                    self.match(McFuncDSLParser.T__5)

                self.state = 354
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 54:
                    self.state = 352
                    self.match(McFuncDSLParser.ASSIGN)
                    self.state = 353
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
            self.state = 365
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 358
                self.match(McFuncDSLParser.VAR)
                self.state = 359
                self.varDeclaration()
                self.state = 360
                self.match(McFuncDSLParser.SEMI)
                pass
            elif token in [10, 11, 12, 13, 58]:
                self.enterOuterAlt(localctx, 2)
                self.state = 362
                self.varDeclaration()
                self.state = 363
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
            self.state = 370
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 367
                self.match(McFuncDSLParser.VAR)
                self.state = 368
                self.varDeclaration()
                pass
            elif token in [10, 11, 12, 13, 58]:
                self.enterOuterAlt(localctx, 2)
                self.state = 369
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
            self.state = 372
            self.match(McFuncDSLParser.ID)
            self.state = 373
            self.match(McFuncDSLParser.ASSIGN)
            self.state = 374
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
            self.state = 376
            self.match(McFuncDSLParser.RETURN)
            self.state = 378
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540581617714888704) != 0):
                self.state = 377
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
            self.state = 380
            self.match(McFuncDSLParser.IF)
            self.state = 381
            self.match(McFuncDSLParser.LPAREN)
            self.state = 382
            self.expr(0)
            self.state = 383
            self.match(McFuncDSLParser.RPAREN)
            self.state = 384
            self.block()
            self.state = 387
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 32:
                self.state = 385
                self.match(McFuncDSLParser.ELSE)
                self.state = 386
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
            self.state = 397
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 40, self._ctx)
            if la_ == 1:
                localctx = McFuncDSLParser.DirectFuncCallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 390
                self.match(McFuncDSLParser.ID)
                self.state = 391
                self.argumentList()
                pass

            elif la_ == 2:
                localctx = McFuncDSLParser.PrimaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 392
                self.primary()
                pass

            elif la_ == 3:
                localctx = McFuncDSLParser.NegExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 393
                self.match(McFuncDSLParser.SUB)
                self.state = 394
                self.expr(7)
                pass

            elif la_ == 4:
                localctx = McFuncDSLParser.LogicalNotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 395
                self.match(McFuncDSLParser.NOT)
                self.state = 396
                self.expr(6)
                pass

            self._ctx.stop = self._input.LT(-1)
            self.state = 423
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 42, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 421
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 41, self._ctx)
                    if la_ == 1:
                        localctx = McFuncDSLParser.MulDivExprContext(self, McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 399
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 400
                        _la = self._input.LA(1)
                        if not (_la == 44 or _la == 45):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 401
                        self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = McFuncDSLParser.AddSubExprContext(self, McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 402
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 403
                        _la = self._input.LA(1)
                        if not (_la == 46 or _la == 47):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 404
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = McFuncDSLParser.CompareExprContext(self,
                                                                      McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                  _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 405
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 406
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 4222124650660608) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 407
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = McFuncDSLParser.LogicalAndExprContext(self,
                                                                         McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 408
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 409
                        self.match(McFuncDSLParser.AND)
                        self.state = 410
                        self.expr(3)
                        pass

                    elif la_ == 5:
                        localctx = McFuncDSLParser.LogicalOrExprContext(self,
                                                                        McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 411
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 412
                        self.match(McFuncDSLParser.OR)
                        self.state = 413
                        self.expr(2)
                        pass

                    elif la_ == 6:
                        localctx = McFuncDSLParser.MethodCallContext(self, McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 414
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 415
                        self.match(McFuncDSLParser.T__6)
                        self.state = 416
                        self.match(McFuncDSLParser.ID)
                        self.state = 417
                        self.argumentList()
                        pass

                    elif la_ == 7:
                        localctx = McFuncDSLParser.MemberAccessContext(self,
                                                                       McFuncDSLParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 418
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 419
                        self.match(McFuncDSLParser.T__6)
                        self.state = 420
                        self.match(McFuncDSLParser.ID)
                        pass

                self.state = 425
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 42, self._ctx)

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
            self.state = 440
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 43, self._ctx)
            if la_ == 1:
                localctx = McFuncDSLParser.VarExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 426
                self.match(McFuncDSLParser.ID)
                pass

            elif la_ == 2:
                localctx = McFuncDSLParser.LiteralExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 427
                self.literal()
                pass

            elif la_ == 3:
                localctx = McFuncDSLParser.ParenExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 428
                self.match(McFuncDSLParser.LPAREN)
                self.state = 429
                self.expr(0)
                self.state = 430
                self.match(McFuncDSLParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = McFuncDSLParser.NewObjectExprContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 432
                self.match(McFuncDSLParser.NEW)
                self.state = 433
                self.match(McFuncDSLParser.ID)
                self.state = 434
                self.argumentList()
                pass

            elif la_ == 5:
                localctx = McFuncDSLParser.TypeCastExprContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 435
                self.match(McFuncDSLParser.LPAREN)
                self.state = 436
                self.type_()
                self.state = 437
                self.match(McFuncDSLParser.RPAREN)
                self.state = 438
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CmdExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CMD(self):
            return self.getToken(McFuncDSLParser.CMD, 0)

        def FSTRING(self):
            return self.getToken(McFuncDSLParser.FSTRING, 0)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_cmdExpr

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCmdExpr"):
                listener.enterCmdExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCmdExpr"):
                listener.exitCmdExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCmdExpr"):
                return visitor.visitCmdExpr(self)
            else:
                return visitor.visitChildren(self)

    def cmdExpr(self):

        localctx = McFuncDSLParser.CmdExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_cmdExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 442
            self.match(McFuncDSLParser.CMD)
            self.state = 443
            self.match(McFuncDSLParser.FSTRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class CmdBlockExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CMD(self):
            return self.getToken(McFuncDSLParser.CMD, 0)

        def LBRACE(self):
            return self.getToken(McFuncDSLParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(McFuncDSLParser.RBRACE, 0)

        def FSTRING(self, i: int = None):
            if i is None:
                return self.getTokens(McFuncDSLParser.FSTRING)
            else:
                return self.getToken(McFuncDSLParser.FSTRING, i)

        def SEMI(self, i: int = None):
            if i is None:
                return self.getTokens(McFuncDSLParser.SEMI)
            else:
                return self.getToken(McFuncDSLParser.SEMI, i)

        def getRuleIndex(self):
            return McFuncDSLParser.RULE_cmdBlockExpr

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterCmdBlockExpr"):
                listener.enterCmdBlockExpr(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitCmdBlockExpr"):
                listener.exitCmdBlockExpr(self)

        def accept(self, visitor: ParseTreeVisitor):
            if hasattr(visitor, "visitCmdBlockExpr"):
                return visitor.visitCmdBlockExpr(self)
            else:
                return visitor.visitChildren(self)

    def cmdBlockExpr(self):

        localctx = McFuncDSLParser.CmdBlockExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_cmdBlockExpr)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 445
            self.match(McFuncDSLParser.CMD)
            self.state = 446
            self.match(McFuncDSLParser.LBRACE)
            self.state = 451
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 57:
                self.state = 447
                self.match(McFuncDSLParser.FSTRING)
                self.state = 448
                self.match(McFuncDSLParser.SEMI)
                self.state = 453
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 454
            self.match(McFuncDSLParser.RBRACE)
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
        self.enterRule(localctx, 62, self.RULE_argumentList)
        self._la = 0  # Token type
        try:
            self.state = 462
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15]:
                self.enterOuterAlt(localctx, 1)
                self.state = 456
                self.match(McFuncDSLParser.LPAREN)
                self.state = 458
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 540581617714888720) != 0):
                    self.state = 457
                    self.exprList()

                self.state = 460
                self.match(McFuncDSLParser.RPAREN)
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 461
                self.match(McFuncDSLParser.T__3)
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
        self.enterRule(localctx, 64, self.RULE_exprList)
        self._la = 0  # Token type
        try:
            self.state = 473
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15, 33, 34, 35, 36, 43, 47, 55, 56, 57, 58]:
                self.enterOuterAlt(localctx, 1)
                self.state = 464
                self.expr(0)
                self.state = 469
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 20:
                    self.state = 465
                    self.match(McFuncDSLParser.COMMA)
                    self.state = 466
                    self.expr(0)
                    self.state = 471
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 472
                self.match(McFuncDSLParser.T__3)
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
        self.enterRule(localctx, 66, self.RULE_literal)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 475
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
