import os
import cv2
import pandas
import smtplib 
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

if not os.path.exists('Output'):
    os.makedirs('Output')
    
data = pandas.read_csv('namestxt.csv')
nametxt = data['name'].tolist()

fromaddr = "youremail@gmail.com"
passwordStr = "yourpassword"
toaddrList = data['mail'].tolist()

#path to the certificate template
imgPath = r'template2.png'
destPath = r'Output/' #dont forget to add / at the end. 

img = cv2.imread(imgPath)

#height, width and channels of img
h, imgWidth, c = img.shape

# font_path = "AutoCertGen-main/GreatVibes-Regular.ttf"  # Replace with the actual path to the font file
# font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX # Use the script simplex font
# fontscale = 3

fontpath = "GreatVibes-Regular.ttf"     
font = ImageFont.truetype(fontpath, 92)

# ft = cv2.freetype.createFreeType2()
# ft.loadFontData(fontFileName='Ubuntu-R.ttf',
#                 id=0)
# ft.putText(img=img,
#            text='Quick Fox',
#            org=(15, 70),
#            fontHeight=60,
#            color=(255,  255, 255),
#            thickness=-1,
#            line_type=cv2.LINE_AA,
#            bottomLeftOrigin=True)

#black colour font, with 3px thickness, and size 3
colour = (0,0,0)
thickness = 3

def mailer(name, toaddr, filename):
  # instance of MIMEMultipart 
  msg = MIMEMultipart() 

  # storing the senders email address   
  msg['From'] = fromaddr 

  # storing the receivers email address  
  msg['To'] = toaddr 

  # storing the subject  
  msg['Subject'] = "Participation Certificate"

  # string to store the body of the mail 
  body = 'Hi. Assalamulaykum! ' + name + '''
Congratulations on completing ...
'''

  # attach the body with the msg instance 
  msg.attach(MIMEText(body, 'plain')) 
    
  # open the file to be sent  
  attachment = open(filename, "rb")
  # instance of MIMEBase and named as p 
  p = MIMEBase('application', 'octet-stream') 
    
  # To change the payload into encoded form 
  p.set_payload((attachment).read()) 
    
  # encode into base64 
  encoders.encode_base64(p) 
     
  p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    
  # attach the instance 'p' to instance 'msg' 
  msg.attach(p) 
    
  # creates SMTP session 
  s = smtplib.SMTP('smtp.gmail.com', 587) 
    
  # start TLS for security 
  s.starttls() 
    
  # Authentication 
  s.login(fromaddr, passwordStr)

  # Converts the Multipart msg into a string 
  text = msg.as_string() 
  
  # sending the mail 
  s.sendmail(fromaddr, toaddr, text) 
    
  # terminating the session 
  s.quit()



for i in range(0, len(nametxt)):
    
    # coordinates for placing text. left aligned is simple.
    # but for center aligning, find the width of image and text size to center
    # 55px is the width of each text character for the given font specs
    name_regular = nametxt[i].title()
    xcor = int(imgWidth/2) - (round(len(nametxt[i])/2)*40) + 10

    # ycor 1490 is chosen by trial and error to fit the template.
    # note that h/2 is almost similar to ycor (1490) 
    cor = (xcor, 580)
    # ft.putText(img=img,
    #            text='Quick Fox',
    #            org=(15, 70),
    #            fontHeight=60,
    #            color=(255,  255, 255),
    #            thickness=-1,
    #            line_type=cv2.LINE_AA,
    #            bottomLeftOrigin=True)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(cor,  name_regular , font = font, fill = (0,0,0))        #, fill = (b, g, r, a)
    img1 = np.array(img_pil)

    ## Display 
    #cv2.imshow("res", img);cv2.waitKey();cv2.destroyAllWindows()
    #cv2.imwrite("res.png", img)
    #img1 = cv2.putText(img, nametxt[i], cor,font , fontscale, colour, thickness, cv2.LINE_AA)

    cv2.namedWindow('Certificate', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Certificate', 1200, 1000)
    cv2.imshow('Certificate', img1)  # Display the image

    # Wait for a key press (0 means wait indefinitely)
    # press y to send the certificate to the mail
    # press any other key to skip sending the certificate to the mail
    key = cv2.waitKey(0) & 0xFF

    if key == ord('y'):
        cv2.imwrite(destPath + str(nametxt[i]) + '.jpg', img1)
        print(str(nametxt[i]) + '.jpg created')
        mailer(nametxt[i], toaddrList[i], destPath + str(nametxt[i]) + '.jpg')
        print('Mailed to ' + nametxt[i])
    else:
        print(f"Skipped sending the certificate to {nametxt[i]}")


    print('-----End of ' + str(i+1) + '-----')
    img = cv2.imread(imgPath)

cv2.destroyAllWindows()  # Close the image window after processing all names