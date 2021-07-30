# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class CentroidTracker():
    def __init__(self, maxDisappeared=50):

        self.nextObjectID = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        # 存储给定对象被允许标记为“消失”的最大连续帧数，直到我们需要从跟踪中注销该对象
        self.maxDisappeared = maxDisappeared

    def register(self, centroid):

        # 注册对象时，我们使用下一个可用的对象ID来存储质心
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1

    def deregister(self, objectID):

        # 要注销注册对象ID，我们从两个字典中都删除了该对象ID
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update(self, rects):

        # 检查输入边界框矩形的列表是否为空
        if len(rects) == 0:
            # 遍历任何现有的跟踪对象并将其标记为消失
            for objectID in list(self.disappeared.keys()):
                self.disappeared[objectID] += 1
                # 如果达到给定对象被标记为丢失的最大连续帧数，请取消注册
                if self.disappeared[objectID] > self.maxDisappeared:
                    self.deregister(objectID)
            # 由于没有质心或跟踪信息要更新，请尽早返回
            return self.objects

        # 初始化当前帧的输入质心数组
        inputCentroids = np.zeros((len(rects), 2), dtype="int")
        # 在边界框矩形上循环
        for (i, (startX, startY, endX, endY)) in enumerate(rects):
            # use the bounding box coordinates to derive the centroid
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            inputCentroids[i] = (cX, cY)

        # 如果我们当前未跟踪任何对象，请输入输入质心并注册每个质心
        if len(self.objects) == 0:
            for i in range(0, len(inputCentroids)):
                self.register(inputCentroids[i])
        # 否则，当前正在跟踪对象，因此我们需要尝试将输入质心与现有对象质心进行匹配
        else:
            # 抓取一组对象ID和相应的质心
            objectIDs = list(self.objects.keys())
            objectCentroids = list(self.objects.values())
            # 分别计算每对对象质心和输入质心之间的距离-我们的目标是将输入质心与现有对象质心匹配
            D = dist.cdist(np.array(objectCentroids), inputCentroids)
            # 为了执行此匹配，我们必须（1）在每行中找到最小值，然后（2）根据行索引的最小值对行索引进行排序，以使具有最小值的行位于索引列表的* front *处
            rows = D.min(axis=1).argsort()
            # 接下来，我们在列上执行类似的过程，方法是在每一列中找到最小值，然后使用先前计算的行索引列表进行排序
            cols = D.argmin(axis=1)[rows]
            # 为了确定是否需要更新，注册或注销对象，我们需要跟踪已经检查过的行索引和列索引
            usedRows = set()
            usedCols = set()

            # 循环遍历（行，列）索引元组的组合
            for (row, col) in zip(rows, cols):
                # 如果我们之前已经检查过行或列的值，请忽略它
                if row in usedRows or col in usedCols:
                    continue
                # 否则，获取当前行的对象ID，设置其新的质心，然后重置消失的计数器
                objectID = objectIDs[row]
                self.objects[objectID] = inputCentroids[col]
                self.disappeared[objectID] = 0
                # 表示我们已经分别检查了行索引和列索引
                usedRows.add(row)
                usedCols.add(col)
            # 计算我们尚未检查的行和列索引
            unusedRows = set(range(0, D.shape[0])).difference(usedRows)
            unusedCols = set(range(0, D.shape[1])).difference(usedCols)
            # 如果对象质心的数量等于或大于输入质心的数量
            # 我们需要检查一下其中的某些对象是否已潜在消失
            if D.shape[0] >= D.shape[1]:
                # loop over the unused row indexes
                for row in unusedRows:
                    # 抓取相应行索引的对象ID并增加消失的计数器
                    objectID = objectIDs[row]
                    self.disappeared[objectID] += 1
                    # 检查是否已将该对象标记为“消失”的连续帧数以用于注销该对象的手令
                    if self.disappeared[objectID] > self.maxDisappeared:
                        self.deregister(objectID)
            # 否则，如果输入质心的数量大于现有对象质心的数量，我们需要将每个新的输入质心注册为可跟踪对象
            else:
                for col in unusedCols:
                    self.register(inputCentroids[col])

        # return the set of trackable objects
        return self.objects