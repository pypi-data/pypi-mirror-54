from PIL import Image
from io import BytesIO
import urllib
import requests
import numpy as np
import matplotlib
import json
from .utils.conversions import convert_uint_to_float, convert_float_to_uint, round_to_uint, get_rgb_float_if_hex, get_array_from_hex
from .utils.layers import mix
from .utils.channels import split_image_into_channels, merge_channels, channel_adjust


class LayerImage():
    @staticmethod
    def from_url(url):
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image_data = convert_uint_to_float(np.asarray(image))

        return LayerImage(image_data)

    @staticmethod
    def from_file(file_path):
        image = Image.open(file_path)
        image_data = convert_uint_to_float(np.asarray(image))

        return LayerImage(image_data)

    @staticmethod
    def from_array(image_data):
        return LayerImage(image_data)

    def __init__(self, image_data):
        self.image_data = image_data

    def grayscale(self):
        self.image_data = np.dot(self.image_data[..., :3], [
                                 0.2989, 0.5870, 0.1140])

        self.image_data = np.stack(
            (self.image_data,) * 3, axis=-1)

        return self

    def darken(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        result = np.minimum(self.image_data, blend_data)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def multiply(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        result = self.image_data * blend_data

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def color_burn(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.clip(np.where(B > 0, 1 - (1 - A) / B, 0), 0, 1)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def linear_burn(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        result = np.clip(A + B - 1, 0, 1)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def lighten(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        result = np.maximum(self.image_data, blend_data)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def screen(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        result = 1 - (1 - A) * (1 - B)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def color_dodge(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.where(B == 1, B, np.clip(A / (1 - B), 0, 1))

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def linear_dodge(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        result = np.clip(A + B, 0, 1)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def overlay(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        data01 = (2 * A) * B
        data02 = 1 - 2 * (1 - A) * (1 - B)

        result = np.where(A <= 0.5, data01, data02)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def soft_light(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        data01 = 2 * A * B + np.square(A) * (1 - 2 * B)
        data02 = np.sqrt(A) * (2 * B - 1) + (2 * A) * (1 - B)

        result = np.where(blend_data <= 0.5, data01, data02)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def hard_light(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        data01 = (2 * A) * B
        data02 = 1 - 2 * (1 - A) * (1 - B)

        result = np.where(blend_data <= 0.5, data01, data02)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def vivid_light(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        with np.errstate(divide='ignore', invalid='ignore'):
            image_color_burn = np.where(B > 0, 1 - (1 - A) / (2 * B), 0)
            image_color_dodge = np.where(B < 1, A / (2 * (1 - B)), 1)

        result = np.clip(
            np.where(B <= 0.5, image_color_burn, image_color_dodge), 0, 1)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def linear_light(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.clip(A + 2 * B - 1, 0, 1)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def pin_light(self, blend_data, opacity=1.0):
        blend_data = get_rgb_float_if_hex(blend_data)

        A = self.image_data
        B = blend_data

        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.clip(np.where(A < 2 * B - 1, 2 * B - 1,
                                      np.where(A > 2 * B, 2 * B, A)), 0, 1)

        self.image_data = mix(self.image_data, result, opacity)

        return self

    def brightness(self, factor):
        self.image_data = np.clip(self.image_data * (1 + factor), 0, 1)

        return self

    # Legacy contrast mode
    def contrast(self, factor):
        self.image_data = np.clip(factor * (self.image_data - 0.5) + 0.5, 0, 1)

        return self

    def hue(self, target_hue):
        image_hsv_data = matplotlib.colors.rgb_to_hsv(self.image_data)
        image_hsv_data[:, :, 0] = target_hue

        self.image_data = matplotlib.colors.hsv_to_rgb(image_hsv_data)

        return self

    def saturation(self, factor):
        image_hsv_data = matplotlib.colors.rgb_to_hsv(self.image_data)
        image_hsv_data = np.clip(
            image_hsv_data + image_hsv_data * [0, factor, 0], 0, 1)

        self.image_data = matplotlib.colors.hsv_to_rgb(image_hsv_data)

        return self

    def lightness(self, factor):
        if factor > 0:
            self.image_data = self.image_data + \
                ((1 - self.image_data) * factor)
        elif factor < 0:
            self.image_data = self.image_data + (self.image_data * factor)

        return self

    def curve(self, channels='rgb', curve_points=[0, 1]):
        r, g, b = split_image_into_channels(self.image_data)

        if 'r' in channels:
            r = channel_adjust(r, curve_points)
        if 'g' in channels:
            g = channel_adjust(g, curve_points)
        if 'b' in channels:
            b = channel_adjust(b, curve_points)

        self.image_data = merge_channels(r, g, b)

        return self

    def clone(self):
        return LayerImage.from_array(self.image_data)

    def get_image_as_array(self):
        return self.image_data

    def apply_from_json(self, filepath):
        with open(filepath, 'r') as content_file:
            content = content_file.read()

        json_obj = json.loads(content)
        operations = json_obj['operations']

        for op in operations:
            hex_string = op['hex'] if 'hex' in op else None
            opacity = op['opacity'] if 'opacity' in op else 1.0
            factor = op['factor'] if 'factor' in op else None

            if op['type'] == 'grayscale':
                print('grayscale')
                self.grayscale()
            elif op['type'] == 'darken':
                if hex_string is not None:
                    self.darken(hex_string, opacity)
            elif op['type'] == 'multiply':
                if hex_string is not None:
                    self.multiply(hex_string, opacity)
            elif op['type'] == 'color_burn':
                if hex_string is not None:
                    self.color_burn(hex_string, opacity)
            elif op['type'] == 'linear_burn':
                if hex_string is not None:
                    self.linear_burn(hex_string, opacity)
            elif op['type'] == 'lighten':
                if hex_string is not None:
                    self.lighten(hex_string, opacity)
            elif op['type'] == 'screen':
                if hex_string is not None:
                    self.screen(hex_string, opacity)
            elif op['type'] == 'color_dodge':
                if hex_string is not None:
                    self.color_dodge(hex_string, opacity)
            elif op['type'] == 'linear_dodge':
                if hex_string is not None:
                    self.linear_dodge(hex_string, opacity)
            elif op['type'] == 'overlay':
                if hex_string is not None:
                    self.overlay(hex_string, opacity)
            elif op['type'] == 'soft_light':
                if hex_string is not None:
                    self.soft_light(hex_string, opacity)
            elif op['type'] == 'hard_light':
                if hex_string is not None:
                    self.hard_light(hex_string, opacity)
            elif op['type'] == 'vivid_light':
                if hex_string is not None:
                    self.vivid_light(hex_string, opacity)
            elif op['type'] == 'linear_light':
                if hex_string is not None:
                    self.linear_light(hex_string, opacity)
            elif op['type'] == 'pin_light':
                if hex_string is not None:
                    self.pin_light(hex_string, opacity)
            elif op['type'] == 'brightness':
                if factor is not None:
                    self.brightness(factor)
            elif op['type'] == 'contrast':
                if factor is not None:
                    self.contrast(factor)
            elif op['type'] == 'hue':
                if 'hue' in op:
                    self.hue(op['hue'])
            elif op['type'] == 'saturation':
                if factor is not None:
                    self.saturation(factor)
            elif op['type'] == 'lightness':
                if factor is not None:
                    self.lightness(factor)
            elif op['type'] == 'curve':
                if 'channels' in op and 'curve_points' in op:
                    self.curve(op['channels'], op['curve_points'])
            else:
                pass

        return self

    def save(self, filename, quality=75):
        pillow_image = Image.fromarray(convert_float_to_uint(self.image_data))
        pillow_image.save(filename, quality=quality)

        return self
