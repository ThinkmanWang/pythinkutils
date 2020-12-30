# -*- coding: utf-8 -*-

from pythinkutils.common.StringUtils import *

class CSVUtils(object):

    @classmethod
    def csv_to_list(cls, szCsvPath):
        with open(szCsvPath, 'r', encoding="UTF-8-sig") as csvFile:
            nLine = 0
            lstHeader = None
            lstRet = []
            for szLine in csvFile:
                szLine = szLine.replace("\t", "")
                nLine += 1

                if 1 == nLine:  # header
                    lstHeader = szLine.split(",")
                    # for szHeader in lstHeader:
                    #     szHeader = szHeader.strip()
                else:
                    dictItem = {}
                    lstItem = szLine.split(",")
                    nPos = 0
                    for szItem in lstItem:
                        if nPos >= len(lstHeader):
                            continue

                        dictItem[lstHeader[nPos].strip()] = szItem.strip()
                        nPos += 1

                    lstRet.append(dictItem)

            return lstRet

    @classmethod
    def dictlist_2_csv(cls, lstData, szFilePath, szHeader = None):
        def read_header_from_dict(dictItem):
            lstHeader = []
            for szKey in dictItem.keys():
                lstHeader.append(szKey)

            return lstHeader


        if is_empty_string(szFilePath) or lstData is None or len(lstData) <= 0:
            return

        lstHeader = read_header_from_dict(lstData[0])
        if is_empty_string(szHeader):
            szHeader = ""
            nPos = 0
            for _szHeader in lstHeader:
                if 0 == nPos:
                    szHeader += _szHeader
                else:
                    szHeader += ","+_szHeader
                nPos += 1
        else:
            pass

        szHeader = szHeader.strip()
        szHeader += "\n"

        with open(szFilePath, 'w', encoding="UTF-8-sig") as csvFile:
            csvFile.write(szHeader)

            for dictItem in lstData:
                szLine = ""
                nPos = 0
                for _header in lstHeader:
                    if 0 == nPos:
                        szLine = "{}".format(dictItem[_header])
                    else:
                        szLine += ",{}".format(dictItem[_header])

                    nPos += 1
                szLine += "\n"
                csvFile.write(szLine)


# lstData = []
# lstData.append({"a":1, "b":2})
# lstData.append({"a":3, "b":4})
# lstData.append({"a":5, "b":6})
# CSVUtils.dictlist_2_csv(lstData, "out.csv")