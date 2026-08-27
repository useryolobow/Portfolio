import cv2

cap = cv2.VideoCapture(0)
AText = """ .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8@$"""
formattedText = ".:-=+*#%@"
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if not cap.isOpened:
	print(f"\033[1;34mERROR\033[0m")
while True:
    ret, frame = cap.read()
    gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray1,(68,38))
    h, w = gray.shape
    for i in range(h):
   		for j in reversed(range(w)):
   			brightness = gray[i,j]
   			index = int((brightness / 255) * (len(formattedText) - 1))
   			pixel = formattedText[index]
   			print(f"{pixel}",end="")
   		print("\n")
    if not ret:
        print("ERROR: Failed to grab frame")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #print("min/max:", gray.min(), gray.max())

   			

cap.release()
cv2.destroyAllWindows()