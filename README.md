# ID-tracking-tool
## Marking tool instruction：

**Input**：1.images of each frame

​                  2.dataset of each detections,  including frame,$x_{min}$,$x_{max}$ ,$y_{min}$,$y_{max}$...

**Output**: Add an ID for each detection according  to the terminal input.

**Tips**:

1.Run the IDmarking at the terminal, there will be two images, an unmarked one and its last frame marked of reference, the red detection is going to be marked.

2.Input "", the program will attribute the ID calculated by IOU(if first frame,it will be 0,1,2...)

3.Input number, the program will attribute the number as the ID of the current red detection

4.Input 'q', back to last frame to re-mark ( In case that you find something wrong )

5.Input 'z' ,back to last detection to re-mark

6.Input other, the program will prompt tp input a number
