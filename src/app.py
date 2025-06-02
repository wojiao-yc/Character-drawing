import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
import threading
from video_processor import VideoProcessor
from PIL import Image, ImageTk

class VideoToASCIIApp:
    def __init__(self, master):
        self.master = master
        master.title("视频转字符画工具")

        # 初始参数
        self.input_video = None
        self.output_video = None
        self.video_fps = 0
        self.video_total_frames = 0
        self.video_duration = 0.0
        self.cap = None  # 视频对象
        self.frame = None  # 当前帧

        # 界面布局

        tk.Label(master, text="输入视频文件:").grid(row=0, column=0, sticky='w')
        self.input_path_var = tk.StringVar()
        tk.Entry(master, textvariable=self.input_path_var, width=25).grid(row=0, column=1, columnspan=1, sticky='w')
        tk.Button(master, text="选择文件", command=self.select_input_file).grid(row=0, column=2, sticky='e')

        tk.Label(master, text="输出文件路径:").grid(row=1, column=0, sticky='w')
        self.output_path_var = tk.StringVar()
        tk.Entry(master, textvariable=self.output_path_var, width=25).grid(row=1, column=1, columnspan=1, sticky='w')
        tk.Button(master, text="选择输出路径", command=self.select_output_file).grid(row=1, column=2, sticky='e')

        tk.Label(master, text="视频总时长(秒):").grid(row=2, column=0, sticky='w')
        self.video_duration_label = tk.Label(master, text="未加载")
        self.video_duration_label.grid(row=2, column=1, sticky='w')
        tk.Button(master, text="加载视频信息", command=self.load_video_info).grid(row=2, column=2, sticky='e')

        self.progress_var = tk.DoubleVar()
        tk.Label(master, text="起始时间(秒):").grid(row=3, column=0, sticky='e')
        self.start_scale = tk.Scale(master, from_=0, to=0, orient='horizontal', length=300, resolution=0.1, command=self.update_frame)
        self.start_scale.grid(row=3, column=1, columnspan=3, sticky='w')

        tk.Label(master, text="结束时间(秒):").grid(row=4, column=0, sticky='e')
        self.end_scale = tk.Scale(master, from_=0, to=0, orient='horizontal', length=300, resolution=0.1, command=self.update_frame)
        self.end_scale.grid(row=4, column=1, columnspan=3, sticky='w')

        # 视频预览区域
        self.video_label = tk.Label(master)
        self.video_label.grid(row=5, column=0, columnspan=3)

        tk.Label(master, text="整体画幅大小:").grid(row=6, column=0, sticky='e')
        self.scale_var = tk.IntVar(value=4)
        tk.Scale(master, from_=1, to=20, orient='horizontal', variable=self.scale_var, length=300).grid(row=6, column=1, columnspan=3, sticky='w')

        tk.Label(master, text="每个字符大小:").grid(row=7, column=0, sticky='e')
        self.font_size_var = tk.IntVar(value=5)
        tk.Scale(master, from_=1, to=20, orient='horizontal', variable=self.font_size_var, length=300).grid(row=7, column=1, columnspan=3, sticky='w')

        self.use_color_filter_var = tk.BooleanVar(value=False)
        tk.Checkbutton(master, text="高对比度", variable=self.use_color_filter_var).grid(row=8, column=0, sticky='w')
        self.use_subject_filter_var = tk.BooleanVar(value=False)
        tk.Checkbutton(master, text="边缘检测", variable=self.use_subject_filter_var).grid(row=8, column=1)
        self.use_pencil_sketch_effect_var = tk.BooleanVar(value=False)
        tk.Checkbutton(master, text="彩铅效果", variable=self.use_pencil_sketch_effect_var).grid(row=8, column=2, sticky='w')
        # 进度条

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(master, orient='horizontal', length=300, mode='determinate', variable=self.progress_var)
        self.progress_bar.grid(row=9, column=1, columnspan=2, sticky='w')


        tk.Button(master, text="开始转换", command=self.start_conversion).grid(row=9, column=0, sticky='w')



    def update_frame(self, val):
        """通过进度条更新视频的帧"""
        if self.cap is None or not self.cap.isOpened():
            return

        # 获取进度条的当前值
        self.current_frame = int(float(val)*self.video_fps)

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
        img = img.resize((365, 210), Image.Resampling.LANCZOS)  # 使用 LANCZOS 代替 ANTIALIAS
        img_tk = ImageTk.PhotoImage(img)

        # 更新视频显示
        self.video_label.config(image=img_tk)
        self.video_label.image = img_tk




    def select_input_file(self):
        file_path = filedialog.askopenfilename(title="选择输入视频文件")
        if file_path:
            self.input_path_var.set(file_path)
            self.video_duration_label.config(text="未加载")
            self.start_scale.config(from_=0, to=0)
            self.end_scale.config(from_=0, to=0)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(title="选择输出文件路径", defaultextension=".mp4")
        if file_path:
            self.output_path_var.set(file_path)

    def load_video_info(self):
        input_video = self.input_path_var.get()
        if not input_video:
            messagebox.showerror("错误", "请先选择输入视频文件")
            return
        self.cap = cv2.VideoCapture(input_video)
        if not self.cap.isOpened():
            messagebox.showerror("错误", "无法打开视频文件")
            return
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        self.video_fps = fps
        self.video_total_frames = total_frames
        self.video_duration = duration

        self.video_duration_label.config(text=f"{duration:.2f} 秒")
        self.start_scale.config(from_=0, to=duration)
        self.start_scale.set(0)
        self.end_scale.config(from_=0, to=duration)
        self.end_scale.set(duration)
        self.update_video()
        # self.cap.release()

    def start_conversion(self):
        input_video = self.input_path_var.get()
        output_video = self.output_path_var.get()
        if not input_video or not output_video:
            messagebox.showerror("错误", "请确认输入和输出文件路径")
            return

        start_time = self.start_scale.get()
        end_time = self.end_scale.get()
        if end_time <= start_time:
            messagebox.showerror("错误", "结束时间必须大于起始时间")
            return

        scale = self.scale_var.get()
        font_size = self.font_size_var.get()
        use_color_filter = self.use_color_filter_var.get()
        use_subject_filter = self.use_subject_filter_var.get()
        use_pencil_sketch_effect = self.use_pencil_sketch_effect_var.get()

        thread = threading.Thread(target=self.run_conversion,
                                  args=(input_video, output_video, scale, font_size, start_time, end_time, use_color_filter, use_subject_filter, use_pencil_sketch_effect))
        thread.start()

    def run_conversion(self, input_video, output_video, scale, font_size, start_time, end_time, use_color_filter, use_subject_filter, use_pencil_sketch_effect):
        def update_progress(current, total):
            progress = (current / total) * 100
            self.progress_var.set(progress)
            self.master.update()

        try:
            VideoProcessor.generate(input_video, output_video, scale=scale, font_size=font_size,
                     start_time=start_time, end_time=end_time,
                     use_color_filter=use_color_filter, use_subject_filter=use_subject_filter, use_pencil_sketch_effect = use_pencil_sketch_effect, 
                     progress_callback=update_progress)
            messagebox.showinfo("完成", "视频转换完成！")
        except Exception as e:
            messagebox.showerror("错误", f"处理失败：{e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = VideoToASCIIApp(root)
    root.mainloop()