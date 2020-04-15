from PIL import Image
import argparse
import pyqrcode
import numpy as np
import numpy.random
import copy
import os

eps = 1e-9

def hexToByte(hexStr):
    byteList = []
    if len(hexStr) % 2 == 1:
        hexStr = hexStr + "0"
    for i in range(0, len(hexStr), 2):
        byte = int(hexStr[i: i + 2], 16)
        byteList.append(byte)
    return bytes(byteList)

def getColorMap():
    colorList = [

                    ("FFEFFF", "00"),
                    ("FF9AAD", "01"),
                    ("EF559C", "02"),
                    ("FF65AD", "03"),
                    ("FF0063", "04"),
                    ("BD4573", "05"),
                    ("CE0052", "06"),
                    ("9C0031", "07"),
                    ("522031", "08"),

                    ("FFBACE", "10"),
                    ("FF7573", "11"),
                    ("DE3010", "12"),
                    ("FF5542", "13"),
                    ("FF0000", "14"),
                    ("CE6563", "15"),
                    ("BD4542", "16"),
                    ("BD0000", "17"),
                    ("8C2021", "18"),

                    ("DECFBD", "20"),
                    ("FFCF63", "21"),
                    ("DE6521", "22"),
                    ("FFAA21", "23"),
                    ("FF6500", "24"),
                    ("BD8A52", "25"),
                    ("DE4500", "26"),
                    ("BD4500", "27"),
                    ("633010", "28"),

                    ("FFEFDE", "30"),
                    ("FFDFCE", "31"),
                    ("FFCFAD", "32"),
                    ("FFBA8C", "33"),
                    ("FFAA8C", "34"),
                    ("DE8A63", "35"),
                    ("BD6542", "36"),
                    ("9C5531", "37"),
                    ("8C4521", "38"),

                    ("FFCFFF", "40"),
                    ("EF8AFF", "41"),
                    ("CE65DE", "42"),
                    ("BD8ACE", "43"),
                    ("CE00FF", "44"),
                    ("9C659C", "45"),
                    ("8C00AD", "46"),
                    ("520073", "47"),
                    ("310042", "48"),

                    ("FFBAFF", "50"),
                    ("FF9AFF", "51"),
                    ("DE20BD", "52"),
                    ("FF55EF", "53"),
                    ("FF00CE", "54"),
                    ("8C5573", "55"),
                    ("BD009C", "56"),
                    ("8C0063", "57"),
                    ("520042", "58"),

                    ("DEBA9C", "60"),
                    ("CEAA73", "61"),
                    ("734531", "62"),
                    ("AD7542", "63"),
                    ("9C3000", "64"),
                    ("733021", "65"),
                    ("522000", "66"),
                    ("311000", "67"),
                    ("211000", "68"),

                    ("FFFFCE", "70"),
                    ("FFFF73", "71"),
                    ("DEDF21", "72"),
                    ("FFFF00", "73"),
                    ("FFDF00", "74"),
                    ("CEAA00", "75"),
                    ("9C9A00", "76"),
                    ("8C7500", "77"),
                    ("525500", "78"),

                    ("DEBAFF", "80"),
                    ("BD9AEF", "81"),
                    ("6330CE", "82"),
                    ("9C55FF", "83"),
                    ("6300FF", "84"),
                    ("52458C", "85"),
                    ("42009C", "86"),
                    ("210063", "87"),
                    ("211031", "88"),

                    ("BDBAFF", "90"),
                    ("8C9AFF", "91"),
                    ("3130AD", "92"),
                    ("3155EF", "93"),
                    ("0000FF", "94"),
                    ("31308C", "95"),
                    ("0000AD", "96"),
                    ("101063", "97"),
                    ("000021", "98"),

                    ("9CEFBD", "a0"),
                    ("63CF73", "a1"),
                    ("216510", "a2"),
                    ("42AA31", "a3"),
                    ("008A31", "a4"),
                    ("527552", "a5"),
                    ("215500", "a6"),
                    ("103021", "a7"),
                    ("002010", "a8"),

                    ("DEFFBD", "b0"),
                    ("CEFF8C", "b1"),
                    ("8CAA52", "b2"),
                    ("ADDF8C", "b3"),
                    ("8CFF00", "b4"),
                    ("ADBA9C", "b5"),
                    ("63BA00", "b6"),
                    ("529A00", "b7"),
                    ("316500", "b8"),

                    ("BDDFFF", "c0"),
                    ("73CFFF", "c1"),
                    ("31559C", "c2"),
                    ("639AFF", "c3"),
                    ("1075FF", "c4"),
                    ("4275AD", "c5"),
                    ("214573", "c6"),
                    ("002073", "c7"),
                    ("001042", "c8"),

                    ("ADFFFF", "d0"),
                    ("52FFFF", "d1"),
                    ("008ABD", "d2"),
                    ("52BACE", "d3"),
                    ("00CFFF", "d4"),
                    ("429AAD", "d5"),
                    ("00658C", "d6"),
                    ("004552", "d7"),
                    ("002031", "d8"),

                    ("CEFFEF", "e0"),
                    ("ADEFDE", "e1"),
                    ("31CFAD", "e2"),
                    ("52EFBD", "e3"),
                    ("00FFCE", "e4"),
                    ("73AAAD", "e5"),
                    ("00AA9C", "e6"),
                    ("008A73", "e7"),
                    ("004531", "e8"),

                    ("ADFFAD", "f0"),
                    ("73FF73", "f1"),
                    ("63DF42", "f2"),
                    ("00FF00", "f3"),
                    ("21DF21", "f4"),
                    ("52BA52", "f5"),
                    ("00BA00", "f6"),
                    ("008A00", "f7"),
                    ("214521", "f8"),

                    ("FFFFFF", "0f"),
                    ("ECECEC", "1f"),
                    ("DADADA", "2f"),
                    ("C8C8C8", "3f"),
                    ("B6B6B6", "4f"),
                    ("A3A3A3", "5f"),
                    ("919191", "6f"),
                    ("7F7F7F", "7f"),
                    ("6D6D6D", "8f"),
                    ("5B5B5B", "9f"),
                    ("484848", "af"),
                    ("363636", "bf"),
                    ("242424", "cf"),
                    ("121212", "df"),
                    ("000000", "ef")]

    colorTable = []
    for color, label in colorList:
        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)
        colorTable.append((np.array([red, green, blue], dtype = np.int), label))

    return colorTable

