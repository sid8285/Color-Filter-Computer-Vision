#importing libraries to be used in the program
import cv2
import numpy as np

 # This funtion takes a video frame using the camera as input
def canny_edge_detection(frame, low_threshold, high_threshold):
    
    #converting the camera frame to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
    #applying Gaussian Blur to improve the edge detetction 
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) 
    
    #using the Canny edge detetction method with the values 20 - 50. I chose these values because i wanted the detection to be fine in detail, but not give too much noise.
    edges = cv2.Canny(blurred, low_threshold , high_threshold) 
    return blurred, edges

#this function is to set the background color of the frame. 
def set_background_color():
    print("Select a background color:")
    print("1. Black")
    print("2. Green")
    print("3. Red")
    print("4. Blue")
    choice = input("Enter the corresponding number (1/2/3/4): ")
    if choice == '1':
        return (0, 0, 0)  # This is for black
    elif choice == '2':
        return (0, 255, 0)  # This is for Green
    elif choice == '3':
        return (20, 20, 230)  # This if for Red
    elif choice == '4':
        return (230, 20, 20)  # This is for Blue
    else:
        print("Invalid choice. Keeping the current background color. Please try again!")
        return None

def main():
    
    #entry statements to inform the user about the script and how it works
    print("Welcome to the Edge Detection Color Filter!")
    print("Here's how to use the script:\t ")
    print("This script allows you to change the color of the filter and how fine the edge detetction is. \t ")
    print("To toggle the color, press 'c'. To toggle the grain press 't' (make sure to keep the lower threshold lower than the higher threshold). To quit press 'q'.\t ")
    print("When using the script, to use the program make sure you have the webcam selected, inputs are all entered via the terminal.")
    
    
    #initializing the video capture utilizing the default webcam
    cap = cv2.VideoCapture(0)
    # Choosing the base color to be black 
    selected_color = (0, 0, 0) 
    
    #this is the default low threshold
    low_threshold = 30
    
    #this is the default low threshold
    high_threshold = 70
    
    #this loop constantly captures frames from the webcam
    while True:
        
        #this reads in the frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print('Image not captured')
            break

        #this function obtains the blurred and edge-detected images
        blurred, edges = canny_edge_detection(frame, low_threshold, high_threshold)

        #this creates a background image with the selected color
        background = np.zeros_like(frame)
        background[:] = selected_color

        #this combines the background and frame with edges
        combined_image = cv2.bitwise_and(frame, frame, mask=edges)
        result = cv2.add(combined_image, background)

        #this displays the results in a window called "Result"
        cv2.imshow("Result", result)

        #this takes in a keystroke and stores the key's ACII value
        key = cv2.waitKey(1) & 0xFF
        
        #if 'q' is pressed, then the program ends
        if key == ord('q'):
            break
        
        #if 'c' is pressed then you can toggle the background color
        elif key == ord('c'):
            new_color = set_background_color()
            if new_color is not None:
                selected_color = new_color
                
        #if 't' is pressed then you can toggle the grain
        elif key == ord('t'):
            print("Enter the Canny edge detection thresholds (e.g., 30 70): ")
            thresholds = input().split()
            if len(thresholds) == 2:
                low_threshold = int(thresholds[0])
                high_threshold = int(thresholds[1])
            else:
                print("Sorry, you entered an invalid input. Try again!")

    #this releases the webcam capture and closes all the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


main()