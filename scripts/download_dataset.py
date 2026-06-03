from roboflow import Roboflow

rf = Roboflow(api_key="TvGomzlyPP8zYXXTl1Fk")

project = rf.workspace().project("person-cctv-dataset")

version = project.version(4)

dataset = version.download(
    model_format="yolov8",
    location="datasets"
)

print("Dataset downloaded successfully")