def getClosest(newColor, colors):
    weights = np.array([1, 1, 1])
    disVec = np.dot((newColor - colors) ** 2, weights)
    pos = np.argmin(disVec)
    return colors[pos], pos, np.dot((newColor - colors[pos]) ** 2, weights)

def getCenters(colors, candidates, nattempts):
    colors = np.reshape(colors, (-1, 3))
    size = len(candidates)
    retCenters = None
    minTotDis = float('inf')
    counts = [0] * size
    for color in colors:
            color, pos, dis = getClosest(color, candidates)
            counts[pos] += 1
    counts = np.array(counts)
    for k_means_attempt in range(nattempts):
        probs = counts / counts.sum()

        #random initialization
        """
        indices = np.random.choice(size, 15, p = probs, replace = False)
        centers = candidates[indices]
        """

        #k-means++-type initialization
        centers = []
        for i in range(15):
            centers.append(candidates[np.random.choice(size, 1, p = probs)[0]])
            for s in range(size):
                _, _, dis = getClosest(candidates[s], np.array(centers))
                probs[s] = dis
            probs = probs / probs.sum()
        centers = np.array(centers)

        previousTotDis = float('inf')
        while True:
            buckets = [[] for i in range(15)]
            reborns = []
            for color in colors:
                _, pos, dis1 = getClosest(color, centers)
                candidate, _, dis2 = getClosest(color, candidates)
                if dis2 < dis1 - eps:
                    reborns.append(candidate)
                buckets[pos].append(color)
            for i in range(15):
                if len(buckets[i]) == 0:
                    numReborns = len(reborns)
                    if numReborns != 0:
                        centers[i] = reborns[np.random.randint(numReborns)]
                else:
                    meanColor = np.array(buckets[i]).mean(axis = 0)
                    centers[i], _, _ = getClosest(meanColor, candidates)
            currentTotDis = 0
            for color in colors:
                _, _, dis = getClosest(color, centers)
                currentTotDis += dis
            assert(currentTotDis < previousTotDis + eps)
            if currentTotDis < previousTotDis - eps:
                previousTotDis = currentTotDis
            else:
                break
        print("attempt:", str(k_means_attempt + 1) + "/" + str(nattempts), "loss:", currentTotDis)
        if currentTotDis < minTotDis:
            minTotDis = currentTotDis
            retCenters = copy.copy(centers)

    print(minTotDis)
    return retCenters

