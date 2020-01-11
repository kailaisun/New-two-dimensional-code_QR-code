# New two-dimensional code/QR code 

## Published paper:[Visual Feedback System for Traditional Chinese Medical Massage Robot](https://ieeexplore.ieee.org/document/8866076)
## Tiny visual tags for robot cameras
We designed a new two-dimensional code dedicated to 'acupoints location', with 'CRC check function', and a new two-dimensional code detection and recognition algorithm was proposed.</br>
  ![img](https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/fig.png)</br>
 Recognition algorithm of the new two-dimensional code</br>
## Usage:
    pip install opencv-python
    python two-code-detetor.py
#### Also,you can try other images by changing the code in two-code-detetor.py:</br> 
    image = cv2.imread('./images/0.jpg')
## Show:
 ![img](https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/show_20190627212736.png)</br>
 ![img](https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/show_20190627212825.png)</br>
 The result represented three centre coordinates of feature points and the value of this two-dimensional code.


