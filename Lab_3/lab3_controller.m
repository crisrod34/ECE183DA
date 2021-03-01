clc;
close all;
clear all;
% Get simulation time step;
%TIME_STEP = wb_robot_get_basic_time_step();
desktop;
keyboard;
%TIME_STEP = 0.5;
%Get Excel Data
time_array = readvars('Webots Path Data2.xlsx','Sheet','Trial 15','Range','A4:A628');
left_motor = readvars('Webots Path Data2.xlsx','Sheet','Trial 15','Range','B4:B628');
right_motor = readvars('Webots Path Data2.xlsx','Sheet','Trial 15','Range','C4:C628');
%Time_Array = readvars('Webots Test.xlsx','Range','A4:A44');
%Left_Motor = readvars('Webots Test.xlsx','Range','B4:B44');
%Right_Motor = readvars('Webots Test.xlsx','Range','C4:C44');
left_motor = -1*left_motor;
right_motor = -1*right_motor;
maxTime = 5000; %ms
i=1;
max = length(time_array);
TIME_STEP = maxTime/(max-1);
position_array = zeros(max,3);
velocity_array = zeros(max,6);
angle_array = zeros(max,4);
right_array = zeros(max,1);
straight_array = zeros(max,1);
compass_array = zeros(max,3);
gyro_array = zeros(max,3);
gyro = wb_robot_get_device('gyro');
wb_gyro_enable(gyro,TIME_STEP);
compass = wb_robot_get_device('compass');
wb_compass_enable(compass, TIME_STEP);
right = wb_robot_get_device('lidar_R');
wb_distance_sensor_enable(right,TIME_STEP)
straight = wb_robot_get_device('lidar_F');
wb_distance_sensor_enable(straight,TIME_STEP)
motor_R = wb_robot_get_device('motor_R'); % Device names have to be char, not string;
motor_L = wb_robot_get_device('motor_L');
robot = wb_supervisor_node_get_from_def('robot'); % For ground truth access;
rotation = wb_supervisor_node_get_field(robot,'rotation');
% Enable sensors (instance, sampling period[ms]);
% Make the motors non-position control mode;
wb_motor_set_position(motor_R, inf);
wb_motor_set_position(motor_L,inf);
% Need to call wb robot step periodically to communicate to the simulator;

while wb_robot_step(TIME_STEP) ~= -1
% Run a motor by velocity rad/sec;
compass_array(i,:) = wb_compass_get_values(compass);
gyro_array(i,:) = wb_gyro_get_values(gyro);
right_array(i) = wb_distance_sensor_get_value(right);
straight_array(i) = wb_distance_sensor_get_value(straight);
position_array(i,:) = wb_supervisor_node_get_position(robot);
angle_array(i,:) = wb_supervisor_field_get_sf_rotation(rotation);
velocity_array(i,:) = wb_supervisor_node_get_velocity(robot);
if i==max
    break;
end
i=i+1;
wb_motor_set_velocity(motor_R,right_motor(i));
wb_motor_set_velocity(motor_L,left_motor(i));
end

angle_array = angle_array+3.14159265359/2;
%figure(1)
%plot(Position_Array(:,3),Position_Array(:,1)) %Plots z as func of x
%figure(2)
%plot(Time_Array,Velocity_Array(:,5))

xlswrite('Webots Path Data2.xlsx',position_array(:,1),'Trial 15','H4');
xlswrite('Webots Path Data2.xlsx',position_array(:,3),'Trial 15','I4');
xlswrite('Webots Path Data2.xlsx',angle_array(:,4),'Trial 15','K4');
xlswrite('Webots Path Data2.xlsx',velocity_array(:,5),'Trial 15','J4')
% xlswrite('Webots Path Data2.xlsx',straight_array(:,1),'Trial 13','H4');
% xlswrite('Webots Path Data2.xlsx',right_array(:,1),'Trial 13','I4');
% xlswrite('Webots Path Data2.xlsx',compass_array(:,1),'Trial 13','J4');
% xlswrite('Webots Path Data2.xlsx',compass_array(:,3),'Trial 13','K4');
% xlswrite('Webots Path Data2.xlsx',gyro_array(:,2),'Trial 13','L4');

% Close your controller;
wb_robot_cleanup()