def getPalette(centers, colorTable):
    paletteList = []
    for center in centers:
        color, pos, _ = getClosest(center, [color for (color, label) in colorTable])
        paletteList.append((color, colorTable[pos][1]))
    return paletteList

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('nrows', type = int, help = 'number of rows')
    parser.add_argument('ncols', type = int, help = 'number of columns')
    parser.add_argument('filename', type = str, help = 'filename for the input image')
    parser.add_argument('--nattempts', type = int, default = 100, help = 'number of k-means attempts')

    args = parser.parse_args()

    nrows = args.nrows
    ncols = args.ncols

    image = Image.open(args.filename)

    resizedImage = np.array(image.resize((ncols * 32, nrows * 32), resample = Image.LANCZOS), dtype = np.int)
    newImage = copy.copy(resizedImage)

    colorTable = getColorMap() # colorTable: list of (color, label)
    allColors = np.array([color for (color, label) in colorTable], dtype = np.int)
    centers = getCenters(resizedImage, allColors, args.nattempts) # centers: list of color
    paletteList = getPalette(centers, colorTable) # paletteList: list of (color, label)

    palette = ""
    for color, label in paletteList:
        palette = palette + label

    for i in range(nrows * 32):
        for j in range(ncols * 32):
            newImage[i][j], _, _ = getClosest(newImage[i][j], [color for (color, label) in paletteList])

    title = "6100" * 20
    author = "6100" * 9
    place = "6100" * 9
    prefix = title + "0000b6ec" + author + "000044c5" + place + "00001931"

    interfix = "cc0a090000"
    qrVec = [[None] * ncols for _ in range(nrows)]

    for row in range(nrows):
        for col in range(ncols):
            canvas = ""
            for i in range(0, 32):
                for j in range(0, 16):
                    color, index, _ = getClosest(newImage[row * 32 + i][col * 32 + j * 2 + 1], [color for (color, label) in paletteList])
                    canvas = canvas + hex(index)[2:]
                    color, index, _ = getClosest(newImage[row * 32 + i][col * 32 + j * 2], [color for (color, label) in paletteList])
                    canvas = canvas + hex(index)[2:]
            byteArray = hexToByte(prefix + palette + interfix + canvas)
            code = pyqrcode.QRCode(byteArray, error = 'M')
            tmpFilename = "qrcode_" + str(row) + "_" + str(col) + ".png"
            code.png(tmpFilename)
            qrVec[row][col] = np.array(Image.open(tmpFilename), dtype = np.int)
            os.remove(tmpFilename)

    padding = 6
    qrSize = len(qrVec[row][col])
    preview = np.ones((nrows * 32 + (nrows - 1) * padding, ncols * 32 + (ncols - 1) * padding, 3), dtype = np.int) * 255
    debug = np.ones((nrows * 32 + (nrows - 1) * padding, ncols * 32 + (ncols - 1) * padding, 3), dtype = np.int) * 255
    qrcodes = np.ones((nrows * qrSize + (nrows - 1) * padding, ncols * qrSize + (ncols - 1) * padding), dtype = np.int)

    for row in range(nrows):
        for col in range(ncols):
            for i in range(0, 32):
                for j in range(0, 32):
                    preview[row * (32 + padding) + i][col * (32 + padding) + j] = newImage[row * 32 + i][col * 32 + j]
                    debug[row * (32 + padding) + i][col * (32 + padding) + j], _, _ = getClosest(resizedImage[row * 32 + i][col * 32 + j], allColors)

    for row in range(nrows):
        for col in range(ncols):
            for i in range(0, qrSize):
                for j in range(0, qrSize):
                    qrcodes[row * (qrSize + padding) + i][col * (qrSize + padding) + j] = qrVec[row][col][i][j]

    preview = np.repeat(preview, 10, axis = 0)
    preview = np.repeat(preview, 10, axis = 1)
    Image.fromarray(preview.astype(np.uint8)).save('preview.png')
    Image.fromarray(debug.astype(np.uint8)).save('debug.png')
    Image.fromarray((qrcodes * 255).astype(np.uint8)).save('qrcodes.png')


if __name__ ==  '__main__':
    main()


