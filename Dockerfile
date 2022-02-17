FROM osrf/ros:melodic-desktop-full

# Install linux packages
RUN apt-get update && apt-get install -y \
locales \
lsb-release \
git \
subversion \
nano \
terminator \
xterm \
wget \
curl \
htop \
libssl-dev \
build-essential \
dbus-x11 \
software-properties-common \
build-essential \
ssh

RUN apt-get clean && rm -rf /var/lib/apt/lists/*


# Configure ROS
RUN rosdep update
RUN echo "source /opt/ros/melodic/setup.bash" >> /root/.bashrc
RUN echo "export ROSLAUNCH_SSH_UNKNOWN=1" >> /root/.bashrc
RUN echo "source /opt/ros/melodic/setup.zsh" >> /root/.zshrc
RUN echo "export ROSLAUNCH_SSH_UNKNOWN=1" >> /root/.zshrc


# Entry script - This will also run terminator
#COPY assets/entrypoint_setup.sh /
#ENTRYPOINT ["/entrypoint_setup.sh"]

#### copy ros_entrypoint.sh
COPY ros_entrypoint.sh /
RUN chmod a+x /ros_entrypoint.sh

#### create entrypoint
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

RUN /bin/bash -c 'source /opt/ros/melodic/setup.bash &&\
   sudo mkdir -p  /root/home/catkin_ws/src &&\
  cd /root/home/catkin_ws/src &&\
   catkin_init_workspace &&\
   cd /root/home/catkin_ws &&\
  catkin_make'

# Source: https://robotics.stackexchange.com/questions/21959/docker-dockerfile-bin-bash-catkin-init-workspace-catkin-make-command-not

RUN  cd /root/home/catkin_ws/src \
   && git clone -b melodic-devel https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git \
   && git clone -b melodic-devel https://github.com/ROBOTIS-GIT/turtlebot3.git \
   && git clone -b melodic-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git \
  && cd /root/home/catkin_ws

RUN /bin/bash -c 'source /opt/ros/melodic/setup.bash &&\
    cd /root/home/catkin_ws &&\
    catkin_make'

RUN echo "source root/home/catkin_ws/devel/setup.bash" >> /root/.bashrc
#CMD ["terminator"]
