import os

folder = r"E:\CDIO3\doan\FE\public\sign_videos"

for filename in os.listdir(folder):
    if filename.endswith(".mp4"):
        new_name = filename.lower()
        os.rename(
            os.path.join(folder, filename),
            os.path.join(folder, new_name)
        )