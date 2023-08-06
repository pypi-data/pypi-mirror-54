//
// Created by yk on 2019/10/22.
//
#include <iomanip>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>

#include <k4a/k4a.hpp>

#include "include/pyk4a.h"
#include "include/Pixel.h"
#include "include/DepthPixelColorizer.h"
#include "include/StaticImageProperties.h"

namespace py = pybind11;
std::stringstream stream;
std::vector<yk::Pixel> depthTextureBuffer;

class pyk4aimage {

public:
    explicit pyk4aimage(k4a::image &image) : _image(std::move(image)) {}

    explicit pyk4aimage(k4a::image &&image) : _image(image) {}

    py::array numpy() {
        switch (_image.get_format()) {
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_NV12:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_MJPG:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_YUY2:
                return py::array(
                        py::buffer_info(
                                _image.get_buffer(),
                                sizeof(unsigned char),
                                py::format_descriptor<unsigned char>::format(),
                                3,
                                {_image.get_height_pixels(), _image.get_width_pixels(), 4},
                                {
                                        sizeof(unsigned char) * 4 * _image.get_width_pixels(),
                                        sizeof(unsigned char) * 4,
                                        sizeof(unsigned char)
                                }
                        )
                );
            case k4a_image_format_t::K4A_IMAGE_FORMAT_DEPTH16:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_IR16:
                return py::array(
                        py::buffer_info(
                                _image.get_buffer(),
                                sizeof(unsigned short int),
                                py::format_descriptor<unsigned short int>::format(),
                                2,
                                {_image.get_height_pixels(), _image.get_width_pixels()},
                                {
                                        sizeof(unsigned short int) * _image.get_height_pixels(),
                                        sizeof(unsigned short int)
                                }
                        )
                );
            default:
                break;
//            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
//            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
        }
    }

    auto get_device_timestamp() {
        return _image.get_device_timestamp();
    }

    auto get_exposure() {
        return _image.get_exposure();
    }

    auto get_format() {
        return _image.get_format();
    }

    auto get_height_pixels() {
        return _image.get_height_pixels();
    }

    auto get_iso_speed() {
        return _image.get_iso_speed();
    }

    auto get_size() {
        return _image.get_size();
    }

    auto get_stride_bytes() {
        return _image.get_stride_bytes();
    }

    auto get_system_timestamp() {
        return _image.get_system_timestamp();
    }

    auto get_white_balance() {
        return _image.get_white_balance();
    }

    auto get_width_pixels() {
        return _image.get_width_pixels();
    }


    uint8_t *get_buffer() noexcept {
        return _image.get_buffer();
    }

    const uint8_t *get_buffer() const noexcept {
        return _image.get_buffer();
    }

    auto get_one_size() {
        switch (_image.get_format()) {
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_NV12:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_MJPG:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_YUY2:
                return sizeof(unsigned char);
                break;
            case k4a_image_format_t::K4A_IMAGE_FORMAT_DEPTH16:
            case k4a_image_format_t::K4A_IMAGE_FORMAT_IR16:
                return sizeof(float);
                break;
            default:
                break;
//            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
//            case k4a_image_format_t::K4A_IMAGE_FORMAT_COLOR_BGRA32:
        }
    }

    k4a::image _image;
};

class pyk4acalibration {

public:
    pyk4acalibration() = delete;

    explicit pyk4acalibration(const k4a::calibration &c) : _c(c) {}

    k4a::calibration _c;
};

class pyk4atransformation {
public:
    explicit pyk4atransformation(pyk4acalibration &c) {
        _t = k4a::transformation(c._c);
    }

    pyk4aimage depth_image_to_color_camera(const pyk4aimage &depth_image) {
        return pyk4aimage(_t.depth_image_to_color_camera(depth_image._image));
    }

    py::array depth_image_colorize_numpy(const pyk4aimage &depth_image, k4a_depth_mode_t &depth_mode) {
        ColorizeDepthImage(depth_image._image, yk::DepthPixelColorizer::ColorizeBlueToRed,
                           yk::GetDepthModeRange(depth_mode), &depthTextureBuffer);
        return py::array(
                py::buffer_info(
                        depthTextureBuffer.data(),
                        sizeof(unsigned char),
                        py::format_descriptor<unsigned char>::format(),
                        3,
                        {depth_image._image.get_height_pixels(), depth_image._image.get_width_pixels(), 4},
                        {
                                sizeof(unsigned char) * 4 * depth_image._image.get_width_pixels(),
                                sizeof(unsigned char) * 4,
                                sizeof(unsigned char)
                        }
                )
        );
    }

