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
        4, 1, 58, 457, 2, 0, 7, 0, 2, 1, 7, 1, 2, 2, 7, 2, 2, 3, 7, 3, 2, 4, 7, 4, 2, 5, 7, 5, 2, 6, 7,
        6, 2, 7, 7, 7, 2, 8, 7, 8, 2, 9, 7, 9, 2, 10, 7, 10, 2, 11, 7, 11, 2, 12, 7, 12, 2, 13, 7, 13,
        2, 14, 7, 14, 2, 15, 7, 15, 2, 16, 7, 16, 2, 17, 7, 17, 2, 18, 7, 18, 2, 19, 7, 19, 2, 20,
        7, 20, 2, 21, 7, 21, 2, 22, 7, 22, 2, 23, 7, 23, 2, 24, 7, 24, 2, 25, 7, 25, 2, 26, 7, 26,
        2, 27, 7, 27, 2, 28, 7, 28, 2, 29, 7, 29, 2, 30, 7, 30, 1, 0, 5, 0, 64, 8, 0, 10, 0, 12, 0,
        67, 9, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 5, 0, 74, 8, 0, 10, 0, 12, 0, 77, 9, 0, 1, 0, 1, 0, 1,
        1, 1, 1, 1, 1, 3, 1, 84, 8, 1, 1, 2, 1, 2, 1, 2, 1, 3, 5, 3, 90, 8, 3, 10, 3, 12, 3, 93, 9, 3,
        1, 3, 1, 3, 1, 3, 1, 3, 3, 3, 99, 8, 3, 1, 3, 1, 3, 3, 3, 103, 8, 3, 1, 3, 1, 3, 1, 3, 1, 3, 5,
        3, 109, 8, 3, 10, 3, 12, 3, 112, 9, 3, 1, 3, 1, 3, 1, 4, 5, 4, 117, 8, 4, 10, 4, 12, 4, 120,
        9, 4, 1, 4, 1, 4, 1, 4, 1, 4, 3, 4, 126, 8, 4, 1, 4, 1, 4, 5, 4, 130, 8, 4, 10, 4, 12, 4, 133,
        9, 4, 1, 4, 1, 4, 1, 5, 5, 5, 138, 8, 5, 10, 5, 12, 5, 141, 9, 5, 1, 5, 1, 5, 1, 5, 1, 5, 1,
        5, 1, 5, 1, 5, 3, 5, 150, 8, 5, 1, 6, 1, 6, 1, 7, 1, 7, 1, 7, 5, 7, 157, 8, 7, 10, 7, 12, 7,
        160, 9, 7, 1, 8, 5, 8, 163, 8, 8, 10, 8, 12, 8, 166, 9, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1,
        8, 1, 8, 1, 8, 1, 8, 5, 8, 177, 8, 8, 10, 8, 12, 8, 180, 9, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 8,
        1, 8, 3, 8, 188, 8, 8, 1, 9, 5, 9, 191, 8, 9, 10, 9, 12, 9, 194, 9, 9, 1, 9, 1, 9, 1, 9, 1,
        9, 1, 9, 1, 9, 1, 9, 1, 9, 5, 9, 204, 8, 9, 10, 9, 12, 9, 207, 9, 9, 1, 9, 1, 9, 1, 9, 1, 9,
        1, 9, 1, 9, 3, 9, 215, 8, 9, 1, 10, 1, 10, 1, 10, 1, 10, 5, 10, 221, 8, 10, 10, 10, 12, 10,
        224, 9, 10, 1, 10, 1, 10, 1, 10, 3, 10, 229, 8, 10, 1, 11, 1, 11, 1, 11, 1, 11, 1, 11, 1,
        11, 3, 11, 237, 8, 11, 1, 12, 1, 12, 5, 12, 241, 8, 12, 10, 12, 12, 12, 244, 9, 12, 1,
        12, 1, 12, 1, 13, 1, 13, 1, 13, 1, 13, 1, 13, 1, 13, 3, 13, 254, 8, 13, 1, 13, 1, 13, 3,
        13, 258, 8, 13, 1, 13, 1, 13, 3, 13, 262, 8, 13, 1, 13, 1, 13, 1, 13, 1, 13, 3, 13, 268,
        8, 13, 1, 13, 1, 13, 3, 13, 272, 8, 13, 1, 13, 3, 13, 275, 8, 13, 1, 14, 1, 14, 1, 15, 1,
        15, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1, 16, 1,
        16, 1, 16, 3, 16, 295, 8, 16, 1, 17, 3, 17, 298, 8, 17, 1, 17, 1, 17, 3, 17, 302, 8, 17,
        1, 17, 1, 17, 3, 17, 306, 8, 17, 1, 18, 1, 18, 1, 18, 1, 18, 1, 18, 1, 18, 1, 19, 1, 19,
        1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 1, 19, 3, 19, 323, 8, 19, 1, 19, 1, 19, 1, 19,
        1, 19, 1, 19, 1, 19, 1, 19, 3, 19, 332, 8, 19, 3, 19, 334, 8, 19, 1, 20, 1, 20, 1, 20, 1,
        20, 1, 20, 3, 20, 341, 8, 20, 1, 20, 1, 20, 3, 20, 345, 8, 20, 1, 20, 1, 20, 1, 20, 3, 20,
        350, 8, 20, 1, 20, 1, 20, 3, 20, 354, 8, 20, 3, 20, 356, 8, 20, 1, 21, 1, 21, 1, 21, 3,
        21, 361, 8, 21, 1, 21, 1, 21, 3, 21, 365, 8, 21, 3, 21, 367, 8, 21, 1, 22, 1, 22, 1, 22,
        3, 22, 372, 8, 22, 1, 23, 1, 23, 1, 23, 1, 23, 1, 24, 1, 24, 3, 24, 380, 8, 24, 1, 25, 1,
        25, 1, 25, 1, 25, 1, 25, 1, 25, 1, 25, 3, 25, 389, 8, 25, 1, 26, 1, 26, 1, 26, 1, 26, 1,
        26, 1, 26, 1, 26, 1, 26, 3, 26, 399, 8, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1,
        26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1, 26, 1,
        26, 1, 26, 1, 26, 5, 26, 423, 8, 26, 10, 26, 12, 26, 426, 9, 26, 1, 27, 1, 27, 1, 27, 1,
        27, 1, 27, 1, 27, 1, 27, 1, 27, 1, 27, 3, 27, 437, 8, 27, 1, 28, 1, 28, 3, 28, 441, 8, 28,
        1, 28, 1, 28, 3, 28, 445, 8, 28, 1, 29, 1, 29, 1, 29, 5, 29, 450, 8, 29, 10, 29, 12, 29,
        453, 9, 29, 1, 30, 1, 30, 1, 30, 0, 1, 52, 31, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22,
        24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 0, 5, 2, 0,
        2, 2, 36, 36, 1, 0, 39, 41, 1, 0, 42, 43, 2, 0, 7, 8, 44, 47, 2, 0, 29, 31, 51, 53, 504,
        0, 65, 1, 0, 0, 0, 2, 80, 1, 0, 0, 0, 4, 85, 1, 0, 0, 0, 6, 91, 1, 0, 0, 0, 8, 118, 1, 0, 0,
        0, 10, 139, 1, 0, 0, 0, 12, 151, 1, 0, 0, 0, 14, 153, 1, 0, 0, 0, 16, 187, 1, 0, 0, 0, 18,
        214, 1, 0, 0, 0, 20, 228, 1, 0, 0, 0, 22, 236, 1, 0, 0, 0, 24, 238, 1, 0, 0, 0, 26, 274,
        1, 0, 0, 0, 28, 276, 1, 0, 0, 0, 30, 278, 1, 0, 0, 0, 32, 294, 1, 0, 0, 0, 34, 297, 1, 0,
        0, 0, 36, 307, 1, 0, 0, 0, 38, 333, 1, 0, 0, 0, 40, 355, 1, 0, 0, 0, 42, 366, 1, 0, 0, 0,
        44, 371, 1, 0, 0, 0, 46, 373, 1, 0, 0, 0, 48, 377, 1, 0, 0, 0, 50, 381, 1, 0, 0, 0, 52, 398,
        1, 0, 0, 0, 54, 436, 1, 0, 0, 0, 56, 444, 1, 0, 0, 0, 58, 446, 1, 0, 0, 0, 60, 454, 1, 0,
        0, 0, 62, 64, 3, 2, 1, 0, 63, 62, 1, 0, 0, 0, 64, 67, 1, 0, 0, 0, 65, 63, 1, 0, 0, 0, 65, 66,
        1, 0, 0, 0, 66, 75, 1, 0, 0, 0, 67, 65, 1, 0, 0, 0, 68, 74, 3, 6, 3, 0, 69, 74, 3, 8, 4, 0,
        70, 74, 3, 16, 8, 0, 71, 74, 3, 42, 21, 0, 72, 74, 3, 38, 19, 0, 73, 68, 1, 0, 0, 0, 73,
        69, 1, 0, 0, 0, 73, 70, 1, 0, 0, 0, 73, 71, 1, 0, 0, 0, 73, 72, 1, 0, 0, 0, 74, 77, 1, 0, 0,
        0, 75, 73, 1, 0, 0, 0, 75, 76, 1, 0, 0, 0, 76, 78, 1, 0, 0, 0, 77, 75, 1, 0, 0, 0, 78, 79,
        5, 0, 0, 1, 79, 1, 1, 0, 0, 0, 80, 81, 5, 15, 0, 0, 81, 83, 3, 60, 30, 0, 82, 84, 5, 13, 0,
        0, 83, 82, 1, 0, 0, 0, 83, 84, 1, 0, 0, 0, 84, 3, 1, 0, 0, 0, 85, 86, 5, 1, 0, 0, 86, 87, 5,
        54, 0, 0, 87, 5, 1, 0, 0, 0, 88, 90, 3, 4, 2, 0, 89, 88, 1, 0, 0, 0, 90, 93, 1, 0, 0, 0, 91,
        89, 1, 0, 0, 0, 91, 92, 1, 0, 0, 0, 92, 94, 1, 0, 0, 0, 93, 91, 1, 0, 0, 0, 94, 95, 5, 18,
        0, 0, 95, 98, 5, 54, 0, 0, 96, 97, 5, 20, 0, 0, 97, 99, 3, 12, 6, 0, 98, 96, 1, 0, 0, 0, 98,
        99, 1, 0, 0, 0, 99, 102, 1, 0, 0, 0, 100, 101, 5, 21, 0, 0, 101, 103, 3, 12, 6, 0, 102,
        100, 1, 0, 0, 0, 102, 103, 1, 0, 0, 0, 103, 104, 1, 0, 0, 0, 104, 110, 5, 11, 0, 0, 105,
        109, 3, 42, 21, 0, 106, 109, 3, 38, 19, 0, 107, 109, 3, 18, 9, 0, 108, 105, 1, 0, 0, 0,
        108, 106, 1, 0, 0, 0, 108, 107, 1, 0, 0, 0, 109, 112, 1, 0, 0, 0, 110, 108, 1, 0, 0, 0,
        110, 111, 1, 0, 0, 0, 111, 113, 1, 0, 0, 0, 112, 110, 1, 0, 0, 0, 113, 114, 5, 12, 0, 0,
        114, 7, 1, 0, 0, 0, 115, 117, 3, 4, 2, 0, 116, 115, 1, 0, 0, 0, 117, 120, 1, 0, 0, 0, 118,
        116, 1, 0, 0, 0, 118, 119, 1, 0, 0, 0, 119, 121, 1, 0, 0, 0, 120, 118, 1, 0, 0, 0, 121,
        122, 5, 19, 0, 0, 122, 125, 5, 54, 0, 0, 123, 124, 5, 20, 0, 0, 124, 126, 3, 12, 6, 0,
        125, 123, 1, 0, 0, 0, 125, 126, 1, 0, 0, 0, 126, 127, 1, 0, 0, 0, 127, 131, 5, 11, 0, 0,
        128, 130, 3, 10, 5, 0, 129, 128, 1, 0, 0, 0, 130, 133, 1, 0, 0, 0, 131, 129, 1, 0, 0, 0,
        131, 132, 1, 0, 0, 0, 132, 134, 1, 0, 0, 0, 133, 131, 1, 0, 0, 0, 134, 135, 5, 12, 0, 0,
        135, 9, 1, 0, 0, 0, 136, 138, 3, 4, 2, 0, 137, 136, 1, 0, 0, 0, 138, 141, 1, 0, 0, 0, 139,
        137, 1, 0, 0, 0, 139, 140, 1, 0, 0, 0, 140, 142, 1, 0, 0, 0, 141, 139, 1, 0, 0, 0, 142,
        143, 5, 17, 0, 0, 143, 144, 5, 54, 0, 0, 144, 145, 3, 20, 10, 0, 145, 146, 5, 2, 0, 0,
        146, 147, 3, 12, 6, 0, 147, 149, 1, 0, 0, 0, 148, 150, 5, 13, 0, 0, 149, 148, 1, 0, 0,
        0, 149, 150, 1, 0, 0, 0, 150, 11, 1, 0, 0, 0, 151, 152, 5, 54, 0, 0, 152, 13, 1, 0, 0, 0,
        153, 158, 3, 12, 6, 0, 154, 155, 5, 14, 0, 0, 155, 157, 3, 12, 6, 0, 156, 154, 1, 0, 0,
        0, 157, 160, 1, 0, 0, 0, 158, 156, 1, 0, 0, 0, 158, 159, 1, 0, 0, 0, 159, 15, 1, 0, 0, 0,
        160, 158, 1, 0, 0, 0, 161, 163, 3, 4, 2, 0, 162, 161, 1, 0, 0, 0, 163, 166, 1, 0, 0, 0,
        164, 162, 1, 0, 0, 0, 164, 165, 1, 0, 0, 0, 165, 167, 1, 0, 0, 0, 166, 164, 1, 0, 0, 0,
        167, 168, 5, 16, 0, 0, 168, 169, 5, 54, 0, 0, 169, 170, 3, 20, 10, 0, 170, 171, 7, 0,
        0, 0, 171, 172, 3, 12, 6, 0, 172, 173, 1, 0, 0, 0, 173, 174, 3, 24, 12, 0, 174, 188, 1,
        0, 0, 0, 175, 177, 3, 4, 2, 0, 176, 175, 1, 0, 0, 0, 177, 180, 1, 0, 0, 0, 178, 176, 1,
        0, 0, 0, 178, 179, 1, 0, 0, 0, 179, 181, 1, 0, 0, 0, 180, 178, 1, 0, 0, 0, 181, 182, 5,
        16, 0, 0, 182, 183, 3, 12, 6, 0, 183, 184, 5, 54, 0, 0, 184, 185, 3, 20, 10, 0, 185, 186,
        3, 24, 12, 0, 186, 188, 1, 0, 0, 0, 187, 164, 1, 0, 0, 0, 187, 178, 1, 0, 0, 0, 188, 17,
        1, 0, 0, 0, 189, 191, 3, 4, 2, 0, 190, 189, 1, 0, 0, 0, 191, 194, 1, 0, 0, 0, 192, 190,
        1, 0, 0, 0, 192, 193, 1, 0, 0, 0, 193, 195, 1, 0, 0, 0, 194, 192, 1, 0, 0, 0, 195, 196,
        5, 17, 0, 0, 196, 197, 5, 54, 0, 0, 197, 198, 3, 20, 10, 0, 198, 199, 7, 0, 0, 0, 199,
        200, 3, 12, 6, 0, 200, 201, 3, 24, 12, 0, 201, 215, 1, 0, 0, 0, 202, 204, 3, 4, 2, 0, 203,
        202, 1, 0, 0, 0, 204, 207, 1, 0, 0, 0, 205, 203, 1, 0, 0, 0, 205, 206, 1, 0, 0, 0, 206,
        208, 1, 0, 0, 0, 207, 205, 1, 0, 0, 0, 208, 209, 5, 17, 0, 0, 209, 210, 3, 12, 6, 0, 210,
        211, 5, 54, 0, 0, 211, 212, 3, 20, 10, 0, 212, 213, 3, 24, 12, 0, 213, 215, 1, 0, 0, 0,
        214, 192, 1, 0, 0, 0, 214, 205, 1, 0, 0, 0, 215, 19, 1, 0, 0, 0, 216, 217, 5, 9, 0, 0, 217,
        222, 3, 22, 11, 0, 218, 219, 5, 14, 0, 0, 219, 221, 3, 22, 11, 0, 220, 218, 1, 0, 0, 0,
        221, 224, 1, 0, 0, 0, 222, 220, 1, 0, 0, 0, 222, 223, 1, 0, 0, 0, 223, 225, 1, 0, 0, 0,
        224, 222, 1, 0, 0, 0, 225, 226, 5, 10, 0, 0, 226, 229, 1, 0, 0, 0, 227, 229, 5, 3, 0, 0,
        228, 216, 1, 0, 0, 0, 228, 227, 1, 0, 0, 0, 229, 21, 1, 0, 0, 0, 230, 231, 5, 54, 0, 0,
        231, 232, 5, 2, 0, 0, 232, 237, 3, 12, 6, 0, 233, 234, 3, 12, 6, 0, 234, 235, 5, 54, 0,
        0, 235, 237, 1, 0, 0, 0, 236, 230, 1, 0, 0, 0, 236, 233, 1, 0, 0, 0, 237, 23, 1, 0, 0, 0,
        238, 242, 5, 11, 0, 0, 239, 241, 3, 26, 13, 0, 240, 239, 1, 0, 0, 0, 241, 244, 1, 0, 0,
        0, 242, 240, 1, 0, 0, 0, 242, 243, 1, 0, 0, 0, 243, 245, 1, 0, 0, 0, 244, 242, 1, 0, 0,
        0, 245, 246, 5, 12, 0, 0, 246, 25, 1, 0, 0, 0, 247, 275, 3, 42, 21, 0, 248, 275, 3, 38,
        19, 0, 249, 275, 3, 32, 16, 0, 250, 275, 3, 36, 18, 0, 251, 253, 3, 46, 23, 0, 252, 254,
        5, 13, 0, 0, 253, 252, 1, 0, 0, 0, 253, 254, 1, 0, 0, 0, 254, 275, 1, 0, 0, 0, 255, 257,
        3, 52, 26, 0, 256, 258, 5, 13, 0, 0, 257, 256, 1, 0, 0, 0, 257, 258, 1, 0, 0, 0, 258, 275,
        1, 0, 0, 0, 259, 261, 3, 48, 24, 0, 260, 262, 5, 13, 0, 0, 261, 260, 1, 0, 0, 0, 261, 262,
        1, 0, 0, 0, 262, 275, 1, 0, 0, 0, 263, 275, 3, 24, 12, 0, 264, 275, 3, 50, 25, 0, 265,
        267, 3, 28, 14, 0, 266, 268, 5, 13, 0, 0, 267, 266, 1, 0, 0, 0, 267, 268, 1, 0, 0, 0, 268,
        275, 1, 0, 0, 0, 269, 271, 3, 30, 15, 0, 270, 272, 5, 13, 0, 0, 271, 270, 1, 0, 0, 0, 271,
        272, 1, 0, 0, 0, 272, 275, 1, 0, 0, 0, 273, 275, 3, 16, 8, 0, 274, 247, 1, 0, 0, 0, 274,
        248, 1, 0, 0, 0, 274, 249, 1, 0, 0, 0, 274, 250, 1, 0, 0, 0, 274, 251, 1, 0, 0, 0, 274,
        255, 1, 0, 0, 0, 274, 259, 1, 0, 0, 0, 274, 263, 1, 0, 0, 0, 274, 264, 1, 0, 0, 0, 274,
        265, 1, 0, 0, 0, 274, 269, 1, 0, 0, 0, 274, 273, 1, 0, 0, 0, 275, 27, 1, 0, 0, 0, 276, 277,
        5, 33, 0, 0, 277, 29, 1, 0, 0, 0, 278, 279, 5, 34, 0, 0, 279, 31, 1, 0, 0, 0, 280, 281,
        5, 24, 0, 0, 281, 282, 5, 9, 0, 0, 282, 283, 3, 34, 17, 0, 283, 284, 5, 10, 0, 0, 284,
        285, 3, 24, 12, 0, 285, 295, 1, 0, 0, 0, 286, 287, 5, 24, 0, 0, 287, 288, 5, 9, 0, 0, 288,
        289, 5, 54, 0, 0, 289, 290, 5, 2, 0, 0, 290, 291, 3, 52, 26, 0, 291, 292, 5, 10, 0, 0,
        292, 293, 3, 24, 12, 0, 293, 295, 1, 0, 0, 0, 294, 280, 1, 0, 0, 0, 294, 286, 1, 0, 0,
        0, 295, 33, 1, 0, 0, 0, 296, 298, 3, 44, 22, 0, 297, 296, 1, 0, 0, 0, 297, 298, 1, 0, 0,
        0, 298, 299, 1, 0, 0, 0, 299, 301, 5, 13, 0, 0, 300, 302, 3, 52, 26, 0, 301, 300, 1, 0,
        0, 0, 301, 302, 1, 0, 0, 0, 302, 303, 1, 0, 0, 0, 303, 305, 5, 13, 0, 0, 304, 306, 3, 46,
        23, 0, 305, 304, 1, 0, 0, 0, 305, 306, 1, 0, 0, 0, 306, 35, 1, 0, 0, 0, 307, 308, 5, 25,
        0, 0, 308, 309, 5, 9, 0, 0, 309, 310, 3, 52, 26, 0, 310, 311, 5, 10, 0, 0, 311, 312, 3,
        24, 12, 0, 312, 37, 1, 0, 0, 0, 313, 314, 5, 4, 0, 0, 314, 315, 5, 54, 0, 0, 315, 316,
        5, 2, 0, 0, 316, 317, 3, 12, 6, 0, 317, 318, 1, 0, 0, 0, 318, 319, 5, 50, 0, 0, 319, 320,
        3, 52, 26, 0, 320, 322, 1, 0, 0, 0, 321, 323, 5, 13, 0, 0, 322, 321, 1, 0, 0, 0, 322, 323,
        1, 0, 0, 0, 323, 334, 1, 0, 0, 0, 324, 325, 5, 4, 0, 0, 325, 326, 3, 12, 6, 0, 326, 327,
        5, 54, 0, 0, 327, 328, 5, 50, 0, 0, 328, 329, 3, 52, 26, 0, 329, 331, 1, 0, 0, 0, 330,
        332, 5, 13, 0, 0, 331, 330, 1, 0, 0, 0, 331, 332, 1, 0, 0, 0, 332, 334, 1, 0, 0, 0, 333,
        313, 1, 0, 0, 0, 333, 324, 1, 0, 0, 0, 334, 39, 1, 0, 0, 0, 335, 336, 5, 54, 0, 0, 336,
        337, 5, 2, 0, 0, 337, 338, 3, 12, 6, 0, 338, 340, 1, 0, 0, 0, 339, 341, 5, 5, 0, 0, 340,
        339, 1, 0, 0, 0, 340, 341, 1, 0, 0, 0, 341, 344, 1, 0, 0, 0, 342, 343, 5, 50, 0, 0, 343,
        345, 3, 52, 26, 0, 344, 342, 1, 0, 0, 0, 344, 345, 1, 0, 0, 0, 345, 356, 1, 0, 0, 0, 346,
        347, 3, 12, 6, 0, 347, 349, 5, 54, 0, 0, 348, 350, 5, 5, 0, 0, 349, 348, 1, 0, 0, 0, 349,
        350, 1, 0, 0, 0, 350, 353, 1, 0, 0, 0, 351, 352, 5, 50, 0, 0, 352, 354, 3, 52, 26, 0, 353,
        351, 1, 0, 0, 0, 353, 354, 1, 0, 0, 0, 354, 356, 1, 0, 0, 0, 355, 335, 1, 0, 0, 0, 355,
        346, 1, 0, 0, 0, 356, 41, 1, 0, 0, 0, 357, 358, 5, 22, 0, 0, 358, 360, 3, 40, 20, 0, 359,
        361, 5, 13, 0, 0, 360, 359, 1, 0, 0, 0, 360, 361, 1, 0, 0, 0, 361, 367, 1, 0, 0, 0, 362,
        364, 3, 40, 20, 0, 363, 365, 5, 13, 0, 0, 364, 363, 1, 0, 0, 0, 364, 365, 1, 0, 0, 0, 365,
        367, 1, 0, 0, 0, 366, 357, 1, 0, 0, 0, 366, 362, 1, 0, 0, 0, 367, 43, 1, 0, 0, 0, 368, 369,
        5, 22, 0, 0, 369, 372, 3, 40, 20, 0, 370, 372, 3, 40, 20, 0, 371, 368, 1, 0, 0, 0, 371,
        370, 1, 0, 0, 0, 372, 45, 1, 0, 0, 0, 373, 374, 5, 54, 0, 0, 374, 375, 5, 50, 0, 0, 375,
        376, 3, 52, 26, 0, 376, 47, 1, 0, 0, 0, 377, 379, 5, 23, 0, 0, 378, 380, 3, 52, 26, 0,
        379, 378, 1, 0, 0, 0, 379, 380, 1, 0, 0, 0, 380, 49, 1, 0, 0, 0, 381, 382, 5, 26, 0, 0,
        382, 383, 5, 9, 0, 0, 383, 384, 3, 52, 26, 0, 384, 385, 5, 10, 0, 0, 385, 388, 3, 24,
        12, 0, 386, 387, 5, 27, 0, 0, 387, 389, 3, 24, 12, 0, 388, 386, 1, 0, 0, 0, 388, 389,
        1, 0, 0, 0, 389, 51, 1, 0, 0, 0, 390, 391, 6, 26, -1, 0, 391, 392, 5, 54, 0, 0, 392, 399,
        3, 56, 28, 0, 393, 399, 3, 54, 27, 0, 394, 395, 5, 43, 0, 0, 395, 399, 3, 52, 26, 7, 396,
        397, 5, 38, 0, 0, 397, 399, 3, 52, 26, 6, 398, 390, 1, 0, 0, 0, 398, 393, 1, 0, 0, 0, 398,
        394, 1, 0, 0, 0, 398, 396, 1, 0, 0, 0, 399, 424, 1, 0, 0, 0, 400, 401, 10, 5, 0, 0, 401,
        402, 7, 1, 0, 0, 402, 423, 3, 52, 26, 6, 403, 404, 10, 4, 0, 0, 404, 405, 7, 2, 0, 0, 405,
        423, 3, 52, 26, 5, 406, 407, 10, 3, 0, 0, 407, 408, 7, 3, 0, 0, 408, 423, 3, 52, 26, 4,
        409, 410, 10, 2, 0, 0, 410, 411, 5, 48, 0, 0, 411, 423, 3, 52, 26, 3, 412, 413, 10, 1,
        0, 0, 413, 414, 5, 49, 0, 0, 414, 423, 3, 52, 26, 2, 415, 416, 10, 11, 0, 0, 416, 417,
        5, 6, 0, 0, 417, 418, 5, 54, 0, 0, 418, 423, 3, 56, 28, 0, 419, 420, 10, 10, 0, 0, 420,
        421, 5, 6, 0, 0, 421, 423, 5, 54, 0, 0, 422, 400, 1, 0, 0, 0, 422, 403, 1, 0, 0, 0, 422,
        406, 1, 0, 0, 0, 422, 409, 1, 0, 0, 0, 422, 412, 1, 0, 0, 0, 422, 415, 1, 0, 0, 0, 422,
        419, 1, 0, 0, 0, 423, 426, 1, 0, 0, 0, 424, 422, 1, 0, 0, 0, 424, 425, 1, 0, 0, 0, 425,
        53, 1, 0, 0, 0, 426, 424, 1, 0, 0, 0, 427, 437, 5, 54, 0, 0, 428, 437, 3, 60, 30, 0, 429,
        430, 5, 9, 0, 0, 430, 431, 3, 52, 26, 0, 431, 432, 5, 10, 0, 0, 432, 437, 1, 0, 0, 0, 433,
        434, 5, 28, 0, 0, 434, 435, 5, 54, 0, 0, 435, 437, 3, 56, 28, 0, 436, 427, 1, 0, 0, 0,
        436, 428, 1, 0, 0, 0, 436, 429, 1, 0, 0, 0, 436, 433, 1, 0, 0, 0, 437, 55, 1, 0, 0, 0, 438,
        440, 5, 9, 0, 0, 439, 441, 3, 58, 29, 0, 440, 439, 1, 0, 0, 0, 440, 441, 1, 0, 0, 0, 441,
        442, 1, 0, 0, 0, 442, 445, 5, 10, 0, 0, 443, 445, 5, 3, 0, 0, 444, 438, 1, 0, 0, 0, 444,
        443, 1, 0, 0, 0, 445, 57, 1, 0, 0, 0, 446, 451, 3, 52, 26, 0, 447, 448, 5, 14, 0, 0, 448,
        450, 3, 52, 26, 0, 449, 447, 1, 0, 0, 0, 450, 453, 1, 0, 0, 0, 451, 449, 1, 0, 0, 0, 451,
        452, 1, 0, 0, 0, 452, 59, 1, 0, 0, 0, 453, 451, 1, 0, 0, 0, 454, 455, 7, 4, 0, 0, 455, 61,
        1, 0, 0, 0, 56, 65, 73, 75, 83, 91, 98, 102, 108, 110, 118, 125, 131, 139, 149, 158,
        164, 178, 187, 192, 205, 214, 222, 228, 236, 242, 253, 257, 261, 267, 271, 274,
        294, 297, 301, 305, 322, 331, 333, 340, 344, 349, 353, 355, 360, 364, 366, 371,
        379, 388, 398, 422, 424, 436, 440, 444, 451
    ]


