"""
Copyright 2019, NIA(한국정보화진흥원), All rights reserved.
Mail : rocketgrowthsj@publicai.co.kr
"""
import os
import glob
import math
import numpy as np
import imgaug.augmenters as iaa
import cv2
from functools import partial
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


ABLE_READ_FORMAT = []
ABLE_READ_FORMAT.extend(['.bmp', "*.dib"])  # WINDOW_BITMAP_FORMAT
ABLE_READ_FORMAT.extend(['.jpeg', '.jpg', '.jpe'])  # JPEG_FORMAT
ABLE_READ_FORMAT.extend(['.jp2'])  # JPEG2000_FORMAT
ABLE_READ_FORMAT.extend(['.png'])  # Portable Network Graphics
ABLE_READ_FORMAT.extend(['.pbm', '.pgm', '.ppm'])  # Portable Image Format
ABLE_READ_FORMAT.extend(['.sr', '.ras'])  # SUR_RASTER_FORMAT
ABLE_READ_FORMAT.extend(['.tiff', '.tif'])  # TIFF_FORMAT


def read_image(file_path: str, gray_scale=True):
    """
    파일 경로로부터 이미지를 읽어들이는 Function

    return: np.ndarray

        if gray_scale==True, 2D Array[height, width]를 반환
        else, 3D Array[height, width, channel(rgb)]를 반환
    """
    assert os.path.exists(file_path), (
            str(file_path) + " 경로에 파일이 존재하지 않습니다.")

    if gray_scale:
        return cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def read_batch_images(batch_paths: list):
    """
    파일 경로 리스트로부터 이미지를 읽어들이는 Function
    """
    return [read_image(file_path) for file_path in batch_paths]


def read_image_paths_from_directory(file_dir: str):
    """
    디렉토리로부터 이미지 파일 경로를 가져오는 Function

    return : List of np.ndarray
    """
    global ABLE_READ_FORMAT
    file_paths = glob.glob(os.path.join(file_dir, "*"))
    file_paths = [file_path
                  for file_path in file_paths
                  if os.path.splitext(file_path)[-1].lower()
                  in ABLE_READ_FORMAT]
    return file_paths


def calculate_num_batches(file_dir: str,
                          multiples=1,
                          num_batch=10):
    """
    처리할 최대 배치 횟수를 반환하는 Function

    """
    num_files = len(read_image_paths_from_directory(file_dir))
    return int(math.ceil(num_files / num_batch)) * multiples


def generate_image_paths_per_batch(file_dir: str,
                                   multiples=1,
                                   num_batch=10):
    """
    이미지 경로를 배치 단위로 반환하는 Generator

    return : List of np.ndarray
    """
    file_paths = read_image_paths_from_directory(file_dir)
    for count in range(multiples):
        if multiples == 1:
            prefix = None
        else:
            prefix = count

        for i in range(0, len(file_paths), num_batch):
            yield file_paths[i:i + num_batch], prefix


def write_images_to_directory(images: np.ndarray,
                              original_paths: list,
                              save_dir: str,
                              prefix=None):
    """
    증강 이미지를 save directory에 저장하는 Function

    원본 이미지의 이름과 동일하게 save directory로 두되, 복수개의 증강 이미지를 생성할 경우
    prefix를 통해 구분합니다.

    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    for original_path, image in zip(original_paths, images):
        original_name = os.path.split(original_path)[1]
        if prefix is not None:
            save_path = os.path.join(save_dir, str(prefix) + "_" + original_name)
        else:
            save_path = os.path.join(save_dir, original_name)
        cv2.imwrite(save_path, image)


def augment_images(images,
                   blur=5.,
                   gaussian_noise=30.,
                   multiply=.2,
                   scale=.1,
                   rotate=10,
                   shear=5.,
                   elastic=.7):
    """
    이미지 증강 Function

    imgaug을 기본으로 Wrapping한 Function으로,
    Text Recognition Dataset에 자주 쓰이는 Data Augmentation
    기법들을 추려 설정해놓았습니다.

    :param blur: 가우시안 블러 효과, 커질수록 노이즈의 효과가 두드러짐
    :param noise: 가우시안 노이즈
    :param multiply: 이미지 strength 효과
    :param scale: 이미지 확대 및 축소
    :param rotate: 회전의 범위, ex 5인 경우, (-5도 ~ 5도 사이 회전)
    :param shear: 전단 회전 효과
    :param elastic: elastic transform 효과

    """
    blur_range = (0., blur),
    noise_range = (0., gaussian_noise)
    multiply_range = (1. - multiply, 1. + multiply)
    scale_range = (1. - scale, 1. + scale)
    rotate_range = (-rotate, rotate)
    shear_range = (-shear, shear)
    elastic_range = (0., elastic)

    seq = iaa.Sequential([
        iaa.GaussianBlur(sigma=blur_range),
        iaa.AdditiveGaussianNoise(loc=0,
                                  scale=noise_range,
                                  per_channel=False),
        iaa.Multiply(multiply_range),
        iaa.Affine(scale=scale_range,
                   rotate=rotate_range,
                   shear=shear_range,
                   fit_output=True),
        iaa.ElasticTransformation(alpha=elastic_range)
    ])
    return seq.augment_images(images)


def process_augmentation(gen_inputs,
                         save_dir,
                         blur=5.,
                         gaussian_noise=30.,
                         multiply=.2,
                         scale=.1,
                         rotate=10,
                         shear=5.,
                         elastic=.7):
    """
    Worker For Augmentation Process

    multiprocess_image_augmentation에서 Worker을 구성하기 위한 Function
    """
    batch_paths, prefix = gen_inputs

    images = read_batch_images(batch_paths)
    augmented_images = augment_images(images,
                                      blur,
                                      gaussian_noise,
                                      multiply,
                                      scale,
                                      rotate,
                                      shear,
                                      elastic)
    write_images_to_directory(augmented_images,
                              batch_paths,
                              save_dir=save_dir,
                              prefix=prefix)


def multiprocess_image_augumentation(file_dir,
                                     save_dir,
                                     multiples=1,
                                     blur=5.,
                                     noise=30.,
                                     strength=.2,
                                     scale=.1,
                                     rotate=10,
                                     shear=5.,
                                     elastic=.7):
    batch_size = 10 # Default Setting, 크게 중요하지 않은 Factor로 One Batch에 처리할 크기
    # 처리할 Worker 생성
    worker = partial(process_augmentation, save_dir,
                     blur=blur,
                     guassian_noise=noise,
                     strength=strength,
                     scale=scale,
                     rotate=rotate,
                     shear=shear,
                     elastic=elastic)
    # 총 이미지의 갯수
    total_counts = len(
        read_image_paths_from_directory(file_dir))
    # 총 처리할 배치의 갯수
    total_batch_counts = calculate_num_batches(
        file_dir, multiples, batch_size)
    # Generator 생성
    generator = generate_image_paths_per_batch(
        file_dir, multiples, batch_size)

    print("총 이미지의 갯수 : ", total_counts * multiples)
    print("처리할 배치 수   : ", total_batch_counts)

    with Pool(cpu_count()) as pool:
        with tqdm(total=total_batch_counts) as pbar:
            for i, _ in tqdm(enumerate(pool.imap_unordered(worker, generator))):
                pbar.update()

