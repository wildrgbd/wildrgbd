import os
import fsspec
import argparse
from fsspec.implementations.zip import ZipFileSystem
import numpy as np
from PIL import Image
import cv2 
import imageio
import open3d as o3d 
import json
from tqdm import tqdm
import pickle


def read_pose(datapath):
    dir_path = datapath
    # print("dir_path: ", dir_path)
    pose_path = os.path.join(dir_path, 'cam_poses.txt')
    poses = np.genfromtxt(pose_path)
    poses = poses[:, 1:].reshape(-1, 4, 4)
    
    return poses

def read_dir(poses, dir_path):
    
    rgb_paths = os.path.join(dir_path, 'rgb')
    depth_dir = os.path.join(dir_path, 'depth')

    img_paths = []
    depth_paths = []
    selected_poses = []
    
    for i in range(0, poses.shape[0]):
        img_path = os.path.join(rgb_paths, f'{i:0>5d}.png')
        depth_path = os.path.join(depth_dir, f'{i:0>5d}.png')
        
        img_paths.append(img_path)
        depth_paths.append(depth_path)
        selected_poses.append(poses[i])
        
    return img_paths, depth_paths, selected_poses

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--save_dir", type=str, required=True)
    
    args = parser.parse_args()
    datapath = args.path
    save_dir = args.save_dir
    os.makedirs(save_dir, exist_ok=True)
    
    poses = read_pose(datapath)
    assert poses.shape[0] > 0
    
    img_paths, depth_paths, selected_poses = read_dir(poses, datapath)
    
    meta_path = os.path.join(datapath, 'metadata')
    with open(meta_path, 'r') as f_json:
        meta = json.load(f_json)
    
    K = np.array(meta["K"]).reshape(3, 3).T
    fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
    w, h = meta["w"], meta["h"]
    intrinsic = o3d.camera.PinholeCameraIntrinsic(w, h, fx, fy, cx, cy)
    
    SCALE = 1000
    depth_max = 5
    depth_min = 0
    frames = []
    points = np.zeros((0, 3))
    points_color = np.zeros((0, 3))
    
    for rgb_path, depth_path, pose in zip(img_paths, depth_paths, selected_poses):
        rgb = Image.open(rgb_path)
        depth = Image.open(depth_path)
        rgb = np.array(rgb, dtype='uint8')
        depth = np.array(depth, dtype="uint16")
        
        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(o3d.geometry.RGBDImage.create_from_color_and_depth(o3d.geometry.Image(rgb), o3d.geometry.Image(depth), depth_scale=SCALE, depth_trunc=depth_max, convert_rgb_to_intensity=False), intrinsic)
        frame_points = np.array(pcd.points)
        frame_points_color = np.array(pcd.colors)
        homo_cw_vertices = np.concatenate((frame_points, np.ones((frame_points.shape[0], 1))), axis=-1).T
        homo_w_points = np.matmul(pose[:3, :4], homo_cw_vertices)
        frame_points = homo_w_points.T
        points = np.concatenate((points, frame_points), 0)
        points_color = np.concatenate((points_color, frame_points_color), 0)
        
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(points_color)
    pcd = pcd.voxel_down_sample(0.001)
    
    pcd_backup_save_path = os.path.join(save_dir, 'pcd.ply')
    with open(os.path.join(save_dir, 'poses.pkl'), 'wb') as f_pkl:
        pickle.dump({
            'poses': poses,
            'K': K,
        }
            , f_pkl)
    o3d.io.write_point_cloud(pcd_backup_save_path, pcd)            
    
    
    
    
    