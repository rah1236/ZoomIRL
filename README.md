# ZoomIRL
A TreeHacks 2023 Thing

![ZoomIRL in action](https://imgur.com/bJj3LBj)

## Inspiration
In March of 2020 a lot of very bad things happened including but not limited to a global pandemic. Some things have returned to a state of normalcy, but other little issues bug me to this very day. One of those issues that just itches me the wrong way every time I have to deal with it is Zoom calls. 

## What it does
ZoomIRL is a robot that leverages computer vision in order to create a real life avatar of the little person in your zoom squares. I'm on a mission to make my Zoom calls a little more real, and a little more uncanny.

## How I built it
ZoomIRL is built on top of a Python based OpenCV stack that interfaces with an Arduino Leonardo over Serial in order to animate a live robot torso. It uses pose estimation in order to find points in space that are calculated into angles that can be fed into the Arduino, which generates PWM signals that steer the servos in a lifelike convincing, robotics, sometimes slightly snakey manner.

## Challenges we ran into
Finding a CV pose estimating stack to use inside of 6 hours is one of the more stress inducing challenges I've faced personally. Eventually OpenPose reared its beautiful gorgeous easy to use little head and enabled me to focus purely on the firmware. The firmware for the Arduino and its communication protocol had its own set of issues that were ultimately solved by the usual fix: reading the documentation. The Serial.read() method worked in a way that I didn't realize that I didn't understand and cost me hours of time.

## Accomplishments that we're proud of
I built a CV based robot in a day! And it works! And it makes me feel feelings that Zoom squares were never able to! Some of those feelings are fear, but anything beats the _crushing numbness_ of staring into a zoom square and seeing nothing behind your meeting mate's eyes.

## What we learned
-Pose estimation is hard but also a largely solved problem
-Angles are a strange piece of data to work with in the form of 8 bit integers. A more powerful microcontroller sweeps this problem under the rug but would also be overkill for this project. I wish I could've done it with ye' ole faithful Attiny85 but there just isn't enough pins or communications interfaces.
-Installing a billion dependencies makes your computer pretty sad, does anyone know how to help me clean them up? Please I need room for class notes.
-A little animatronic man sitting atop your computer can strike a new fear in you that doesn't really make sense because he is so small.

## What's next for ZoomIRL
A good nights sleep hopefully.

