import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading


class VideoPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Tkinter 视频播放器")

        # 初始化视频相关变量
        self.cap = None
        self.total_frames = 0
        self.fps = 0
        self.current_frame = 0

        # 创建视频播放区域
        self.video_label = tk.Label(master)
        self.video_label.pack()

        # 创建进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(master, from_=0, to=100, orient="horizontal", length=400,
                                      variable=self.progress_var, showvalue=False, command=self.update_frame)
        self.progress_bar.pack()

        # 创建加载视频按钮
        self.load_button = tk.Button(master, text="加载视频", command=self.load_video)
        self.load_button.pack()

        # 创建播放控制按钮
        self.play_button = tk.Button(master, text="播放", command=self.play_video)
        self.play_button.pack()

    def load_video(self):
        """加载视频文件"""
        file_path = filedialog.askopenfilename(title="选择视频文件", filetypes=(("MP4 Files", "*.mp4"), ("All Files", "*.*")))
        if not file_path:
            return

        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            messagebox.showerror("错误", "无法打开视频文件")
            return

        # 获取视频的总帧数和帧率
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        # 设置进度条的最大值为视频的总帧数
        self.progress_bar.config(to=self.total_frames - 1)

        self.current_frame = 0
        self.update_video()

    def play_video(self):
        """播放视频"""
        if self.cap is None or not self.cap.isOpened():
            messagebox.showerror("错误", "请先加载视频文件")
            return

        # 播放视频
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # 更新当前帧位置
            self.current_frame += 1
            self.progress_var.set(self.current_frame)

            # 将图像转换为 Tkinter 可显示的格式
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)

            # 缩放图像到小尺寸，例如 320x240
            img = img.resize((320, 240), Image.Resampling.LANCZOS)  # 使用 LANCZOS 代替 ANTIALIAS
            img_tk = ImageTk.PhotoImage(img)

            # 更新视频显示
            self.video_label.config(image=img_tk)
            self.video_label.image = img_tk

            # 控制帧率
            cv2.waitKey(int(1000 / self.fps))

            # 退出时检查
            if self.current_frame >= self.total_frames:
                break

    def update_frame(self, val):
        """通过进度条更新视频的帧"""
        if self.cap is None or not self.cap.isOpened():
            return

        # 获取进度条的当前值
        self.current_frame = int(val)

        # 设置视频的当前帧
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)

        # 更新视频显示
        self.update_video()

    def update_video(self):
        """更新当前帧的显示"""
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # 将图像转换为 Tkinter 可显示的格式
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        # 缩放图像到小尺寸，例如 320x240
        img = img.resize((320, 240), Image.Resampling.LANCZOS)  # 使用 LANCZOS 代替 ANTIALIAS
        img_tk = ImageTk.PhotoImage(img)

        # 更新视频显示
        self.video_label.config(image=img_tk)
        self.video_label.image = img_tk


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()
