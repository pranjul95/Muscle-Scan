# Muscle-Scan
The objective is to obtain the measurement of different body parts using openCV(Python) given:

1- Frontal and lateral images of the person.
2- A full rotation video of the person.

We have done this using first approach but looking forward to implement it using video of the person as well. Now, What we have done is we have taken the height as the input as we were unable to calculate it using the images. Now I divided the entire body in ten equal parts to allocate a particular region to each body part as shown in figure 1.
                                                
                                                                 Figure 1

Once the image is segmented modelling the spatial body parts as an ellipse where its major axis(2a) is taken from the frontal image and its minor axis(2b) is taken from the lateral image. Now,Taking proper assumptions, circumference are generalised as:

   C=[32(a+b)-a.b]


Now, applying the above formula for different body parts as per their standard landmark definition.
For example:
Neck circumference,   N = min C in (1,2)
Waist Circumference, W = min C in (4,5)
Hip Circumference,     H = max C in (5,6)
Chest Circumference, C = max C in (2,3)

Comparison of the standard anthropometric method and our method of measuring sizes of various body parts:-[Link]

1- Neck Circumference:
The neck girth is defined as the circumference of the neck, taken over the cervical at the back and the top of the collarbone at the front.
We decided that we can specify the neck girth as the place with
the minimum circumference around the neck at the neck level measured horizontally in the front and on the side.
 2- Chest Circumference:
The chest circumference is defined as the maximum horizontal girth at chest level measured under the armpits, over the shoulder blades, and across the nipples with the subject breathing normally, parallel to the floor.
We have taken the chest girth as maximum circumference at the chest level measured horizontally.
3- Waist Circumference:
The waist girth is defined as the minimum horizontal circumference around the body at waist level. 
We have done the same way.
4- Hip Circumference:
The hip girth is defined as the maximum horizontal circumference around the body at hip height. 
Our method is same.

Now to obtain major and minor axes, First we have extracted the foreground of the image using thresholding and  flood filling, then making an array of arrays of white pixels count for each row. This way we get the white pixels count for each specified body part using circumference formula.
Now to convert it into standard units we have taken into account height pixels and input height using them calculated pixels per metric. By applying pixels per metric for each body part circumference, we can get measurements in standard unit.

This way, we can obtain the entire measurements.

Now our challenge part is: With our approach we can even calculate size of thighs legs but we can not calculate arms and forearms circumference as they are in the same row as the central part of the body is, this makes it hidden in lateral view as well. Also there is no way to get any clue about abs structure of the person using this method.

Using second approach we can also do the same by extracting the required images from the video of the full rotation of the person.
A Demo video for the full rotation is provided HERE.

