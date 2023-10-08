from cyber_record.record import Record
import csv
from pyproj import Transformer
from util import *
from envload import *

MODE_CHASSIS_DETAIL = '/apollo/canbus/chassis_detail'
MODE_CHASSIS = '/apollo/canbus/chassis'
MODE_POSE = '/apollo/localization/pose'
MODE_GNSS = '/apollo/localization/mfs_gnss'
# file_name = "./data/20230301173130.record.00000"
# file_name = "20230302172944.record.00000"

ROUTE_EVENTS = [
   
]

EXPRIMENT_TIMESTAMP = [

]



# gpsfix
fixedidx = 1
LASTGPSLONGITUDE = 0.0
shift = 0.0165884
shiftadd = 0.0165884
shiftallowed = 113.622

# file_name = "20230410170600.record"
file_name = APOLLO_RECORD_FILE_INDEX
# folder = './data/bag/2023-03-30-22-36-41_s/'
# folder = 'G://P04/'
# folder = 'F://ORED_Dataset//P16//7.CANBus/'
folder = CANBUS_FOLDER_PATH
filelist = []
filetype = '.csv'
fileCount = getFileCount(CANBUS_FOLDER_PATH, APOLLO_RECORD_FILE_INDEX)

for i in range(fileCount):
   filelist.append(folder + file_name + '.000' + '{:0>2d}'.format(i))


# field names
def get_fields(mode):
   if (mode == MODE_POSE):
      fields = ['mode', 'timestamp',
                'position-x', 'position-y', 'position-z',
                'linear_velocity-x', 'linear_velocity-y', 'linear_velocity-z',
                'linear_acceleration-x', 'linear_acceleration-y', 'linear_acceleration-z',
                'angular_velocity-x', 'angular_velocity-y', 'angular_velocity-z',
                'euler_angles-x', 'euler_angles-y', 'euler_angles-z',
                'imu_data_status', 'imu_delay_status', 'imu_missing_status']
   if (mode == MODE_CHASSIS_DETAIL):
      fields = ['mode', 'timestamp',
                'canbus_fault',
                'latitude', 'longitude',
                'brake_input', 'brake_output', 'brake_torque_req', 'brake_torque_act',
                'wheel_torque_act', 'hsa_mode']
   if (mode == MODE_CHASSIS):
      fields = ['mode', 'timestamp',
                'gps.latitude', 'gps.longitude.fix', 'gps.altitude', 'gps.longitude.raw',
                'chassis_gps.gps_valid',
                'chassis_gps.is_gps_fault',
                'chassis_gps.gps_speed',
                'speed_mps',
                'fuel_range_m',
                'throttle_percentage',
                'brake_percentage',
                'steering_percentage',
                'steering_torque_nm',
                'parking_brake',
                'error_code',
                'gear_location',
                ]
   return fields

fields_pose = get_fields(MODE_POSE)
fields_chassis_detail = get_fields(MODE_CHASSIS_DETAIL)
fields_chassis = get_fields(MODE_CHASSIS)


f_pose = open(folder  + 'pose--' + file_name + ".csv", 'w', newline='')
f_chassis_detail = open(folder  + 'chassis_detail--' + file_name + ".csv", 'w', newline='')
f_chassis = open(folder  + 'fixgps' + 'chassis--' + file_name + ".csv", 'w', newline='')
f_module = open(folder + 'moduleName--' + file_name + filetype, 'w', newline='')

writer_pose = csv.writer(f_pose)
writer_chassis_detail = csv.writer(f_chassis_detail)
writer_chassis = csv.writer(f_chassis)
writer_module = csv.writer(f_module)

writer_pose.writerow(fields_pose)
writer_chassis_detail.writerow(fields_chassis_detail)
writer_chassis.writerow(fields_chassis)

# GPS Transformer (Apollo WGS84 to Beijing 1954 Coordinate System)
# Create a transformer object that defines the source and destination coordinate systems
transformer = Transformer.from_crs('EPSG:4326', 'EPSG:4214', always_xy=True)

