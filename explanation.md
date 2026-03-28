# Chinese Reminder Theorem Encoders

I hate basically every existing explanation of CRT encoders available.

It feels like they all have some leap of logic somewhere and people just put their trust into magic boxes.

I dislike that from a pedegogical perspective, so let's actually try and break it down.

## The intuition

We have two encoders connected to some mechanism.

These two encoders are geared at different rates to the mechanism.

The offsets of these encoders thus will provide us some information about where the mechanism is.
If we assume they both start at (0, 0), .....

// TODO

## The mathematics

The Chinese Remainder Theorem states basically:



## Determining the range of motion

If our two encoders start at (0, 0), and we spin our mechanism enough times, we'll eventually hit a spot where both encoders read (0, 0) again.
This determines the limit of how many rotations we can uniquely solve for. 

We want to know the range of motion for some given gear ratios so we can design our system correctly. 

As a worked example, say your two encoders are geared 9:1 and 5:1 with your mechanism.
When your mechanism completes 1 full rotation, encoder 1 will have completed 9 rotations and encoder 5 will have completed 5.
They will both read (0, 0) after 1 rotation, meaning the detectable range in this setup is at most 1 rotation. 