class transpilerParser(Parser):
    grammarFileName = "transpiler.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = ["<INVALID>", "'@'", "':'", "'()'", "'const'", "'?'",
                    "'.'", "'<='", "'>='", "'('", "')'", "'{'", "'}'",
                    "';'", "','", "'include'", "'func'", "'method'", "'class'",
                    "'interface'", "'extends'", "'implements'", "'var'",
                    "'return'", "'for'", "'while'", "'if'", "'else'", "'new'",
                    "'true'", "'false'", "'null'", "'in'", "'break'", "'continue'",
                    "<INVALID>", "'->'", "'::'", "'!'", "'*'", "'/'", "'%'",
                    "'+'", "'-'", "'>'", "'<'", "'=='", "'!='", "<INVALID>",
                    "<INVALID>", "'='"]

    symbolicNames = ["<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>",
                     "<INVALID>", "LPAREN", "RPAREN", "LBRACE", "RBRACE",
                     "SEMI", "COMMA", "INCULDE", "FUNC", "METHOD", "CLASS",
                     "INTERFACE", "EXTENDS", "IMPLEMENTS", "VAR", "RETURN",
                     "FOR", "WHILE", "IF", "ELSE", "NEW", "TRUE", "FALSE",
                     "NULL", "IN", "BREAK", "CONTINUE", "CMD", "ARROW",
                     "DOUBLE_COLON", "NOT", "MUL", "DIV", "MOD", "ADD",
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
    RULE_functionDecl = 8
    RULE_methodDecl = 9
    RULE_paramList = 10
    RULE_paramDecl = 11
    RULE_block = 12
    RULE_statement = 13
    RULE_breakStmt = 14
    RULE_continueStmt = 15
    RULE_forStmt = 16
    RULE_forControl = 17
    RULE_whileStmt = 18
    RULE_constDecl = 19
    RULE_varDeclaration = 20
    RULE_varDecl = 21
    RULE_forLoopVarDecl = 22
    RULE_assignment = 23
    RULE_returnStmt = 24
    RULE_ifStmt = 25
    RULE_expr = 26
    RULE_primary = 27
    RULE_argumentList = 28
    RULE_exprList = 29
    RULE_literal = 30

    ruleNames = ["program", "includeStmt", "annotation", "classDecl",
                 "interfaceDecl", "interfaceMethodDecl", "type", "typeList",
                 "functionDecl", "methodDecl", "paramList", "paramDecl",
                 "block", "statement", "breakStmt", "continueStmt", "forStmt",
                 "forControl", "whileStmt", "constDecl", "varDeclaration",
                 "varDecl", "forLoopVarDecl", "assignment", "returnStmt",
                 "ifStmt", "expr", "primary", "argumentList", "exprList",
                 "literal"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    LPAREN = 9
    RPAREN = 10
    LBRACE = 11
    RBRACE = 12
    SEMI = 13
    COMMA = 14
    INCULDE = 15
    FUNC = 16
    METHOD = 17
    CLASS = 18
    INTERFACE = 19
    EXTENDS = 20
    IMPLEMENTS = 21
    VAR = 22
    RETURN = 23
    FOR = 24
    WHILE = 25
    IF = 26
    ELSE = 27
    NEW = 28
    TRUE = 29
    FALSE = 30
    NULL = 31
    IN = 32
    BREAK = 33
    CONTINUE = 34
    CMD = 35
    ARROW = 36
    DOUBLE_COLON = 37
    NOT = 38
    MUL = 39
    DIV = 40
    MOD = 41
    ADD = 42
    SUB = 43
    GT = 44
    LT = 45
    EQ = 46
    NEQ = 47
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
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 15:
                self.state = 62
                self.includeStmt()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18014398514528274) != 0):
                self.state = 73
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input, 1, self._ctx)
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
                    pass

                elif la_ == 5:
                    self.state = 72
                    self.constDecl()
                    pass

                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 78
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

        def INCULDE(self):
            return self.getToken(transpilerParser.INCULDE, 0)

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
            self.state = 80
            self.match(transpilerParser.INCULDE)
            self.state = 81
            self.literal()
            self.state = 83
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 13:
                self.state = 82
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
            self.state = 85
            self.match(transpilerParser.T__0)
            self.state = 86
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
            self.state = 91
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 88
                self.annotation()
                self.state = 93
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 94
            self.match(transpilerParser.CLASS)
            self.state = 95
            self.match(transpilerParser.ID)
            self.state = 98
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 20:
                self.state = 96
                self.match(transpilerParser.EXTENDS)
                self.state = 97
                self.type_()

            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 21:
                self.state = 100
                self.match(transpilerParser.IMPLEMENTS)
                self.state = 101
                self.type_()

            self.state = 104
            self.match(transpilerParser.LBRACE)
            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 18014398513807378) != 0):
                self.state = 108
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [22, 54]:
                    self.state = 105
                    self.varDecl()
                    pass
                elif token in [4]:
                    self.state = 106
                    self.constDecl()
                    pass
                elif token in [1, 17]:
                    self.state = 107
                    self.methodDecl()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 113
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

        def interfaceMethodDecl(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.InterfaceMethodDeclContext)
            else:
                return self.getTypedRuleContext(transpilerParser.InterfaceMethodDeclContext, i)

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
            self.state = 118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 115
                self.annotation()
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 121
            self.match(transpilerParser.INTERFACE)
            self.state = 122
            self.match(transpilerParser.ID)
            self.state = 125
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 20:
                self.state = 123
                self.match(transpilerParser.EXTENDS)
                self.state = 124
                self.type_()

            self.state = 127
            self.match(transpilerParser.LBRACE)
            self.state = 131
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1 or _la == 17:
                self.state = 128
                self.interfaceMethodDecl()
                self.state = 133
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 134
            self.match(transpilerParser.RBRACE)
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
            return self.getToken(transpilerParser.METHOD, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def paramList(self):
            return self.getTypedRuleContext(transpilerParser.ParamListContext, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(transpilerParser.AnnotationContext, i)

        def SEMI(self):
            return self.getToken(transpilerParser.SEMI, 0)

        def getRuleIndex(self):
            return transpilerParser.RULE_interfaceMethodDecl

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

        localctx = transpilerParser.InterfaceMethodDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_interfaceMethodDecl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 1:
                self.state = 136
                self.annotation()
                self.state = 141
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 142
            self.match(transpilerParser.METHOD)
            self.state = 143
            self.match(transpilerParser.ID)
            self.state = 144
            self.paramList()

            self.state = 145
            self.match(transpilerParser.T__1)
            self.state = 146
            self.type_()
            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 13:
                self.state = 148
                self.match(transpilerParser.SEMI)


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
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.match(transpilerParser.ID)
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
                return self.getTypedRuleContexts(transpilerParser.TypeContext)
            else:
                return self.getTypedRuleContext(transpilerParser.TypeContext, i)

        def COMMA(self, i: int = None):
            if i is None:
                return self.getTokens(transpilerParser.COMMA)
            else:
                return self.getToken(transpilerParser.COMMA, i)

        def getRuleIndex(self):
            return transpilerParser.RULE_typeList

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

        localctx = transpilerParser.TypeListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_typeList)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            self.type_()
            self.state = 158
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 14:
                self.state = 154
                self.match(transpilerParser.COMMA)
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

    class FunctionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNC(self):
            return self.getToken(transpilerParser.FUNC, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def block(self):
            return self.getTypedRuleContext(transpilerParser.BlockContext, 0)

        def paramList(self):
            return self.getTypedRuleContext(transpilerParser.ParamListContext, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(transpilerParser.AnnotationContext, i)

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

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
        self.enterRule(localctx, 16, self.RULE_functionDecl)
        self._la = 0  # Token type
        try:
            self.state = 187
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 17, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 164
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 161
                    self.annotation()
                    self.state = 166
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 167
                self.match(transpilerParser.FUNC)
                self.state = 168
                self.match(transpilerParser.ID)

                self.state = 169
                self.paramList()

                self.state = 170
                _la = self._input.LA(1)
                if not (_la == 2 or _la == 36):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 171
                self.type_()
                self.state = 173
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 178
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 175
                    self.annotation()
                    self.state = 180
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 181
                self.match(transpilerParser.FUNC)
                self.state = 182
                self.type_()
                self.state = 183
                self.match(transpilerParser.ID)

                self.state = 184
                self.paramList()
                self.state = 185
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

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def block(self):
            return self.getTypedRuleContext(transpilerParser.BlockContext, 0)

        def ARROW(self):
            return self.getToken(transpilerParser.ARROW, 0)

        def annotation(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(transpilerParser.AnnotationContext)
            else:
                return self.getTypedRuleContext(transpilerParser.AnnotationContext, i)

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
        self.enterRule(localctx, 18, self.RULE_methodDecl)
        self._la = 0  # Token type
        try:
            self.state = 214
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 20, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 192
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 189
                    self.annotation()
                    self.state = 194
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 195
                self.match(transpilerParser.METHOD)
                self.state = 196
                self.match(transpilerParser.ID)
                self.state = 197
                self.paramList()
                self.state = 198
                _la = self._input.LA(1)
                if not (_la == 2 or _la == 36):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 199
                self.type_()
                self.state = 200
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 205
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 1:
                    self.state = 202
                    self.annotation()
                    self.state = 207
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 208
                self.match(transpilerParser.METHOD)
                self.state = 209
                self.type_()
                self.state = 210
                self.match(transpilerParser.ID)
                self.state = 211
                self.paramList()
                self.state = 212
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
        self.enterRule(localctx, 20, self.RULE_paramList)
        self._la = 0  # Token type
        try:
            self.state = 228
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 216
                self.match(transpilerParser.LPAREN)

                self.state = 217
                self.paramDecl()
                self.state = 222
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la == 14:
                    self.state = 218
                    self.match(transpilerParser.COMMA)
                    self.state = 219
                    self.paramDecl()
                    self.state = 224
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 225
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 227
                self.match(transpilerParser.T__2)
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
        self.enterRule(localctx, 22, self.RULE_paramDecl)
        try:
            self.state = 236
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 23, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 230
                self.match(transpilerParser.ID)

                self.state = 231
                self.match(transpilerParser.T__1)
                self.state = 232
                self.type_()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 233
                self.type_()
                self.state = 234
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
        self.enterRule(localctx, 24, self.RULE_block)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self.match(transpilerParser.LBRACE)
            self.state = 242
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 33786098102635026) != 0):
                self.state = 239
                self.statement()
                self.state = 244
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 245
            self.match(transpilerParser.RBRACE)
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

        def functionDecl(self):
            return self.getTypedRuleContext(transpilerParser.FunctionDeclContext, 0)

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
        self.enterRule(localctx, 26, self.RULE_statement)
        self._la = 0  # Token type
        try:
            self.state = 274
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 30, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 247
                self.varDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 248
                self.constDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 249
                self.forStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 250
                self.whileStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 251
                self.assignment()
                self.state = 253
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 252
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 255
                self.expr(0)
                self.state = 257
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 256
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 259
                self.returnStmt()
                self.state = 261
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 260
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 263
                self.block()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 264
                self.ifStmt()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 265
                self.breakStmt()
                self.state = 267
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 266
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 269
                self.continueStmt()
                self.state = 271
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 270
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 273
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
        self.enterRule(localctx, 28, self.RULE_breakStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 276
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
        self.enterRule(localctx, 30, self.RULE_continueStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 278
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

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

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
        self.enterRule(localctx, 32, self.RULE_forStmt)
        try:
            self.state = 294
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 31, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 280
                self.match(transpilerParser.FOR)
                self.state = 281
                self.match(transpilerParser.LPAREN)
                self.state = 282
                self.forControl()
                self.state = 283
                self.match(transpilerParser.RPAREN)
                self.state = 284
                self.block()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 286
                self.match(transpilerParser.FOR)
                self.state = 287
                self.match(transpilerParser.LPAREN)
                self.state = 288
                self.match(transpilerParser.ID)
                self.state = 289
                self.match(transpilerParser.T__1)
                self.state = 290
                self.expr(0)
                self.state = 291
                self.match(transpilerParser.RPAREN)
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
        self.enterRule(localctx, 34, self.RULE_forControl)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 297
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 22 or _la == 54:
                self.state = 296
                self.forLoopVarDecl()

            self.state = 299
            self.match(transpilerParser.SEMI)
            self.state = 301
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 33786072202740224) != 0):
                self.state = 300
                self.expr(0)

            self.state = 303
            self.match(transpilerParser.SEMI)
            self.state = 305
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 54:
                self.state = 304
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
        self.enterRule(localctx, 36, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 307
            self.match(transpilerParser.WHILE)
            self.state = 308
            self.match(transpilerParser.LPAREN)
            self.state = 309
            self.expr(0)
            self.state = 310
            self.match(transpilerParser.RPAREN)
            self.state = 311
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
            return self.getToken(transpilerParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

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
        self.enterRule(localctx, 38, self.RULE_constDecl)
        self._la = 0  # Token type
        try:
            self.state = 333
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 37, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 313
                self.match(transpilerParser.T__3)
                self.state = 314
                self.match(transpilerParser.ID)

                self.state = 315
                self.match(transpilerParser.T__1)
                self.state = 316
                self.type_()

                self.state = 318
                self.match(transpilerParser.ASSIGN)
                self.state = 319
                self.expr(0)
                self.state = 322
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 321
                    self.match(transpilerParser.SEMI)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 324
                self.match(transpilerParser.T__3)
                self.state = 325
                self.type_()
                self.state = 326
                self.match(transpilerParser.ID)

                self.state = 327
                self.match(transpilerParser.ASSIGN)
                self.state = 328
                self.expr(0)
                self.state = 331
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 330
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

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def type_(self):
            return self.getTypedRuleContext(transpilerParser.TypeContext, 0)

        def ASSIGN(self):
            return self.getToken(transpilerParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(transpilerParser.ExprContext, 0)

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
        self.enterRule(localctx, 40, self.RULE_varDeclaration)
        self._la = 0  # Token type
        try:
            self.state = 355
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 42, self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 335
                self.match(transpilerParser.ID)

                self.state = 336
                self.match(transpilerParser.T__1)
                self.state = 337
                self.type_()
                self.state = 340
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 5:
                    self.state = 339
                    self.match(transpilerParser.T__4)

                self.state = 344
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 50:
                    self.state = 342
                    self.match(transpilerParser.ASSIGN)
                    self.state = 343
                    self.expr(0)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 346
                self.type_()
                self.state = 347
                self.match(transpilerParser.ID)
                self.state = 349
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 5:
                    self.state = 348
                    self.match(transpilerParser.T__4)

                self.state = 353
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 50:
                    self.state = 351
                    self.match(transpilerParser.ASSIGN)
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
            return self.getToken(transpilerParser.VAR, 0)

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
        self.enterRule(localctx, 42, self.RULE_varDecl)
        self._la = 0  # Token type
        try:
            self.state = 366
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 357
                self.match(transpilerParser.VAR)
                self.state = 358
                self.varDeclaration()
                self.state = 360
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 359
                    self.match(transpilerParser.SEMI)

                pass
            elif token in [54]:
                self.enterOuterAlt(localctx, 2)
                self.state = 362
                self.varDeclaration()
                self.state = 364
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == 13:
                    self.state = 363
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

    class ForLoopVarDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(transpilerParser.VAR, 0)

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
        self.enterRule(localctx, 44, self.RULE_forLoopVarDecl)
        try:
            self.state = 371
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 368
                self.match(transpilerParser.VAR)
                self.state = 369
                self.varDeclaration()
                pass
            elif token in [54]:
                self.enterOuterAlt(localctx, 2)
                self.state = 370
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
        self.enterRule(localctx, 46, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 373
            self.match(transpilerParser.ID)
            self.state = 374
            self.match(transpilerParser.ASSIGN)
            self.state = 375
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
        self.enterRule(localctx, 48, self.RULE_returnStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 377
            self.match(transpilerParser.RETURN)
            self.state = 379
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 47, self._ctx)
            if la_ == 1:
                self.state = 378
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
        self.enterRule(localctx, 50, self.RULE_ifStmt)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 381
            self.match(transpilerParser.IF)
            self.state = 382
            self.match(transpilerParser.LPAREN)
            self.state = 383
            self.expr(0)
            self.state = 384
            self.match(transpilerParser.RPAREN)
            self.state = 385
            self.block()
            self.state = 388
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la == 27:
                self.state = 386
                self.match(transpilerParser.ELSE)
                self.state = 387
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

    class DirectFuncCallContext(ExprContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def argumentList(self):
            return self.getTypedRuleContext(transpilerParser.ArgumentListContext, 0)

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
        _startState = 52
        self.enterRecursionRule(localctx, 52, self.RULE_expr, _p)
        self._la = 0  # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 398
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 49, self._ctx)
            if la_ == 1:
                localctx = transpilerParser.DirectFuncCallContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 391
                self.match(transpilerParser.ID)
                self.state = 392
                self.argumentList()
                pass

            elif la_ == 2:
                localctx = transpilerParser.PrimaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 393
                self.primary()
                pass

            elif la_ == 3:
                localctx = transpilerParser.NegExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 394
                self.match(transpilerParser.SUB)
                self.state = 395
                self.expr(7)
                pass

            elif la_ == 4:
                localctx = transpilerParser.LogicalNotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 396
                self.match(transpilerParser.NOT)
                self.state = 397
                self.expr(6)
                pass

            self._ctx.stop = self._input.LT(-1)
            self.state = 424
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input, 51, self._ctx)
            while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 422
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input, 50, self._ctx)
                    if la_ == 1:
                        localctx = transpilerParser.FactorExprContext(self,
                                                                      transpilerParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 400
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 401
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 3848290697216) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 402
                        self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = transpilerParser.TermExprContext(self, transpilerParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 403
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 404
                        _la = self._input.LA(1)
                        if not (_la == 42 or _la == 43):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 405
                        self.expr(5)
                        pass

                    elif la_ == 3:
                        localctx = transpilerParser.CompareExprContext(self,
                                                                       transpilerParser.ExprContext(self, _parentctx,
                                                                                                    _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 406
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 407
                        _la = self._input.LA(1)
                        if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 263882790666624) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 408
                        self.expr(4)
                        pass

                    elif la_ == 4:
                        localctx = transpilerParser.LogicalAndExprContext(self,
                                                                          transpilerParser.ExprContext(self, _parentctx,
                                                                                                       _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 409
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 410
                        self.match(transpilerParser.AND)
                        self.state = 411
                        self.expr(3)
                        pass

                    elif la_ == 5:
                        localctx = transpilerParser.LogicalOrExprContext(self,
                                                                         transpilerParser.ExprContext(self, _parentctx,
                                                                                                      _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 412
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 413
                        self.match(transpilerParser.OR)
                        self.state = 414
                        self.expr(2)
                        pass

                    elif la_ == 6:
                        localctx = transpilerParser.MethodCallContext(self,
                                                                      transpilerParser.ExprContext(self, _parentctx,
                                                                                                   _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 415
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 416
                        self.match(transpilerParser.T__5)
                        self.state = 417
                        self.match(transpilerParser.ID)
                        self.state = 418
                        self.argumentList()
                        pass

                    elif la_ == 7:
                        localctx = transpilerParser.MemberAccessContext(self,
                                                                        transpilerParser.ExprContext(self, _parentctx,
                                                                                                     _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 419
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 420
                        self.match(transpilerParser.T__5)
                        self.state = 421
                        self.match(transpilerParser.ID)
                        pass

                self.state = 426
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 51, self._ctx)

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

    class NewObjectExprContext(PrimaryContext):

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NEW(self):
            return self.getToken(transpilerParser.NEW, 0)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

        def argumentList(self):
            return self.getTypedRuleContext(transpilerParser.ArgumentListContext, 0)

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

        def __init__(self, parser, ctx: ParserRuleContext):  # actually a transpilerParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(transpilerParser.ID, 0)

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
            self.state = 436
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [54]:
                localctx = transpilerParser.VarExprContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 427
                self.match(transpilerParser.ID)
                pass
            elif token in [29, 30, 31, 51, 52, 53]:
                localctx = transpilerParser.LiteralExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 428
                self.literal()
                pass
            elif token in [9]:
                localctx = transpilerParser.ParenExprContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 429
                self.match(transpilerParser.LPAREN)
                self.state = 430
                self.expr(0)
                self.state = 431
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [28]:
                localctx = transpilerParser.NewObjectExprContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 433
                self.match(transpilerParser.NEW)
                self.state = 434
                self.match(transpilerParser.ID)
                self.state = 435
                self.argumentList()
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
            self.state = 444
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                self.enterOuterAlt(localctx, 1)
                self.state = 438
                self.match(transpilerParser.LPAREN)
                self.state = 440
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 33786072202740224) != 0):
                    self.state = 439
                    self.exprList()

                self.state = 442
                self.match(transpilerParser.RPAREN)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 443
                self.match(transpilerParser.T__2)
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
            self.state = 446
            self.expr(0)
            self.state = 451
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la == 14:
                self.state = 447
                self.match(transpilerParser.COMMA)
                self.state = 448
                self.expr(0)
                self.state = 453
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
            self.state = 454
            _la = self._input.LA(1)
            if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 15762602453893120) != 0)):
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
