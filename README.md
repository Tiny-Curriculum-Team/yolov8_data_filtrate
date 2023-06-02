## 0. 数据处理

> 首先，我们没有爬虫爬取数据并进行个人标注，在不论版权的情况下，我认为自己爬取数据并标注会有质量差，数量少，耗时间三个问题，自己采集数据并找专业标注以制作数据集才可制作出高质量数据集。而为了获得较好的效果，网络数据集就是一个好选择了，所以我们在寻找数据集之前，根据常见数据集情况及可能存在的一些数据集问题制作了一些数据处理脚本：
>
> 在目标检测任务中，有COCO，VOC，YOLO三个常见数据标注类型
>
> 其中COCO类型的数据集为图片文件夹加一个json格式的标注文件，该文件存储着所有图片文件的标注
>
> VOC类型的数据集为一个图片文件夹加一个内含一一对应的xml格式/json格式的标注文件
>
> YOLO类型的数据集为一个图片文件夹加一个内含一一对应的txt格式的标注文件
>
> 我们使用的算法需要使用的yolo类型的数据集，其文件类型为：

      --train—— images
             |—— labels
      --test —— images
             |—— labels
      --valid—— images
             |—— labels

> 其中数据为 class_id center_x center_y w h
>
> COCO类型转YOLO类型首先无法使用json包直接打开提取其中数据，因为其单个文件过大，直接打开提取会导致内存爆满，所以我们选用pycocotools.coco中的coco包来利用catIDs来进行数据集处理，最后使用coco2017数据集验证了脚本可用性，并实现了根据需求标注类型提取对应标注和图片数据打包成为YOLO格式的效果
>
> VOC类型转YOLO类型首要问题是Json格式文件其常见转换常常是json转xml转txt，且存储标注位置信息的box中只有标注框的左上角和右上角的点，那么在计算转换时，我们需要获取一下图片的尺寸才可计算出其满足yolo格式的标注数据，并且直接调用json包转json为txt，最后使用bdd100k数据集验证了脚本可用性，并实现了根据需求标注类型提取对应标注和图片数据打包成为YOLO格式的效果
>
> 处理完转换，针对数据集处理中一些常见问题：
>
> 针对数据分布，我制作了统计label数量的label_count，以防止出现自处理数据的数据不均衡问题
>
> 针对标注数据为空的情况，我制作了检查对应label关系以删除空标注图片和空标注文件的check_data
>
> 针对数据集的脏数据，我制作了可人工介入查看图片及其标注并进行picture_tool
>
> 针对数据集中在不同系统上绝对路径的问题，我制作可在windows和linux平台转换绝对图片路径的linux_txt
>
> 针对原始数据集标注和各类型图片混杂在一起，且没有分类别的问题，我制作了可按比例分开数据集train_val_divide 和按不同种类型分开图片和标注的splite_file(收录了常见的标注类型和图片类型)
>
> 针对过大数据量无法快速训练的问题，我制作了可缩小数据集规模的small_data

## 1. 数据集选择

> 我们的训练数据集来源于：[Construction Site Safety Image Dataset Roboflow | Kaggle](https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow?resource=download) 
>
> kaggle上的公开数据集，其license类别允许直接获取并完成学业任务
>
> 其自带标注格式为yolo格式
>
> 其数据自带数据增强
>
> 数据类别为`{0: 'Hardhat', 1: 'Mask', 2: 'NO-Hardhat', 3: 'NO-Mask', 4: 'NO-Safety Vest', 5: 'Person', 6: 'Safety Cone', 7: 'Safety Vest', 8: 'machinery', 9: 'vehicle'}`

## 2. 算法选择

> 我们算法选择了yolov8
>
> [ultralytics/ultralytics: NEW - YOLOv8 🚀 in PyTorch > ONNX > CoreML > TFLite (github.com)](https://github.com/ultralytics/ultralytics)
>
> 其作者和标注格式都同yolov5相同，作为现在的目标检测SOTA算法，这是我们选择其的原因
>
> 在yolo的n、s、m、l四个网络中，根据部署状态，我们选择使用n模型，训练资源消耗少，部署环境要求低是我们选择其的理由
>
> 根据我们现在的训练情况：
>
> ![image-20230526175517301](https://xiaomai-aliyunoss.oss-cn-shenzhen.aliyuncs.com/img/202305261755368.png)
>
> 在375个epochs时取得最优，person类的mAP50为0.883