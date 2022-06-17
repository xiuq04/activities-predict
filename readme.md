# 代码运行说明

* comp_base.py功能

实现了八种模式：

```
pattern 0: 只考虑成员初始兴趣
pattern 1: 考虑训练集全部数据，对成员兴趣进行调整
pattern 2: 考虑训练集部分数据，成员兴趣的调整只依赖于所预测时间点以前的数据 

pattern 3: 考虑训练集全部数据，对成员兴趣进行调整，引入网络，权值为相似度（即两个人在该社团的兴趣相似度）
pattern 4: 考虑训练集部分数据，成员（只对所要预测的进行调整）兴趣的调整只依赖于所预测时间点以前的数据，引入网络，权值为相似度（即两个人在该社团的兴趣相似度）
pattern 5: 考虑训练集全部数据，对成员兴趣进行调整，引入共同出现次数无权网络，当以往两个人出现在同一回应结果中是有边
pattern 6: 考虑训练集全部数据，对成员兴趣进行调整，引入共同出现次数网络，边权值为两个人出现的次数比上两个人出现的总次数
pattern 7: 考虑训练集全部数据，对成员兴趣进行调整，引入相似度无权网络，当相似度超过阈值时建立边
```

运行前请将数据包（exp2data）放在同一目录下，并确保目录下没有文件result.xlsx（程序将创建该文件并将结果写入）

* comp_high.py功能

实现了共同出现次数网络（无权和有权）的社交级联以及考虑成员的选择偏好

运行前请将数据包（exp2data）放在同一目录下，并确保目录下没有文件result-sim.xlsx（程序将创建该文件并将结果写入）