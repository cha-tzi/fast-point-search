# fast-point-search
Spatial Database: For a set of geograpical locations (points) find if the belong in one or multiple circles.

The input data is thousends of geographical points around the UK and a dataframe with half a million circles that contain the flood probabilities.
It outputs the highest probability that a point has and if a point belongs to no circles it outputs "Zero".

This function was the fastest in the class because it uses the KDTree algorithm. 
As the scikit learn KDTree function is not made for circles, the circles were simulated 
by changed the querry radious for each point to the radious of each circle.

This was very fast but it caused a considerable effort to relate the points back to each probability as the the test and train set were swapped.

This module was created as part of a group project for the Imperial College Applied Computational Science and Engineering MSc course.


