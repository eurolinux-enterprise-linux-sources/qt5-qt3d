TEMPLATE = app

TARGET = tst_qsortmethod
QT += core-private 3dcore 3dcore-private 3drender 3drender-private testlib

CONFIG += testcase

SOURCES += tst_qsortmethod.cpp

include(../commons/commons.pri)
