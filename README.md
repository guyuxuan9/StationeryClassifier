# StationeryClassifier
This is a small project that use Raspberry Pi with a camera to take pictures of my stationaries and use neural network to classify them into categories.

## Camera App
![1688402647202](https://github.com/guyuxuan9/StationeryClassifier/assets/58468284/05459d42-ee2c-48ea-b549-f4de8c04d276)

The full code is given in the **CameraApp.py** file. This is a very basic version of a camera app that has the following functions:
- If **Take Picture** button is pressed, an image will be saved to the given directory
- It offers two modes: **Manual** and **Automatic**. In Manual mode, the user needs to press the **Take Picture** button manually to capture an image. In Automatic mode, the user can set the interval between image captures by entering the desired interval in seconds into the input box and pressing the **Set Interval(s)** button.
- The console message will be displayed as well.
- The image name represents the date and time of the image taken.

After testing locally, the **CameraApp.py** is run in Raspberry Pi. For this simple project, I took pictures of a pen, an eraser and a stapler from different angles using the raspberry pi camera (V2.1). The pictures are in the folders pen/, eraser/ and stapler/.

## Machine learning
The full code is given in **CameraApp.ipynb** file. This is used to train a very basic model to classify the picture into one of the three categories: **pen**, **eraser**, **stapler**. The summary of the model is given below:

![image](https://github.com/guyuxuan9/StationeryClassifier/assets/58468284/0a9fc277-f6b0-4a3e-b6fb-52e84c7bde9a)

The dataset is divided into a train set, which accounts for 80% of the data, and a test set, which makes up the remaining 20%. After training the model for 10 epochs, the accuracy on the train set reaches approximately 0.9724, while the accuracy on the test set is around 0.9. To visualize the training results, the following graphs are plotted to display the actual and predicted categories.

![image](https://github.com/guyuxuan9/StationeryClassifier/assets/58468284/515ec127-9147-4c91-bd7c-68f90d844579)


# TroubleShooting
- When I try to connect to the raspberry pi desktop to see the GUI using VNC server, the following error occurs. See this [link](https://www.youtube.com/watch?v=hA9r13ZUS08) for solution.

    ![image](https://github.com/guyuxuan9/UROP_robotic_arm/assets/58468284/2c1db8e1-aa6d-4808-8974-642030fb0331)

    Solution:
    Open /boot/config.txt, add the following lines:
    ```
    hdmi_force_hotplug=1
    hdmi_group=2
    hdmi_mode=9
    ```
- When I try to run **Camera.py** in raspberry pi, the following error occurs. See this [link](https://github.com/NVlabs/instant-ngp/discussions/300#discussioncomment-3179213) for solution.

    ![4e13973e210cbd0e6c961366502f04f](https://github.com/guyuxuan9/StationeryClassifier/assets/58468284/7f1e2dbb-855d-45e4-ad88-7530931bd32f)

    Solution:
    ```
    pip uninstall opencv-python
    pip install opencv-python-headless
    ```
