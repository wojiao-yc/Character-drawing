import cv2
import numpy as np

class Filter:
    @staticmethod
    def adjust_contrast_and_saturation(img, contrast=2.0, brightness=50, saturation=2.0):
        # 调整对比度和亮度
        img_contrast = cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)
        # 转换到HSV颜色空间
        hsv_img = cv2.cvtColor(img_contrast, cv2.COLOR_BGR2HSV)
        # 增强饱和度
        hsv_img[..., 1] = np.clip(hsv_img[..., 1] * saturation, 0, 255)
        # 转换回BGR
        img_final = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
        return img_final

    @staticmethod
    def sobel_edge_detection(img):
        """
        应用 Sobel 边缘检测
        :param frame: 当前视频帧
        :return: 边缘检测结果
        """
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        sobel_edges = cv2.magnitude(sobel_x, sobel_y)
        return cv2.convertScaleAbs(sobel_edges)
    
    @staticmethod
    def pencil_sketch_effect(img, radius=5, intensity_levels=20):
        """
        实现油画效果滤镜
        :param img: 输入图像
        :param radius: 油画效果的邻域半径，值越大，模糊效果越强
        :param intensity_levels: 强度等级，决定颜色分层的细腻程度
        :return: 油画效果图像
        """
        # 检查输入图像是否为彩色
        if len(img.shape) != 3 or img.shape[2] != 3:
            raise ValueError("输入图像必须是彩色的 (BGR) 图像。")

        # 应用油画效果
        oil_paint_img = cv2.xphoto.oilPainting(img, radius, intensity_levels)

        return oil_paint_img