    pyk4atransformation() = default;

    k4a::transformation _t = nullptr;
};

class pyk4acapture {
public:
    pyk4acapture() = default;

    pyk4acapture(pyk4atransformation &t, k4a_device_configuration_t &config) {
        _trans._t = std::move(t._t);
        _config = config;
    }

    pyk4aimage get_depth_image() {
        return pyk4aimage(_cap.get_depth_image());
    }

    pyk4aimage get_ir_image() {
        return pyk4aimage(_cap.get_ir_image());
    }

    pyk4aimage get_color_image() {
        return pyk4aimage(_cap.get_color_image());
    }

    void reset() noexcept {
        _cap.reset();
    }

    float get_temperature_c() const noexcept {
        return _cap.get_temperature_c();
    }

    k4a::capture _cap = nullptr;
    pyk4atransformation _trans;
    k4a_device_configuration_t _config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;

};

class pyk4adevice {
public:

    pyk4adevice() = delete;

    explicit pyk4adevice(k4a::device device) {
        _device = std::move(device);
    }

    static pyk4adevice open(uint32_t index) {
        return pyk4adevice(k4a::device::open(index));
    }

    static uint32_t get_installed_count() {
        return k4a_device_get_installed_count();
    }

    std::string get_serialnum() {
        return _device.get_serialnum();
    }

    auto get_raw_calibration() {
        return _device.get_raw_calibration();
    }

    void get_color_control(){
//        TODO
    }
    void set_color_control(){
//        TODO
    }
    void k4a_device_get_color_control_capabilities(){
//        TODO
    }
    pyk4acalibration get_calibration(k4a_depth_mode_t depth_mode, k4a_color_resolution_t color_resolution) {
        return pyk4acalibration(_device.get_calibration(depth_mode, color_resolution));
    }

    void start_cameras(const k4a_device_configuration_t &configuration) {
        _device.start_cameras(&configuration);
    }

    void start_imu() {
        _device.start_imu();
    }

    bool get_capture(pyk4acapture &cap, int timeout) {
        return _device.get_capture(&cap._cap,
                                   std::chrono::milliseconds(timeout));
    }

    k4a_imu_sample_t get_imu_sample() {
        k4a_imu_sample_t temp_data;
        _device.get_imu_sample(&temp_data);
        return temp_data;
    }

    k4a::device _device = nullptr;
};


k4a_device_configuration_t config_init() {
    return K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
}

