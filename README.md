# apollo_recording_dataprocessing
The dataprocessing scripts for ORED real car dataset

1. 配置文件位置：打开.env, 按照格式修改文件位置以及标准的Sync同步时间 (来自脑电数据文件内的Sync时间)。
- PNAME：试次编号，也是文件夹路径变量 （如，'P04'）
- APOLLO_RECORD_FILE_INDEX: apollo recorder的录制文件的前缀 （如，'20230505170116.record'）
- MARKER_TIME_EEG： Sync时间的世界时间 （格式为，'2023-05-05 17:03:34.344'）
- STANDARD_TIME_EEG：以脑电curry9中的Sync时间为标准的Sync秒数（s）(如，'247.531')
- CANBUS_FOLDER_PATH：Canbus Raw data所在文件夹，试次编号以_PXX_替换 （如，'G://Real Road AIR Dataset//_PXX_//7.CANBus//'）
2. 解析底盘数据和GPS数据：运行 1_readrecord_fixgps.py，代码将读取所有环境配置内的.record文件，解析pose model和chassis model的数据，对GPS进行修正，并保存成CSV格式文件（fixgpschassis--yyyymmddhhmmss.record.csv）。【解析包 cyber_recorder】
- timestamp：工控机时间戳
- gps.latitude：融合定位后的纬度
- gps.longitude.fix：融合定位后的精度（修正后）
- speed_mps：速度mps
- throttle_percentage: 控制车身底层的油门百分比
- brake_percentage：控制车身底层的刹车百分比
- steering_percentage：控制车身底层的方向盘百分比
- steering_torque_nm：方向盘转向距离
- gear_location：控制车身底层的档位
- error_code：错误码
3. 生成时间切割文件（按工况）：运行  2_timedivision_gps_new.py，代码将根据Sync和预设的gps位置，生成每个工况在csv解析文件内的相对开始和结束时间戳，绝对开始和结束时间戳，以及duration时长，并保存成CSV格式文件（timedivision--yyyymmddhhmmss.record.csv）。【执行的工况包括：'Baseline','A1','A2','D1','S1','A3','A4','L1','L2','R1','R2','R3','R4','L3','End'】
- state： 工况名称状态
- start_time：工况开始的世界时间 (yyyy/m/dd hh:mm:ss, 2023/5/11  15:39:27)
- finish_time: 工况结束的世界时间 (yyyy/m/dd hh:mm:ss, 2023/5/11  15:39:27)
- start_timestamp：工况开始时间戳
- finish_timestamp：工况结束时间戳
- duration：工况持续时间 （s）
- relative_time: 工况相对于Sync时间的开始时间秒数 （s）
- RGB_relative_time_before_3000：工况相对于Sync时间的往前修正3s的开始时间秒数 （s）
4. 可视化gps轨迹：运行 3_gps_visualization.py ，代码将可视化gps轨迹和工况起始点的大致位置。