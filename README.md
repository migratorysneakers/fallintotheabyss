#  :crescent_moon: Fall Into The Abyss
![Abyss Landing Page](/Abyss_Demo/search_by_color.PNG)

**Abyss** lets you discover songs based on the color you picked or the dominant color detected in an image. OpenCV is used for image processing, specifically [K-means clutering for determining the dominant color](https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/). Spotify Web API is used for personalizing the user's song exploration.

**UPDATE APRIL 2021:** I [revamped](https://github.com/migratorysneakers/fallintotheabyssagain) this project!


![Abyss Results Page](/Abyss_Demo/result_page.PNG)

The selected (or detected) color returns a set of songs based on a combination of audio features. These songs fall under the user's top genres in the last four weeks, but have low popularity scores to emulate deep discovery--making the user fall deeper into the abyss.

### :mushroom: Powered by
:hamster: [OpenCV](https://opencv.org)

:hamster: [Spotify Web API](https://developer.spotify.com/documentation/web-api/quick-start/)

:hamster: [Flask](https://flask.palletsprojects.com/en/1.1.x/)

:hamster: [Materialize](https://materializecss.com/)
