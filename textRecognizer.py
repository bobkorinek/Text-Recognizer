import cv2


def Compare(img1, img2):
   match = 0
   for x in range(50):
      for y in range(50):
         if img1[x,y] == img2[x,y]:
            match += 1

   return match

def ResizeLine(image):
   
   #Zakladni info o lince
   y, x = image.shape
   print("X:",x,",","Y:",y)

   #Oriznuti 'white space' okolo cisel
   numberHeight = []
   for line in range(y):
      for column in range(x):
         if image[line, column] != 255:
            numberHeight.append(line)
            break
      if len(numberHeight) == 1:
         break

   for line in range(y-1,0,-1):
      for column in range(x):
         if image[line, column] != 255:
            numberHeight.append(line)
            break
      if len(numberHeight) == 2:
         break


   numberWidth = []
   for column in range(x):
      for line in range(y):
         if image[line, column] != 255:
            numberWidth.append(column)
            break
      if len(numberWidth) == 1:
         break

   for column in range(x-1,0,-1):
      for line in range(y):
         if image[line, column] < 250:
            numberWidth.append(column)
            break
      if len(numberWidth) == 2:
         break

   crop = image[numberHeight[0]:numberHeight[1], numberWidth[0]:numberWidth[1]]

   #Vytvoreni seznamu obrazku jednotlivych cisel
   y, x = crop.shape

   def all_same(items):
      return all(x == items[0] for x in items)

   numbers = []
   number = []
   for column in range(x):
      cnt = 0
      for color in crop[0:y-1,column]:
         if color != 255:
            number.append(column)
            break
         cnt += 1
         if len(number) != 0 and cnt == y-1:
            numbers.append(number)
            number = []
      if column == x-1:
         numbers.append(number)

   croppNum = []
   for number in numbers:
      croppNum.append(crop[0:y-1, number[0]:number[-1]])

   resNumbers = []
   for number in croppNum:
      resNum = cv2.resize(number, (50, 50))
      resNumbers.append(resNum)

   return resNumbers


def CompareAllNums(numbers, trainNums):
   string = ""
   for number in numbers:
      maxNum = 0
      curTrain = 0
      for trainNum in trainNums:
         x = Compare(number, trainNum)
         if x >= maxNum:
            corNum = curTrain
            maxNum = x
         curTrain += 1
      string += str(corNum)
   return string


def CutLines(image):
   y, x = image.shape
   freeLines = []
   
   for line in range(y-1):
      if not 0 in image[line, 0:x-1]:
         freeLines.append(line)

   lines = 0
   newLines = []
   lastLine = freeLines[0]
   
   for line in freeLines[1:]:
      if line-1 != lastLine:
         lines +=1
         newLines.append(lastLine)
         newLines.append(line)
      lastLine = line

   cuts = []

   if lines == 0 or lines == 1:
      return [image]

   else:
      for i in range(2,len(newLines)-1,2):
         cuts.append(int((newLines[i]+newLines[i-1])/2))
         
      lastCut = 0
      returnLines = []
      for cut in cuts:
         returnLines.append(image[lastCut:cut, 0:x-1])
         lastCut = cut
      
      returnLines.append(image[lastCut:y-1, 0:x-1])

      return returnLines
      
   
def ReadImage(image, trainNums):
   lines = CutLines(image)
   resizedLines = []
   
   for line in lines:
      resizedLines.append(ResizeLine(line))

   value = []
   for line in resizedLines:
      value.append(CompareAllNums(line, trainNums))

   return value


def LoadTrainNums():
   value = []
   for i in range(10):
      path = "Chars/numbers/num"+str(i)+".png"
      value.append(cv2.imread(path , 0))
   return value


output = ReadImage(cv2.imread("lines_test.png",0), LoadTrainNums())
for line in output:
   print(line)


"""

In progress (:

latters = ResizeLine(cv2.imread("alphaTest_lower.png",0))
alpha = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
count = 0
for latter in latters:
   cv2.imwrite("Chars/latters/low_"+alpha[count]+".png", latter)
   count += 1

"""