# -*- coding: utf-8 -*-
import sys

import traceback

import tendo.ansiterm

from colouredprinter.color.ColorConstant import FrontColor, BackgroundColor

from colouredprinter.style.FontStyleConstant import FontStyle


class FontStyleParamError(Exception):
    def __init__(self, message='Illegal param Exception,expected param type is FontStyle'):
        self.message = message


class FrontColorParamError(Exception):
    def __init__(self, message='Illegal param Exception,expected param type is FrontColor'):
        self.message = message


class BackGroundColorParamError(Exception):
    def __init__(self, message='Illegal param Exception,expected param type is BackGroundColor'):
        self.message = message


def printErrorMsg(traceBack, exception):
    printer = Printer()
    printer.setFrontColor(FrontColor.RED)
    printer.print(traceBack + exception.message)
    sys.exit(1)


class Printer:

    def __init__(self):
        pass

    __OUTPUT_PREFIX = '\033['

    __OUTPUT_SUFFIX = '\033[0m'

    __fontStyle = FontStyle.DEFAULT

    __frontColor = FrontColor.DEFAULT

    __backgroundColor = BackgroundColor.DEFAULT

    def setFrontColor(self, frontColor: FrontColor):

        if frontColor not in FrontColor:
            try:
                raise FrontColorParamError()
            except FrontColorParamError as e:
                msg = traceback.format_exc()
                printErrorMsg(msg, e)

        self.__frontColor = frontColor

    def setBackGroundColor(self, backgroundColor: BackgroundColor):

        if backgroundColor not in BackgroundColor:

            try:
                raise BackGroundColorParamError()
            except BackGroundColorParamError as e:
                msg = traceback.format_exc()
                printErrorMsg(msg, e)

        self.__backgroundColor = backgroundColor

    def setFontStyle(self, fontStyle: FontStyle):

        if fontStyle not in FontStyle:
            try:
                raise FontStyleParamError()
            except FontStyleParamError as e:
                msg = traceback.format_exc()
                printErrorMsg(msg, e)

        self.__fontStyle = fontStyle

    def println(self, obj):

        formatStyle = self.__OUTPUT_PREFIX + \
                      str(self.__fontStyle.value) + ';' \
                      + str(self.__frontColor.value) + ';' \
                      + str(self.__backgroundColor.value) + 'm' + \
                      obj + self.__OUTPUT_SUFFIX
        sys.stdout.write(formatStyle)
        sys.stdout.write('\n')

    def print(self, obj):
        formatStyle = self.__OUTPUT_PREFIX + \
                      str(self.__fontStyle.value) + ';' \
                      + str(self.__frontColor.value) + ';' \
                      + str(self.__backgroundColor.value) + 'm' + \
                      obj + self.__OUTPUT_SUFFIX

        sys.stdout.write(formatStyle)

    def reset(self):
        self.setFontStyle(FontStyle.DEFAULT)
        self.setFrontColor(FrontColor.DEFAULT)
        self.setBackGroundColor(BackgroundColor.DEFAULT)