PYBIND11_MODULE(_pyk4a, m) {
    py::class_<pyk4aimage>(m, "Image")
            .def("numpy", &pyk4aimage::numpy)
            .def("get_exposure", &pyk4aimage::get_exposure)
            .def("get_format", &pyk4aimage::get_format)
            .def("get_height_pixels", &pyk4aimage::get_height_pixels)
            .def("get_iso_speed", &pyk4aimage::get_iso_speed)
            .def("get_size", &pyk4aimage::get_size)
            .def("get_stride_bytes", &pyk4aimage::get_stride_bytes)
            .def("get_device_timestamp", &pyk4aimage::get_device_timestamp)
            .def("get_white_balance", &pyk4aimage::get_white_balance)
            .def("get_width_pixels", &pyk4aimage::get_width_pixels)
            .def("get_system_timestamp", &pyk4aimage::get_system_timestamp);

    py::class_<pyk4atransformation>(m, "Transformation")
            .def(py::init<pyk4acalibration &>())
            .def("depth_image_to_color_camera", &pyk4atransformation::depth_image_to_color_camera)
            .def("depth_image_colorize_numpy", &pyk4atransformation::depth_image_colorize_numpy);
    py::class_<pyk4acalibration>(m, "Calibration");
    py::class_<pyk4acapture>(m, "Capture")
            .def(py::init<>())
            .def(py::init<pyk4atransformation &, k4a_device_configuration_t &>())
            .def("get_depth_image", &pyk4acapture::get_depth_image)
            .def("get_color_image", &pyk4acapture::get_color_image)
            .def("get_ir_image", &pyk4acapture::get_ir_image);
    py::class_<pyk4adevice>(m, "Device")
            .def("open", &pyk4adevice::open)
            .def("get_installed_count", &pyk4adevice::get_installed_count)
            .def("get_serialnum", &pyk4adevice::get_serialnum)
            .def("get_calibration", &pyk4adevice::get_calibration)
            .def("start_cameras", &pyk4adevice::start_cameras)
            .def("get_imu_sample", &pyk4adevice::get_imu_sample)
            .def("start_imu", &pyk4adevice::start_imu)
            .def("get_capture", &pyk4adevice::get_capture).
                    def("get_raw_calibration", &pyk4adevice::get_raw_calibration);
    py::class_<k4a_device_configuration_t>(m, "Configuration")
            .def(py::init(&config_init))
            .def_readwrite("depth_mode", &k4a_device_configuration_t::depth_mode)
            .def_readwrite("color_resolution", &k4a_device_configuration_t::color_resolution)
            .def_readwrite("camera_fps", &k4a_device_configuration_t::camera_fps)
            .def_readwrite("color_format", &k4a_device_configuration_t::color_format)
            .def_readwrite("synchronized_images_only", &k4a_device_configuration_t::synchronized_images_only);
    py::enum_<k4a_depth_mode_t>(m, "depth_mode_t")
            .value("K4A_DEPTH_MODE_OFF", K4A_DEPTH_MODE_OFF)
            .value("K4A_DEPTH_MODE_NFOV_2X2BINNED", K4A_DEPTH_MODE_NFOV_2X2BINNED)
            .value("K4A_DEPTH_MODE_NFOV_UNBINNED", K4A_DEPTH_MODE_NFOV_UNBINNED)
            .value("K4A_DEPTH_MODE_WFOV_2X2BINNED", K4A_DEPTH_MODE_WFOV_2X2BINNED)
            .value("K4A_DEPTH_MODE_WFOV_UNBINNED", K4A_DEPTH_MODE_WFOV_UNBINNED)
            .value("K4A_DEPTH_MODE_PASSIVE_IR", K4A_DEPTH_MODE_PASSIVE_IR)
            .export_values();
    py::enum_<k4a_color_resolution_t>(m, "color_resolution_t")
            .value("K4A_COLOR_RESOLUTION_720P", K4A_COLOR_RESOLUTION_720P)
            .value("K4A_COLOR_RESOLUTION_1080P", K4A_COLOR_RESOLUTION_1080P)
            .value("K4A_COLOR_RESOLUTION_1440P", K4A_COLOR_RESOLUTION_1440P)
            .value("K4A_COLOR_RESOLUTION_1536P", K4A_COLOR_RESOLUTION_1536P)
            .value("K4A_COLOR_RESOLUTION_2160P", K4A_COLOR_RESOLUTION_2160P)
            .value("K4A_COLOR_RESOLUTION_3072P", K4A_COLOR_RESOLUTION_3072P)
            .export_values();
    py::enum_<k4a_fps_t>(m, "fps_t")
            .value("K4A_FRAMES_PER_SECOND_5", K4A_FRAMES_PER_SECOND_5)
            .value("K4A_FRAMES_PER_SECOND_15", K4A_FRAMES_PER_SECOND_15)
            .value("K4A_FRAMES_PER_SECOND_30", K4A_FRAMES_PER_SECOND_30)
            .export_values();
    py::enum_<k4a_image_format_t>(m, "image_format_t")
            .value("K4A_IMAGE_FORMAT_COLOR_MJPG", K4A_IMAGE_FORMAT_COLOR_MJPG)
            .value("K4A_IMAGE_FORMAT_COLOR_NV12", K4A_IMAGE_FORMAT_COLOR_NV12)
            .value("K4A_IMAGE_FORMAT_COLOR_YUY2", K4A_IMAGE_FORMAT_COLOR_YUY2)
            .value("K4A_IMAGE_FORMAT_COLOR_BGRA32", K4A_IMAGE_FORMAT_COLOR_BGRA32)
            .value("K4A_IMAGE_FORMAT_DEPTH16", K4A_IMAGE_FORMAT_DEPTH16)
            .value("K4A_IMAGE_FORMAT_IR16", K4A_IMAGE_FORMAT_IR16)
            .export_values();
    py::enum_<k4a_color_control_command_t>(m, "color_control_command_t")
            .value("K4A_COLOR_CONTROL_EXPOSURE_TIME_ABSOLUTE", K4A_COLOR_CONTROL_EXPOSURE_TIME_ABSOLUTE)
            .value("K4A_COLOR_CONTROL_AUTO_EXPOSURE_PRIORITY", K4A_COLOR_CONTROL_AUTO_EXPOSURE_PRIORITY)
            .value("K4A_COLOR_CONTROL_BRIGHTNESS", K4A_COLOR_CONTROL_BRIGHTNESS)
            .value("K4A_COLOR_CONTROL_CONTRAST", K4A_COLOR_CONTROL_CONTRAST)
            .value("K4A_COLOR_CONTROL_SATURATION", K4A_COLOR_CONTROL_SATURATION)
            .value("K4A_COLOR_CONTROL_SHARPNESS", K4A_COLOR_CONTROL_SHARPNESS)
            .value("K4A_COLOR_CONTROL_WHITEBALANCE", K4A_COLOR_CONTROL_WHITEBALANCE)
            .value("K4A_COLOR_CONTROL_BACKLIGHT_COMPENSATION", K4A_COLOR_CONTROL_BACKLIGHT_COMPENSATION)
            .value("K4A_COLOR_CONTROL_GAIN", K4A_COLOR_CONTROL_GAIN)
            .value("K4A_COLOR_CONTROL_POWERLINE_FREQUENCY", K4A_COLOR_CONTROL_POWERLINE_FREQUENCY)
            .export_values();
    py::enum_<k4a_color_control_mode_t>(m, "color_control_mode_t")
            .value("K4A_COLOR_CONTROL_MODE_AUTO", K4A_COLOR_CONTROL_MODE_AUTO)
            .value("K4A_COLOR_CONTROL_MODE_MANUAL", K4A_COLOR_CONTROL_MODE_MANUAL)
            .export_values();
    py::class_<k4a_float3_t>(m, "float3_t")
            .def("__repr__", [](const k4a_float3_t &self) {
                stream.clear();
                stream << "x: " << std::fixed << std::setprecision(4) << self.xyz.x
                       << "y: " << std::fixed << std::setprecision(4) << self.xyz.y
                       << "z: " << std::fixed << std::setprecision(4) << self.xyz.z;
                return stream.str();
            })
            .def_property_readonly("x",
                                   [](k4a_float3_t &self) {
                                       return self.xyz.x;
                                   })
            .def_property_readonly("y",
                                   [](k4a_float3_t &self) {
                                       return self.xyz.y;
                                   })
            .def_property_readonly("z",
                                   [](k4a_float3_t &self) {
                                       return self.xyz.z;
                                   });
    py::class_<k4a_imu_sample_t>(m, "imu_sample_t")
            .def("__repr__", [](const k4a_imu_sample_t &self) {
                stream.clear();
                stream << "\n\nt: " << std::fixed << std::setprecision(4) << self.temperature
                       << "\nacc: timestamp: " << self.acc_timestamp_usec << "\n"
                       << "x: " << std::fixed << std::setprecision(4) << self.acc_sample.xyz.x
                       << " y: " << std::fixed << std::setprecision(4) << self.acc_sample.xyz.y
                       << " z: " << std::fixed << std::setprecision(4) << self.acc_sample.xyz.z
                       << "\ngyro: timestamp: " << self.gyro_timestamp_usec << "\n"
                       << "x: " << std::fixed << std::setprecision(4) << self.gyro_sample.xyz.x
                       << " y: " << std::fixed << std::setprecision(4) << self.gyro_sample.xyz.y
                       << " z: " << std::fixed << std::setprecision(4) << self.gyro_sample.xyz.z;
                return stream.str();
            })
            .def_readonly("temperature", &k4a_imu_sample_t::temperature)
            .def_readonly("acc_sample", &k4a_imu_sample_t::acc_sample)
            .def_readonly("acc_timestamp_usec", &k4a_imu_sample_t::acc_timestamp_usec)
            .def_readonly("gyro_sample", &k4a_imu_sample_t::gyro_sample)
            .def_readonly("gyro_timestamp_usec", &k4a_imu_sample_t::gyro_timestamp_usec);
    m.attr("K4A_DEVICE_DEFAULT") = K4A_DEVICE_DEFAULT;
};