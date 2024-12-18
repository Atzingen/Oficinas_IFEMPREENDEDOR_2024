from ultralytics import YOLO
import os

def get_dataset_yaml_path():
    dataset_dir = os.path.join(os.getcwd(), "../datasets", "RipenessApple")
    yaml_path = os.path.join(dataset_dir, "data.yaml")
    if not os.path.exists(yaml_path):
        print(f"Error: data.yaml not found in {yaml_path}")
        exit()
    return yaml_path

def train_yolo(dataset_yaml, model_type="yolov8n.pt", epochs=50, batch=16):
    model = YOLO(model_type)
    model.train(
        data=dataset_yaml,
        epochs=epochs,
        batch=batch,
        imgsz=640,
        project="runs/train",
        name="custom_yolo"
    )

if __name__ == "__main__":
    yaml_path = get_dataset_yaml_path()
    train_yolo(
        dataset_yaml=yaml_path,
        model_type="yolo11m.pt",
        epochs=50,
        batch=16
    )
