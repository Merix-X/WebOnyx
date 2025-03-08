import cv2

def take_photo():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    # reading the input using the camera
    result, image = cam.read()

    # If image will detected without any error,
    # show result
    if result:

        # showing result, it take frame name and image
        # output
        cv2.imshow("Capture", image)

        name = f"{str(input('Enter name: '))}.jpg"
        # saving image in local storage
        cv2.imwrite(name, image)

        # If keyboard interrupt occurs, destroy image
        # window
        # cv2.waitKey(0)
        cv2.destroyWindow("Capture")
        # os.system("xdg-open photo.png")
        return name

    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please try again!")