# New QR code 

 Published paper:[Visual Feedback System for Traditional Chinese Medical Massage Robot](https://ieeexplore.ieee.org/document/8866076)
## Innovation:Tiny visual tags for robot cameras
In the above paper, we designed a new tiny QR code dedicated to 'acupoints location', with CRC check function.  
This project introduces how to implement the proposed tiny QR code detection and recognition algorithm:</br>
  <div align=center><img width='250' height='300'  src="https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/fig.png"/></div>
  
## Installation:
    pip install opencv-python

## Get Started:
    python two-code-detetor.py
    
#### Also,you can test other images by changing the path in two-code-detetor.py:</br> 
    image = cv2.imread('./images/0.jpg')
### Show:
 <div align=center><img  src="https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/show_20190627212736.png"/></div>
 <div align=center><img  src="https://github.com/kailaisun/New-two-dimensional-code_QR-code/blob/master/show_20190627212825.png"/></div>
The last image represented three center coordinates of feature points.  

The '[1,1,1,1,1,1,1,1,1]' are the values of nine black areas;The '31' is the value of this two-dimensional code;the 'True' is the CRC check result.


