import cv2
import numpy as np
from filters import Filter

class VideoProcessor:

    def pixel2char(pixel):
        # 使用灰度值来选择字符的映射
        char_list = "@#$%&erytuioplkszxcv=+---.."
        index = int(pixel / 256 * len(char_list))
        return char_list[index]

    def get_char_img(img, color_img, scale=4, font_size=5):
        # 调整图片大小
        h, w = img.shape
        re_im = cv2.resize(img, (w//scale, h//scale))
        re_color = cv2.resize(color_img, (w//scale, h//scale))
        # 创建一张图片用来填充字符
        char_img = np.ones((h//scale*font_size, w//scale*font_size, 3), dtype=np.uint8) * 255
        font = cv2.FONT_HERSHEY_SIMPLEX
        # 遍历图片像素
        for y in range(0, re_im.shape[0]):
            for x in range(0, re_im.shape[1]):
                # 获取字符
                char_pixel = VideoProcessor.pixel2char(re_im[y][x])
                # 获取原图颜色
                color = tuple(int(c) for c in re_color[y][x])
                # 在字符图中绘制字符，并应用颜色
                cv2.putText(char_img, char_pixel, (x*font_size, y*font_size),
                            font, 0.5, color, thickness=1)
        return char_img

    def generate(input_video, output_video, scale=4, font_size=5, frame_count=None,
             start_time=0, end_time=None, use_color_filter=False, use_subject_filter=False, use_pencil_sketch_effect = False, 
             progress_callback=None):


        cap = cv2.VideoCapture(input_video)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


        if end_time is None:
            end_time = total_frames / fps
        if frame_count is None:
            frame_count = int(fps * (end_time - start_time))

        start_frame = int(start_time * fps)
        end_frame =  int(fps * (end_time))
        duration_frame =  int(fps * (end_time - start_time))

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read the video")
            return


        filters = []
        if use_color_filter:
            filters.append(Filter.adjust_contrast_and_saturation)
        if use_subject_filter:
            filters.append(Filter.sobel_edge_detection)
        if use_pencil_sketch_effect:
            filters.append(Filter.pencil_sketch_effect)

        filtered_frame = frame
        for f in filters:
            filtered_frame = f(filtered_frame)

        gray = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2GRAY)
        char_img = VideoProcessor.get_char_img(gray, filtered_frame, scale, font_size)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_video, fourcc, fps, (char_img.shape[1], char_img.shape[0]))

        frame_skip = max(1, duration_frame // frame_count)

        i = 0
        frame_idx = start_frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # 如果存在进度回调，在开始处理前先调用一次，指示0%进度
        if progress_callback:
            progress_callback(0, frame_count)

        while i < frame_count and frame_idx < end_frame:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_skip == 0:
                filtered_frame = frame
                for f in filters:
                    filtered_frame = f(filtered_frame)

                gray = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2GRAY)
                char_img = VideoProcessor.get_char_img(gray, filtered_frame, scale, font_size)

                writer.write(char_img)
                i += 1

                # 每处理一帧更新进度
                if progress_callback:
                    progress_callback(i, frame_count)

            frame_idx += 1

        writer.release()
        cap.release()
