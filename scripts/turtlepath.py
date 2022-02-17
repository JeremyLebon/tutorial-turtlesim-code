
#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)

        # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)
        self.path = []
        
        self.posepoint1 = Pose()
        self.posepoint1.x = 1
        self.posepoint1.y = 1
        self.posepoint1.theta= 0
        self.path.append(self.posepoint1)
	self.posepoint2 = Pose()

        self.posepoint2.x = 1
        self.posepoint2.y = 9
        self.posepoint2.theta= 0.50
        self.path.append(self.posepoint2) 
	self.posepoint3 = Pose()

        self.posepoint3.x = 9
        self.posepoint3.y = 9
        self.posepoint3.theta= 1.57
        self.path.append(self.posepoint3) 

        self.posepoint4 = Pose()
        self.posepoint4.x = 9
        self.posepoint4.y = 1
        self.posepoint4.theta= 0
        self.path.append(self.posepoint4)         

        self.posepoint5 = Pose()
        self.posepoint5.x = 5
        self.posepoint5.y = 5
        self.posepoint5.theta= 0
        self.path.append(self.posepoint5) 

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
        """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)
    
    def takepath(self):
	print(self.path)
        for point in self.path:
            print(point)
            self.move2goal(point)
         # If we press control + C, the node will stop.
        rospy.spin()

    def move2goal(self,point):
        """Moves the turtle to the goal."""
        goal_pose = Pose()

        # Get the input from the user.
        goal_pose.x = point.x
        
        goal_pose.y = point.y

        # Please, insert a number slightly greater than 0 (e.g. 0.01).
        distance_tolerance = 1

        vel_msg = Twist()

        try:
            while self.euclidean_distance(goal_pose) >= distance_tolerance:

            # Porportional controller.
            # https://en.wikipedia.org/wiki/Proportional_control

            # Linear velocity in the x-axis.
                vel_msg.linear.x = self.linear_vel(goal_pose)
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
                vel_msg.angular.x = 0
                vel_msg.angular.y = 0
                vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
                self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
                self.rate.sleep()
                
        except KeyboardInterrupt:
                print("stopped")
        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.takepath()
    except rospy.ROSInterruptException:
        pass