def parse_pose(pose, time):
   '''
   save pose to csv file
   '''
   row = ['pose', time,
          pose.pose.position.x, pose.pose.position.y, pose.pose.position.z,
          pose.pose.linear_velocity.x, pose.pose.linear_velocity.y, pose.pose.linear_velocity.z,
          pose.pose.linear_acceleration.x, pose.pose.linear_acceleration.y, pose.pose.linear_acceleration.z,
          pose.pose.angular_velocity.x, pose.pose.angular_velocity.y, pose.pose.angular_velocity.z,
          pose.pose.euler_angles.x, pose.pose.euler_angles.y, pose.pose.euler_angles.z,
          pose.sensor_status.imu_data_status, pose.sensor_status.imu_delay_status, pose.sensor_status.imu_missing_status
          ]
   writer_pose.writerow(row)


def parse_chassis_detail(chassis_detail, time):
   '''
   save chassis_detail to csv file
   '''
   row = ['chassis_detail', time,
          chassis_detail.basic.canbus_fault,
          chassis_detail.basic.latitude,
          chassis_detail.basic.longitude,
          chassis_detail.brake.brake_input,
          chassis_detail.brake.brake_output,
          chassis_detail.brake.brake_torque_req,
          chassis_detail.brake.brake_torque_act,
          chassis_detail.brake.wheel_torque_act,
          chassis_detail.brake.hsa_mode,
          ]
   writer_chassis_detail.writerow(row)

def getfixlongitude(lastgpslongitude, lg):
   lgshifed = 0.0
   # if(abs(lastgpslongitude-lg)>shift):
   #    # lgshifed = lg + abs(lastgpslongitude-lg)
   #    lgshifed = lg + shift
   #    LASTGPSLONGITUDE = lgshifed
   if(lg < shiftallowed):
      lgshifed = lg + shiftadd
   else:
      lgshifed = lg
      
   return lgshifed

def parse_chassis(chassis, time, lastgpslongitude):
   '''
   save chassis to csv file
   '''
   # target_longitude, target_latitude = transformer.transform(getfixlongitude(lastgpslongitude, chassis.chassis_gps.longitude), chassis.chassis_gps.latitude)
   row = ['chassis', time,
          chassis.chassis_gps.latitude, getfixlongitude(lastgpslongitude, chassis.chassis_gps.longitude), chassis.chassis_gps.altitude, chassis.chassis_gps.longitude,
          chassis.chassis_gps.gps_valid,
          chassis.chassis_gps.is_gps_fault,
          chassis.chassis_gps.gps_speed,
          chassis.speed_mps,
          chassis.fuel_range_m,
          chassis.throttle_percentage,
          chassis.brake_percentage,
          chassis.steering_percentage,
          chassis.steering_torque_nm,
          chassis.parking_brake,
          chassis.error_code,
          chassis.gear_location
          ]
   writer_chassis.writerow(row)
   lastgpslongitude = chassis.chassis_gps.longitude


for fp in filelist:
   try:
      record = Record(fp)

      for topic, message, t in record.read_messages():
         writer_module.writerow([t, topic])
         #    print("{}, {}, {}".format(topic, type(message), t))
         # if (topic == MODE_CHASSIS_DETAIL):
         #    parse_chassis_detail(message, t)
         if (topic == MODE_POSE):
            parse_pose(message, t)
         elif (topic == MODE_CHASSIS):
            if(fixedidx==1):
               LASTGPSLONGITUDE = message.chassis_gps.longitude
               fixedidx=-1
            parse_chassis(message, t, LASTGPSLONGITUDE)
         else:
            pass
   except AttributeError as e:
         print(e)
f_pose.close()
# f_chassis_detail.close()
f_chassis.close()


# for fp in filelist:
#    record = Record(fp)
#
#    for topic, message, t in record.read_messages():
#       writer_module.writerow([t, topic])
#       #    print("{}, {}, {}".format(topic, type(message), t))
#       if (topic == MODE_CHASSIS_DETAIL):
#          parse_chassis_detail(message, t)
#       elif (topic == MODE_POSE):
#          parse_pose(message, t)
#       elif (topic == MODE_CHASSIS):
#          if(fixedidx==1):
#             LASTGPSLONGITUDE = message.chassis_gps.longitude
#             fixedidx=-1
#          parse_chassis(message, t, LASTGPSLONGITUDE)
#       else:
#          pass
#
# f_pose.close()
# f_chassis_detail.close()
# f_chassis.close()

# '/apollo/canbus/chassis_detail'
