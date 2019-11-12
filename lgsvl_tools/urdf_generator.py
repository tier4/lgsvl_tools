#The MIT License (MIT)

#Copyright (c) 2015 bpyamasinn.

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import argparse
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import json

CAMERA_SENSOR_TYPES = ['Color Camera']
SENSOR_TYPES = ['GPS Device','GPS Odometry','IMU','Lidar','Color Camera']

class UrdfGenerator:
    def __init__(self,json_path,output_file,base_link_offset_x,base_link_offset_y,base_link_offset_z,robot_name,dae_path):
        self.json_path = json_path
        self.output_file = output_file
        self.base_link_offset_x = base_link_offset_x
        self.base_link_offset_y = base_link_offset_y
        self.base_link_offset_z = base_link_offset_z
        self.robot_name = robot_name
        self.dae_path = dae_path
        try:
            f = open(self.json_path, 'r')
            self.json_data = json.load(f)
        except:
            print("json path is invalid")
            return
        self.generate()
    def parse_json(self):
        self.non_camera_frames = {}
        self.camera_frames = {}
        for data in self.json_data:
            if data['type'] in SENSOR_TYPES and data['params']['Frame'] not in self.non_camera_frames:
                if data['type'] in CAMERA_SENSOR_TYPES:
                    self.camera_frames[data['params']['Frame']] = data['transform']
                else:
                    self.non_camera_frames[data['params']['Frame']] = data['transform']
    def generate_base_urdf(self):
        base = Element('robot')
        base.set('name',self.robot_name)
        base_link = SubElement(base,'link')
        base_link.set('name','base_link')
        base_link_visual = SubElement(base_link,'visual')
        origin = SubElement(base_link_visual,'origin')
        xyz_str = str(self.base_link_offset_z*-1) + " " + str(self.base_link_offset_x*-1) + " " + str(self.base_link_offset_y*-1)
        origin.set('rpy', "0 0 0")
        origin.set('xyz', xyz_str)
        base_link_geometry = SubElement(base_link_visual,'geometry')
        base_link_mesh = SubElement(base_link_geometry,'mesh')
        base_link_mesh.set('filename',self.dae_path)
        return base
    def reshape_urdf(self,urdf_tree):
        reparsed = minidom.parseString(tostring(urdf_tree))
        return reparsed.toprettyxml(indent="  ")
    def add_frame(self,urdf,frame_id,transform):
        link = SubElement(urdf,'link')
        link.set('name',frame_id+'_link')
        joint = SubElement(urdf,'joint')
        joint.set('name',frame_id+'_joint')
        joint.set('type','fixed')
        parent = SubElement(joint,'parent')
        parent.set('link','base_link')
        #child = SubElement(joint,'child')
        #child.set('link',frame_id+'_link')
        origin = SubElement(joint,'origin')
        rpy_str = str(transform["yaw"]) + " " + str(transform["roll"]) + " " + str(transform["pitch"])
        origin.set('rpy', rpy_str)
        xyz_str = str(transform["z"]-self.base_link_offset_z) + " " + str(transform["x"]-self.base_link_offset_x) + " " + str(transform["y"]-self.base_link_offset_y)
        origin.set('xyz', xyz_str)
        return urdf
    def add_optical_frame(self,urdf,frame_id):
        optical_link = SubElement(urdf,'link')
        optical_link.set('name',frame_id+"_optical_link")
        optical_joint = SubElement(urdf,'joint')
        optical_joint.set('name',frame_id+'_optical_joint')
        optical_joint.set('type','fixed')
        parent = SubElement(optical_joint,'parent')
        parent.set('link',frame_id)
        origin = SubElement(optical_joint,'origin')
        origin.set('rpy', "-1.57079632679 0 -1.57079632679")
        origin.set('xyz', "0 0 0")
        return urdf
    def output_urdf(self,urdf_string):
        with open(self.output_file, mode='w') as f:
            f.write(urdf_string)
        print("urdf saved to "+self.output_file)
    def generate(self):
        self.parse_json()
        urdf = self.generate_base_urdf()
        for frame_id in self.non_camera_frames.keys():
            self.add_frame(urdf,frame_id,self.non_camera_frames[frame_id])
        for frame_id in self.camera_frames.keys():
            self.add_frame(urdf,frame_id,self.camera_frames[frame_id])
            self.add_optical_frame(urdf,frame_id)
        urdf_string = self.reshape_urdf(urdf)
        self.output_urdf(urdf_string)

def main():
    parser = argparse.ArgumentParser(description='URDF generation tool for LGSVL Simulator')
    parser.add_argument('json_path', help='json_file_path for the LGSVL simulator vehicle configuration')
    parser.add_argument('output_file', help='output_path of the URDF')
    parser.add_argument('base_link_offset_x', help='offset value of the base_link (in ROS coordinate)',type=float)
    parser.add_argument('base_link_offset_y', help='offset value of the base_link (in ROS coordinate)',type=float)
    parser.add_argument('base_link_offset_z', help='offset value of the base_link (in ROS coordinate)',type=float)
    parser.add_argument('robot_name', help='name of the robot')
    parser.add_argument('dae_path',help='path of the .dae files')
    args = parser.parse_args()
    generator = UrdfGenerator(args.json_path,args.output_file,args.base_link_offset_x,args.base_link_offset_y,args.base_link_offset_z,args.robot_name,args.dae_path)

if __name__ == "__main__":
    main()