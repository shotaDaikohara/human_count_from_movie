
# Setting
target_url = ['https://www.youtube.com/watch?v=z_Mvr_WHEy8']


# import
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
import pandas as pd
import cv2
import os
from ultralytics import YOLO
import os
import shutil
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from yt_dlp import YoutubeDL
model = YOLO('yolov8n.pt')


#動画取得関数
def get_video(target_url):
  ydl_opts = {'format': 'best'}
  with YoutubeDL(ydl_opts) as ydl:
      result = ydl.download(target_url)
  videos = [n for n in os.listdir(".") if "mp4" in n]
  return videos

#動画からコマを取得関数
def save_frame_range(video_path, start_frame, stop_frame, step_sec,
                     dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    if stop_frame == "end":
        stop_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    step_frame = int(video_fps*step_sec)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    for n in range(start_frame, stop_frame, step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
        else:
            return
# 切り抜いたコマの人数を検出し、矩形付与画像.jpgと検出データ.txtを保存
def detect_person():
  if os.path.exists("runs"):
      shutil.rmtree("runs")
  #人数検出
  l_frame = os.listdir(dir_path)
  model.predict(dir_path, save=True, conf=0.5, save_txt=True)
  #pathをリストに格納
  dir_path_txt = '/content/runs/detect/predict/labels/'
  l_file_txt = os.listdir(dir_path_txt)
  l_img_path = []
  l_people_num = []
  for f_txt in l_file_txt:
    path_txt = dir_path_txt + f_txt
    txt = pd.read_csv(path_txt, sep=' ', names=["ID","pred1","pred2","pred3","pred4"])
    txt_person = txt[txt['ID']==0]
    img_path = "runs/detect/predict/" + f_txt[:-4] + ".jpg"
    l_img_path.append(img_path)
    l_people_num.append(len(txt_person))
  return l_img_path, l_people_num


#動画取得
videos = get_video(target_url)
#フレームを抽出
dir_path = 'data/crop/'
step_sec = 5
save_frame_range(videos[0], 1, "end", step_sec, dir_path, 'sample_video_img')
# 人を検出
l_img_path, l_people_num = detect_person()
#人の数をグラフ化して保存
left = np.array([n*step_sec for n in range(len(l_peopre_num))])
height = np.array(l_peopre_num)
plt.xlabel("Time(s)")
plt.ylabel("person count")
plt.plot(left, height)
plt.savefig("count_person.png") 
