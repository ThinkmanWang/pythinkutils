# -*- coding: utf-8 -*-

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