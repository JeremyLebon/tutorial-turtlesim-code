#!/bin/bash

export ROS_REMOTE_PC=127.0.0.1
export ROS_PORT=11311
export ROS_MASTER_CONTAINER=turtlebot3-rosmaster1:1_0_0
export TURTLEBOT3_MODEL=burger

# END MODIFY

docker run -it \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --env="XAUTHORITY=$XAUTH" \
    --volume="$XAUTH:$XAUTH" \
    --mount source=turtlesimvolume,destination=/root/home/catkin_ws \
    --env "ROS_MASTER_URI=http://$ROS_REMOTE_PC:$ROS_PORT" \
    --env "ROS_HOSTNAME=$ROS_REMOTE_PC" \
    --env "TURTLEBOT3_MODEL=$TURTLEBOT3_MODEL" \
    --name turtlesim_cont \
    --rm \
    ros-turtle \
    bash

#--gpus all \
#--device /dev/dri \
