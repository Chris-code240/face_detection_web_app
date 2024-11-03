# Face Detection System

The system was deloped around _MTCNN_ (Multi-Task Cascaded Convolutional Networks), a face detection algorithm that utilizes multiple neurial networks to do its job. It is very popular due to its lightweight, robust, and efficiency.
The MTCNN instance is wrapped around a flask application, which is also very efficient for small API implementation.

## How It Works

The system consist of only one endpoint `/video_feed`, through which frames a served to the frontend or target client.
Running the flask application, the system uses the client's webcam as a source of live video feed. _OpenCV_ is used to capture frames. For convenience sake, each frame at the position `multiples-of-5` is analyzed, and facial landmarks are drawn on the frame, then returned via the already mentioned endpoint.
The frontend application, a React App, mimics a live video stream from the API. This is done by using <img /> with the `src` set to the `/video_feed` endpoint.


### How to run the system

1. While in the root directory, navigate to the `frontend` directory
2. run `npm install` to install all dependencies
3. run `npm start` to start the react app on your local machine
        
4. Navigate to `backend` directory, from the root directory.
5. run `pip install -r requirements.txt` to install dependencies 
6. run `python api.py` to start the backend

