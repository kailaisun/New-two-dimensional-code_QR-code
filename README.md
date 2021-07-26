# New QR code 

 Published paper:[Visual Feedback System for Traditional Chinese Medical Massage Robot](https://ieeexplore.ieee.org/document/8866076)
## Innovation:Tiny visual tags for robot cameras
In this paper, we designed a new tiny QR code dedicated to 'acupoints location', with CRC check function.  
This project implemented the proposed tiny QR code detection and recognition algorithm:</br>
  <div align=center><img  src="https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/fig.png"/></div>

## Installation:
    pip install opencv-python

## Get Started:
    python two-code-detetor.py
    
#### Also,you can test other images by changing the path in two-code-detetor.py:</br> 
    image = cv2.imread('./images/0.jpg')
### Show:
 <div align=center><img  src="https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/show_20190627212736.png"/></div>
 <div align=center><img  src="https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/show_20190627212825.png"/></div>
<!--  ![img](https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/show_20190627212736.png)</br>
 ![img](https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/show_20190627212825.png)</br> -->
 The result represented three centre coordinates of feature points and the value of this two-dimensional code.


